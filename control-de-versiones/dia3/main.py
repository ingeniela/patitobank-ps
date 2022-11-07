import random
from sql_file import *

## TAREAS (dejé otras en el archivo con el nombre de SG):
# Colocar los checkers, que funcionen bien los nombres, curp, cuando se hace input un numero de cuenta y asi
# Que hacer en caso de que el numero de cuenta sea incorrecto/no exista?
# Mejorar el Output para que se vea bonito todo

### ------------ BACKEND: que todo funcione ###

### SQL: Conectar variable con las bases de datos
# Base de datos de cuentas
local_cuentas = database_cuentas(bind=engine_cuentas)
# Base de datos de transacciones
local_transacciones = database_transacciones(bind=engine_transacciones)

### --- FUNCIONES SQL
class SQLFuncion:
    def añadir(tipo, variable):
        if tipo == "cuenta":
            local_cuentas.add(variable)
            local_cuentas.commit()
        elif tipo == "transaccion":
            local_transacciones.add(variable)
            local_transacciones.commit()

### --- OPCIONES DE SELECCION
# Opcion 1: Crear una cuenta
def crear_cuenta():
    print("Crear una cuenta nueva")
    ## A // Crear la cuenta: Nombre del titular
    titular_input = str(input("Coloque el nombre del titular: "))

    ## B// Curp: Ingresar Clave Unica de Registro Poblacional
    curp_input = str(input("Coloque el CURP: "))

    ## C // Generar Numero de cuenta de 10 dígitos
    nuevo_NumCuenta = int(random.randint(1000000000, 9999999999))
    nueva_cuenta = Cuenta(titular=titular_input, curp=curp_input, numCuenta=nuevo_NumCuenta)
    nuevo_balance = Transaccion(numCuenta=nuevo_NumCuenta, balance=0, tipo="Cuenta creada")
    # Agregar a la base de datos
    SQLFuncion.añadir("cuenta", nueva_cuenta)
    SQLFuncion.añadir("transaccion", nuevo_balance)

    ## D // Mostrar datos de la cuenta creada
    print("\n¡Cuenta creada con éxito!\n", nueva_cuenta, "Por favor guarde estos datos en un lugar seguro.")

    ## E // Volver al menu de opciones
    PatitoBank.volver("1")

# Opcion 2: Ver el balance de una cuenta
def ver_cuenta_balance():
    ## A // Ingresar numero de cuenta para ver el balance
    numCuenta_input = int(input("Coloque el numero de cuenta del usuario: "))
    # mostrar datos de la cuenta
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
    print("El número de cuenta colocado está asociado a esta cuenta:: ", buscar_numCuenta)

    ## B // Mostrar balance de la cuenta
    cuenta_balance = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    print("El balance es cuenta es: $", cuenta_balance.soloBalance())

    ## C // Pedir préstamo
    posible_prestamo = int(cuenta_balance.soloBalance() * 0.8) # Solo se puede prestar hasta el 80% del balance de la cuenta
    print("Puede pedir hasta $", posible_prestamo, "como prestamo")
    # SG: mostrar interes si paga en 30 dias, 60 dias y 90 dias
    prestamo = input("\n¿Desea pedir un préstamo? (Si o No): ")

    if prestamo == "Si":
        user_input = int(input("¿Cuanto dinero necesita?: $"))

        # SG: if user_input > posible_prestamo: (agregar que no se pueda hacer)

        # Seleccionar fecha a pagar
        ano = int(input('¿En que año va a pagar? (Coloque un numero): '))
        mes = int(input('¿En que mes lo va a pagar? (Coloque un numero): '))
        dia = int(input('¿En que dia lo va a pagar? (Coloque un numero): '))
        # Tomar la fecha actual
        fecha_input = datetime(ano, mes, dia, 12, 0, 0)
        fecha_ahora = datetime.now()
        # Calcular fecha
        diferencia = datetime.now() - fecha_input
        segundos_restantes = diferencia.total_seconds()
        dias_restantes = int(segundos_restantes / 86400) * -1

        # SG: if dias_restantes > 200: (agregar que no se pueda hacer)

        # Tasa de interes segun el monto
        interesXmonto = 0.12  # 12% de interes por el monto que se realice
        # Tasa de Interés según los dias faltantes
        interesXfecha = (dias_restantes * 0.0026)  # 8% de interes por cada 30 dias

        # Interés completo
        interesXprestamo = (interesXmonto + interesXfecha)  # cuanto porcentaje es en total
        dinero_total = int((user_input * interesXprestamo) + user_input)

        # Print al usuario
        print("/nSe le va a realizar un prestamo de: ", user_input, ". Debe pagarlo en", dias_restantes, "dias. \n Interes a pagar en total: ", interesXprestamo)
        print("Es decir, que debe pagar: $", dinero_total, "en total")

        # Pregunta:
        transaccion = input("/n ¿Desea pedir este préstamo? (Si o No): ")

        if transaccion == "Si":
            transacciones = local_transacciones.query(Transaccion).filter(
                Transaccion.numCuenta == numCuenta_input).order_by(
                Transaccion.id.desc()).first()
            nuevo_balance = transacciones.soloBalance() + dinero_total
            nueva_transaccion = Transaccion(numCuenta=numCuenta_input, balance=nuevo_balance, tipo="Péstamo",
                                            monto=dinero_total,
                                            concepto="Prestamo realizado por PatitoBank")
            # Añadir a la base de datos
            SQLFuncion.añadir("transaccion", nueva_transaccion)

            print("Prestamo realizado con éxito. Información: ", nueva_transaccion.dataTransaccion())
        elif transaccion == "No":
            print("Ha cancelado este prestamo, por lo que no se realizará")
            pass
    elif prestamo == "No":
        pass

    ## D // Volver al menu de opciones
    PatitoBank.volver("2")

