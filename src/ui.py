import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
from database import Database
from chat import Chat


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.resize(500, 200)

        layout = QGridLayout()

        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Username:')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Password:')
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QPushButton('LogIn')
        button_login.clicked.connect(self.log_in)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        button_register = QPushButton('Register')
        button_register.clicked.connect(self.register)
        layout.addWidget(button_register, 3, 0, 1, 2)
        layout.setRowMinimumHeight(2, 10)

        self.setLayout(layout)

    def register(self):
        db = Database()

        if(not db._register(self.lineEdit_username.text(), self.lineEdit_password.text())):
            msg = QMessageBox()
            msg.setText(f'Username {self.lineEdit_username.text()} taken!')
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setText(
                f'{self.lineEdit_username.text()} you have been registerd!')
            msg.exec_()

    def log_in(self):

        db = Database()

        if(not db._log_in(self.lineEdit_username.text(), self.lineEdit_password.text())):
            msg = QMessageBox()
            msg.setText('Incorrect credientals')
            msg.exec_()
        else:
            chat = Chat(self.lineEdit_username.text())
            self.dialogs.append(chat)
            chat.show()


def main():
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
