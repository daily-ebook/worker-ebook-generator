from celery import Celery
import mongoengine

celery = Celery('tasks',
            broker="redis://redis:6379/0",
            backend="redis://redis:6379/0")

@celery.task(bind=True, name="tasks.generate_ebook_from_recipe")
def get_sources_metadata(self, recipe):
    pass