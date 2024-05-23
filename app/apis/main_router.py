from fastapi import APIRouter, HTTPException, FastAPI, Query, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from ..services import predict, contextualize, chat_bot, get_response, perform_prediction, fetch_contextual_information, celery_app
from ..models import ImageModel
from ..database import database
import json
import requests
from ..services.websockets import *

manager = ConnectionManager()

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

    # @router post('/image/predict')
    # async def predict_incident_type(data: ImageModel):
    #     """
    #     Receives an image as input and predicts the type of incident depicted in the image.
    #     Additionally, it fetches contextual information based on the prediction and stores the results in a database.

    #     Args:
    #         data (ImageModel): The image data received from the client, which includes the image path, sensitivity of structures in the image, and an incident ID.

    #     Returns:
    #         JSONResponse: A JSON response containing the prediction, probabilities of each predicted class, contextual information, impact analysis, and proposed solutions.

    #     Raises:
    #         HTTPException: An error response with status code 500 if the image could not be fetched or if there is an issue during processing.
    #     """
    #     try:
    #         # Extract data from ImageModel
    #         image_path = data.image_name  # Use the correct field name here
    #         sensitive_structures = data.sensitive_structures
    #         incident_id = data.incident_id

    #         # Fetch image and preprocess it
    #         response = requests.get(base_url + image_path)
    #         if response.status_code != 200:
    #             raise HTTPException(status_code=500, detail=f"Failed to fetch image from {base_url + image_path}")

    #         image = response.content

    #         # Perform prediction and contextualization
    #         prediction_task = perform_prediction.delay(image)
    #         prediction, probabilities = await prediction_task.get(timeout=120)

    #         context_task = fetch_contextual_information.delay(prediction, data.sensitive_structures)
    #         get_context, impact, piste_solution = await context_task.get(timeout=120)

    #         query = """
    #         INSERT INTO "Mapapi_prediction" (incident_id, incident_type, piste_solution, impact_potentiel, context)
    #         VALUES (:incident_id, :incident_type :piste_solution, :impact_potentiel, :context);
    #         """
    #         values = {
    #             "incident_id": data.incident_id,
    #             "incideent_type": prediction,
    #             "piste_solution": piste_solution,
    #             "impact_potentiel": impact,
    #             "context": get_context
    #         }
    #         result = await database.execute(query=query, values=values)

    #         # Return JSON response
    #         return JSONResponse(content={
    #             "prediction": prediction,
    #             "probabilities": probabilities.tolist(),
    #             "context": get_context,
    #             "in_depht": impact,
    #             "piste_solution": piste_solution
    #         })

    #     except Exception as e:
    #         # Handle exceptions and return appropriate HTTP response
    #         raise HTTPException(status_code=500, detail=str(e))


@router.websocket('ws/image/predict')
async def prediction_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for predicting incident type based on an image.

    Args:
        websocket (WebSocket): The WebSocket connection.

    Raises:
        WebSocketDisconnect: If the WebSocket connection is disconnected.

    Returns:
        None
    """
    origin = websocket.headers.get('origin')
    allowed_origins = ["http://localhost:5432"]

    if origin not in allowed_origins:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        while True:

            data = await websocket.receive_json()
            image_path = data.get('image_name')
            sensitive_structures = data.get('sensitive_structures')
            incident_id = data.get('incident_id')

            response = requests.get(base_url + image_path)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500, detail=f"Failed to fetch image from {base_url + image_path}")

            image = response.content

            # Perform prediction
            prediction, probabilities = predict(image)

            # Fetch contextual information, impact, and solution
            get_context = get_response(
                f"What is a {prediction} in an African zone?")
            impact = get_response(
                f"What is the impact of {prediction} on {sensitive_structures}")
            piste_solution = get_response(
                "What are the possible solutions for the previous case? Assuming it's managed by a local community.")

            query = """
             INSERT INTO "Mapapi_prediction" (incident_id, incident_type, piste_solution, impact_potentiel, context)
             VALUES (:incident_id, :incident_type :piste_solution, :impact_potentiel, :context);
             """
            values = {
                "incident_id": data.incident_id,
                "incideent_type": prediction,
                "piste_solution": piste_solution,
                "impact_potentiel": impact,
                "context": get_context
            }

            result = await database.execute(query=query, values=values)

            # Send the result back to the client
            await websocket.send_json({
                "prediction": prediction,
                "probabilities": probabilities.tolist(),
                "context": get_context,
                "in_depth": impact,
                "piste_solution": piste_solution
            })
    except Exception as e:
        # Handle exceptions and close the WebSocket connection
        await websocket.close(code=status.WS_1002_PROTOCOL_ERROR)
