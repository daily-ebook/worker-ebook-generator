from celery import Celery
from EbookGenerator import EbookGenerator
from Uploader import Uploader

celery = Celery('daily-ebook',
            broker="redis://redis:6379/0",
            backend="redis://redis:6379/0")
celery.conf.task_routes = ([
    ('ebook_generator.*', {'queue': 'eg'}),
    ('data_provider.*', {'queue': 'dp'})
],)

@celery.task(bind=True, name="ebook_generator.render_recipe_to_ebook")
def render_recipe_to_ebook(self, recipe_dict):
    self.update_state(state='PROGRESS', meta={'type': 'update', 'message': 'Starting conversion to ebook'})
    ebook_generator = EbookGenerator(recipe_dict)
    self.update_state(state='PROGRESS', meta={'type': 'update', 'message': 'Creating folders'})
    ebook_generator.setup()
    
    self.update_state(state='PROGRESS', meta={'type': 'update', 'message': 'Generating ebook'})
    file_path = ebook_generator.generate_mobi()
    self.update_state(state='PROGRESS', meta={'type': 'update', 'message': 'Uploading'})
    
    uploader = Uploader()
    response = uploader.upload(file_path)

    self.update_state(state='PROGRESS', meta={'type': 'update', 'message': 'Cleaning up'})
    ebook_generator.cleanup()
    
    return {
        'type': 'update',
        'message': 'Ebook converted and uploaded',
        'url': response["url"]
    }
