from PySide6.QtWidgets import QApplication, QMainWindow
from ui_mini import Ui_MainWindow
import requests
import time
import threading
import platform
import subprocess


class MiniConnectUtil(QMainWindow):
    def __init__(self):
        super(MiniConnectUtil, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.thread_exit_flag = False
        self.ui.pushButton.clicked.connect(self.try_connect_to_wifi)
        self.check_status_thread = threading.Thread(target=self.check_status_thread)
        self.check_status_thread.start()
    
    def closeEvent(self, event) -> None:
        self.thread_exit_flag = True
        return super().closeEvent(event)

    def check_status_thread(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '192.168.4.1']

        while True:
            if subprocess.call(command) == True:
                self.ui.label_5.setText('192.168.4.1 disconnected')
            else:
                self.ui.label_5.setText('192.168.4.1 connected')
            time.sleep(1)
            if self.thread_exit_flag:
                break
        return

    def try_connect_to_wifi(self):
        mini_ip = '192.168.4.1'
        ssid = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        api_str = f'http://{mini_ip}/control?function=wifi&command=connect&ssid={ssid}&password={password}'
        try:
            response = requests.get(api_str)
        except requests.exceptions.ConnectTimeout:
            self.ui.label_4.setText('Connection Timeout')
        if response.status_code == 200:
            ip = response.json().get('wifi_sta_ip', '0.0.0.0')
            if ip == '0.0.0.0':
                self.ui.label_4.setText(f'Error connected to {ssid}')
            else:
                self.ui.label_4.setText(f'Connected!\n{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}')
        else: 
            self.ui.label_4.setText('Status code: ' + str(response.status_code))
        print('Hello')






if __name__ == "__main__":
    app = QApplication([])

    window = MiniConnectUtil()
    window.show()

    app.exec()
