from PyQt6.QtWidgets import QApplication
from Gui.view_principal import view_Principal

class App():
    def __init__(self):
        self.app = QApplication([])
        self.view = view_Principal()
        self.app.exec()


App()