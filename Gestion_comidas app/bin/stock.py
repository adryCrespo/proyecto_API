import tkinter as tk
from tkinter import ttk
import datetime
import pandas as pd

import logging
logging.basicConfig(filename='example.text')

LARGEFONT =("Verdana", 15)



class Vista(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        

        THEME_COLOR = "#BFCCB5"
        self.config(padx=20,pady=20,background=THEME_COLOR)
        
        # Titulo
        label_titulo = tk.Label(self, text ="Lista elementos", font = LARGEFONT, anchor="center", background=THEME_COLOR)
        label_titulo.grid(column=0,row=0,columnspan=4)

        # Filtros
        self.var_aviso = tk.IntVar()
        self.var_caducado = tk.IntVar()
        self.var_normal = tk.IntVar()
        self.cb_aviso = tk.Checkbutton(self, text='Aviso',variable= self.var_aviso, onvalue=1, offvalue=0, background=THEME_COLOR)
        self.cb_caducado = tk.Checkbutton(self, text='Caducado',variable= self.var_caducado, onvalue=1, offvalue=0, background=THEME_COLOR)
        self.cb_normal = tk.Checkbutton(self, text='normal',variable= self.var_normal, onvalue=1, offvalue=0, background=THEME_COLOR)
        
        self.var_aviso.set(1)
        self.var_caducado.set(1)
        self.var_normal.set(1)

  

        self.cb_aviso.grid(column = 0, row = 1)
        self.cb_caducado.grid(column = 1, row = 1)
        self.cb_normal.grid(column = 2, row = 1)

        # Botones
        self.b_actualizacion_query = tk.Button(self,text='actualizar', command=self.actualizar_tree)
        self.b_actualizacion_query.grid(column = 3, row = 1, padx = 10)

        self.b_borrar = tk.Button(self,text='borrar', command=self.borrar_registro_seleccionado)
        self.b_borrar.grid(column = 4, row = 1, padx = 10)

        self.b_info = tk.Button(self,text='info', command=self.info_tipos)
        self.b_info.grid(column = 5, row = 1, padx = 10)

        # Visualizador de registros: Treeview

        self.tree = ttk.Treeview(self, column=("Nombre", "Tipo", "Fecha"), show='headings', height=5)
        self.tree.grid(row=3, column=0, sticky='nsew', columnspan=3,rowspan=10, pady=20)

        scrollbar = tk.Scrollbar(self,orient="vertical")
        scrollbar.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=4 )


        def fixed_map(option):      
            # Returns the style map for 'option' with any styles starting with
            # ("!disabled", "!selected", ...) filtered out

            # style.map() returns an empty list for missing o  ptions, so this should
            # be future-safe
            return [elm for elm in style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

        style = ttk.Style()
        style.map("Treeview", 
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))

 
        self.tree.column("# 1", anchor='center')
        self.tree.heading("# 1", text="Nombre")
        self.tree.column("# 2", anchor='center')
        self.tree.heading("# 2", text="Tipo")
        self.tree.column("# 3", anchor='center')
        self.tree.heading("# 3", text="Fecha")

        self.tree.tag_configure('aviso',background='yellow',foreground="red")
        self.tree.tag_configure('caducado',background='red',foreground="white")
        self.tree.tag_configure('normal',background="white",foreground="black")

        # Insert the data in Treeview widget
        self.conseguir_registros_entradas()


        # Cambio Frame         
        button_inicio = tk.Button(self, text ="Main",  command = lambda : controller.show_frame2("inicio"))
        button_inicio.grid(column=0, row=20)

        button_entradas = tk.Button(self, text ="Entradas Comida",  command = lambda : controller.show_frame2("entradacomida"))
        button_entradas.grid(column=1, row=20)

        button_historico = tk.Button(self, text ="Historico", command = lambda : controller.show_frame2("historico"))
        button_historico.grid(column=2, row=20, pady=20)
    
    def insertar_entradas_treeview(self, nombre, tipo, fecha_entrada,tag)-> None:
        
        self.tree.insert('', 'end', text="1", values=(nombre,tipo, fecha_entrada.strftime('%d-%m-%Y')),tags=(tag,))

        return None
    

    def conseguir_registros_entradas(self):
        # df_registros = self.controller.select_tabla_tipos()
        # df_tipos = pd.DataFrame(self.controller.select_tabla_tipos() )


        # df = df_registros.merge(df_tipos, on="tipo",how="inner")




        tranformaciones = Transformaciones(self.controller, self.obtener_check_aviso(),self.obtener_check_caduco(),self.obtener_check_normal() )
        registros = tranformaciones.obtener_df_filtrado()

        for  _, registro in registros.iterrows():

            self.insertar_entradas_treeview(registro.nombre, registro.tipo, registro.fecha_entrada,tag=registro.tag)
        
        return None





    def borrar_treeview_registros(self):
        registros = self.tree.get_children()
        for registro in registros:
            self.tree.delete(registro)
        return None
    
    def borrar_registro_seleccionado(self)-> None:
        """Seleccionar un registro y lo borra"""
        selected_item = self.tree.selection()[0]
        
        item_valores = self.tree.item(selected_item,option="values")
        
        self.controller.borrar_entrada_por_indice(item_valores)
        self.tree.delete(selected_item)
        
        return None
    
    def actualizar_tree(self):
        self.borrar_treeview_registros()
        self.conseguir_registros_entradas()
        return None
    
    def info_tipos(self):
        new_window = tk.Toplevel(self.controller)
        tipos = Tabla_Tipos(self.controller)
        df_tipos = tipos.obtener_daframe()
        indice = 2
        self.e = tk.Entry(new_window, width=20, font=('Arial',16,'bold'))
        self.e.grid(row = 0, column = 0)
        self.e.insert(indice, "TIPO COMIDA")

        self.e = tk.Entry(new_window, width=20, font=('Arial',16,'bold'))
        self.e.grid(row = 0, column = 1)
        self.e.insert(indice, 'DIAS AMARILLO')

        self.e = tk.Entry(new_window, width=20, font=('Arial',16,'bold'))
        self.e.grid(row = 0, column = 2)
        self.e.insert(indice, 'DIAS ROJO')

        for numero_fila, registro in df_tipos.iterrows():
            for numero_columna,dato in enumerate(registro):
                 
                self.e = tk.Entry(new_window, width=20, font=('Arial',16,'bold'))
                 
                self.e.grid(row = numero_fila+1, column = numero_columna)
                self.e.insert(indice, dato)
        self.e = tk.Entry(new_window, width=20, font=('Arial',16,'bold'))

    def obtener_check_aviso(self):
            return    self.var_aviso.get() 
    
    def obtener_check_caduco(self):
            return    self.var_caducado.get()

    def obtener_check_normal(self):
            return    self.var_normal.get()             
    
