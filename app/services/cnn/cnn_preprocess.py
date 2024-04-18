import io
from PIL import Image
from torchvision.transforms import transforms



transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                #transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])

def preprocess_image(image):
    image = Image.open(io.BytesIO(image)).convert("RGB")
    image = transform(image).unsqueeze(0)
    return image