from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)
app.qt_app_instance = None

###################################
#Train Contoller Input Functions
###################################

@app.route('/train-controller/receive-authority', methods=['POST'])
def receive_authority():
    data = request.get_json()

    float_value = data.get("authority", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_authority(float_value)
    #app.qt_app_instance.Train_Controller_HW_UI.set_authority(float_value)
    return jsonify("Success"), 200


@app.route('/train-controller/receive-beacon-info', methods=['POST'])
def receive_beacon_info():
    data = request.get_json()

    string_value = data.get("beacon_info", None)
    index = data.get("train_id", None)

    if string_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_beacon_info(string_value)
    #app.qt_app_instance.Train_Controller_HW_UI.set_beacon_information(string_value)
    return jsonify("Success"), 200


@app.route('/train-controller/receive-commanded-velocity', methods=['POST'])
def receive_commanded_velocity():
    data = request.get_json()

    float_value = data.get("commanded_velocity", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_commanded_velocity(float_value)
    #app.qt_app_instance.Train_Controller_HW_UI.set_commanded_velocity(float_value)
    return jsonify("Success"), 200


@app.route('/train-controller/receive-actual-velocity', methods=['POST'])
def receive_actual_velocity():
    data = request.get_json()

    float_value = data.get("actual_velocity", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.Train_Controler_SW_UI.train_list[index].set_actual_velocity(float_value)
    #app.qt_app_instance.Train_Controller_HW_UI.set_actual_velocity(float_value)
    return jsonify("Success"), 200


@app.route('/train-controller/receive-failure_modes', methods=['POST'])
def receive_failure_modes():
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
    #app.qt_app_instance.Train_Controller_HW_UI.set_engine_failure(engine_string)
    #app.qt_app_instance.Train_Controller_HW_UI.set_brake_failure(brake_string)
    #app.qt_app_instance.Train_Controller_HW_UI.set_signal_failure(signal_string)
    return jsonify("Success"), 200


###################################
#Train Model Input Functions
###################################

@app.route('/train-model/receive-commanded-power', methods=['POST'])
def receive_commanded_power():
    data = request.get_json()

    float_value = data.get("commanded_power", None)
    index = data.get("train_id", None)

    if float_value is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.train_model.train_list[index].set_commanded_power(float_value)
    return jsonify({"status": "Ok"}), 200
 
@app.route('/train-model/receive-lights', methods=['POST'])
def receive_lights():
    data = request.get_json()

    inside_lights = data.get("i_light", None)
    outside_lights = data.get("o_light", None)
    index = data.get("train_id", None)

    if inside_lights is None or index is None or outside_lights is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.train_model.train_list[index].set_insideLights(inside_lights)
    app.qt_app_instance.train_model.train_list[index].set_headLights(outside_lights)
    return jsonify({"status": "Ok"}), 200

@app.route('/train-model/receive-doors', methods=['POST'])
def receive_doors():
    data = request.get_json()

    left_door = data.get("l_door", None)
    right_door = data.get("r_door", None)
    index = data.get("train_id", None)

    if left_door is None or index is None or right_door is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.train_model.train_list[index].set_leftDoor(left_door)
    app.qt_app_instance.train_model.train_list[index].set_rightDoor(right_door)
    return jsonify({"status": "Ok"}), 200

@app.route('/train-model/receive-announcement', methods=['POST'])
def receive_announcement():
    data = request.get_json()

    announcement = data.get("pa_announcement", None)
    index = data.get("train_id", None)

    if announcement is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.train_model.train_list[index].set_announcements(announcement)
    return jsonify({"status": "Ok"}), 200

@app.route('/train-model/receive-temperature', methods=['POST'])
def receive_temperature():
    data = request.get_json()

    temperature = data.get("temperature", None)
    index = data.get("train_id", None)

    if temperature is None or index is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.train_model.train_list[index].set_temperature(temperature)
    return jsonify({"status": "Ok"}), 200

@app.route('/train-model/receive-brakes', methods=['POST'])
def receive_brakes():
    data = request.get_json()

    service_brake = data.get("s_brake", None)
    emergency_brake = data.get("e_brake", None)
    index = data.get("train_id", None)

    if service_brake is None or index is None or emergency_brake is None:
        return jsonify({"error": "No float vlaue recieved"}), 400

    app.qt_app_instance.train_model.train_list[index].set_serviceBrake(service_brake)
    app.qt_app_instance.train_model.train_list[index].set_emergencyBrake(emergency_brake)
    return jsonify({"status": "Ok"}), 200
    
    
###################################
# Train Controller API Endpoints  #
###################################

@app.route('/track-controller-sw/get-data/block_data', methods=['GET'])
def get_data1():
    # Access the `data_main` attribute from the MyApp instance
    if hasattr(app.qt_app_instance, 'track_controller'):
        data = app.qt_app_instance.track_controller.get_block_data()
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not available"}), 500

@app.route('/track-controller-sw/give-data/maintenance', methods=['POST'])
def get_data2():
    data = request.get_json()

    # check that the data is in the right format
    for attribute in ["line", "index", "maintenance"]:
        if attribute not in data:
            return jsonify({"error": "Data not in correct format. Make sure 'line', 'index' and 'maintenance' are included in data."}), 500

    if hasattr(app.qt_app_instance, 'track_controller'):
        data = app.qt_app_instance.track_controller.add_maintenance(data)
        return jsonify(data), 200
    
@app.route('/track-controller-sw/give-data/authority', methods=['POST'])
def get_data3():
    data = request.get_json()

    # check that the data is in the right format
    for attribute in ["line", "index", "authority"]:
        if attribute not in data:
            return jsonify({"error": "Data not in correct format. Make sure 'line', 'index' and 'authority' are included in data."}), 500

    if hasattr(app.qt_app_instance, 'track_controller'):
        data = app.qt_app_instance.track_controller.add_maintenance(data)
        return jsonify(data), 200
    
@app.route('/track-controller-sw/give-data/speed', methods=['POST'])
def get_data4():
    data = request.get_json()

    # check that the data is in the right format
    for attribute in ["line", "index", "speed"]:
        if attribute not in data:
            return jsonify({"error": "Data not in correct format. Make sure 'line', 'index' and 'speed' are included in data."}), 500

    if hasattr(app.qt_app_instance, 'track_controller'):
        data = app.qt_app_instance.track_controller.add_speed(data)
        return jsonify(data), 200
    
@app.route('/track-controller-sw/give-data/wayside-vsion', methods=['POST'])
def get_data5():
    data = request.get_json()

    # check that the data is in the right format
    for attribute in ["line", "id", "vision"]:
        if attribute not in data:
            return jsonify({"error": "Data not in correct format. Make sure 'line', 'id' and 'vision' are included in data."}), 500

    if hasattr(app.qt_app_instance, 'track_controller'):
        data = app.qt_app_instance.track_controller.wayside_vision(data)
        return jsonify(data), 200
    
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    print("Flask server shutting down...")

#Track Model 
@app.route('/track-model/get-data/all', methods=['GET'])
def get_data_track_model_all():
    # Access the data_main attribute from the MyApp instance
    if hasattr(app.qt_app_instance, 'track_model'):
        data = app.qt_app_instance.track_model.get_post_dict()
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not available"}), 500
    
@app.route('/train-model/get-data/current-speed', methods=['GET'])
def get_data_train_model_current_speed():
    # Access the data_main attribute from the MyApp instance
    if hasattr(app.qt_app_instance, 'train_model'):
        data = app.qt_app_instance.train_model.get_current_speed()
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not available"}), 500
    
#Track Controller to Track Model
@app.route('/track-model/recieve-signals', methods=['POST'])
def recieve_signals():
    data = request.get_json()
    app.qt_app_instance.track_model.set_signals(data)

#Track Model to Track Controller
@app.route('/track-model/get-data/occupancies', methods=['GET'])
def get_data_track_model_occupancies():
    # Access the data_main attribute from the MyApp instance
    if hasattr(app.qt_app_instance, 'track_model'):
        data = app.qt_app_instance.track_model.get_occupancies()
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not available"}), 500


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
