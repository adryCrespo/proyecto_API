
import tkinter as tk
from tkinter import ttk
import datetime
import pandas as pd

import logging
logging.basicConfig(filename='example.text')

LARGEFONT =("Verdana", 15)



class HistoricoFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        
        THEME_COLOR = "#BFCCB5"
        self.config(padx=20,pady=20,background=THEME_COLOR)

        label_titulo = tk.Label(self, text ="Histórico comidas", font = LARGEFONT, anchor="center", background=THEME_COLOR)
        label_titulo.grid(column=0,row=0,columnspan=4)

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

        # self.tree.tag_configure('aviso',background='yellow',foreground="red")
        # self.tree.tag_configure('caducado',background='red',foreground="white")
        # self.tree.tag_configure('normal',background="white",foreground="black")


        # Cambio Frame         
        button_inicio = tk.Button(self, text ="Main",  command = lambda : controller.show_frame2("inicio"))
        button_inicio.grid(column=0, row=20)

        button_entradas = tk.Button(self, text ="Entradas Comida",  command = lambda : controller.show_frame2("entradacomida"))
        button_entradas.grid(column=1, row=20)

        button_stock = tk.Button(self, text ="Ver comidas", command = lambda : controller.show_frame2("stock"))
        button_stock.grid(column=2, row=20, pady=20)


        # Insert the data in Treeview widget
        self.insert_todas_entradas_treeview()


    
    def insertar_entradas_treeview(self, nombre, tipo, fecha_entrada)-> None:
        
        self.tree.insert('', 'end', text="1", values=(nombre,tipo, fecha_entrada.strftime('%d-%m-%Y')))

        return None
    
    
    def insert_todas_entradas_treeview(self):
        registros = self.controller.select_tabla_historica()

        for registro in registros:
            self.insertar_entradas_treeview(nombre = registro[0], tipo = registro[1], fecha_entrada=registro[2])
        
        return None
    
    def borrar_treeview_registros(self):
        registros = self.tree.get_children()
        for registro in registros:
            self.tree.delete(registro)
        return None
    
    def actualizar_tree(self):
        self.borrar_treeview_registros()
        self.insert_todas_entradas_treeview()
        return None