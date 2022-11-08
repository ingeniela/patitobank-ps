from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import exc
from sqlalchemy import *
from sqlalchemy import Column,String,DateTime,Integer,create_engine
from datetime import datetime
import os

### ---- TECNICO DE LA BASE DE DATOS
### Direccion de la maquina
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
Base = declarative_base()

### Link
Link1 = "sqlite:///"+os.path.join(BASE_DIR, 'db_cuenta.db')
Link2 = "sqlite:///"+os.path.join(BASE_DIR, 'db_transaccion.db')

### Engine
engine_cuentas = create_engine(Link1)
engine_transacciones = create_engine(Link2)

### Session maker
database_cuentas = sessionmaker(engine_cuentas)
database_transacciones = sessionmaker(engine_transacciones)

### ---- CLASES PARA LA BASE DE DATOS
### Clase de Cuenta
class Cuenta(Base):
    __tablename__= "cuentas"
    id=Column(Integer(), primary_key=True)
    titular=Column(String(25),nullable=False, unique=False)
    curp=Column(String(20), nullable=False, unique=True)
    numCuenta=Column(String(10), nullable=False, unique=True)
    fecha_creacion=Column(DateTime(), nullable=True, unique=False)

    def __repr__(self):
        return f"\n• Titular = {self.titular} \n• Curp = {self.curp} \n• Numero de cuenta = {self.numCuenta}"

    def data_basico(self):
        return f"| Titular = {self.titular} | Numero de cuenta = {self.numCuenta} |"

### Clase de Transaccion
class Transaccion(Base):
    __tablename__= "transacciones"
    id=Column(Integer(), primary_key=True)
    numCuenta=Column(String(10), nullable=False, unique=False)
    balance=Column(Integer(), nullable=False, unique=False)
    tipo=Column(String(10), nullable=True, unique=False)
    monto=Column(Integer(), nullable=True, unique=False)
    fecha=Column(DateTime(), nullable=True, unique=False)
    concepto=Column(String(25), nullable=True, unique=False)

    def __repr__(self):
        return f"| Número de Cuenta = {self.numCuenta} | Balance = ${self.balance} | Tipo = {self.tipo}  | Monto = ${self.monto}  | Fecha = {self.fecha} | Concepto = {self.concepto} |"

    def dataTransaccion(self):
        return f"| Número de Cuenta = {self.numCuenta} | Tipo = {self.tipo}  | Monto = ${self.monto}  | Fecha = {self.fecha} | Concepto = {self.concepto} |"
    def soloBalance(self):
        return self.balance

###----
