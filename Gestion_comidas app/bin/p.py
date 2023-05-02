

import tkinter as tk
from tkinter import ttk

# falta escribir la funcion que envia el registro a la base de datos
# ponerlo todo en entradacomida.py

class NewEntradaComida(tk.Toplevel):
    def __init__(self,  controller):
        tk.Toplevel.__init__(self)

        THEME_COLOR = "#BFCCB5"
        TEXT_COLOR = "#7C96AB"
        self.config(padx=20,pady=20)
        self.controller = controller            
        
     
        # label titulo
        label_titulo = tk.Label( text="Introducir tipo",font=32, pady=20)
        label_titulo.grid(column=0,row=0,columnspan=2)

        # Labels
        label_tipo = tk.Label(text="tipo comida:    ")
        label_naranja = tk.Label(text="dias para naranja:   ")
        label_rojo = tk.Label(text="dias para rojo: ")

        label_tipo.grid(column=0,row=1)
        label_naranja.grid(column=0,row=2)
        label_rojo.grid(column=0,row=3)
        

        # Entrys
        self.entrys_tipo = tk.Entry(text="tipo comida:    ")
        self.entrys_naranja = tk.Entry(text="dias para naranja:   ")
        self.entrys_rojo = tk.Entry(text="dias para rojo: ")

        self.entrys_tipo.grid(column=1,row=1)
        self.entrys_naranja.grid(column=1,row=2)
        self.entrys_rojo.grid(column=1,row=3)

        #botones
        bt_tipo = tk.Button(text="añadir tipo",command= self.introducir_entrada_tipo)
        bt_tipo.grid(column=0,columnspan=2,row=4)


        self.status = tk.StringVar() 
        self.label_status = tk.Label ( textvariable= self.status ,padx=25 )
        self.label_status.grid(column=0,row=5)  

    def introducir_entrada_tipo(self):
         
         if not self.campos_validos():
            return False
         
         #### enviar registros
         self.reset_entrys()
         self.visualiza_exito()

    def reset_entrys(self):
        self.entrys_tipo.delete(0, 100)
        self.entrys_naranja.delete(0, 100)
        self.entrys_rojo.delete(0, 100)
        return None
    

    def campos_validos(self):
         if not self.isValidTipo():
              
              self.visualiza_error("Tipo no es correcto")
              return False
        
         if not self.isValidNaranja():
              
              self.visualiza_error("Naranja no es correcto")
              return False

         if not self.isValidRojo():
              
              self.visualiza_error("Rojo no es correcto")
              return False
         
         return True



    def visualiza_error(self, valor)->None:
        print(f"visualiza error")
        self.status.set(f"campo {valor}")
        self.label_status.config(fg="red")
        return None
    
    def isValidTipo(self):
         
         nombre_tipo = self.entrys_tipo.get()
        #  print(f"{nombre_tipo} texto")
         if  nombre_tipo.isnumeric() or nombre_tipo =="": 
             return False


        #  print(f"aaa :{type(nombre_tipo)}")
         return isinstance(nombre_tipo,str)

  
    
    def isValidNaranja(self):
         nombre_naranja = self.entrys_naranja.get()
         if   nombre_naranja =="": 
             return False
         
         return nombre_naranja.isnumeric() 
    
    def isValidRojo(self):
         nombre_rojo = self.entrys_rojo.get()
         if   nombre_rojo =="": 
             return False
         
         return nombre_rojo.isnumeric() 
    
    def isValidRed(self):
         nombre_rojo = self.entrys_rojo.get()
         return isinstance(nombre_rojo,int)    

    def visualiza_exito(self)->None:
        self.status.set("Registro añadido")
        self.label_status.config(fg="green")
        return None


if __name__ == "__main__":

    qi = tk.Tk()

    new = NewEntradaComida(qi)
    # print(new.isInteger(3))
    qi.mainloop()
