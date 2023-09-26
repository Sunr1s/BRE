from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

traits = ['Экстраверсия', 'Нейротизм', 'Доброжелательность', 'Добросовестность', 'Открытость к опыту']

def predict_personality(model, image):

    image = np.expand_dims(image, axis=0)
    
    predictions = model.predict(image)
    

    predicted_traits = {}
    for i, trait in enumerate(traits):
        predicted_traits[trait] = predictions[i][0][0]
        
    return predicted_traits
