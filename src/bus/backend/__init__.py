from src.config import Settings
from src.bus.backend.mongo import MongoBackend


def get_mongo_backend():
    settings = Settings()
    backend = MongoBackend(
        host=settings.MongoBackend.HOST,
        port=settings.MongoBackend.PORT,
        db=settings.MongoBackend.DB,
        dagobah_collection=settings.MongoBackend.DAGOBAH_COLLECTION,
        log_collection=settings.MongoBackend.LOG_COLLECTION,
        job_collection=settings.MongoBackend.JOB_COLLECTION
    )
    return backend