# Opcion 3
def depositar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = int(input("Coloque el numero de cuenta del usuario: "))
    # mostrar datos de la cuenta
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
    print("El número de cuenta colocado está asociado a esta cuenta:: ", buscar_numCuenta)
    # SG: seleccionar si el usuario es correcto o no

    # B // Ingresar datos del depósito (Monto / Fecha y Hora / Concepto)
    monto_input = int(input("¿Cuanto dinero desea depositar?: $"))
    fecha_input = print("La fecha será colocada como: ", datetime.now())
    # SG: seleccionar si se quiere o no la fecha así
    concepto_input = str(input("Coloque el concepto de este deposito: "))

    # Agregar balance nuevo
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    nuevo_balance = transacciones.soloBalance() + monto_input
    nueva_transaccion = Transaccion(numCuenta=numCuenta_input,
                                    balance=nuevo_balance,
                                    tipo="Deposito",
                                    monto=monto_input,
                                    concepto=concepto_input)
    print("Transaccion realizada con éxito. Información:", nueva_transaccion.dataTransaccion())
    # Añadir a la base de datos
    SQLFuncion.añadir("transaccion", nueva_transaccion)

    # C // Volver al menu de opciones
    PatitoBank.volver("3")

# Opcion 4
def retirar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = int(input("Coloque el numero de cuenta del usuario: "))
    # mostrar datos de la cuenta
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
    print("El número de cuenta colocado está asociado a esta cuenta:: ", buscar_numCuenta)
    # SG: seleccionar si el usuario es correcto o no

    # B // Ingresar datos del depósito (Monto / Fecha y Hora / Concepto)
    monto_input = int(input("¿Cuanto dinero desea retirar?: $"))
    fecha_input = print("La fecha será colocada como: ", datetime.now())
    # SG: seleccionar si se quiere o no la fecha así
    concepto_input = str(input("Coloque el concepto de este retiro: "))

    # Agregar balance nuevo
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    nuevo_balance = transacciones.soloBalance() + monto_input
    nueva_transaccion = Transaccion(numCuenta=numCuenta_input,
                                    balance=nuevo_balance,
                                    tipo="Retiro",
                                    monto=monto_input,
                                    concepto=concepto_input)
    print("Retiro realizado con éxito. Información:", nueva_transaccion.dataTransaccion())
    # Añadir a la base de datos
    SQLFuncion.añadir("transaccion", nueva_transaccion)

    # C // Volver al menu de opciones
    PatitoBank.volver("4")

