'''
Created on Apr 14, 2019

@author: Gabriel Torrandella
'''
from RedisManager.manager import Manager

class Enlistador(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.manager = Manager()
    
    def enlistar(self):
        listado = self.manager.listadoDeCuentas()
        listado = sorted(listado, key=lambda d: d['id'])
        self.imprimirListado(listado)
        
    def imprimirListado(self, listado):
        print("")
        print(" =============================================")
        print("  ID | Titular | Balance | Tasa de Int | Tipo ")
        for cuenta in listado:
            self._imprimirCuenta(cuenta)
        print(" =============================================")
    
    def _agregarBlanco(self, palabra, longitud):
        palabra = " " + palabra + " "
        while len(palabra) < longitud:
            palabra += " "
        return palabra
    
    def _defTipo(self, tipo):
        if tipo == "corriente":
            return self._agregarBlanco("Cte", 6)
        elif tipo == "ahorro":
            return self._agregarBlanco("Ahr", 6)
    
    def _imprimirCuenta(self, cuenta):
        print(" ---------------------------------------------")
        idc = self._agregarBlanco(cuenta['id'], 4)
        nombre = cuenta['t'].split()
        bal = self._agregarBlanco(cuenta['balance'], 9)
        tint = self._agregarBlanco(cuenta['interes'], 13)
        t = self._defTipo(cuenta['tipo'])
        
        print(' '+idc+'|'+self._agregarBlanco(nombre[0], 9)+'|'+bal+'|'+tint+'|'+t)
        
        for i in range(1, len(nombre)):
            print("     |"+self._agregarBlanco(nombre[i], 9)+"|         |             |     ")
        