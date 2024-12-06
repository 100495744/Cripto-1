from Criptografia import FirmaDigital
from interface import Interface

class Main:
    def __init__(self):
        self.firma_digital = FirmaDigital()
        self.firma_digital.inicializar_ac()  # Inicializar las AC en el arranque

    @staticmethod
    def iniciar():
        Interface.inicial()

if __name__ == '__main__':
    Main().iniciar()
