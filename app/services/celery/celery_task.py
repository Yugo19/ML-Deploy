# In celery_config.py or similar file

from .celery_config import celery_app
from ..cnn import predict  # Ensure these are adapted to work as standalone functions
from ..llm import get_response

@celery_app.task
def perform_prediction(image):
    prediction, probabilities = predict(image)
    return prediction, probabilities.tolist()

@celery_app.task
def fetch_contextual_information(prediction, sensitive_structures):
    get_context = get_response(f"What is a {prediction} in an African zone?")
    impact = get_response(f"What is the impact of {prediction} on {sensitive_structures}")
    piste_solution = get_response("What are the possible solutions for the previous case? Assuming it's managed by a local community.")
    return get_context, impact, piste_solution
