from repositories.source_repository import SourceRepository


class SourceManager:

    def __init__(self):
        self.source_repo = SourceRepository()

    def get_active_sources(self):
        return self.source_repo.get_active()