'''
Created on Apr 14, 2019

@author: Gabriel Torrandella
'''
from RedisManager.manager import Manager
from RedisManager.cuenta import TipoCuenta

class BuscadorTitulares(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.manager = Manager()
        
    def buscar(self):
        print(" ---Ingrese el(los) nombre(s) a consultar, separados por ','---")
        tits = input(" --> ")
        if ", " in tits:
            tits = tits.split(", ")
        else:
            tits = tits.split(",")
        print("=========================================================")
        print("       Titular       | ID | Balance | Tasa de Int | Tipo ")
        for i in tits:
            self._imprimirCuentasPorTitular(i)
        print("=========================================================")
        
    def _agregarBlanco(self, palabra, longitud):
        palabra = " " + palabra + " "
        while len(palabra) < longitud:
            palabra += " "
        return palabra
    
    def _defTipo(self, tipo):
        if tipo == TipoCuenta.Cuenta_Corriente:
            return self._agregarBlanco("Cte", 6)
        elif tipo == TipoCuenta.Caja_de_Ahorro:
            return self._agregarBlanco("Ahr", 6)
        
    def _imprimirCuentasPorTitular(self, titular):
        print("---------------------------------------------------------")
        print(self._agregarBlanco(titular+":", 21))
        cuentas = self.manager.cuentasPorTitular(titular)
        for c in cuentas:
            aux = self._agregarBlanco("", 21)
            aux += "|"+self._agregarBlanco(c[0], 4)
            aux += "|"+self._agregarBlanco(c[1], 9)
            aux += "|"+self._agregarBlanco(c[3], 13)
            aux += "|"+self._defTipo(c[2])
            print(aux)