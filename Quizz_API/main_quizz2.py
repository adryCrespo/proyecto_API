import requests
import html



class Score():
    def __init__(self) -> None:
        self.score = 0
    
    def raise_score(self):
        self.score +=1
    
    def get_score(self):
        return self.score
    
    def print(self):
        print(f"Your game score is {self.score}")


class PreguntasAPI():
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

    def respuesta_correcta(self,respuesta):
        solucion = bool(self.preguntas[self.numero_pregunta]['correct_answer'])
        
        print(f"solucion: {solucion}")
        print(f"respuesta: {respuesta}")
    
        acierto = solucion is respuesta
        print(f"acierto: {acierto}")

        print(f"Tipo acierto: {type(acierto)}")
        print(f"Tipo respuesta: {type(respuesta)}")
        print(f"Tipo solucion: {type(solucion)}")

        return acierto




    def siguiente_pregunta(self):
        self.numero_pregunta +=1
        
    def mostrar_numero_preguntas(self):

        return len(self.preguntas)

    def tiene_mas_preguntas_check(self):
        hay_mas = (self.mostrar_numero_preguntas()-1) > self.numero_pregunta
        return hay_mas

    def obtener_numero_actual(self):
        return self.numero_pregunta
    
class QuizzShow():

    def __init__(self,numero_preguntas=10) -> None:
        self.ronda = PreguntasAPI(numero_preguntas)
        self.score = Score()
    
    def revisar_respuesta(self,respuesta):
        
        print("revisar pregunta" )
        print(f"Numero pregunta: {self.ronda.obtener_numero_actual()}")

        if self.ronda.tiene_mas_preguntas_check() is False:
            return None
        

        acierto = self.ronda.respuesta_correcta(respuesta)
        print(f"He acertado: {acierto}")
  
        if acierto:
            self.score.raise_score()
        

        self.ronda.siguiente_pregunta()
        return acierto
        
    def mostrar_pregunta(self):
        return self.ronda.mostrar_pregunta()
    
    def mostrar_resultado(self):
        return self.score.get_score()
    
    def tiene_mas_preguntas_check(self):
        return self.ronda.tiene_mas_preguntas_check()

    

if __name__ == "__main__":

    qi = QuizzShow()

