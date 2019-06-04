'''
Created on Apr 14, 2019

@author: Gabriel Torrandella
'''
from RedisManager.manager import Manager

class BuscadorBalance(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.manager = Manager()
        
    def buscar(self):
        print(" ---Ingrese id(s) de cuenta(s) a consultar---")
        userInput = input(" --> ")
        print("==================")
        print(" ID |  Balance     ")
        for idCuenta in userInput.split():
            print("------------------")
            bal = self.manager.balance(idCuenta)
            if bal != "ERROR":
                print(self._agregarBlanco(idCuenta, 4)+"|"+self._agregarBlanco(bal, 14))
        print("==================")
        
    def _agregarBlanco(self, palabra, longitud):
        palabra = " " + palabra + " "
        while len(palabra) < longitud:
            palabra += " "
        return palabra