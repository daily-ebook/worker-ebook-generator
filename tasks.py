from celery import Celery

celery = Celery('daily-ebook',
            broker="redis://redis:6379/0",
            backend="redis://redis:6379/0")
celery.conf.task_routes = ([
    ('ebook_generator.*', {'queue': 'eg'}),
    ('data_provider.*', {'queue': 'dp'})
],)

@celery.task(bind=True, name="ebook_generator.render_recipe_to_ebook")
def render_recipe_to_ebook(self, recipe):
    return {'message': 'All good'}