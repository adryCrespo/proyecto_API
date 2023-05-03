
import sqlalchemy as db
import os, sys
import datetime

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class ConexionBBDD:
    def __init__(self) -> None:
        
        self.engine = db.create_engine('sqlite:///Sobras.db')
        # self.engine = db.create_engine(resource_path('Sobras.db'))
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

        self.entrada_comida = db.Table('Entradas', self.metadata,
              db.Column('id', db.Integer(),primary_key=True),
              db.Column('nombre', db.String(255), nullable=False),
              db.Column('tipo', db.String(255), nullable=False),
              db.Column('fecha_entrada', db.DateTime() , default=True)
              )


        self.historico = db.Table('Historico', self.metadata,
              
              db.Column('nombre', db.String(255), nullable=False),
              db.Column('tipo', db.String(255), nullable=False),
              db.Column('fecha_entrada', db.DateTime() , default=True)
              )

        self.tabla_tipos = db.Table('Tipos', self.metadata,
              db.Column('tipo', db.String(50),primary_key=True),
              db.Column('naranja', db.Integer(), nullable=False),
              db.Column('rojo', db.Integer(), nullable=False) )

        self.metadata.create_all(self.engine) #Creates the table    


    def select_all_rows(self, tabla_metadatos)-> list:
        # SELECT ALL
        query = db.select(tabla_metadatos)
        result_Proxy = self.connection.execute(query)
        result = result_Proxy.fetchall()
        return result
    
    def select_tabla_tipos(self):
        """ muestra todos los datos de tabla tipos"""
        
        return self.select_all_rows(self.tabla_tipos)
    
    def select_entrada(self):
        """ muestra todos los datos de tabla tipos"""
        
        return self.select_all_rows(self.entrada_comida)
    

    def select_historico(self):
        """ muestra todos los datos de tabla tipos"""
        
        return self.select_all_rows(self.historico)


    def insertar_entrada(self, nombre, tipo, fecha):
        """
        inputs: 
            nombre: str
            tipo: str
            datetime: datetime.datetime(2020,5,18)
            """
        if isinstance(fecha, str):
            fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        query = db.insert(self.entrada_comida).values( nombre = nombre, tipo = tipo, fecha_entrada = fecha  ) 
        ResultProxy = self.connection.execute(query)


        query = db.insert(self.historico).values( nombre = nombre, tipo = tipo, fecha_entrada = fecha  ) 
        ResultProxy = self.connection.execute(query)

        return None
    
    def insertar_tipos(self, tipo, naranja, rojo):
        """
        inputs: 
            tipo: str
            naranjo: inter
            rojo: integer
            """
        query = db.insert(self.tabla_tipos).values( tipo = tipo, naranja = naranja, rojo = rojo) 
        ResultProxy = self.connection.execute(query)
        return None

    
    def borrar_entrada_por_indice(self,registro):
        """
        Inputs:
          index: integer"""
        query = db.delete(self.entrada_comida)

        nombre = registro[0]
        tipo = registro[1]
        fecha_entrada = registro[2]
        if isinstance(fecha_entrada, str):
            fecha_entrada = datetime.datetime.strptime(fecha_entrada, '%d-%m-%Y')
        

        query = query.where(self.entrada_comida.columns.nombre == nombre)\
                    .where(self.entrada_comida.columns.tipo == tipo)\
                    .where(self.entrada_comida.columns.fecha_entrada == fecha_entrada)  

        self.connection.execute(query)
        
        return None
    
    def borrar_tipo(self,tipo):
        """
        Inputs:
          index: integer"""
        query = db.delete(self.tabla_tipos)
        query = query.where(self.tabla_tipos.columns.tipo == tipo)
                    
        self.connection.execute(query)
        return None    

    def ver_todas_tablas(self):
       
        x = db.inspect(self.connection).get_table_names()
        print(x)
        return None

if __name__ == "__main__":

    c = ConexionBBDD()
    # print(c.select_tabla_tipos())
    # print(c.select_entrada())
    print(c.ver_todas_tablas())

    # lista=[]
    # lista.append(['carne',3,4])
    # lista.append(['pescado',3,4])
    # lista.append(['mahonesa',3,4])
    # lista.append(["otros",3,5])
    # lista.append(["salsa",8,10])

    # for entrada in lista:
    #     c.insertar_tipos( tipo = entrada[0], naranja = entrada[1], rojo = entrada[2]) 
    import datetime
    c.insertar_entrada(  nombre="filete", tipo="carne", fecha=datetime.datetime(2020,5,18)) 
    print(c.select_tabla_tipos())    
    print(c.select_entrada())