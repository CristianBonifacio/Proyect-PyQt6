import pymysql
import pandas as pd


class Conexion():
#Conectar a la base de datos
    def __init__(self):
        self.conexion = pymysql.connect(host='127.0.0.1',
                           user='root',
                           passwd='password',
                           database='testcentral')


    # Crear un cursor
      
    def consulta_tofecha(self,todate, fromdate):
        self.cursor = self.conexion.cursor()
        # Ejecutar la consulta
        consulta = "SELECT * FROM  call_operations as co inner join call_data_records as cdr WHERE co.cdr_id=cdr.id and call_start_time BETWEEN %s AND %s"
        self.cursor.execute(consulta, (todate, fromdate))
        # Obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        # Guardar los resultados en una lista   
        resultados =self.cursor.fetchall()
        # Cerrar el cursor y la conexión
        self.cursor.close()
        return resultados,nombres_columnas


    def consultar_anexo(self,anexo,todate, fromdate):
        self.cursor = self.conexion.cursor()
        # Ejecutar la consulta
        consulta = "SELECT * FROM  call_operations as co inner join call_data_records as cdr WHERE co.cdr_id=cdr.id and cdr.source=%s and cdr.call_start_time BETWEEN %s AND %s"
        self.cursor.execute(consulta, (anexo, todate, fromdate))
        # Obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        # Guardar los resultados en una lista
        resultados =self.cursor.fetchall()
        # Cerrar el cursor y la conexión
        self.cursor.close()
        return resultados,nombres_columnas
    
    def consultar_destination(self,destination,todate,fromdate):
        self.cursor =self.conexion.cursor()
        #Ejecutar la consulta
        consulta = "SELECT * FROM  call_operations as co inner join call_data_records as cdr WHERE co.cdr_id=cdr.id and cdr.destination=%s and cdr.call_start_time BETWEEN %s AND %s"
        self.cursor.execute(consulta, (destination, todate, fromdate))
        # Obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        # Guardar los resultados en una lista
        resultados =self.cursor.fetchall()
        # Cerrar el cursor
        self.cursor.close()
        return resultados,nombres_columnas
    def consultar_anexo_destination(self,anexo,destination,todate,fromdate):
        self.cursor =self.conexion.cursor()
        #Ejecutar la consulta
        consulta = "SELECT * FROM  call_operations as co inner join call_data_records as cdr WHERE co.cdr_id=cdr.id and cdr.source=%s and cdr.destination=%s  and cdr.call_start_time BETWEEN %s AND %s"
        self.cursor.execute(consulta, (anexo,destination, todate, fromdate))
        # Obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        # Guardar los resultados en una lista
        resultados =self.cursor.fetchall()
        # Cerrar el cursor
        self.cursor.close()
        return resultados,nombres_columnas