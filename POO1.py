class Animal:
    def Falar(self):
        print("O animal faz um som genérico.")
    
class Cachorro:
    def Falar(self):
        print("O cachorro está latindo.")

class Gato:
    def Falar(self):
        print("O gato está miando.")


animal = Animal()
animal.Falar()
cachorro = Cachorro()
cachorro.Falar()
gato = Gato()
gato.Falar()