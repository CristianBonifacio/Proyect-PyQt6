from PyQt6.QtWidgets import QApplication
from view_app import view_app

#test
class App():
    def __init__(self):
        self.app = QApplication([])
        self.view = view_app()
        self.app.exec()


App()