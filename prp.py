
import numpy as np

traits = ['Екстраверсія', 'Нейротизм', 'Доброзичливість', 'Добросовісність', 'Відкритість до досвіду']

def predict_personality(model, image):

    image = np.expand_dims(image, axis=0)
    
    predictions = model.predict(image)
    

    predicted_traits = {}
    for i, trait in enumerate(traits):
        predicted_traits[trait] = predictions[i][0][0]
        
    return predicted_traits