# Opcion 5
def mostrar_cuentas():
    # A // Ingresar contraseña especial
    modo_admin = input("Ingrese la contraseña especial para acceder a este espacio: ")

    # B // Mostrar todas las cuentas creadas
    print("\n Cuentas creadas hasta ahora")
    cuentas = local_cuentas.query(Cuenta).all()
    for cuenta in cuentas:
        print(cuenta.dataBasico())

    # C // Opciones:
    opciones_avanzadas = int(input("\nSi desea acceder a las opciones avanzadas, coloque 1. Sino, coloque 2."))

    if opciones_avanzadas == 1:
        print(
            "1. Eliminar todas las cuentas de banco creadas hasta ahora. \n 2. Eliminar todas las transacciones creadas hasta ahora")
        seleccionar = int(input("¿Que desea hacer?"))

        if seleccionar == 1:
            try:
                eliminar_cuentas = local_cuentas.query(Cuenta).delete()
                local_cuentas.commit()
                print("Se han eliminado todas las cuentas de la base de datos")
                pass
            except:
                local_cuentas.rollback()
                pass
        elif seleccionar == 2:
            try:
                eliminar_transacciones = local_transacciones.query(Transaccion).delete()
                local_transacciones.commit()
                print("Se han eliminado todas las transacciones de la base de datos")
                pass
            except:
                local_transacciones.rollback()
                pass

    ## C // Volver al menu de opciones
    PatitoBank.volver("5")

# Opcion 6
def ver_cuenta_historial():
    # A // Ingresar contraseña especial
    modo_admin = input("Ingrese la contraseña especial para acceder a este espacio: ")

    # B // Ingresar numero de cuenta
    numCuenta_input = int(input("Coloque el numero de cuenta: "))
    print("Se ha entcontrado la siguiente cuenta")
    # buscar transacciones de la cuenta
    buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
    print(buscar_numCuenta)

    # C // Ver historial numero de cuenta
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).all()
    for transaccione in transacciones:
        print(transaccione)

    ## D // Volver al menu de opciones
    PatitoBank.volver("6")

### ------------ FrontEnd: que todo se vea bonito ###
class PatitoBank:
    def bienvenida(self):
        print("¡Sea bienvenido a PatitoBank!\n")

    def menu_opcion():
        print("\nMenu de opciones:")
        print(
            "1: Crear una cuenta de banco \n2: Ver el balance de una cuenta de banco \n3: Depositar dinero a una cuenta de banco \n4: Retirar dinero de una cuenta de banco \n5: Mostrar todas las cuentas de banco \n6: Ver historial de transaccion de una cuenta de banco\n")
        opcion = str(input("Seleccione la opción que desee: "))

        if opcion == "1":
            print("\n")
            crear_cuenta()
        elif opcion == "2":
            print("\n")
            ver_cuenta_balance()
        elif opcion == "3":
            print("\n")
            depositar_dinero()
        elif opcion == "4":
            print("\n")
            retirar_dinero()
        elif opcion == "5":
            print("\n")
            mostrar_cuentas()
        elif opcion == "6":
            print("\n")
            ver_cuenta_historial()
        else:
            print("La opción que seleccionó es no existe o es inválida")
            PatitoBank.menu_opcion()

    def volver_opcion(opcion):
        if opcion == "1":
            print("Será redirigido a crear una Cuenta")
            crear_cuenta()
        elif opcion == "2":
            print("Será redirigido a ver el balance de una Cuenta Bancaria")
            ver_cuenta_balance()
        elif opcion == "3":
            print("Será redirigido a depositar dinero")
            depositar_dinero()
        elif opcion == "4":
            print("Será redirigido a retirar dinero")
            retirar_dinero()
        elif opcion == "5":
            print("Será redirigido a Mostrar cuentas")
            mostrar_cuentas()
        elif opcion == "6":
            print("Será redirigido a ver el historial de una cuenta")
            ver_cuenta_historial()
        else:
            print("La opción que seleccionó es no existe o es inválida")
            PatitoBank.menu_opcion()

    def volver_menu():
        PatitoBank.menu_opcion()

    def volver(opcion):
        pregunta = input("\n¿Desea volver al menu de opciones? (Si o No): ")

        if pregunta == "Si":
            PatitoBank.volver_menu()
        elif pregunta == "No":
            PatitoBank.volver_opcion(opcion)

### ------------ SetUp: que el usuario lo pueda utilizar ###
PatitoBank.bienvenida(1)
PatitoBank.menu_opcion()