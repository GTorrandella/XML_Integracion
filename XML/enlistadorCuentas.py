'''
Created on Apr 14, 2019

@author: Gabriel Torrandella
'''
from RedisManager.manager import Manager
from RedisManager.cuenta import TipoCuenta

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
        if tipo == TipoCuenta.Cuenta_Corriente:
            return self._agregarBlanco("Cte", 6)
        elif tipo == TipoCuenta.Caja_de_Ahorro:
            return self._agregarBlanco("Ahr", 6)
    
    def _imprimirCuenta(self, cuenta):
        print(" ---------------------------------------------")
        nombreSeparadoEnLineas = cuenta['titular'].split()
        infoCuenta = cuenta['cuenta']
        idc = self._agregarBlanco(cuenta.id, 4)
        balance = self._agregarBlanco(infoCuenta.balance, 9)
        interes = self._agregarBlanco(infoCuenta.interes, 13)
        tipo = self._defTipo(infoCuenta.tipo)
        
        print(' '+idc+'|'+self._agregarBlanco(nombreSeparadoEnLineas[0], 9)+'|'+balance+'|'+interes+'|'+tipo)
        
        for linea in range(1, len(nombreSeparadoEnLineas)):
            print("     |"+self._agregarBlanco(nombreSeparadoEnLineas[linea], 9)+"|         |             |     ")
        