class Tabla_Tipos:
     def __init__(self, controller) -> None:
        self.controller = controller
        self.df_tipo = self.obtener_tipo()

     def obtener_tipo(self):
        return pd.DataFrame(self.controller.select_tabla_tipos() ) 

     def obtener_dimensiones(self):
         return self.df_tipo.shape
     
     def obtener_daframe(self):
         return self.df_tipo 
     
class Transformaciones:
    def __init__(self, controller, EsAviso,EsCaducado, EsNormal ) -> None:
        self.controller = controller
        self.df_final = None
        self.EsAviso = EsAviso
        self.EsCaducado = EsCaducado
        self.EsNormal = EsNormal

    def obtener_entrada(self):
        return pd.DataFrame(self.controller.select_tabla_entrada() )

    def obtener_tip(self):
        return pd.DataFrame(self.controller.select_tabla_tipos() ) 

    def encontrar_color(self,registro):
        if registro.n_naranja>0: 
            return "normal"
        
        if registro.n_rojo <= 0 :
            return "caducado"
        
        return "aviso"



    def transformaciones(self):

        entradas = self.obtener_entrada()
        tipos = self.obtener_tip()

        df = entradas.merge(tipos, how="inner", on="tipo")

        df['f_naranja'] = df.apply(lambda x:  x.fecha_entrada + pd.Timedelta(x.naranja, unit="d"),axis=1).dt.date
        df['f_rojo'] = df.apply(lambda x:  x.fecha_entrada + pd.Timedelta(x.rojo, unit="d"),axis=1).dt.date


        df['hoy'] = datetime.datetime.now().date()
        df['n_rojo'] = df.apply(lambda x: x.f_rojo-x.hoy ,axis=1).dt.days
        df['n_naranja'] = df.apply(lambda x: x.f_naranja-x.hoy ,axis=1).dt.days

        df['tag'] = df.apply(lambda x: self.encontrar_color(x), axis=1)
        return df[['nombre'	,'tipo',	'fecha_entrada','tag']]

    def obtener_df_filtrado(self):
        df = self.transformaciones()
        
        c_caducado = df['tag'] == "caducado"
        c_aviso = df['tag'] == "aviso"
        c_normal = df['tag'] == "normal"
        c_falso = df['tag'] == "n"

        c = self.condicion_filtrado(c_caducado,c_aviso,c_normal,c_falso)
        return df.loc[c]
        
    def condicion_filtrado(self,c_caducado,c_aviso,c_normal,c_falso):


        if self.EsAviso!=1:
            c_aviso = c_falso
        
        if self.EsCaducado !=1:
            c_caducado = c_falso

        if self.EsNormal !=1:
            c_normal = c_falso


        c = (c_aviso|c_caducado|c_normal)
        
       
        return  c