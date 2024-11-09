import sys
from threading import Thread
from TrackController.app import MyApp
import requests
from api import start_api
from CTC.ctc import MyWindow
from TrainModel.TrainModel_UI import Train_UI
from Train_Controller_SW.User_Interface import Train_Controler_SW_UI
from PyQt6.QtWidgets import QApplication


class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.ctc = MyWindow()
        self.track_controller = MyApp()
        self.train_model=Train_UI()
        self.train_controller_sw = Train_Controler_SW_UI()

        self.track_controller.show()
        self.ctc.show()
        self.train_model.show()
        self.train_controller_sw.show()

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