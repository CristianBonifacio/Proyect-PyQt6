from PyQt6 import uic
from PyQt6.QtWidgets import QFileDialog,QTableWidgetItem
from PyQt6 import QtCore
from PyQt6.QtCore import QDate
import sys
import os
import pandas as pd
# Añadir el directorio principal al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexion import Conexion

class view_Principal():
    def __init__(self):
        self.conexion = Conexion()
        self.viewPrincipal=uic.loadUi("Gui/Form_view_principal.ui")
        self.viewPrincipal.FormDate.setDisplayFormat("yyyy-MM-dd")
        self.viewPrincipal.FormDate_2.setDisplayFormat("yyyy-MM-dd")
        date_str = "2024-05-28"
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        self.viewPrincipal.FormDate.setDate(date)
        self.viewPrincipal.FormDate_2.setDate(QtCore.QDate.currentDate())
        self.viewPrincipal.show()
        #conectar el boton toolButton a la funcion openFileNameDialog
        self.viewPrincipal.Buscar.clicked.connect(self.button_Buscar)
        self.button_File()

    def open_file_dialog(self):
        dialog = QFileDialog()
        options = dialog.options()
        file_name, _ = dialog.getOpenFileName(None, "Select File", "", "All Files (*);;Excel Files (*.xlsx;*.xls,*.csv)", options=options)
        if file_name.endswith('.xlsx'):
            df =pd.read_excel(file_name)
            num_filas = len(df)
            num_columnas = len(df.columns)
            nombres_columnas=df.columns.tolist()
            print(num_columnas)
            print(num_filas)
            print(nombres_columnas)
        elif file_name.endswith('.csv'):
            df = pd.read_csv(file_name)
            num_filas = len(df)
            num_columnas = len(df.columns)
            print(f"Número de filas: {num_filas}")
            print(f"Número de columnas: {num_columnas}")
        if file_name:
            file_base_name = os.path.basename(file_name)
            self.viewPrincipal.toolButton.setText(file_base_name)  # Mostrar la ruta del archivo en el cuadro de texto (TextEdit)
             # Cambiar el tamaño del botón toolButton
            self.viewPrincipal.toolButton.setFixedWidth(100)  # Aumenta el ancho del botón

    def mostrar_export_intable(self,datos,columnas,filas,nombre_columnas):
        self.viewPrincipal.tableWidget.setRowCount(filas)
        self.viewPrincipal.tableWidget.setColumnCount(columnas)
        self.viewPrincipal.tableWidget.setHorizontalHeaderLabels(nombre_columnas)
        for i in range(              ):
            for j in range(5):
                item = QTableWidgetItem(f"({i}, {j})")
                self.viewPrincipal.tableWidget.setItem(i, j, item)                                                                                                             


    def button_File(self):
        self.viewPrincipal.toolButton.clicked.connect(self.open_file_dialog)

#Consultas a la basededatos
    #consulta por fecha de inicio y fecha final
    def consulta_todate_tofrom(self):
        todate = self.viewPrincipal.FormDate.date().toString("yyyy-MM-dd")
        fromdate = self.viewPrincipal.FormDate_2.date().toString("yyyy-MM-dd")
        resultados,nombres_columnas = self.conexion.consulta_tofecha(todate, fromdate)
        self.Mostrar_datos_entabla_general(resultados,nombres_columnas)
    #consulta por anexo y fecha de inicio y fecha final
    def consulta_anexo(self):
        anexo = self.viewPrincipal.TextEdit.text()
        todate = self.viewPrincipal.FormDate.date().toString("yyyy-MM-dd")
        fromdate = self.viewPrincipal.FormDate_2.date().toString("yyyy-MM-dd")
        resultados,nombres_columnas = self.conexion.consultar_anexo(anexo,todate, fromdate)
        self.mostrar_Datos_por_anexo(resultados,nombres_columnas)    


    #consulta por destino y fecha de inicio y fecha final
    def consulta_destination(self):
        destination = self.viewPrincipal.TextNumero.text()
        todate = self.viewPrincipal.FormDate.date().toString("yyyy-MM-dd")
        fromdate = self.viewPrincipal.FormDate_2.date().toString("yyyy-MM-dd")
        resultados,nombres_columnas = self.conexion.consultar_destination(destination,todate,fromdate)
        self.mostrar_Datos_por_destino(resultados,nombres_columnas)     

    #consulta por anexo,destino,fecha de inicio y fecha final
    def consulta_anexo_destination(self):
        anexo = self.viewPrincipal.TextEdit.text()
        destination = self.viewPrincipal.TextNumero.text()
        todate = self.viewPrincipal.FormDate.date().toString("yyyy-MM-dd")
        fromdate = self.viewPrincipal.FormDate_2.date().toString("yyyy-MM-dd")
        resultados,nombres_columnas = self.conexion.consultar_anexo_destination(anexo,destination,todate,fromdate)
        self.Mostrar_datos_entabla_general(resultados,nombres_columnas)

