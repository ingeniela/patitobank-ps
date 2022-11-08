# Importar librerías SQL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import *
from sqlalchemy import Column,String,DateTime,Integer,create_engine
import sqlalchemy as sa
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError, ProgrammingError

# Importar otras liberías
import os
from datetime import datetime
from copy import copy

### ---------------------- Base de datos ---------------------- ###
### Direccion de la maquina
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
Base = declarative_base()
### Link
Link1 = "sqlite:///"+os.path.join(BASE_DIR, 'cuentas.db')
Link2 = "sqlite:///"+os.path.join(BASE_DIR, 'transacciones.db')
### Engine
engine_cuentas = create_engine(Link1)
engine_transacciones = create_engine(Link2)
### Session maker
database_cuentas = sessionmaker(engine_cuentas)
database_transacciones = sessionmaker(engine_transacciones)

### ---------------------- Clases para las bases de datos ---------------------- ###
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

### ---------------------- SQL Utils ---------------------- ###
# Se transfirió de esta manera para no tener que descargar la librería oficial (sqlalchemy_utils)
def _set_url_database(url: sa.engine.url.URL, database):
    if hasattr(url, '_replace'):
        # Cannot use URL.set() as database may need to be set to None.
        ret = url._replace(database=database)
    else:  # SQLAlchemy <1.4
        url = copy(url)
        url.database = database
        ret = url
    assert ret.database == database, ret
    return ret
def _get_scalar_result(engine, sql):
    with engine.begin() as conn:
        return conn.scalar(sql)
def _sqlite_file_exists(database):
    if not os.path.isfile(database) or os.path.getsize(database) < 100:
        return False

    with open(database, 'rb') as f:
        header = f.read(100)

    return header[:16] == b'SQLite format 3\x00'
def database_exists(url):
    url = make_url(url)
    database = url.database
    dialect_name = url.get_dialect().name
    engine = None
    try:
        if dialect_name == 'postgresql':
            text = "SELECT 1 FROM pg_database WHERE datname='%s'" % database
            for db in (database, 'postgres', 'template1', 'template0', None):
                url = _set_url_database(url, database=db)
                engine = sa.create_engine(url)
                try:
                    return bool(_get_scalar_result(engine, sa.text(text)))
                except (ProgrammingError, OperationalError):
                    pass
            return False

        elif dialect_name == 'mysql':
            url = _set_url_database(url, database=None)
            engine = sa.create_engine(url)
            text = ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                    "WHERE SCHEMA_NAME = '%s'" % database)
            return bool(_get_scalar_result(engine, sa.text(text)))

        elif dialect_name == 'sqlite':
            url = _set_url_database(url, database=None)
            engine = sa.create_engine(url)
            if database:
                return database == ':memory:' or _sqlite_file_exists(database)
            else:
                # The default SQLAlchemy database is in memory, and :memory: is
                # not required, thus we should support that use case.
                return True
        else:
            text = 'SELECT 1'
            try:
                engine = sa.create_engine(url)
                return bool(_get_scalar_result(engine, sa.text(text)))
            except (ProgrammingError, OperationalError):
                return False
    finally:
        if engine:
            engine.dispose()
