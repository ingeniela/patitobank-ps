from sql_file import Cuenta, Session, Engine, Base

# Crear la base de datos
Base.metadata.create_all(Engine)