#Mostrar tablas en la interfaz conectando la consultas
    def Mostrar_datos_entabla_general(self, datos,nombres_columnas):
        #Limpiar tabla actual
        self.viewPrincipal.tableWidget.clear()
        

        # Obtener el número de filas y columnas
        num_filas = len(datos)
        num_columnas = len(nombres_columnas)

        # Configurar la tabla
        self.viewPrincipal.tableWidget.setRowCount(num_filas)
        self.viewPrincipal.tableWidget.setColumnCount(num_columnas)

        #Añadir los nombres de la columna a la tabla
        self.viewPrincipal.tableWidget.setHorizontalHeaderLabels(nombres_columnas)


        # Añadir los datos a la tabla
        for fila in range(num_filas):
            for columna in range(num_columnas):
                item = QTableWidgetItem(str(datos[fila][columna]))
                self.viewPrincipal.tableWidget.setItem(fila, columna, item)
    
    def mostrar_Datos_por_anexo(self, datos,nombres_columnas):
        #Limpiar tabla actual
        self.viewPrincipal.tableWidget.clear()

        # Obtener el número de filas y columnas
        num_filas = len(datos)
        num_columnas = len(nombres_columnas)

        # Configurar la tabla
        self.viewPrincipal.tableWidget.setRowCount(num_filas)
        self.viewPrincipal.tableWidget.setColumnCount(num_columnas)

        #Añadir los nombres de la columna a la tabla
        self.viewPrincipal.tableWidget.setHorizontalHeaderLabels(nombres_columnas)
        # Añadir los datos a la tabla
        for fila in range(num_filas):
            for columna in range(num_columnas):
                item = QTableWidgetItem(str(datos[fila][columna]))
                self.viewPrincipal.tableWidget.setItem(fila, columna, item)

    def mostrar_Datos_por_destino(self,datos,nombres_columnas):
        #Limpiar tabla actual
        self.viewPrincipal.tableWidget.clear()

        # Obtener el número de filas y columnas
        num_filas = len(datos)
        num_columnas = len(nombres_columnas)

        # Configurar la tabla
        self.viewPrincipal.tableWidget.setRowCount(num_filas)
        self.viewPrincipal.tableWidget.setColumnCount(num_columnas)

        #Añadir los nombres de la columna a la tabla
        self.viewPrincipal.tableWidget.setHorizontalHeaderLabels(nombres_columnas)
        # Añadir los datos a la tabla
        for fila in range(num_filas):
            for columna in range(num_columnas):
                item = QTableWidgetItem(str(datos[fila][columna]))
                self.viewPrincipal.tableWidget.setItem(fila, columna, item)

    def mostrar_Datos_por_anexo_Destino(self,datos,nombres_columnas):
        #limpiar tabla 
        self.viewPrincipal.tableWidget.clear()
        #obtener el numero de filas y columnas
        num_filas =len(datos)
        num_Columnas=len(nombres_columnas)

        #configurar la tabla
        self.viewPrincipal.tableWidget.setRowCount(num_filas)
        self.viewPrincipal.tableWidget.setColumnCount(num_Columnas)

        #añadir los nombres de la columna a la tabla
        self.viewPrincipal.tableWidget.setHorizontalHeaderLabels(nombres_columnas)  
        #añadir los datos a la tabla
        for fila in range(num_filas):
            for columna in range(num_Columnas):
                item = QTableWidgetItem(str(datos[fila][columna]))
                self.viewPrincipal.tableWidget.setItem(fila,columna,item)




#Buton que se encarga de mostrar las consultas y las tablas
    def button_Buscar(self):
            if self.viewPrincipal.TextEdit.text() == "" and self.viewPrincipal.TextNumero.text() == "":
                self.consulta_todate_tofrom()
            elif self.viewPrincipal.TextEdit.text() == "" and self.viewPrincipal.TextNumero.text() != "":
                self.consulta_destination()
            elif self.viewPrincipal.TextEdit.text() != "" and self.viewPrincipal.TextNumero.text() == "":
                self.consulta_anexo()   
            elif self.viewPrincipal.TextEdit.text() != "" and self.viewPrincipal.TextNumero.text() != "":
                self.consulta_anexo_destination() 
