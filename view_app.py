from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import QFileDialog,QTableWidgetItem
from PyQt6 import QtCore
from PyQt6.QtCore import QDate
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexion import conexion

class view_app:
    def __init__(self):
        self.conexion = conexion()
        self.view_app= uic.loadUi(r'D:\Desarrollos-Belltech\INTERFAZ-MARCOVERA\Beta-App\gui\Main.ui')
        self.view_app.show()
        self.view_app.BuscarButton.clicked.connect(self.button_clicked)
        self.view_app.toolButton.clicked.connect(self.open_file_dialog)
        self.dato_file = []
        self.headers_file = []        
        


#OPEN FILE
    def open_file_dialog(self):
        dialog = QFileDialog()
        options = dialog.options()
        file_name, _ = dialog.getOpenFileName(None, "Select File", "", "All Files (*);;Excel Files (*.xlsx;*.xls,*.csv)", options=options)
        if file_name.endswith('.xlsx'):
            self.dato_file =pd.read_excel(file_name)
            # Convertir los Timestamps a strings
            self.headers_file = self.dato_file.columns.to_list()
            self.dato_file = self.dato_file.applymap(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x)
            # Convertir el DataFrame a lista de listas
            self.dato_file=self.dato_file.values.tolist()
            print(self.dato_file)

        elif file_name.endswith('.csv'):
            self.dato_file = pd.read_csv(file_name, sep=',|;')
            self.headers_file = self.dato_file.columns.to_list()
            self.dato_file = self.dato_file.values.tolist()
            print(self.dato_file)



        if file_name:
            file_base_name = os.path.basename(file_name)
            self.view_app.toolButton.setText(file_base_name)  # Mostrar la ruta del archivo en el cuadro de texto (TextEdit)
             # Cambiar el tamaño del botón toolButton
            self.view_app.toolButton.setFixedWidth(100)  # Aumenta el ancho del botón
            #resultados,nombres_columnas=self.conexion.consulta_multiple_ani_Fecha(df)
            self.mostrar_export_intable(self.dato_file,self.headers_file)

    def mostrar_export_intable(self,datos,nombre_columnas):
        
        filas=len(datos)
        columnas=len(nombre_columnas)

        self.view_app.tableWidget.setRowCount(filas)
        self.view_app.tableWidget.setColumnCount(columnas)
        self.view_app.tableWidget.setHorizontalHeaderLabels(nombre_columnas)
        for fila in range(filas):
            for columna in range(columnas):
                item = QTableWidgetItem(str(datos[fila][columna]))
                self.view_app.tableWidget.setItem(fila,columna,item)    

#realizar las consultas hechas en la base de datos
    def consultar_by_fecha_todate_tofrom(self):
        todate=self.view_app.StartDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        tofrom=self.view_app.EndDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        datos,nombre_columnas = self.conexion.consulta_tofecha(todate,tofrom)
        self.mostrarTable(datos,nombre_columnas)

    def consultar_by_Ani_todate_tofrom(self):
        todate=self.view_app.StartDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        tofrom=self.view_app.EndDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        ANIS=self.view_app.AnisImput.text()
        datos,nombre_columnas = self.conexion.consulta_tofecha_ANI(todate,tofrom,ANIS)
        self.mostrarTable(datos,nombre_columnas)

    def consultar_by_DNIS_todate_tofrom(self):
        todate=self.view_app.StartDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        tofrom=self.view_app.EndDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        DNIS=self.view_app.DnisImput.text()
        datos,nombre_columnas = self.conexion.consulta_tofecha_DNIS(todate,tofrom,DNIS)
        self.mostrarTable(datos,nombre_columnas)
    
    def consultar_by_ANIS_DNIS_todate_tofrom(self):
        todate=self.view_app.StartDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        tofrom=self.view_app.EndDateTime.dateTime().toString("yyyy-MM-dd hh:mm")
        ANIS=self.view_app.AnisImput.text()
        DNIS=self.view_app.DnisImput.text()
        datos,nombre_columnas = self.conexion.consulta_tofecha_ANIS_DNIS(todate,tofrom,ANIS,DNIS)
        self.mostrarTable(datos,nombre_columnas)
    
    def consultar_multiple_ani_Fecha(self):
        datos,nombre_columnas = self.conexion.consulta_multiple_ani_Fecha(self.dato_file)
        self.mostrarTable(datos,nombre_columnas)
         



#Mostrar las consultas en las tablas
    def mostrarTable(self,datos,nombre_columnas):
        #Limpia la tabla
        self.view_app.tableWidget.clear()
        num_filas = len(datos)
        num_columnas = len(nombre_columnas)
        self.view_app.tableWidget.setRowCount(num_filas)
        self.view_app.tableWidget.setColumnCount(num_columnas)
        # Insertar los nombres de las columnas
        self.view_app.tableWidget.setHorizontalHeaderLabels(nombre_columnas)
        # Insertar los datos
        for i in range(num_filas):
            for j in range(num_columnas):
                self.view_app.tableWidget.setItem(i,j,QTableWidgetItem(str(datos[i][j])))

    





    def button_clicked(self):
        if(self.view_app.toolButton.text()!='...'):
            print("1")
            self.consultar_multiple_ani_Fecha()
            return
        if(self.view_app.StartDateTime.dateTime() < self.view_app.EndDateTime.dateTime()):
            self.consultar_by_fecha_todate_tofrom()
            print("2")
            return
        if(self.view_app.AnisImput.text() != '' and self.view_app.StartDateTime.dateTime() < self.view_app.EndDateTime.dateTime() and self.view_app.DnisImput.text() == ''):
            self.consultar_by_Ani_todate_tofrom()
            print("3")
            return
        if(self.view_app.AnisImput.text() == '' and self.view_app.StartDateTime.dateTime() < self.view_app.EndDateTime.dateTime() and self.view_app.DnisImput.text() != ''):
            self.consultar_by_DNIS_todate_tofrom()
            print("3")
            return
        if(self.view_app.AnisImput.text() != '' and self.view_app.StartDateTime.dateTime() < self.view_app.EndDateTime.dateTime() and self.view_app.DnisImput.text() != ''):
            self.consultar_by_ANIS_DNIS_todate_tofrom()
            print("4")
            return
        
            
        
                        
       