### ---- BACKEND: que todo funcione
import random
from sql_file import *

# SQL ALCHEMY
local_cuentas = database_cuentas(bind=engine_cuentas)
local_transacciones = database_transacciones(bind=engine_transacciones)
# database

### --- OTROS

# opciones que podria escoger el usuario
# Opcion 1
def crear_cuenta():
    # A // Crear la cuenta: Nombre del titular
    titular_input = str(input("Coloque el nombre del titular: "))

    # B// Curp
    curp_input = str(input("Coloque el CURP: "))

    # C // Generar numero de cuenta
    generar_numero = int(random.randint(1000000000, 9999999999))
    nueva_cuenta = Cuenta(titular=titular_input, curp=curp_input, numCuenta=generar_numero)
    nuevo_balance = Transaccion(numCuenta=generar_numero, balance=0, tipo="Cuenta creada")

    # Agregar a la base de datos
    local_cuentas.add(nueva_cuenta)
    local_cuentas.commit()
    local_transacciones.add(nuevo_balance)
    local_transacciones.commit()

    # D // Mostrar datos de la cuenta creada
    print("\n¡Cuenta creada con éxito!\n")
    print(nueva_cuenta)
    print("Por favor guarde estos datos en un lugar seguro.")

    # C // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 2
def ver_cuenta_balance():
    # A // Ingresar numero de cuenta para ver el balance
    numCuenta_input = int(input("Coloque el numero de cuenta del usuario: "))
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()

    print("Se ha encontrado la siguiente cuenta: ")
    print(buscar_numCuenta)
    # Encontrar balance de la cuenta
    print("El balance de esa cuenta es: ")
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    print(transacciones.soloBalance())
    # C // Pedir préstamo
    user_input = int(input("Cuanto dinero desea prestar"))
    # Seleccionar mes a pagar
    ano = int(input('En que año va a pagar: '))
    mes = int(input('En que mes lo va a pagar: '))
    dia = int(input('En que dia lo va a pagar: '))
    # Tomar la fecha actual
    fecha_input = datetime(ano, mes, dia, 12, 0, 0)
    fecha_ahora = datetime.now()
    # Tasa de interes segun el monto
    interesXmonto = 0.12  # 12% de interes por el monto que se realice
    # Tasa de Interés según los dias faltantes
    diff = datetime.now() - fecha_input
    segundos_restantes = diff.total_seconds()
    dias_restantes = int(segundos_restantes / 86400) * -1
    interesXfecha = (dias_restantes * 0.0026)  # 8% de interes por cada 30 dias
    # Interés completo
    interesXprestamo = (interesXmonto + interesXfecha)  # cuanto porcentaje es en total
    dinero_total = int((user_input * interesXprestamo) + user_input)
    print("Se le va a realizar un prestamo de: ", user_input, ". Debe pagarlo en", dias_restantes, "dias")
    print("Interes a pagar en total: ", interesXprestamo)
    # print("/ Interes por el monto", interesXmonto, "/ Interes por la fecha", interesXfecha)
    print("Es decir, que debe pagar: ", dinero_total, "Pesos en total")

    # Agregar balance nuevo
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    nuevo_balance = transacciones.soloBalance() + dinero_total
    nueva_transaccion = Transaccion(numCuenta=numCuenta_input, balance=nuevo_balance, tipo="Préstamo",
                                    monto=dinero_total,
                                    concepto="Prestamo realizado por PatitoBank")
    print("Transaccion realizada con éxito. Información:")
    print(nueva_transaccion.dataTransaccion())

    local_transacciones.add(nueva_transaccion)
    local_transacciones.commit()
    # D // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 3
def depositar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = int(input("Coloque el numero de cuenta del usuario: "))
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()

    print("Se ha encontrado la siguiente cuenta: ")
    print(buscar_numCuenta)

    # B // Ingresar datos del depósito (Cantidad / Fecha y Hora / Concepto)
    monto_input = int(input("Cuando dinero desea transferir: "))
    concepto_input = str(input("Coloque el concepto de esta transaccion: "))

    # Agregar balance nuevo
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    nuevo_balance = transacciones.soloBalance() + monto_input
    nueva_transaccion = Transaccion(numCuenta=numCuenta_input, balance=nuevo_balance, tipo="Deposito",
                                    monto=monto_input,
                                    concepto=concepto_input)
    print("Transaccion realizada con éxito. Información:")
    print(nueva_transaccion.dataTransaccion())

    local_transacciones.add(nueva_transaccion)
    local_transacciones.commit()
    # C // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 4
