'''
Created on Apr 14, 2019

@author: Gabriel Torrandella
'''
import sys

from XML.lector import Lector
from XML.enlistadorCuentas import Enlistador
from XML.buscadorTitulares import BuscadorTitulares
from XML.buscadorBalance import BuscadorBalance

class Menu(object):
    
    def __init__(self):
        pass
    
    def mostrarMenu(self):
        pass
    
    def mostrarAyuda(self):
        print(" # balance. Busca el balance de una cuenta")
        print(" # listar.  Lista todas las cuentas")
        print(" # titular. Busca todas las cuentas a nombre del titular")
        print(" # exit, salir, quir. Salir del programa")
    
    def bucle(self):
        i = ""
        self.mostrarMenu()
        while not i.lower() in ["exit", "salir", "quit"]:
            i = input('-->')
            if i == "balance":
                BuscadorBalance().buscar()
            elif i == "listar":
                Enlistador().enlistar()
            elif i == "titular":
                BuscadorTitulares().buscar()
            elif ".xml" in i:
                Lector(i).guardarXML()
            elif i in ["help", "ayuda", "?"]:
                self.mostrarAyuda()
                

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Menu().bucle()
    else:
        print(sys.argv)