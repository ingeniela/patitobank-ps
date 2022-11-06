from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import *
from sqlalchemy import Column,String,DateTime,Integer,create_engine
from datetime import datetime
import os

### ---- TECNICO DE LA BASE DE DATOS
### Direccion de la maquina
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CONECCION_LINK = "sqlite:///"+os.path.join(BASE_DIR, 'BaseDeDatos.db')

### Base declarativa, máquina, sesión del usuario
Base = declarative_base()
Engine = create_engine(CONECCION_LINK)
Session = sessionmaker()


### ---- CLASES PARA LA BASE DE DATOS
### Clase de Usuario
class Cuenta(Base):
    __tablename__= "cuentas"
    id=Column(Integer(), primary_key=True)
    titular=Column(String(25),nullable=False, unique=True)
    curp=Column(String(20), nullable=False, unique=True)
    numCuenta=Column(Integer(), nullable=False, unique=True)
    date_created=Column(DateTime(),default=datetime.utcnow)

    def __repr__(self):
        return f"< Titular = {self.titular} / Curp = {self.curp} / Numero de cuenta = {self.numCuenta} >"
