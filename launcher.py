import sys
from threading import Thread
from TrackController.app import MyApp
import requests
from api import start_api
from CTC.ctc import MyWindow
from TrackModel.FinalUI import TrackUI
from TrainModel.TrainModel_UI import Train_UI
from Train_Controller_SW.User_Interface import Train_Controller_SW_UI
from Train_Controller_HW.TrainControllerHW import Train_Controller_HW_UI
from Train_Controller_HW.World_Timer import World_Clock
from PyQt6.QtWidgets import QApplication


class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        self.clock = World_Clock()
        self.ctc = MyWindow()
        self.track_controller = MyApp()
        self.train_model=Train_UI()
        self.train_controller_sw = Train_Controller_SW_UI(self.train_model.train_list, self.train_model.train_controller_list)
        self.train_controller_hw = Train_Controller_HW_UI(self.train_model.train_list)
        self.track_model = TrackUI()


        self.track_controller.show()
        self.ctc.show()
        self.train_model.show()
        self.train_controller_sw.show()
        self.train_controller_hw.show()
        self.track_model.show()

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
