# In celery_config.py or similar file

from .celery_config import celery_app
from ..cnn import predict  # Ensure these are adapted to work as standalone functions
from ..llm import get_response

@celery_app.task
def perform_prediction(image):
    """
    A Celery task that performs image prediction using a convolutional neural network.
    This function processes an image to predict its content and calculate the probabilities of different classifications.
    
    Args:
        image (bytes): The image data in bytes format, ready to be processed by the prediction model.

    Returns:
        tuple: A tuple containing the predicted classification and a list of probabilities associated with each class.
    """
    prediction, probabilities = predict(image)
    return prediction, probabilities.tolist()

@celery_app.task
def fetch_contextual_information(prediction, sensitive_structures):
    """
    A Celery task that fetches contextual information based on a given prediction and the sensitivity of certain structures.
    This function uses language models to generate text responses that provide context, impact assessment, and potential solutions
    for the predicted event, specifically tailored to an African context and local community management.

    Args:
        prediction (str): The predicted incident or object from the image.
        sensitive_structures (list): A list of structures or elements identified as sensitive and relevant to the incident.

    Returns:
        tuple: A tuple containing contextual information about the incident, its impact on the sensitive structures, and suggested solutions.
    """
    get_context = get_response(f"What is a {prediction} in an African zone?")
    impact = get_response(f"What is the impact of {prediction} on {sensitive_structures}")
    piste_solution = get_response("What are the possible solutions for the previous case? Assuming it's managed by a local community.")
    return get_context, impact, piste_solution
