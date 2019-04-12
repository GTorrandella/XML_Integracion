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
        self._db.hmset("cuenta:"+cuenta.id, mapa)
        self._db.sadd("cuentas", cuenta.id)
    
    def guardarCliente(self, cliente):
        mapa = {"nombre":cliente.nombre,
                "direccion":cliente.direccion}
        self._db.hmset("cliente:"+cliente.id, mapa)
        self._db.hset("clientes", cliente.nombre, cliente.id)
        
    def guardarRelacion(self, cliente, cuenta):
        self._db.hset("cuenta-cliente", cuenta.id, cliente.id)
        self._db.sadd("cliente-cuenta:"+cliente.id, cuenta.id)

    def listadoDeCuentas(self):
        lista = []
        for idCuenta in self._db.smembers("cuentas"):
            aux = {}
            cuenta = self._db.hgetall("cuenta:"+ idCuenta.decode())
            for dato in cuenta:
                aux[dato.decode()] = cuenta[dato].decode()
            lista.append(aux)
        return lista
    
    def cuentasPorTitular(self, titular):
        lista = []
        idCliente = self._db.hget("clientes", titular).decode()
        for idCuenta in self._db.smembers("cliente-cuenta:"+idCliente):
            aux = []
            for dato in self._db.hmget("cuenta:"+ idCuenta.decode(), "balance", "tipo", "interes"):
                aux.append(dato.decode())
            lista.append(aux)
        return lista
    
    def balance(self, cuenta):
        return self._db.hget("cuenta:"+cuenta, "balance").decode()
        
        