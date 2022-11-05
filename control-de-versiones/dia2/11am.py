# BACKEND: que todo funcione
import random

# checkers de información para evitar errores en el input del usuario
class check:
    def titular():
        titular = user_input
        # regex formula para verificar que tenga SOLO letras, no numeros ni simbolos
    def curp():
        curp = user_input
        # regex formula para verificar que tenga letras Y numeros, no simbolos
        # len(curp) para verificar que sean 18 caracters, no más ni menos de 18
    def numCuenta(input):
        numCuenta = input
        print("El numero de Cuenta ya ha sido chequeado")
        # regex formula para verificar que solo sean numeros
        # len(numCuenta) para verificar que sean solo 10 numeros, ni mas ni menos
    def transaccion():
        print("X")
        # cantidad de dinero solo en numeros, limite de transacicon
        # fecha y hora correctas
        # concepto de no más de 25 caracteres
    def admin_contrasena():
        acceso = False
    
        contrasena = input("Ingrese la contraseña especial")
        respuesta = str("administradorPato")
    
        if contrasena != respuesta:
            acceso = False
            print("La contraseña que ha ingresado es incorrecta")
            admin_contrasena()
        elif contrasena == respuesta:
            acceso = True
 
# opciones que podria escoger el usuario  
class opcion:
    # Opcion 1
    def crear_cuenta():
        # A // Ingresar a la cuenta
        titular = input("Nombre y Apellido del titular: ")
        curp = input("Clave Unica de Registro de la Poblacion: ")
        
        # B // Acceder al balance de la cuenta
        numCuenta = str(random.randint(1000000000, 9999999999))
        print("Su numero de cuenta es: ", numCuenta, ". Por favor, guardela en un lugar seguro")
        PatitoBank.volver_menu()
    # Opcion 2
    def ver_cuenta_balance():
        # A // ingresar a la cuenta
        user_input = input("Numero de Cuenta: ")
        check_numCuenta(user_input)
        ## acceder directamente  a la base de datos y mostrar la cuenta
         
        # B // acceder al balance de la cuenta
        ver_balance = print("Balance de una cuenta")
        
        # C // Volver al menu de opciones
        PatitoBank.volver_menu()
    # Opcion 3
    def depositar_dinero():
        # A // Ingresar numero de cuenta a depositar dinero
        titular = input("Nombre y Apellido del titular: ")
        
        # B // Ingresar datos del depósito (Cantidad / Fecha y Hora / Concepto)
        print("Realizar el monto, tan tan tan")
        # C // Volver al menu de opciones
        PatitoBank.volver_menu()
    # Opcion 4
    def retirar_dinero():
        # A // Ingresar numero de cuenta a retirar dinero
        titular = input("Nombre y Apellido del titular: ")
        
        # B // Ingresar datos del retiro (Cantidad / Fecha y Hora / Concepto)
        print("Retirar el monto, tan tan tan")
        # C // Volver al menu de opciones
        PatitoBank.volver_menu()
    # Opcion 5
    def mostrar_cuentas():
        # A // Ingresar contraseña especial
        contrasena = "Ingrese la contraseña especial para acceder a las cuentas"
        
        # B // Mostrar todas las cuentas creadas
        cuentas_creadas = "cuentas creadas"
        # C // Volver al menu de opciones
        PatitoBank.volver_menu()
    # Opcion 6
    def ver_cuenta_historial():
        # A // Ingresar contraseña especial
        contrasena = "Ingrese la contraseña especial para mostrar el historial de una cuenta"
        
        # B // Ingresar numero de cuenta
        
        # C // Ingresar numero de cuenta
        
        # D // Volver al menu de opciones
        PatitoBank.volver_menu()
        
# FRONTEND: Que todo se vea bonito
class PatitoBank:
    def bienvenida():
        print("¡Sea bienvenido a Patito Bank!\n")
    
    def menu_opcion():
        print("1: Crear una cuenta \n2: Ver el balance de una cuenta de banco \n3: Depositar dinero a una cuenta de banco \n4: Retirar dinero de una cuenta de banco \n5: Mostrar todas las cuentas de banco \n6: Ver historial de transaccion de una cuenta de banco\n")
        user_opcion = str(input("Seleccione la opción que desee"))
        
        if user_opcion == "1":
            print("Crear una cuenta")
            opcion.crear_cuenta()
        elif user_opcion == "2":
            print("Ver el balance de una cuenta")
            opcion.ver_cuenta_balance()
        elif user_opcion == "3":
            print("Depositar dinero a una cuenta")
            opcion.depositar_dinero()
        elif user_opcion == "4":
            print("Retirar dinero de una cuenta")
            opcion.retirar_dinero()
        elif user_opcion == "5":
            print("Mostrar las cuentas creadas hasta ahora")
            opcion.mostrar_cuentas()
        elif user_opcion == "6":
            print("Ver el historial de transacciones de una cuenta")
            opcion.ver_cuenta_historial()
        else:
            print("La opción que seleccionó es no existe o es inválida")
            PatitoBank.menu_opcion()
        
    def volver_menu():
        decision = input("¿Desea volver al menu de inicio?")
        
        if decision == "Si" or "SI" or "no":
            PatitoBank.menu_opcion()
        elif decision == "No" or "NO" or "no":
            print("x")
            # regresar a esa misma opcion
        else:
            print("Disculpe, la respuesta que colocó es inválida")
            PatitoBank.volver_menu()


# SET UP
PatitoBank.bienvenida()
PatitoBank.menu_opcion()
