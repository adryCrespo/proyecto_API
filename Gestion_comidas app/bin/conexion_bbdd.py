
import sqlalchemy as db
import os, sys
import datetime
import sqlite3 

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)




class BaseDatos_comidas:
    def __init__(self,nombre="gestion_comidas.db"):
    
        self.nombre_ddbb = nombre
        self.create_table_entrada()
        self.create_table_historico()
        self.create_table_tipos()
    
    def create_table_entrada(self):
        query = """ 
        CREATE TABLE IF NOT EXISTS entradas (
            id INTEGER PRIMARY KEY,
            nombre TEXT NULL,
            tipo  TEXT NULL,
            fecha_entrada TEXT NULL);
        """
        self.query_alter_table(query)


    def create_table_historico(self):
        query = """ 
        CREATE TABLE IF NOT EXISTS historico (
            nombre TEXT NULL,
            tipo  TEXT NULL,
            fecha_entrada TEXT NULL);
        """
        self.query_alter_table(query)


    def create_table_tipos(self):
        query = """ 
        CREATE TABLE IF NOT EXISTS tipos (
            tipo TEXT NULL,
            naranja  INTEGER NULL,
            rojo INTEGER NULL);
        """
        self.query_alter_table(query)



    def query_get_data(self,query:str):
        "obtener datos haciendo una query"
        conn = sqlite3.connect(self.nombre_ddbb)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results



    def query_alter_table(self,query:str):
        "modificar base de datos"
        conn = sqlite3.connect(self.nombre_ddbb)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        return None



class Comidas_acciones:

    def __init__(self):
        self.base_datos = BaseDatos_comidas()
        
        # tipos por defecto
        self.insertar_tipos('pescado',3,4)
        self.insertar_tipos('carne',3,4)
        self.insertar_tipos('mahonesa',3,4)
        self.insertar_tipos('otros',3,5)
        self.insertar_tipos('salsa',8,10)

    def select_tabla_tipos(self):
        """ muestra todos los datos de tabla tipos"""
        query = """SELECT * FROM tipos """
        return self.base_datos.query_get_data(query)
    
    def select_entrada(self):
        """ muestra todos los datos de tabla tipos"""
        
        query = """SELECT * FROM entradas """
        return self.base_datos.query_get_data(query)
    

    def select_historico(self):
        """ muestra todos los datos de tabla tipos"""
        
        query = """SELECT * FROM historico """
        return self.base_datos.query_get_data(query)


    # insertar registros tabla entrada
    def insertar_entrada(self, nombre, tipo, fecha):
        """
        inputs: 
            nombre: str
            tipo: str
            datetime: datetime.datetime(2020,5,18)
            """
        # if isinstance(fecha, str):
        #     fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')

        assert type(nombre) == str 
        assert type(tipo) == str

        try:
            assert type(fecha) == str
        except AssertionError:
            print(f"data type fecha: {fecha}")

        # si ya existe no insertar
        numero_filas_nombre = self.base_datos.query_get_data(f"select count(distinct nombre) from entradas where nombre =='{nombre}'")
        if numero_filas_nombre[0][0] >0:
            return None

        query_insert = f"""INSERT INTO entradas (nombre,tipo,fecha_entrada )
            VALUES( '{nombre}',	'{tipo}' ,'{fecha}') """

        self.base_datos.query_alter_table(query_insert)

        query_insert = f"""INSERT INTO historico (nombre,tipo,fecha_entrada)
            VALUES( '{nombre}',	'{tipo}' ,'{fecha}')"""

        self.base_datos.query_alter_table(query_insert)        

        return None
    
    def insertar_tipos(self, tipo, naranja, rojo):
        """
        inputs: 
            tipo: str
            naranjo: inter
            rojo: integer
            """
        
        assert type(tipo) == str 
        assert type(naranja) == int
        assert type(rojo) == int


        # si ya existe no insertar
        numero_filas_tipo = self.base_datos.query_get_data(f"select count(distinct tipo) from tipos where tipo =='{tipo}'")
        
        if numero_filas_tipo[0][0] >0:
            return None
        
        query_insert = f"""INSERT INTO tipos (tipo,naranja ,rojo)
            VALUES( '{tipo}',	{naranja} ,{rojo})"""
        
        self.base_datos.query_alter_table(query_insert)
        return None

    
    def borrar_entrada_por_indice(self,registro):
        """
        Inputs:
          index: integer"""
        # query = db.delete(self.entrada_comida)

        nombre = registro[0]
        tipo = registro[1]
        fecha = registro[2]
        # if isinstance(fecha_entrada, str):
        #     fecha_entrada = datetime.datetime.strptime(fecha_entrada, '%d-%m-%Y')
        
        query_delete = f"""delete from entradas where nombre == '{nombre}' and tipo =='{tipo}' and fecha_entrada = '{fecha}'  """
        self.base_datos.query_alter_table(query_delete)

        return None
    
    def borrar_tipo(self,tipo):
        """
        Inputs:
          index: integer"""
        
        assert type(tipo) == str

        query_delete = f"""delete from tipos WHERE tipo =='{tipo}'"""
        self.base_datos.query_alter_table(query_delete)

        return None    

    # def ver_todas_tablas(self):
       
    #     x = db.inspect(self.connection).get_table_names()
    #     print(x)
    #     return None




