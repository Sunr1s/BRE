from flask import Flask, request, jsonify
from flask import Flask
from flask_cors import CORS
import base64
from PIL import Image
import io
import numpy as np
from tensorflow.keras.models import load_model
from prp import predict_personality  # Импортируем функцию из вашего файла

app = Flask(__name__)
cors = CORS(app)

# Загрузка модели
model = load_model('C:\\Users\\admin\\Desktop\\fio\\tmp')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data.get('image')
    if not image_data:
        return jsonify({'error': 'Missing image data'}), 400
    
    # Декодирование изображения
    image_data = image_data.split(',')[1]
    image_data = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    
    predicted_traits = predict_personality(model, image)
    
    # Формирование ответа в формате JSON
    response = {}
    for trait, value in predicted_traits.items():
        response[trait] = f"{value:.2f}%"
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
