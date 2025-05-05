import numpy as np
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model

# Load the model once when this module is first imported
model = load_model("models/efficientnetv2_fracture_final.keras")

def preprocess_image(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))            # Same size as during training
    image_array = np.array(image) / 255.0      # Normalize to [0,1]
    return np.expand_dims(image_array, axis=0)  # Add batch dimension

def predict_fracture(image_bytes):
    """
    Given raw image bytes, return a float probability of fracture.
    """
    input_tensor = preprocess_image(image_bytes)
    prediction = model.predict(input_tensor)[0][0]
    return float(prediction)