if __name__ == "__main__":
    # c= BaseDatos_comidas()


    # nombre = 'filete'
    # tipo = 'carne'
    # fecha = '2020-05-18'
    # query = f"""select * from entradas where nombre == '{nombre}' and tipo =='{tipo}' and fecha_entrada = '{fecha}' """
    # resultados = c.query_get_data(query)
    # print(resultados)
    
    # c.query_alter_table(f"delete from entradas where nombre == '{nombre}' and tipo =='{tipo}' and fecha_entrada = '{fecha}'  " )

    # query = f"""select * from entradas """
    # resultados = c.query_get_data(query)
    # print(resultados)


    ##############################################

    # ca = Comidas_acciones()
    # # ca.borrar_tipo('carne')
    # results =     ca.select_tabla_tipos()
    # print(results)
    ######################################
    import pandas as pd
    ca = Comidas_acciones()
    # entradas_list = ca.select_entrada()
    entradas =  pd.DataFrame(ca.select_entrada(),columns=['id','nombre','tipo','fecha_entrada'] )
    entradas['fecha_entrada'] = pd.to_datetime(entradas['fecha_entrada'])
    
    # tipos = ca.select_tabla_tipos()
    #     if entradas.shape[0]==0:
    #        return pd.DataFrame(columns=['nombre'	,'tipo',	'fecha_entrada','tag'])
    #     df = entradas.merge(tipos, how="inner", on="tipo")

    #     df['f_naranja'] = df.apply(lambda x:  x["fecha_entrada"] + pd.Timedelta(x["naranja"], unit="d"),axis=1)
    #     # df['f_naranja'] =  df["fecha_entrada"] + pd.Timedelta(df["naranja"])
    #     df['f_rojo'] = df.apply(lambda x:  x.fecha_entrada + pd.Timedelta(x["rojo"], unit="d"),axis=1)


    #     df['hoy'] = datetime.datetime.now().date()
    #     df['n_rojo'] = df.apply(lambda x: x.f_rojo-x.hoy ,axis=1).dt.days
    #     df['n_naranja'] = df.apply(lambda x: x.f_naranja-x.hoy ,axis=1).dt.days

    #     df['tag'] = df.apply(lambda x: self.encontrar_color(x), axis=1)
    #     return df[['nombre'	,'tipo',	'fecha_entrada','tag']]


    # ca.insertar_entrada(  nombre="filete", tipo="carne", fecha="2020-05-18") 
    # ca.insertar_entrada(  nombre="filete", tipo="carne", fecha="2020-05-18") 
    # results =     ca.select_entrada()
    # print(results)
    # ca.borrar_entrada_por_indice( ("filete", "carne", "2020-05-18") )
    # results =     ca.select_entrada()
    # print(results)

    ##########################################################


    