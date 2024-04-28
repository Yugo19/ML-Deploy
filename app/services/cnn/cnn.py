import os
import torch
from ..cnn.cnn_preprocess import preprocess_image
from ..cnn.cnn_model import m_a_model

# Initialize the VGG16 model with batch-normalized weights for 6 classes
model = m_a_model(6)
# Load state dict from a pre-trained model
loaded_state_dict = torch.load(os.environ.get('MODEL_PATH', 'cv_model/TCM1.pth'))
# Load the updated state dict into the model
model.load_state_dict(loaded_state_dict)

# List of categories for prediction
categories = ["Caniveau bouché", "Déchets solides", "Déchets solides dans les caniveaux",
              "Pollution de l’eau (matière en suspension)", "Pollution de l’eau (présence de déchets plastiques)", "Sol aride"]

def predict(image):
    """
    Performs image classification using a pre-trained VGG16 model modified for six specific categories.
    This function processes an input image, applies a pre-trained model, and returns the predicted category and
    probability distribution over all categories.

    Args:
        image (bytes): The image data in bytes format.

    Returns:
        tuple: A tuple containing the predicted category as a string and the probabilities of all categories as a tensor.
    """
    model.eval()  # Set the model to evaluation mode
    input_data = preprocess_image(image)  # Preprocess the image
    with torch.no_grad():  # Disable gradient calculation
        output = model(input_data)  # Get the model output
        probabilities = torch.nn.functional.softmax(output[0], dim=0)  # Calculate probabilities
        predicted_class = torch.argmax(probabilities, dim=0)  # Determine the predicted class

        predict_label_index = predicted_class.item()
        predict_label = categories[int(predict_label_index)]  # Get the category name from the index

        return predict_label, probabilities.tolist()  # Return the predicted category and probabilities

