from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)
app.qt_app_instance = None

###################################
#Train Contoller Input Functions
###################################

@app.route('/train-controller/recieve-authority', methods=['POST'])
def recieve_authority():
    data = request.get_json()

    float_value = data.get("authority", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_authority(float_value)


@app.route('/train-controller/recieve-beacon-info', methods=['POST'])
def recieve_beacon_info():
    data = request.get_json()

    string_value = data.get("beacon_info", None)
    index = data.get("train_id", None)

    if string_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_beacon_info(string_value)


@app.route('/train-controller/recieve-commanded-velocity', methods=['POST'])
def recieve_commanded_velocity():
    data = request.get_json()

    float_value = data.get("commanded_velocity", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_commanded_velocity(float_value)


@app.route('/train-controller/recieve-actual-velocity', methods=['POST'])
def recieve_actual_velocity():
    data = request.get_json()

    float_value = data.get("actual_velocity", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_actual_velocity(float_value)


@app.route('/train-controller/recieve-failure_modes', methods=['POST'])
def recieve_failure_modes():
    data = request.get_json()

    engine_string = data.get("failure_engine", None)
    brake_string = data.get("failure_brake", None)
    signal_string = data.get("failure_signal", None)
    index = data.get("train_id", None)

    if engine_string is None or brake_string or signal_string or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_failure_engine(engine_string)
    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_failure_brake(brake_string)
    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_failure_signal(signal_string)


###################################
#Train Model Input Functions
###################################

@app.route('/train-model/recieve-commanded-power', methods=['POST'])
def recieve_commanded_power():
    data = request.get_json()

    float_value = data.get("commanded_power", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.train_model.train_list[index].set_commanded_power(float_value)




@app.route('/track-controller/get-data/block_occupancies', methods=['GET'])
def get_data():
    # Access the `data_main` attribute from the MyApp instance
    if hasattr(app.qt_app_instance, 'track_controller'):
        if hasattr(app.qt_app_instance.track_controller, 'data_test'):
            data = app.qt_app_instance.track_controller.get_test_data()["Blue"]["SW"]["blocks"]
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

@app.route('/', methods=['GET'])
def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Group 2 API Server</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                color: #333;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 20px;
                border: 1px solid #ddd;
                background-color: #fff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                max-width: 500px;
                width: 90%;
            }
            h1 {
                color: #4CAF50;
            }
            p {
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Group 2 API Server</h1>
            <p>You have reached the root of our API server. Use the available endpoints to interact with the server.</p>
            <p>Thank you for visiting!</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content), 200

# Function to start the Flask server
def start_api(qt_app_instance):
    app.qt_app_instance = qt_app_instance
    app.run(host='127.0.0.1', port=5000)
