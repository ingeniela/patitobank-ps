### ---- BACKEND: que todo funcione
import random
from sql_file import Cuenta, Session, Engine

# SQL ALCHEMY
local_session = Session(bind=Engine)
# database

# opciones que podria escoger el usuario
def crear_cuenta():
    # A // Crear la cuenta: Nombre del titular
    titular_input = str(input("Coloque el nombre del titular: "))

    # B// Curp
    curp_input = str(input("Coloque el CURP: "))

    # C // Generar numero de cuenta
    number_random = int(random.randint(1000000000, 9999999999))
    nueva_cuenta = Cuenta(titular=titular_input, curp=curp_input, numCuenta=number_random)
    local_session.add(nueva_cuenta)
    local_session.commit()

    # D // Mostrar datos de la cuenta creada
    print("\n¡Cuenta creada con éxito!\n")
    print(nueva_cuenta)
    print("Por favor guarde estos datos en un lugar seguro.")

    # C // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 2
def ver_cuenta_balance(data):
    # A // ingresar a la cuenta


# Opcion 3
def depositar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = int(input("Coloque el numero de cuenta del Usuario: "))
    buscar_numCuenta = local_session.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
    print("Se ha encontrado la siguiente cuenta: ")
    print(buscar_numCuenta)

    # B // Ingresar datos del depósito (Cantidad / Fecha y Hora / Concepto)
    print("Realizar el monto, tan tan tan")

    # C // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 4
def retirar_dinero():
    # A // Ingresar numero de cuenta a retirar dinero
    titular = input("Nombre y Apellido del titular: ")

    # B // Ingresar datos del retiro (Cantidad / Fecha y Hora / Concepto)
    print("Retirar el monto, tan tan tan")

    # C // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 5
def mostrar_cuentas():
    # A // Ingresar contraseña especial
    contrasena = input("Ingrese la contraseña especial para acceder a las cuentas")

    # B // Mostrar todas las cuentas creadas
    cuentas = local_session.query(Cuenta).all()
    for cuenta in cuentas:
        print(cuenta)

    # C // Volver al menu de opciones
    pregunta = input("¿Desea volver al inicio?")
    PatitoBank.volver_menu(pregunta)

# Opcion 6
def ver_cuenta_historial():
    # A // Ingresar contraseña especial
    contrasena = "Ingrese la contraseña especial para mostrar el historial de una cuenta"

    # B // Ingresar numero de cuenta

    # C // Ingresar numero de cuenta

    # D // Volver al menu de opciones
    PatitoBank.volver_menu()


### ---- FRONTEND: Que todo se vea bonito
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
