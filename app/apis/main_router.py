from fastapi import APIRouter, HTTPException, FastAPI, Query
from fastapi.responses import JSONResponse
from ..services import predict, contextualize, chat_bot, get_response, perform_prediction, fetch_contextual_information, celery_app
from ..models import ImageModel
from ..database import database

import requests

router = APIRouter()

base_url = "http://139.144.63.238"

@router.get('/')
def index():
    """
    Returns a greeting message indicating the API is operational.
    
    Returns:
        dict: A dictionary with a message key indicating the service status.
    """
    return {'message': 'Map Action classification model'}

@router.post('/image/predict')
async def predict_incident_type(data: ImageModel):
    """
    Receives an image as input and predicts the type of incident depicted in the image.
    Additionally, it fetches contextual information based on the prediction and stores the results in a database.

    Args:
        data (ImageModel): The image data received from the client, which includes the image path, sensitivity of structures in the image, and an incident ID.

    Returns:
        JSONResponse: A JSON response containing the prediction, probabilities of each predicted class, contextual information, impact analysis, and proposed solutions.
    
    Raises:
        HTTPException: An error response with status code 500 if the image could not be fetched or if there is an issue during processing.
    """
    try:
        # Extract data from ImageModel
        image_path = data.image_name  # Use the correct field name here
        sensitive_structures = data.sensitive_structures
        incident_id = data.incident_id

        # Fetch image and preprocess it
        response = requests.get(base_url + image_path)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to fetch image from {base_url + image_path}")

        image = response.content

        # Perform prediction and contextualization
        prediction_task = perform_prediction.delay(image)
        prediction, probabilities = await prediction_task.get(timeout=120)

        context_task = fetch_contextual_information.delay(prediction, data.sensitive_structures)
        get_context, impact, piste_solution = await context_task.get(timeout=120)

        query = """
        INSERT INTO "Mapapi_prediction" (incident_id, piste_solution, impact_potentiel, context)
        VALUES (:incident_id, :piste_solution, :impact_potentiel, :context);
        """
        values = {
            "incident_id": data.incident_id,
            "piste_solution": piste_solution,
            "impact_potentiel": impact,
            "context": get_context
        }
        result = await database.execute(query=query, values=values)

        # Return JSON response
        return JSONResponse(content={
            "prediction": prediction,
            "probabilities": probabilities.tolist(),
            "context": get_context,
            "in_depht": impact,
            "piste_solution": piste_solution
        })

    except Exception as e:
        # Handle exceptions and return appropriate HTTP response
        raise HTTPException(status_code=500, detail=str(e))
