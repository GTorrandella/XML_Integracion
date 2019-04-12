'''
Created on Apr 12, 2019

@author: Gabriel Torrandella
'''

class Cuenta(object):
    '''
    classdocs
    '''


    def __init__(self, id, tipo, balance, interes = 0):
        '''
        Constructor
        '''
        self.id = id
        self.tipo = tipo
        self.balance = balance
        self.interes = interes