import torch
from ..cnn.cnn_preprocess import preprocess_image
from ..cnn.cnn_model import m_a_model


# Initialize the VGG16 model with batch-normalized weights
model = m_a_model(6)
# Load state dict from a pre-trained model
loaded_state_dict = torch.load('cv_model/TCM1.pth')
# Load the updated state dict into the model
model.load_state_dict(loaded_state_dict)

categories = ["Caniveau bouché","Déchets solides","Déchets solides dans les caniveaux",
            "Pollution de l’eau (matière en suspension)","Pollution de l’eau (présence de déchets plastiques)","Sol aride"]

def predict(image):
    model.eval()
    input_data = preprocess_image(image)
    with torch.no_grad():
        output = model(input_data)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        predicted_class = torch.argmax(output, dim=1)
        
        print(predicted_class.item())  # Corrected line
        predict_label_index = predicted_class.item()
        predict_label = categories[int(predict_label_index)]

        return predict_label, probabilities
        
    return predict_label, probabilities , predict_label_index