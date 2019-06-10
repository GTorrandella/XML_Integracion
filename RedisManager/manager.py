"""
@author: Gabriel Torrandella
"""

import redis
import logging
from RedisManager.cuenta import Cuenta, TipoCuenta

logging.basicConfig(level=logging.DEBUG)

class Manager():
    
    _BASE_NAME_HM_CUENTAS = "cuenta:"
    _NAME_SET_CUENTAS = "cuentas"
    _BASE_NAME_HM_CLIENTE = "cliente:"
    _NAME_SET_CLIENTES = "clientes"
    _NAME_HM_CUENTA_CLIENTE = "cuenta-cliente"
    _BASE_NAME_SET_CLIENTE_CUENTA = "cliente-cuenta:"
    
    def __init__(self, contexto = "estandar"):
        if contexto == "test":
            self._db = redis.from_url("redis://localhost:6379", db = 1)
        else:
            self._db = redis.from_url("redis://redis:6379", db = 0)
    
    def _crearNombreHMCuentas(self, idCuenta):
        return self._BASE_NAME_HM_CUENTAS + idCuenta
    
    def _crearNombreHMCliente(self, idCliente):
        return self._BASE_NAME_HM_CLIENTE + idCliente
    
    def _crearNombreSetClienteCuenta(self, idCliente):
        return self._BASE_NAME_SET_CLIENTE_CUENTA + idCliente
    
    def guardarCuenta(self, cuenta):
        mapa = {"balance":cuenta.balance,
                "tipo":cuenta.tipo.name,
                "interes":cuenta.interes}
        try:
            self._db.hmset(self._crearNombreHMCuentas(cuenta.id), mapa)
            self._db.sadd(self._NAME_SET_CUENTAS, cuenta.id)
        except redis.exceptions.ConnectionError:
            logging.debug(redis.exceptions.ConnectionError)
            print("Base de datos offline. Revisar la conexión.")
    
    def guardarCliente(self, cliente):
        mapa = {"nombre":cliente.nombre,
                "direccion":cliente.direccion}
        try:
            self._db.hmset(self._crearNombreHMCliente(cliente.id), mapa)
            self._db.hset(self._NAME_SET_CLIENTES, cliente.nombre, cliente.id)
        except redis.exceptions.ConnectionError:
            logging.debug(redis.exceptions.ConnectionError)
            print("Base de datos offline. Revisar la conexión.")        
        
    def guardarRelacion(self, idCliente, idCuenta):
        try:
            self._db.hset(self._NAME_HM_CUENTA_CLIENTE, idCuenta, idCliente)
            self._db.sadd(self._crearNombreSetClienteCuenta(idCliente), idCuenta)
        except redis.exceptions.ConnectionError:
            logging.debug(redis.exceptions.ConnectionError)
            print("Base de datos offline. Revisar la conexión.")

    def _buscarCuenta(self, idCuenta):
        tipo, balance, interes = self._db.hmget(self._crearNombreHMCuentas(idCuenta), "tipo", "balance", "interes")
        return Cuenta(idCuenta, TipoCuenta[tipo.decode()], balance.decode(), interes.decode()) 

    def listadoDeCuentas(self):
        try:
            lista = []
            for idCuenta in self._db.smembers(self._NAME_SET_CUENTAS):
                idTitular = self._db.hget(self._NAME_HM_CUENTA_CLIENTE, idCuenta.decode()).decode()
                aux ={'cuenta':self._buscarCuenta(idCuenta.decode()),
                      'titular':self._db.hget("cliente:"+idTitular, "nombre").decode()}
                lista.append(aux)
            return lista
        except redis.exceptions.ConnectionError:
            logging.debug(redis.exceptions.ConnectionError)
            print("Base de datos offline. Revisar la conexión.")
            return "ERROR"
    
    def cuentasPorTitular(self, titular):
        try:
            lista = []
            idCliente = self._db.hget(self._NAME_SET_CLIENTES, titular)
            if not idCliente == None:
                for idCuenta in self._db.smembers(self._crearNombreHMCliente(idCliente.decode())):
                    lista.append(self._buscarCuenta(idCuenta.decode()))
            return lista
        except redis.exceptions.ConnectionError:
            logging.debug(redis.exceptions.ConnectionError)
            print("Base de datos offline. Revisar la conexión.")
            return "ERROR"
    
    def balance(self, idCuenta):
        try:
            bal = self._db.hget(self._crearNombreHMCuentas(idCuenta), "balance")
            if not bal == None:
                return bal.decode()
        except redis.exceptions.ConnectionError:
            logging.debug(redis.exceptions.ConnectionError)
            print("Base de datos offline. Revisar la conexión.")
            return "ERROR"
        
        
