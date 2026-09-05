import concurrent.futures
import multiprocessing
import queue

from ollama import chat

from config.settings import (
    OLLAMA_LOCAL_MODEL,
    OLLAMA_CLOUD_MODEL,
    OLLAMA_LOCAL_TIMEOUT,
    OLLAMA_CLOUD_TIMEOUT,
)

from services.ai.prompt_builder import PromptBuilder
from services.ai.json_validator import JSONValidator


# ============================================================
# WORKER PROCESS
# ============================================================

def _ollama_worker(model: str, prompt: str, result_queue):
    """
    Runs Ollama in a separate process.

    This is important on Windows because a process can be
    terminated if Ollama takes too long.
    """

    try:

        response = chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0.2,
            },
        )

        result_queue.put(
            {
                "success": True,
                "content": response.message.content,
            }
        )

    except Exception as exc:

        result_queue.put(
            {
                "success": False,
                "error": str(exc),
            }
        )


# ============================================================
# OLLAMA SERVICE
# ============================================================

class OllamaService:

    def generate(
        self,
        title: str,
        article: str,
        source: str,
    ):

        prompt = PromptBuilder.build(
            title=title,
            article=article,
            source=source,
        )

        # ====================================================
        # 1. LOCAL AI
        # ====================================================

        print(
            f"Trying local AI: {OLLAMA_LOCAL_MODEL} "
            f"(timeout={OLLAMA_LOCAL_TIMEOUT}s)"
        )

        try:

            local_response = self._run_with_timeout(
                model=OLLAMA_LOCAL_MODEL,
                prompt=prompt,
                timeout=OLLAMA_LOCAL_TIMEOUT,
            )

            print("Local AI succeeded.")

            return JSONValidator.validate(
                local_response
            )

        except TimeoutError:

            print(
                f"Local AI timeout after "
                f"{OLLAMA_LOCAL_TIMEOUT} seconds."
            )

        except Exception as exc:

            print(
                f"Local AI failed: {exc}"
            )

        # ====================================================
        # 2. CLOUD AI
        # ====================================================

        print(
            f"Trying cloud AI: {OLLAMA_CLOUD_MODEL} "
            f"(timeout={OLLAMA_CLOUD_TIMEOUT}s)"
        )

        try:

            cloud_response = self._run_with_timeout(
                model=OLLAMA_CLOUD_MODEL,
                prompt=prompt,
                timeout=OLLAMA_CLOUD_TIMEOUT,
            )

            print("Cloud AI succeeded.")

            return JSONValidator.validate(
                cloud_response
            )

        except TimeoutError:

            print(
                f"Cloud AI timeout after "
                f"{OLLAMA_CLOUD_TIMEOUT} seconds."
            )

            raise RuntimeError(
                "Cloud AI timed out."
            )

        except Exception as exc:

            print(
                f"Cloud AI failed: {exc}"
            )

            raise RuntimeError(
                "Both local and cloud AI failed."
            ) from exc

    # ========================================================
    # PROCESS TIMEOUT
    # ========================================================

    @staticmethod
    def _run_with_timeout(
        model: str,
        prompt: str,
        timeout: int,
    ):

        # Windows requires spawn.
        context = multiprocessing.get_context("spawn")

        result_queue = context.Queue()

        process = context.Process(
            target=_ollama_worker,
            args=(
                model,
                prompt,
                result_queue,
            ),
        )

        process.start()

        try:

            # Wait for the worker to finish.
            process.join(timeout)

            # ------------------------------------------------
            # TIMEOUT
            # ------------------------------------------------

            if process.is_alive():

                print(
                    f"AI process exceeded "
                    f"{timeout}s. Terminating..."
                )

                process.terminate()

                process.join(
                    timeout=2
                )

                if process.is_alive():

                    print(
                        "AI process did not terminate "
                        "cleanly. Killing it..."
                    )

                    process.kill()

                    process.join()

                raise TimeoutError(
                    f"AI process timed out after "
                    f"{timeout} seconds."
                )

            # ------------------------------------------------
            # PROCESS FINISHED
            # ------------------------------------------------

            try:

                result = result_queue.get_nowait()

            except queue.Empty:

                raise RuntimeError(
                    "AI process finished without "
                    "returning a result."
                )

            if not result.get("success"):

                raise RuntimeError(
                    result.get(
                        "error",
                        "Unknown AI process error.",
                    )
                )

            return result["content"]

        finally:

            # Make absolutely sure the process is gone.
            if process.is_alive():

                process.terminate()
                process.join()

            try:
                result_queue.close()
            except Exception:
                pass