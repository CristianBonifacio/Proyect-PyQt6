from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets  import QFileDialog
import pandas as pd
class view_directory(QtWidgets.QWidget):
    def __init__(self,datos,colums):
        super(view_directory, self).__init__()
        self.view_directory = uic.loadUi(r'D:\Desarrollos-Belltech\INTERFAZ-MARCOVERA\Beta-App\gui\directory.view.ui')
        self.view_directory.show()
        self.view_directory.toolButton.clicked.connect(self.Open_File)
        self.datos=datos
        self.columns=colums
        self.mi_lista = [list(tupla) for tupla in self.datos]


    def Open_File(self):
        dialog = QFileDialog()
        options = dialog.options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "Archivos CSV (*.csv);;Excel Files (*.xlsx;*.xls)", options=options)
        
        if file_name:
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = pd.DataFrame(self.mi_lista, columns=self.columns)
                df.to_excel(file_name, index=False)
                print(f"Guardando archivo Excel en: {file_name}")
            elif file_name.endswith('.csv'):
                df = pd.DataFrame(self.mi_lista, columns=self.columns)
                df.to_csv(file_name, index=False)
                print(f"Guardando archivo CSV en: {file_name}")
            else:
                print("Formato de archivo no soportado.")