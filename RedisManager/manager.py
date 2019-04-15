"""
@author: Gabriel Torrandella
"""

import redis

class Manager():
    
    def __init__(self, contexto = "estandar"):
        if contexto == "test":
            self._db = redis.from_url("redis://localhost:6379", db = 1)
        else:
            self._db = redis.from_url("redis://xmlredis:6379", db = 0)
    
    def guardarCuenta(self, cuenta):
        mapa = {"balance":cuenta.balance,
                "tipo":cuenta.tipo,
                "interes":cuenta.interes}
        try:
            self._db.hmset("cuenta:"+cuenta.id, mapa)
            self._db.sadd("cuentas", cuenta.id)
        except redis.exceptions.ConnectionError:
            print("Base de datos offline. Revisar la conexión.")
    
    def guardarCliente(self, cliente):
        mapa = {"nombre":cliente.nombre,
                "direccion":cliente.direccion}
        try:
            self._db.hmset("cliente:"+cliente.id, mapa)
            self._db.hset("clientes", cliente.nombre, cliente.id)
        except redis.exceptions.ConnectionError:
            print("Base de datos offline. Revisar la conexión.")        
        
    def guardarRelacion(self, idCliente, idCuenta):
        try:
            self._db.hset("cuenta-cliente", idCuenta, idCliente)
            self._db.sadd("cliente-cuenta:"+idCliente, idCuenta)
        except redis.exceptions.ConnectionError:
            print("Base de datos offline. Revisar la conexión.")

    def listadoDeCuentas(self):
        try:
            lista = []
            for idCuenta in self._db.smembers("cuentas"):
                aux = {"id":idCuenta.decode()}
                cuenta = self._db.hgetall("cuenta:"+ idCuenta.decode())
                for dato in cuenta:
                    aux[dato.decode()] = cuenta[dato].decode()
                idTitular = self._db.hget("cuenta-cliente", idCuenta.decode()).decode()
                aux['t'] = self._db.hget("cliente:"+idTitular, "nombre").decode()
                lista.append(aux)
            return lista
        except redis.exceptions.ConnectionError:
            print("Base de datos offline. Revisar la conexión.")
            return "ERROR"
    
    def cuentasPorTitular(self, titular):
        try:
            lista = []
            idCliente = self._db.hget("clientes", titular)
            if not idCliente == None:
                for idCuenta in self._db.smembers("cliente-cuenta:"+idCliente.decode()):
                    aux = [idCuenta.decode()]
                    for dato in self._db.hmget("cuenta:"+ idCuenta.decode(), "balance", "tipo", "interes"):
                        aux.append(dato.decode())
                    lista.append(aux)
            return lista
        except redis.exceptions.ConnectionError:
            print("Base de datos offline. Revisar la conexión.")
            return "ERROR"
    
    def balance(self, cuenta):
        try:
            bal = self._db.hget("cuenta:"+cuenta, "balance")
            if not bal == None:
                return bal.decode()
        except redis.exceptions.ConnectionError:
            print("Base de datos offline. Revisar la conexión.")
            return "ERROR"
        
        