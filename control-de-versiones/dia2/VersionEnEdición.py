### ---- BACKEND: que todo funcione
import random

# database
# cuenta de banco
class cuenta:
    'Cuentas de banco'
    cuentas_creadas = 0
    
    def __init__(self):
        print("( Hasta ahora se han creado", cuenta.cuentas_creadas, "cuentas) ")
        
        self.codigo = cuenta.cuentas_creadas
        self.titular = input("Titular de la cuenta: ")
        self.curp = input("CURP del titular: ")
        self.numCuenta = int(random.randint(1000000000, 9999999999))
        self.balance = 0
        
        cuenta.cuentas_creadas +=1
        
    def balanceCuenta(self):
        self.balance = int(input("Balance: "))
        self.transacciones = 0
    
    def depositarCuenta(self):
        self.tipo = "Depósito"
        self.cantidad = int(input("Dinero a depositar: "))
        self.fecha = input("Fecha de pago: ")
        self.concepto = input("Concepto del depósito: ")
        
        self.balance+=self.cantidad
        self.transacciones+=1
    
    def retirarCuenta(self):
        self.tipo = "Retiro"
        self.cantidad = int(input("Dinero a retirar: "))
        self.fecha = input("Fecha de pago: ")
        self.concepto = input("Concepto del retiro: ")
        
        self.balance-=self.cantidad
        self.transacciones+=1
        
    def mostrarData(self):  
        print("Datos de la cuenta: \n- Titular:", self.titular, " \n- Curp:", self.curp, " \n- Número de Cuenta:", self.numCuenta, " \n- Balance: $", self.balance, "\n")

    def mostrarCuentas(self):  
        print("(", self.codigo, "). Titular:", self.titular, ". Curp:", self.curp, ". Número de Cuenta:", self.numCuenta, ". Balance: $", self.balance, ". Transacciones realizadas: ", self.transacciones)
    
    def historialTransacciones(self):  
        print("(", self.transacciones, ") / Cantidad: ", self.cantidad, "/ Fecha: ", self.fecha, "/ Concepto: ", self.concepto)

# checkers de información para evitar errores en el input del usuario
class check:
    # se trabajará a profundidad en los checkers en otro día, ya que en este (Dia 2) se va a enfocar en que el programa funcione en sí

    def titular(input):
        titular2check = input
        # regex formula para verificar que tenga SOLO letras, no numeros ni simbolos
    def curp(input):
        curp2check = input
        # regex formula para verificar que tenga letras Y numeros, no simbolos
        # len(curp) para verificar que sean 18 caracters, no más ni menos de 18
    def numCuenta(input):
        numCuenta2check = input
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
            check.admin_contrasena()
        elif contrasena == respuesta:
            acceso = True
 
# opciones que podria escoger el usuario  
class opcion:
    # Opcion 1
    # Opcion 1
    def crear_cuenta(cuenta_code):
        # A // Crear la cuenta: Nombre del titular, B// Curp C// Generar numero de cuenta
        print("\nPara crear una cuenta, por favor, coloque los datos que se le piden.")
        cuenta_code = cuenta()
        
        # D // Mostrar datos de la cuenta creada
        print("\n¡Cuenta creada con éxito!\n")
        cuenta_code.mostrarData()
        print("Por favor guarde estos datos en un lugar seguro.")

        # C // Volver al menu de opciones
        pregunta = input("¿Desea volver al inicio?")
        PatitoBank.volver_menu(pregunta)
    # Opcion 2
    def ver_cuenta_balance():
        # A // ingresar a la cuenta
        data_cuenta1.mostrarData()
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
        cuentas_creadas = "Cuentas creadas"
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
        
### ---- FRONTEND: Que todo se vea bonito
class PatitoBank:
    def bienvenida():
        print("¡Sea bienvenido a Patito Bank!\n")
    
    def menu_opcion():
        print("1: Crear una cuenta \n2: Ver el balance de una cuenta de banco \n3: Depositar dinero a una cuenta de banco \n4: Retirar dinero de una cuenta de banco \n5: Mostrar todas las cuentas de banco \n6: Ver historial de transaccion de una cuenta de banco\n")
        user_opcion = str(input("Seleccione la opción que desee: "))
        
        if user_opcion == "1":
            print("Crear una cuenta")
            if cuenta.cuentas_creadas == 0:
                data_cuenta1 = ""
                opcion.crear_cuenta(data_cuenta1)
            elif cuenta.cuentas_creadas == 1:
                data_cuenta2 = ""
                opcion.crear_cuenta(data_cuenta2)
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
PatitoBank.bienvenida()
PatitoBank.menu_opcion()
