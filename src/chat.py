from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from receiver import Receiver
from sender import Sender


class Chat(QWidget):

    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Chat')
        self.resize(500, 200)
        self.USERNAME = username

        layout = QGridLayout()

        self.text_area = QTextEdit()
        self.text_area.setFocusPolicy(Qt.NoFocus)

        self.message = QLineEdit()
        self.message.returnPressed.connect(self.send_msg)

        self.to = QLineEdit()
        self.to.returnPressed.connect(self.create_sender)

        layout.addWidget(self.text_area, 0, 0)
        layout.addWidget(self.message, 1, 0)
        layout.addWidget(self.to, 2, 0)

        self.setLayout(layout)

    def send_msg(self):
        self.sender._send(self.message.text())
        self.text_area.append(f"You: {self.message.text()}")
        self.message.clear()

    def recive_msg(self, ch, method, properties, body):
        self.text_area.append(f"{method.exchange_name}: {body.decode()}")

    def create_sender(self):
        self.sender = Sender(
            host='localhost', exchange_name=self.USERNAME, routing_key=self.to.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    chat = Chat(sys.argv[1])
    chat.show()

    sys.exit(app.exec_())
