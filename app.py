from flask import Flask, render_template, request
from keras.models import load_model
from tensorflow import get_default_graph
from keras.preprocessing.image import img_to_array 
from PIL import Image, ImageChops, ImageFilter
from numpy import argmax, invert, expand_dims
from base64 import b64decode


def load():
    global model, graph
    model = load_model("model/model.h5")
    graph = get_default_graph()


app=Flask(__name__)
load()


def prepare_image(image):
    # Aplico filtros para que se vea más parecido a los datos con los que entreno el modelo y lo convierto al formato necesario
    image = image.convert("L")
    image = ImageChops.invert(image)
    image = image.filter(ImageFilter.BLUR).filter(ImageFilter.SMOOTH_MORE).filter(ImageFilter.SHARPEN)
    image = image.filter(ImageFilter.BLUR).filter(ImageFilter.SMOOTH_MORE).filter(ImageFilter.SHARPEN)
    image = image.resize((28,28))
    image = image.filter(ImageFilter.SMOOTH_MORE).filter(ImageFilter.SHARPEN)
    image.save("effected.png")
    image = img_to_array(image)
    image = expand_dims(image,0)
    return image

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Decodifico los datos y creo la imágen
    img_decoded = b64decode(request.get_data()[22:])
    with open("temp.png","wb") as temp:
        temp.write(img_decoded)

    # Preparo los datos para analizarlos
    image = Image.open("temp.png")
    image_data = prepare_image(image)

    # Realizo la predicción y tomo la mejor respuesta
    with graph.as_default():
        predictions = model.predict(image_data,steps=5)
    
    best_answer = argmax(predictions[0])

    return str(best_answer)


app.run(debug=True, port=8000)