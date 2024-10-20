from src.database.models.FileModel import File
from src.repositories.BaseRepository import BaseRepository


class FileRepository(BaseRepository):
    model = File


def get_file_repository() -> FileRepository:
    return FileRepository()
