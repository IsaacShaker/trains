from flask import Flask, jsonify, request

app = Flask(__name__)
app.my_app_instance = None  # Placeholder for the MyApp instance

# @app.route('/data', methods=['GET'])
# def get_data():
#     # Access the `data_main` attribute from the MyApp instance
#     if hasattr(app.my_app_instance, 'data_main'):
#         data = app.my_app_instance.get_main_data()
#         return jsonify(data), 200
#     else:
#         return jsonify({"error": "Data not available"}), 500
    
@app.route('/data/block_occupancies/', methods=['GET'])
def get_data():
    # Access the `data_main` attribute from the MyApp instance
    if hasattr(app.my_app_instance, 'data_main'):
        data = app.my_app_instance.get_main_data()["Blue"]["SW"]["blocks"]
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not available"}), 500

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    print("Flask server shutting down...")

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return "Shutting down...", 200

# Function to start the Flask server
def start_api(my_app_instance):
    app.my_app_instance = my_app_instance
    app.run(host='127.0.0.1', port=5000)
