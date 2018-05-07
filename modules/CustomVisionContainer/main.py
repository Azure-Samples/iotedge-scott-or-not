import tensorflow as tf
import requests
import socket
import argparse 
import io
import tensorflow as tf
from PIL import Image
import numpy as np
import json
import os
import sys
from flask import Flask, redirect, request, Response, flash
import glob

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MODEL_SUFFIX = '.pb'
LABEL_MAP_SUFFIX = '.pbtxt'
MODEL_NAME = 'model'

MODEL_FOLDER = os.getenv('MODEL_FOLDER', './models_classify')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './pics/')


PORT = int(os.getenv('PORT', '8080'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_labelmap(filename):
    categories = []
    for category in open(filename, "r"):
        categories.append(category)
    return categories

def create_category_index(categories):
  category_index = {}
  for i,cat in enumerate(categories):
    category_index[i] = cat
  return category_index

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

def load_model(model_dir, model_prefix):
    categories = load_labelmap('{}/{}{}'.format(model_dir, model_prefix, LABEL_MAP_SUFFIX))
    category_index = create_category_index(categories)

    with tf.Graph().as_default() as classification_graph:
        ic_graph_def = tf.GraphDef()
   
        with tf.gfile.GFile('{}/{}{}'.format(model_dir, model_prefix, MODEL_SUFFIX), "rb") as f:
            
            ic_graph_def.ParseFromString(f.read())
            tf.import_graph_def(ic_graph_def, name='')

            ops = classification_graph.get_operations()
            all_tensor_names = {
                    output.name
                    for op in ops for output in op.outputs
                }

            tensor_dict = {}
            for key in [
                        'loss', 
                ]:
                tensor_name = key + ':0'
                
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = classification_graph.get_tensor_by_name(tensor_name)
                image_tensor = classification_graph.get_tensor_by_name('Placeholder:0')
                sess = tf.Session(graph=classification_graph)
            print("tensor_dict", tensor_dict)

    return {
        'session': sess,
        'image_tensor': image_tensor, 
        'tensor_dict': tensor_dict,
        'category_index': category_index
    }


def load_models(model_dir):

    models = {}
    for model_file in glob.glob('{}/*{}'.format(model_dir, MODEL_SUFFIX)):
        model_prefix = os.path.basename(model_file)[:-len(MODEL_SUFFIX)]
        print('Loading model {} from {}/{}{}'.format(model_prefix, model_dir, model_prefix, MODEL_SUFFIX))
        models[model_prefix] = load_model(model_dir, model_prefix)
    return models

def evaluate(model, image):


    image_np = np.asarray(Image.open(image).resize((227,227)))
    image_np_expanded = np.expand_dims(image_np, axis=0)

    output_dict = model['session'].run(
        model['tensor_dict'], feed_dict={model['image_tensor']: image_np_expanded})


    result_idx = np.argmax(output_dict['loss'])
    print(result_idx)
    result = {}
    print('category: ', model['category_index'])
    initial_class = model['category_index'][result_idx]
    result['class'] = initial_class.replace('\n', '')
    result['confidence'] = str(output_dict['loss'][0][result_idx])
    print('result: ', result)
    sys.stdout.flush()
    return (result)


@app.route('/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        if 'image' not in request.files:
            return Response(response='Missing file', status=400)
        modelname = MODEL_NAME
        if modelname not in app.config['MODELS']:
            models = load_models(MODEL_FOLDER)
            app.config['MODELS'] = models
            if modelname not in app.config['MODELS']:
                return Response(response='Model {} not found'.format(modelname), status=404)
        
        model = app.config['MODELS'][modelname]
        file = request.files['image']
        bin_file = io.BytesIO(file.read())
        
        try:
            print('Evaluating {} with model {}'.format(file.filename, modelname))
            evaluation = evaluate(model, file)
            call_azure_function(evaluation, bin_file)
            response = Response(response=json.dumps(evaluation), status=200, mimetype='application/json')
        except Exception as e:
            print(e)
            response = Response(response=str(e), status=501)

        return response
    return

def call_azure_function(json, image):
    # Send the image and the results to the Azure Function
    requests.post('http://' + socket.gethostbyname(AZURE_FUNCTION_HOSTNAME) + ':80/api/analyze', data=image, headers={'content-type': 'application/octet-stream'}, params=json, timeout=10)

def teardown(models):
    for model in models:
        print('Tearing down {}'.format(model))
        models[model]['session'].close()
        
import atexit
if __name__ == '__main__':
    
    global AZURE_FUNCTION_HOSTNAME
    AZURE_FUNCTION_HOSTNAME = os.environ['AZURE_FUNCTION_HOSTNAME']

    models = load_models(MODEL_FOLDER)
    print('Loading models')
    atexit.register(lambda: teardown(models))
    app.config['MODELS'] = models
    app.run(host='0.0.0.0', port=PORT)