def retirar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = int(input("Coloque el numero de cuenta del usuario: "))
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()

    print("Se ha encontrado la siguiente cuenta: ")
    print(buscar_numCuenta)

    # B // Ingresar datos del depósito (Cantidad / Fecha y Hora / Concepto)
    monto_input = int(input("Cuando dinero desea retirar: "))
    concepto_input = str(input("Coloque el concepto de este retiro: "))

    # Agregar balance nuevo
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    nuevo_balance = transacciones.soloBalance() - monto_input
    # if transacciones.soloBalance() < monto_input_
    nueva_transaccion = Transaccion(numCuenta=numCuenta_input, balance=nuevo_balance, tipo="Deposito",
                                    monto=monto_input,
                                    concepto=concepto_input)
    print("Transaccion realizada con éxito. Información:")
    print(nueva_transaccion.dataTransaccion())

    local_transacciones.add(nueva_transaccion)
    local_transacciones.commit()
    # C // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 5
def mostrar_cuentas():
    # A // Ingresar contraseña especial
    contrasena = input("Ingrese la contraseña especial para acceder a las cuentas")

    # B // Mostrar todas las cuentas creadas
    cuentas = local_cuentas.query(Cuenta).all()
    for cuenta in cuentas:
        print(cuenta.data_basico())

    # C // Opciones:
    pregunta = int(input("Presione 1. Para eliminar todas las cuentas. Presione 2. Para volver al menu de inicio"))

    if pregunta == 1:
        try:
            eliminar_cuentas = local_cuentas.query(Cuenta).delete()
            local_cuentas.commit()
            print("Se han eliminado todas las cuentas de la base de datos")
            pass
        except:
            local_cuentas.rollback()
            pass
    elif pregunta == 2:
        PatitoBank.volver_menu("Si")
    # C // Volver al menu de opciones
    PatitoBank.volver_menu("Si")

# Opcion 6
def ver_cuenta_historial():
    # A // Ingresar contraseña especial
    contrasena = input("Ingrese la contraseña especial para acceder a las cuentas")

    # B // Ingresar numero de cuenta
    numCuenta_input = int(input("Coloque el numero de cuenta: "))
    print("Se ha entcontrado la siguiente cuenta")
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
    print(buscar_numCuenta)
    # C // Ver historial numero de cuenta
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).all()
    for transaccione in transacciones:
        print(transaccione)
    # D // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)


### ---- FRONTEND: Quetodo se vea bonito
class PatitoBank:
    def bienvenida(self):
        print("¡Sea bienvenido a Patito Bank!\n")

    def menu_opcion():
        print(
            "1: Crear una cuenta \n2: Ver el balance de una cuenta de banco \n3: Depositar dinero a una cuenta de banco \n4: Retirar dinero de una cuenta de banco \n5: Mostrar todas las cuentas de banco \n6: Ver historial de transaccion de una cuenta de banco\n")
        user_opcion = str(input("Seleccione la opción que desee: "))

        if user_opcion == "1":
            crear_cuenta()
            print("Crear una cuenta")
        elif user_opcion == "2":
            print("Ver el balance de una cuenta")
            ver_cuenta_balance()
        elif user_opcion == "3":
            print("Depositar dinero a una cuenta")
            depositar_dinero()
        elif user_opcion == "4":
            print("Retirar dinero de una cuenta")
            retirar_dinero()
        elif user_opcion == "5":
            print("Mostrar las cuentas creadas hasta ahora")
            mostrar_cuentas()
        elif user_opcion == "6":
            print("Ver el historial de transacciones de una cuenta")
            ver_cuenta_historial()
        else:
            print("La opción que seleccionó es no existe o es inválida")
            PatitoBank.menu_opcion()

    def volver_menu(decision):
        if decision == "Si" or "SI" or "no":
            PatitoBank.menu_opcion()
        elif decision == "No" or "NO" or "no":
            print("x")
            # regresar a esa misma opcion
        else:
            print("Disculpe, la respuesta que colocó es inválida")
            PatitoBank.volver_menu()


### ---- SET UP
PatitoBank.bienvenida(1)
PatitoBank.menu_opcion()
