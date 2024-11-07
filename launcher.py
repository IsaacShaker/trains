import sys
from threading import Thread
from TrackController.app import MyApp
import requests
from api import start_api
from CTC.ctc import MyWindow
from TrainModel.TrainModel_UI import MyTrain
from PyQt6.QtWidgets import QApplication

def getBlocksFromTrackController(self):
        try:
            url = '/track-controller/get-data/block_occupancies'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()  # Converts JSON to a dictionary
                print("Data received:", data)
            else:
                print("Error:", response.json())
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.ctc = MyWindow()
        self.track_controller = MyApp()
        self.train_model=MyTrain()

        self.track_controller.show()
        self.ctc.show()
        self.train_model.show()

    def closeEvent(self, event):
        """Override close event to shutdown Flask server."""
        requests.get('http://127.0.0.1:5000/shutdown')
        event.accept()
    
if __name__ == '__main__':
    ex = MainApp(sys.argv)

    # Start the API server and pass the MyApp instance
    flask_thread = Thread(target=start_api, args=(ex,), daemon=True)
    flask_thread.start()

    sys.exit(ex.exec())
