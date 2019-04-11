"""
created by: Gabriel Torrandella
"""

import redis

class Manager():
    
    def __init__(self):
        self.db = redis.from_url("redis://localhost:6379", db=None)
    
    def guardarCuenta(self, cuenta):
        mapa = {"balance":cuenta.balance,
                "tipo":cuenta.tipo,
                "interes":cuenta.interes}
        self.db.hmset("cuenta:"+cuenta.id, mapa)
        self.db.sadd("cuentas", cuenta.id)
    
    def guardarCliente(self, cliente):
        mapa = {"nombre":cliente.nombre,
                "direccion":cliente.direccion}
        self.db.hmset("cliente:"+cliente.id, mapa)
        self.db.hset("clientes", cliente.nombre, cliente.id)
        
    def guardarRelacion(self, cliente, cuenta):
        self.db.hset("cuenta-cliente", cuenta.id, cliente.id)
        self.db.sadd("cliente-cuenta:"+cliente.id, cuenta.id)

    def listadoDeCuentas(self):
        lista = []
        for cuenta in self.db.smembers("cuentas"):
            lista.append(self.db.hgetall("cuenta:"+cuenta))
        return lista
    
    def cuentasPorTitular(self, titular):
        lista = []
        return lista
    
    def balance(self, cuenta):
        return self.db.hget("cuenta:"+cuenta, "balance").decode
        
        