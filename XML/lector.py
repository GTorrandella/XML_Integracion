"""
@author: Gabriel Torrandella
"""
import xml.etree.ElementTree as ET
import xmlschema

from RedisManager.cliente import Cliente
from RedisManager.cuenta import Cuenta, TipoCuenta
from RedisManager.manager import Manager


class Lector(object):
    '''
    classdocs
    '''


    def __init__(self, xml, schema = ""):
        '''
        Constructor
        '''
        self.manager = Manager()
        if not schema == "":
            try:
                if xmlschema.XMLSchema(schema).is_valid(xml):
                    self.xml = ET.parse(xml).getroot()
                else:
                    raise Exception()
            except:
                print("Bad Schema or XML")
        else:
            self.xml = ET.parse(xml).getroot()
        
    def guardarXML(self):
        for child in self.xml:
            if child.tag == "cuentas":
                self._guardarCuentas(child)
            elif child.tag == "clientes":
                self._guardarClientes(child)
            elif child.tag == "clientes_cuentas":
                self._guardarRelaciones(child)
            
    def _guardarCuentas(self, cuentas):
        for child in cuentas:
            if child.tag == "caja_ahorros":
                self._guardarCajaAhorro(child)
            elif child.tag == "cuentas_corrientes":
                self._guardarCuentaCorriente(child)
            
    def _guardarCajaAhorro(self, cajas):
        for caja in cajas:
            balance = caja[0].text
            self.manager.guardarCuenta(Cuenta(caja.attrib['id'], TipoCuenta.Caja_de_Ahorro, balance, caja.attrib['interes']))
    
    def _guardarCuentaCorriente(self, cuenta):
        for cuenta in cuenta:
            balance = cuenta[0].text
            self.manager.guardarCuenta(Cuenta(cuenta.attrib['id'], TipoCuenta.Cuenta_Corriente, balance))
            
    def _guardarClientes(self, clientes):
        for cliente in clientes:
            nom = cliente[0].text
            direc = cliente[1].text
            self.manager.guardarCliente(Cliente(cliente.attrib['id'], nom, direc))
    
    def _guardarRelaciones(self, relaciones):
        for relacion in relaciones:
            self.manager.guardarRelacion(relacion.attrib['c_id'], relacion.attrib['cu_id'])