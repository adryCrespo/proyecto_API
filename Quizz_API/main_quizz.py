import requests
import html



class score():
    def __init__(self) -> None:
        self.score = 0
    
    def raise_score(self):
        self.score +=1
    
    def get_score(self):
        return score
    
    def print(self):
        print(f"Your game score is {self.score}")

    def reset_score(self):
        self.score = 0

class preguntas_API():
    def __init__(self,numero_preguntas=10) -> None:

        self.preguntas = self.get_preguntas(numero_preguntas)
        self.numero_pregunta=0

    def get_preguntas(self,numero_preguntas):
        url_quizz = "https://opentdb.com/api.php"
        parameters ={
            'amount': numero_preguntas,
            'type': 'boolean'
        }
        response = requests.get(url = url_quizz,params=parameters)
        return response.json()['results']

    def mostrar_pregunta(self):
        print(self.numero_pregunta)
        return html.unescape(self.preguntas[self.numero_pregunta]['question'])

    def respuesta_correcta(self):
        solucion = self.preguntas[self.numero_pregunta]['correct_answer']

        respuesta_correcta= True
        while(respuesta_correcta):         
            try:
                respuesta = self.get_respuesta()
                respuesta_correcta =False
            except TypeError:
                    print("respuesta equivocada. Vuelve a escribir")
        
        return solucion == respuesta


    def get_respuesta(self):
        
            respuesta =  input('Tu respuesta: ')
            respuesta_valida = self.respuesta_valida( respuesta )
            if respuesta_valida is False:
                raise TypeError("Solo True o False")
            return respuesta
    
    def respuesta_valida(self, respuesta):
        is_valid = respuesta in ["True", "False"]
        return is_valid

    def siguiente_pregunta(self):
        self.numero_pregunta +=1
        
    def mostrar_numero_preguntas(self):

        return len(self.preguntas)



class quizz_show():

    def __init__(self,numero_preguntas=10) -> None:
        self.ronda = preguntas_API(numero_preguntas)
        self.score = score()
        self.play_game()

    def play_game(self):
        numero_preguntas = self.ronda.mostrar_numero_preguntas()
        print(f"numero preguntas {numero_preguntas}")
        for numero in range(numero_preguntas):
            print(f"Pregunta {numero}:")
            self.play_round()
            self.ronda.siguiente_pregunta()
        self.score.print()
    
    def play_round(self):

        print(self.ronda.mostrar_pregunta() )
        acierto = self.ronda.respuesta_correcta()
        resultado = ""
        if acierto:
            self.score.raise_score()
            print( "Respuesta correcta")
        else: 
            print("Respuesta incorrecta")
        

quizz_show(3)

