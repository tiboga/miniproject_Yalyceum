import json
import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

import return_params

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        params = return_params.ret_params()
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def image_redistribution(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            data = return_params.ret_params()
            print(float(data['spn'].split(',')[0]))
            if float(data['spn'].split(',')[0]) > 0.04:
                if float(data['spn'].split(',')[0]) < 0.5:
                    data['spn'] = f"{float(data['spn'].split(',')[0]) - 0.04},{float(data['spn'].split(',')[1]) - 0.04}"
                else:
                    data['spn'] = f"{float(data['spn'].split(',')[0]) - 0.5},{float(data['spn'].split(',')[1]) - 0.5}"
            with open('params.json', 'w') as f:
                json.dump(data, f)
        elif event.key() == Qt.Key_PageUp:
            data = return_params.ret_params()
            print(float(data['spn'].split(',')[0]))
            if float(data['spn'].split(',')[0]) < 9.5:
                if float(data['spn'].split(',')[0]) < 0.5:
                    data['spn'] = f"{float(data['spn'].split(',')[0]) + 0.04},{float(data['spn'].split(',')[1]) + 0.04}"

                else:
                    data['spn'] = f"{float(data['spn'].split(',')[0]) + 0.5},{float(data['spn'].split(',')[1]) + 0.5}"
            with open('params.json', 'w') as f:
                json.dump(data, f)
        self.getImage()
        self.image_redistribution()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
