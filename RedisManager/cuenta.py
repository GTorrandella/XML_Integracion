'''
Created on Apr 12, 2019

@author: Gabriel Torrandella
'''
from enum import IntEnum, unique

class Cuenta(object):
    '''
    classdocs
    '''


    def __init__(self, idC, tipo, balance, interes = "N/A"):
        '''
        Constructor
        '''
        self.id = idC
        self.tipo = tipo
        self.balance = balance
        self.interes = interes
        
@unique
class TipoCuenta(IntEnum):
    Caja_de_Ahorro = 1
    Cuenta_Corriente = 2
    