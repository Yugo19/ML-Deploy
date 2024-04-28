from celery import Celery

def make_celery():
    """
    Create and configure a Celery application instance with Redis as the message broker and backend.
    
    This function sets up Celery with Redis, specifying the same URI for both the backend and broker. 
    This configuration is necessary for task queueing and result storage for distributed task processing.

    Returns:
        Celery: A Celery application instance configured to use Redis for queuing tasks and storing results.
    """
    # Initialize Celery
    celery = Celery(
        'worker',  # Name of the worker
        backend='redis://yugo:Maoene@redis:6379/0',  # URI for Redis backend (Results backend)
        broker='redis://yugo:Maoene@redis:6379/0'    # URI for Redis broker (Queue)
    )
    return celery

celery_app = make_celery()
