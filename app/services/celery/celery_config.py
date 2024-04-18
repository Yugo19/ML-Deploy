from celery import Celery

def make_celery():
    # Initialize Celery
    celery = Celery(
        'worker',
        backend='redis://yugo:Maoene@192.168.0.7:6379/0',
        broker='redis://yugo:Maoene@192.168.0.7:6379/0'
    )
    return celery

celery_app = make_celery()
