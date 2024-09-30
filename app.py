from flask import Flask, jsonify, request, render_template, send_file
import numpy as np
from lloyds import KMeans, random_centers, farthest_centers, kplusplus_centers 
import sklearn.datasets as datasets
from matplotlib import pyplot as plt
import os
import shutil

app = Flask(__name__)

global data_points

@app.route('/')
def index():
    return render_template('index.html')

def initial_capture(data):
    # Generate the scatter plot and save it as 'static/plot.png'
    plt.scatter(data[:, 0], data[:, 1], c='blue', alpha=0.6)
    plt.savefig('static/plot.png')
    plt.close()  # Close the plot to prevent memory leaks

@app.route('/initialize', methods=['GET'])
def initialize():
    print("initializing")
    global data_points

    return generate_data()

# @app.route('/step')
# def step():
#     step_number = int(request.args.get('step', 0))
#     # Logic to determine the appropriate image for the step
#     image_path = f'static/step_images/step_{step_number}.png'
#     return send_file(image_path)

@app.route('/generate_data', methods=['GET'])
def generate_data(num_points=300):
    global data_points
    data_points = []
    # Generate random data points with specified num_points
    data_points, _ = datasets.make_blobs(n_samples=300, cluster_std=1)

    if os.path.exists('static/plot.png'):
        os.remove('static/plot.png')

    initial_capture(data_points)

    return send_file('static/plot.png', mimetype='image/png') # Return the generated data

@app.route('/kmeans', methods=['GET'])   #, methods=['POST']
def kmeans():
    global data_points

    data = data_points
    n_clusters = int(request.args.get("k"))
    init_method = request.args.get('init_method', 'random')
    centers = []

    if init_method == "random":
        centers = random_centers(n_clusters, data)
    elif init_method == "farthest_first":
        centers = farthest_centers(n_clusters, data)
    elif init_method == "kmeans++":
        centers = kplusplus_centers(n_clusters, data)

    kmeans = KMeans(data, n_clusters, centers)
    kmeans.lloyds()
    images = kmeans.snaps
    # return jsonify(images)
    # images = [image_to_base64(img) for img in kmeans.snaps]
    return jsonify({"images": images, "steps": len(images)})

def image_to_base64(img):
    import io
    import base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if __name__ == '__main__':
    app.run(port=3000, debug=True)
