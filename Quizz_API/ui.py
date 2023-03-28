import tkinter as tk
from main_quizz2 import QuizzShow



class QuizzInterface():
    def __init__(self,quizz_show: QuizzShow):

        THEME_COLOR = "#375362"

        self.window = tk.Tk()
        self.window.title("Concurso")
        self.window.config(padx=20,pady=20,background=THEME_COLOR)


        #quizz_show
        self.quizz_show = quizz_show

        # Scores
        # self.var = tk.StringVar()
        self.score_value=0
        self.label_score = tk.Label ( text= f"Score: {self.score_value}",padx=25,background=THEME_COLOR,fg='white' )
        self.label_score.grid(column=1,row=1)
        
        # preguntas
        self.canvas = tk.Canvas(width= 300,height= 300, bg="white")
        self.question_canvas = self.canvas.create_text(150,150, width= 200,text='Preguntas',fill=THEME_COLOR, font=('Arial',10))

        self.canvas.grid(column=0,row=2,columnspan=2,pady=20)

        # Botones
        img_false = tk.PhotoImage(file = r"04_quizz\images\false.png")
        img_true = tk.PhotoImage(file = r"04_quizz\images\true.png")
        self.button_true = tk.Button(image =img_true,padx=25,command=self.press_boton_true )
        self.button_false = tk.Button(image =img_false,padx=25,command=self.press_boton_false )
        self.button_true.grid(column=0,row=3)
        self.button_false.grid(column=1,row=3)
        

        self.cambiar_pregunta()

        self.window.mainloop()
       



    def cambiar_pregunta(self):
            
            self.canvas.config( bg="white")

            self.score_value = self.quizz_show.mostrar_resultado()
            print(f"Score value actual: {self.score_value}")
            self.label_score.config(text=f"Score: {self.score_value}")

            pregunta = self.quizz_show.mostrar_pregunta()
            self.canvas.itemconfig(self.question_canvas, text=pregunta)

    def press_boton(self,respuesta):
         
         acierto = self.quizz_show.revisar_respuesta(respuesta)
         self.cambiar_color_canvas(acierto)

    def press_boton_true(self):
         self.press_boton(respuesta=True)

    def press_boton_false(self):
         self.press_boton(respuesta=False)



    def cambiar_color_canvas(self,acierto):
         if acierto:
            self.canvas.config( bg="green")
         else:
            self.canvas.config( bg="red")
         self.window.after(500,self.cambiar_pregunta)
         
if __name__ == "__main__":

    qi = QuizzInterface()
