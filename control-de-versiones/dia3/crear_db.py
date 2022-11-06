from sql_file import *

# Crear la base de datos para las cuentas
Base.metadata.create_all(engine_cuentas)
# Crear la base de datos para las transacciones
Base.metadata.create_all(engine_transacciones)