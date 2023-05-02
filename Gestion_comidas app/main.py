import tkinter as tk



from bin.entradacomida import EntradaComida
from bin.stock import Vista
from bin.conexion_bbdd import ConexionBBDD
from bin.historico import HistoricoFrame




class SobrasApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        self.conexion_bbdd = ConexionBBDD()

        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Inicio, EntradaComida,Vista, HistoricoFrame):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Inicio)
        # self.mainloop()

    def show_frame2(self,nombre):
        if nombre == "inicio":
           self.show_frame( Inicio) 
        
        elif nombre == "entradacomida":
            self.show_frame(EntradaComida)
        
        elif nombre == "stock":
            self.actualizar_entrada(Vista)
            self.show_frame(Vista)
        
        elif nombre == "historico":
            self.actualizar_entrada(HistoricoFrame)
            self.show_frame(HistoricoFrame)

    def actualizar_entrada(self,cont):
            self.frames[cont].actualizar_tree()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
    def select_tabla_tipos(self)-> list:
        return  self.conexion_bbdd.select_tabla_tipos() 

    def select_tabla_entrada(self):
        return self.conexion_bbdd.select_entrada() 

    def select_tabla_historica(self):
        return self.conexion_bbdd.select_historico() 

    def insertar_entrada(self, nombre, tipo, fecha):
        self.conexion_bbdd.insertar_entrada(nombre, tipo, fecha)
        return None

    def borrar_entrada_por_indice(self,registro):
        self.conexion_bbdd.borrar_entrada_por_indice(registro)
        return None

class Inicio (tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        
        #colores
        THEME_COLOR = "#BFCCB5"
        TEXT_COLOR = "#7C96AB"
        

        controller.title("Gestion Comidas")

        self.config(padx=20,pady=20,background=THEME_COLOR)

        self.label_titulo = tk.Label (self, text= "Gestion sobras",padx=25,background=THEME_COLOR,fg=TEXT_COLOR )
        self.label_titulo.grid(column=0,row=1)


        button_inicio = tk.Button(self, text ="Entrada comida", command = lambda : controller.show_frame2("entradacomida"))
        button_inicio.grid(column=0, row=2, pady=20)

        button_stock = tk.Button(self, text ="Ver comidas", command = lambda : controller.show_frame2("stock"))
        button_stock.grid(column=1, row=2, pady=20)

        button_historico = tk.Button(self, text ="Historico", command = lambda : controller.show_frame2("historico"))
        button_historico.grid(column=1, row=3, pady=20)
   


if __name__ == "__main__":

    qi = SobrasApp()
    qi.mainloop()