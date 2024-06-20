import pyodbc



class conexion:
    def __init__(self):
        self.conexion = pyodbc.connect(
            'DRIVER=SQL Server;'
            'SERVER=DESKTOP-8U4V5CH\SQLEXPRESS;'
            'DATABASE=testCentral;'
            'UID=admin;'
            'PWD=password'
        )


    def consulta_tofecha(self,startDate, endDate):
        self.cursor = self.conexion.cursor()
        # Ejecutar la consulta
        consulta = "SELECT TOP 1000 * FROM  testCentral.dbo.cdr as cdr inner join  testCentral.dbo.inums as inums on  cdr.sid_key=inums.sid_key where ( cdr.local_start_time between ? and ?)"
        self.cursor.execute(consulta, (startDate, endDate)) 
        # Obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        # Guardar los resultados en una lista   
        resultados =self.cursor.fetchall()
        # Cerrar el cursor y la conexión
        self.cursor.close()
        return resultados,nombres_columnas
    
    def consulta_tofecha_ANI(self,startDate,endDate,ANI):
        self.cursor = self.conexion.cursor()
        # Ejecutar la consulta
        consulta="SELECT TOP 1000 * FROM  testCentral.dbo.cdr as cdr inner join  testCentral.dbo.inums as inums on  cdr.sid_key=inums.sid_key where ( (cdr.local_start_time between ? and ? ) and (cdr.ANI = ? or cdr.DNIS=?))"
        self.cursor.execute(consulta, (startDate,endDate,ANI,ANI))
        #obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        resultados =self.cursor.fetchall()
        resultados = [tuple(row) for row in resultados]
        print(resultados)
        print(nombres_columnas)
        # Cerrar el cursor y la conexion
        self.cursor.close()
        return resultados,nombres_columnas
    
    def consulta_tofecha_DNIS(self,startDate,endDate,DNIS):
        self.cursor = self.conexion.cursor()
        # Ejecutar la consulta
        consulta="SELECT TOP 1000 * FROM  testCentral.dbo.cdr as cdr inner join  testCentral.dbo.inums as inums on  cdr.sid_key=inums.sid_key where ( cdr.local_start_time between ? and ? and (cdr.ANI = ? or cdr.DNIS=?))"
        self.cursor.execute(consulta, (startDate,endDate,DNIS,DNIS))
        #obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        resultados =self.cursor.fetchall()
        # Cerrar el cursor y la conexion
        self.cursor.close()
        return resultados,nombres_columnas
    
    def consulta_tofecha_ANIS_DNIS(self,startDate,endDate,ANIS,DNIS):
        self.cursor = self.conexion.cursor()
        # Ejecutar la consulta
        consulta="SELECT TOP 1000 * FROM  testCentral.dbo.cdr as cdr inner join  testCentral.dbo.inums as inums on  cdr.sid_key=inums.sid_key where ( cdr.local_start_time between ? and ? and (cdr.ANI = ? and cdr.DNIS=?))"
        self.cursor.execute(consulta, (startDate,endDate,ANIS,DNIS))
        #obtener los nombres de las columnas
        nombres_columnas = [i[0] for i in self.cursor.description]
        resultados =self.cursor.fetchall()
        
        # Cerrar el cursor y la conexion
        self.cursor.close()
        return resultados,nombres_columnas
    


    def consulta_multiple_ani_Fecha(self,datos):
        # Construir la consulta dinámica
        self.cursor = self.conexion.cursor()
        # Lista para almacenar partes de la condición WHERE
        numeros = []
        dates    = []
        # Construcción de la condición WHERE dinámica
        for  dato in datos:
            numero,date=dato
            numeros.append(numero)
            dates.append(date)

        query="""
        SELECT TOP 1000 *FROM testCentral.dbo.cdr as cdr INNER JOIN testCentral.dbo.inums as inums ON cdr.sid_key = inums.sid_key
        WHERE("""
        condiciones = []
        for numero, fecha in zip(numeros, dates):
            condicion = f"""
            (
            (cdr.ANI = '{numero}' OR cdr.DNIS = '{numero}') 
            AND CONVERT(DATE, cdr.local_start_time) = '{fecha}'
            )
            """
            condiciones.append(condicion)
    
    # Unir todas las condiciones con "OR"
        query += " OR ".join(condiciones)
        query=query + ")"
        self.cursor.execute(query)
        resultados =self.cursor.fetchall()
        nombres_columnas = [i[0] for i in self.cursor.description]
        self.cursor.close()

        return resultados,nombres_columnas
    
    

        

# Ejemplo de uso
#conect = conexion()
#datos = [[3864906, '2024-06-12'], [65473, '2024-06-12']]
#result=conect.consulta_multiple_ani_Fecha(datos)
#print(result)
#print(nombres_columnas)
#conect.consulta_tofecha_ANI('2024-06-12 00:00','2024-06-12 23:59','993024134')
#print(conect.consulta_tofecha_ANI('2024-06-12 00:00','2024-06-12 23:59','993024134')

#conect.consulta_tofecha_ANI('2024-06-12 00:00','2024-06-12 23:59','993024134')

    


        