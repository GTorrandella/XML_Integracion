'''
Created on Apr 11, 2019

@author: gabo
'''
import unittest
from RedisManager.manager import Manager
from RedisManager.cliente import Cliente
from RedisManager.cuenta import Cuenta

class Test(unittest.TestCase):
    # Datos iniciales
    
    # Dos clientes
    clienteUno = {"id":"c1", 
                  "datos":{
                      "nombre":"Pedro Romero",
                      "direccion":"Falsa 123"}}
    clienteDos = {"id":"c2",
                  "datos":{
                      "nombre":"Sofia Romero",
                      "direccion":"Equivocada 456"}}
    # Tres cuentas
    cuentaUno = {"id":"a1",
                 "datos":{
                     "balance":"5000",
                     "tipo":"corriente",
                     "interes":"0"}}
    cuentaDos = {"id":"a2",
                 "datos":{
                     "balance":"4000",
                     "tipo":"corriente",
                     "interes":"0"}}
    cuentaTres = {"id":"a3",
                  "datos":{
                     "balance":"100000",
                     "tipo":"ahorro",
                     "interes":"0.05"}}

    # c1 posee a1; c2 posse a2 y a4
    
    def setUp(self):
        self.manager = Manager("test")
        
        self.manager._db.hmset("cliente:"+self.clienteUno['id'], self.clienteUno['datos'])
        self.manager._db.hset("clientes", self.clienteUno['datos']['nombre'], self.clienteUno['id'])
        
        self.manager._db.hmset("cliente:"+self.clienteDos['id'], self.clienteDos['datos'])
        self.manager._db.hset("clientes", self.clienteDos['datos']['nombre'], self.clienteDos['id'])
        
        self.manager._db.hmset("cuenta:"+self.cuentaUno['id'], self.cuentaUno['datos'])
        self.manager._db.sadd("cuentas", self.cuentaUno['id'])
        
        self.manager._db.hmset("cuenta:"+self.cuentaDos['id'], self.cuentaDos['datos'])
        self.manager._db.sadd("cuentas", self.cuentaDos['id'])
        
        self.manager._db.hmset("cuenta:"+self.cuentaTres['id'], self.cuentaTres['datos'])
        self.manager._db.sadd("cuentas", self.cuentaTres['id'])
        
        self.manager._db.hset("cuenta-cliente", self.cuentaUno['id'], self.clienteUno['id'])
        self.manager._db.sadd("cliente-cuenta:"+self.clienteUno['id'], self.cuentaUno['id'])
        
        self.manager._db.hset("cuenta-cliente", self.cuentaDos['id'], self.clienteDos['id'])
        self.manager._db.sadd("cliente-cuenta:"+self.clienteDos['id'], self.cuentaDos['id'])
        
        self.manager._db.hset("cuenta-cliente", self.cuentaTres['id'], self.clienteDos['id'])
        self.manager._db.sadd("cliente-cuenta:"+self.clienteDos['id'], self.cuentaTres['id'])
        
    def tearDown(self):
        self.manager._db.flushdb()


    def test_guardarCuenta(self):
        self.assertEqual(len(self.manager._db.smembers("cuentas")), 3)
        self.assertFalse(self.manager._db.hgetall("cuenta:a4"))
        
        cuentaNueva = Cuenta('a4', 'ahorro', '7000', '0.06')
        self.manager.guardarCuenta(cuentaNueva)
        
        self.assertEqual(len(self.manager._db.smembers("cuentas")), 4)
        cuentaNuevaDatos = self.manager._db.hgetall("cuenta:a4")
        self.assertEqual(cuentaNuevaDatos['tipo'.encode()].decode(), 'ahorro')
        self.assertEqual(cuentaNuevaDatos['balance'.encode()].decode(), '7000')
        self.assertEqual(cuentaNuevaDatos['interes'.encode()].decode(), '0.06')
        
        
    def test_guardarCliente(self):
        self.assertEqual(self.manager._db.hget("clientes", 'Francisco Romero'), None)
        self.assertFalse(self.manager._db.hgetall("cliente:c3"))
        
        clienteNuevo = Cliente('c3', 'Francisco Romero', 'Erronea 789')
        self.manager.guardarCliente(clienteNuevo)
        
        self.assertEqual(self.manager._db.hget("clientes", 'Francisco Romero').decode(), 'c3')
        clienteNuevoDatos = self.manager._db.hgetall("cliente:c3")
        self.assertEqual(clienteNuevoDatos['direccion'.encode()].decode(), 'Erronea 789')
        self.assertEqual(clienteNuevoDatos['nombre'.encode()].decode(), 'Francisco Romero')
    
    def test_guardarRelacion(self):
        self.assertEqual(len(self.manager._db.hgetall('cuenta-cliente')), 3)
        self.assertEqual(self.manager._db.scard("cliente-cuenta:c3"), 0)
        
        cuentaNueva = Cuenta('a4', 'ahorro', '7000', '0.06')
        clienteNuevo = Cliente('c3', 'Francisco Romero', 'Erronea 789')
        self.manager.guardarRelacion(Cliente.id, Cuenta.id)
        
        self.assertEqual(len(self.manager._db.hgetall('cuenta-cliente')), 4)
        self.assertEqual(self.manager._db.scard("cliente-cuenta:c3"), 1)
        self.assertTrue('a4'.encode() in self.manager._db.smembers("cliente-cuenta:c3"))
    
    def test_listadoDeCuentas(self):
        cuentas = self.manager.listadoDeCuentas()
        self.assertTrue({'tipo': 'ahorro', 'interes': '0.05', 'balance': '100000'} in cuentas)
        self.assertTrue({'tipo': 'corriente', 'balance': '5000', 'interes': '0'} in cuentas)
        self.assertTrue({'tipo': 'corriente', 'balance': '4000', 'interes': '0'} in cuentas)
    
    def test_cuentasPorTitular(self):
        cuentasPedro = self.manager.cuentasPorTitular("Pedro Romero")
        self.assertTrue(['5000', 'corriente', '0'] in cuentasPedro)
        
        cuentasSofia = self.manager.cuentasPorTitular("Sofia Romero")
        self.assertTrue(['100000', 'ahorro', '0.05'] in cuentasSofia)
        self.assertTrue(['4000', 'corriente', '0'] in cuentasSofia)
    
    def test_balance(self):
        balanceUno = self.manager.balance('a1')
        self.assertEqual(balanceUno, self.cuentaUno['datos']['balance'])
        
        balanceDos = self.manager.balance('a2')
        self.assertEqual(balanceDos, self.cuentaDos['datos']['balance'])
        
        balanceTres = self.manager.balance('a3')
        self.assertEqual(balanceTres, self.cuentaTres['datos']['balance'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()