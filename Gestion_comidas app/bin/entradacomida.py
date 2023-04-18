import tkinter as tk
from tkinter import ttk
import datetime
from tkcalendar import  DateEntry
# from main import Inicio
class EntradaComida(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        THEME_COLOR = "#BFCCB5"
        TEXT_COLOR = "#7C96AB"
        self.config(padx=20,pady=20,background=THEME_COLOR)
     

        self.controller = controller        

        # Labels
        
        self.label_comida = tk.Label (self, text= "Nombre comida",padx=25,background=THEME_COLOR,fg=TEXT_COLOR )
        self.label_comida.grid(column=0,row=1)
        
        self.label_tipo = tk.Label (self, text= "Tipo comida",padx=25,background=THEME_COLOR,fg=TEXT_COLOR )
        self.label_tipo.grid(column = 0,row = 2,padx = 20)

        self.label_fecha = tk.Label (self, text= "Fecha",padx=25,background=THEME_COLOR,fg=TEXT_COLOR )
        self.label_fecha.grid(column = 0,row=3,padx = 20)

        # inputs
        self.entry_comida = tk.Entry(self)
        self.entry_comida.grid(column = 3, row = 1)

        # Tipo comida
        self.cb_tipo = ttk.Combobox(self)
        self.cb_tipo['values'] = ('carne', 'pescado', 'mahonesa','salsa','otros')
        self.cb_tipo.grid(column = 3, row = 2, padx = 20)


        # date entry
        año_actual = datetime.datetime.today().year
        self.cal = DateEntry(self, width=12, background='darkblue',  foreground='white', borderwidth=2, year=año_actual)
        self.cal.grid(column = 3, row = 3)


        # Botones
        self.button_stock = tk.Button(self,text="Añadir comida", command=self.send_entrada_comida)
        self.button_stock.grid(column = 1,row = 5)

        
        self.status = tk.StringVar() 
        self.label_status = tk.Label (self, textvariable= self.status ,padx=25,background=THEME_COLOR,fg=TEXT_COLOR )
        self.label_status.grid(column=2,row=4)        
        

        # Cambio Frame         
        button_inicio = tk.Button(self, text ="Main", command = lambda : controller.show_frame2("inicio"))
        button_inicio.grid(column=1, row=6, padx=20, pady=20)
        
        button_stock = tk.Button(self, text ="Ver comidas", command = lambda : controller.show_frame2("stock"))
        button_stock.grid(column=2, row=6, padx=20)

    def send_entrada_comida(self):
        
        if (self.isEntryValid(self.entry_comida.get()) is False) or (self.isEntryValid(self.cb_tipo.get()) is False):
            self.visualiza_error()
        
        # entrada = []
        # entrada.append(self.entry_comida.get() )
        # entrada.append(self.cb_tipo.get())
        # entrada.append(str(self.cal.get_date().strftime("%Y%m%d")) )
        # entrada.append(str(self.cal.get_date()) )
        nombre = self.entry_comida.get()
        tipo =   self.cb_tipo.get()
        fecha =  self.cal.get_date()

        self.controller.insertar_entrada( nombre, tipo, fecha)

        self.envio_existoso()
        # print(entrada)
        # print(self.entry_comida.get())
        # print(self.cb_tipo.get())
        # print(self.cal.get_date())
        
    def visualiza_error(self)->None:
        self.status.set("Campos Incompletos")
        self.label_status.config(fg="red")
        return None
    
    def envio_existoso(self):
        self.status.set("Envio exitoso")
        self.label_status.config(fg="green")
        return None
    
    def isEntryValid(self,valor):
        if valor == "":
            return False
        return True
    
if __name__ == "__main__":

    qi = EntradaComida()
