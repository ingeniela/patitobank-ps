from SQLArchivo import *
from datetime import datetime
import random
import re


### Cambios realizados:
##PRINCIPALES

##SECUNDARIOS

### TAREAS SG:
## PRINCIPAL
# OP2: Mostrar fecha actual y hacer calculos del prestamo +30 dias a partir de hoy en datetime.now()
# Aceptar responder con "Si" "si" y "SI" (lo mismo con NO, no, No)

## SECUNDARIO
# Corregir "redirigido a" o qué, elimina eso
# Corregir Output colocado (agregar Mayusculas, acentos y \n donde sea necesario)
# Corregir todos los comentarios, agregarle comentarios a las funciones para explicar para qué sirven

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

### --- FUNCIOENS CHECK
class Check:
    def titular(input, opcion):
        titular_input = input
        nombre_apellido = "([a-zñáéíóúA-ZÑÁÉÍÓÚ]{2,}\s[a-zñáéíóúA-ZÑÁÉÍÓÚ]{1,}'?-?[a-zñáéíóúA-ZÑÁÉÍÓÚ]{2,}\s?([a-zñáéíóúA-ZÑÁÉÍÓÚ]{1,})?)"

        if (re.search(nombre_apellido, titular_input)):
            pass
        else:
            print("Por favor, coloque su nombre y su apellido, no se aceptan números ni símbolos. \n Coloque sus datos una vez más \n")
            PatitoBank.volver_opcion(opcion)
    def curp(input, opcion):
        letrasMayus_numeros = "[A-Z]+[0-9]"
        titular_input = input
        largo = len(titular_input)

        if largo != 18:
            print("El CURP debe tener 18 caracteres en total\n Por favor, verifique su respuesta e intente otra vez")
            PatitoBank.volver_opcion(opcion)
        else:
            if (re.search(letrasMayus_numeros, titular_input)):
                pass
            else:
                print("Recuerde que el CURP contiene letras en Mayusculas y numeros\n Por favor, verifique su respuesta e intente otra vez")
                PatitoBank.volver_opcion(opcion)
    def existe_curp(curp_input, opcion):
        buscar_curp = local_cuentas.query(Cuenta).filter(Cuenta.curp == curp_input).first()
        if buscar_curp == None:
            pass
        elif buscar_curp != None:
            print("El CURP que usted colocó ya esta asociado a una cuenta")
            PatitoBank.volver_opcion(opcion)
    def numCuenta(input, opcion):
        solo_numeros = "[0-9]"
        numCuenta_input = input
        largo = len(numCuenta_input)

        if largo != 10:
            print("El Número de Cuenta debe contener 10 numeros\n Por favor, verifique su respuesta e intente otra vez")
            PatitoBank.volver_opcion(opcion)
        else:
            if (re.search(solo_numeros, numCuenta_input)) and largo == 10:
                pass
            else:
                print("Recuerde que el Numero de cuenta solo contiene numeros\n Por favor, verifique su respuesta e intente otra vez")
                PatitoBank.volver_opcion(opcion)
    def existe_numCuenta(numCuenta_input, opcion):
        buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
        if buscar_numCuenta == None:
            print("El numero de cuenta que usted colocó no existe")
            PatitoBank.volver_opcion(opcion)
        elif buscar_numCuenta != None:
            print("El número de cuenta colocado está asociado a esta cuenta:: ", buscar_numCuenta)
    def transaccion_cuentaCreada(input):
        numCuenta_input = input
        user_to_delete = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input, Transaccion.tipo == "Cuenta Creada").first()
        if user_to_delete != None:
            local_transacciones.delete(user_to_delete)
            local_transacciones.commit()
        elif user_to_delete == None:
            pass

### --- OTRAS FUNCIONES
def pedir_prestamo(monto_input, numCuenta_input):
    # Seleccionar fecha a pagar
    ano = int(input('¿En que año va a pagar? (Coloque un numero): '))
    mes = int(input('¿En que mes lo va a pagar? (Coloque un numero): '))
    dia = int(input('¿En que dia lo va a pagar? (Coloque un numero): '))
    # Tomar la fecha actual
    fecha_input = datetime(ano, mes, dia, 12, 0, 0)
    fecha_ahora = datetime.now()

    # Calcular fecha
    diferencia = fecha_ahora - fecha_input
    segundos_restantes = diferencia.total_seconds()
    dias_restantes = int(segundos_restantes / 86400) * -1

    if dias_restantes > 200:
        print("Tiene más de 200 dias para realizar este pago")

    # Tasa de interes segun el monto
    interesXmonto = 0.5 # 10% de interes por el monto que se realice
    # Tasa de Interés según los dias faltantes
    interesXfecha = (dias_restantes * 0.0026)  # 8% de interes por cada 30 dias

    # Interés completo
    interesXprestamo = (interesXmonto + interesXfecha)  # cuanto porcentaje es en total
    dinero_total = int((monto_input * interesXprestamo) + monto_input)

    # Print al usuario
    print("\nSe le va a realizar un prestamo de: ", monto_input, ". Debe pagarlo en", dias_restantes,
          "dias. \n Interes a pagar en total: ", interesXprestamo)
    print("Es decir, que debe pagar: $", dinero_total, "en total")

    # Pregunta:
    transaccion = input("\n ¿Desea pedir este préstamo? (Si o No): ")

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
def calcular_prestamo(monto_input):
    interesFecha = 0.08 #8% por 30 dias
    interesMonto = 0.05 #5% por el prestamo que se pida
    interesX30dias = int((interesFecha + interesMonto)*100)
    interesX60dias = int((interesFecha * 2 + interesMonto)*100)
    interesX90dias = int((interesFecha * 3 + interesMonto)*100)

    print("Si lo paga en: / 30 dias: %", interesX30dias , "de interes / 60 días: %", interesX60dias, "de interes / 90 dias: %", interesX90dias, "de interes")
def modo_admin(input, opcion):
    contrasena = input
    respuesta = "PatosPatos"

    if contrasena == respuesta:
        pass
    else:
        print("Contraseña de Administrador incorrecta")
        PatitoBank.volver_opcion(opcion)

### --- OPCIONES DE SELECCION
# Opcion 1: Crear una cuenta
def crear_cuenta():
    print("Crear una cuenta nueva")
    ## A // Crear la cuenta: Nombre del titular
    titular_input = str(input("Coloque el nombre del titular: "))
    Check.titular(titular_input, "1")

    ## B// Curp: Ingresar Clave Unica de Registro Poblacional
    curp_input = str(input("Coloque el CURP: "))
    Check.curp(curp_input, "1")
    Check.existe_curp(curp_input, "1")

    ## C // Generar Numero de cuenta de 10 dígitos
    generar_numCuenta = int(random.randint(1000000000, 9999999999))
    nuevo_numCuenta = str(generar_numCuenta)
    fecha_actual = datetime.now()

    nueva_cuenta = Cuenta(titular=titular_input, curp=curp_input, numCuenta=nuevo_numCuenta, fecha_creacion=fecha_actual)
    nuevo_balance = Transaccion(numCuenta=nuevo_numCuenta, balance=0, tipo="Cuenta Creada", concepto="Esta cuenta ha sido creada recientemente y no tiene ninguna transacción", fecha=fecha_actual)

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
    numCuenta_input = str(input("Coloque el numero de cuenta del usuario: "))
    Check.numCuenta(numCuenta_input, "2") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "2") # Si existe la cuenta

    ## B // Mostrar balance de la cuenta
    cuenta_balance = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()

    if cuenta_balance.soloBalance() == 0:
        print("Esta cuenta no tiene dinero")
    elif cuenta_balance.soloBalance() > 1:
        print("El balance es cuenta es: $", cuenta_balance.soloBalance())

        ## C // Pedir préstamo
        posible_prestamo = int(cuenta_balance.soloBalance() * 0.8) # Solo se puede prestar hasta el 80% del balance de la cuenta
        print("Puede pedir hasta $", posible_prestamo, "como prestamo")
        calcular_prestamo(posible_prestamo)
        prestamo = input("\n¿Desea pedir un préstamo? (Si o No): ")

        if prestamo == "Si":
            monto_input = int(input("¿Cuanto dinero necesita?: $"))
            if monto_input > posible_prestamo:
                print("Disculpe, el monto que necesita es más del que le podemos prestar")
                pass
            elif monto_input < posible_prestamo:
                pedir_prestamo(monto_input, numCuenta_input)
        elif prestamo == "No":
            pass

    ## D // Volver al menu de opciones
    PatitoBank.volver("2")

# Opcion 3
def depositar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = str(input("Coloque el numero de cuenta del usuario: "))
    Check.numCuenta(numCuenta_input, "3") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "3") # Si existe la cuenta

    # ¿Desea depositar dinero a esa cuenta?
    esta_cuenta = input("¿Desea depositar dinero a esta cuenta? (Si o No): ")

    if esta_cuenta == "Si":
        pass
    elif esta_cuenta == "No":
        PatitoBank.volver_opcion("3")

    # B // Ingresar datos del depósito (Monto / Fecha y Hora / Concepto)
    monto_input = int(input("¿Cuanto dinero desea depositar?: $"))
    fecha_input = print("La fecha será colocada como: ", datetime.now())
    # SG: seleccionar si se quiere o no la fecha así
    concepto_input = str(input("Coloque el concepto de este deposito: "))

    # Agregar balance nuevo
    fecha_actual = datetime.now()
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    nuevo_balance = transacciones.soloBalance() + monto_input
    nueva_transaccion = Transaccion(numCuenta=numCuenta_input,
                                    balance=nuevo_balance,
                                    tipo="Deposito",
                                    monto=monto_input,
                                    concepto=concepto_input,
                                    fecha= fecha_actual)
    print("Transaccion realizada con éxito. Información:", nueva_transaccion.dataTransaccion())
    # Quitar de la base de datos la primera transaccion (Cuenta Creada)
    Check.transaccion_cuentaCreada(numCuenta_input)
    # Añadir a la base de datos
    SQLFuncion.añadir("transaccion", nueva_transaccion)

    # C // Volver al menu de opciones
    PatitoBank.volver("3")

# Opcion 4
def retirar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = str(input("Coloque el numero de cuenta del usuario: "))
    Check.numCuenta(numCuenta_input, "3") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "3") # Si existe la cuenta

    # ¿Desea depositar dinero a esa cuenta?
    esta_cuenta = input("¿Desea depositar dinero a esta cuenta? (Si o No): ")

    if esta_cuenta == "Si":
        pass
    elif esta_cuenta == "No":
        PatitoBank.volver_opcion("4")
    # B // Ingresar datos del depósito (Monto / Fecha y Hora / Concepto)
    monto_input = int(input("¿Cuanto dinero desea retirar?: $"))
    fecha_input = print("La fecha será colocada como: ", datetime.now())
    # SG: seleccionar si se quiere o no la fecha así
    concepto_input = str(input("Coloque el concepto de este retiro: "))

    # Agregar balance nuevo
    fecha_actual = datetime.now()
    transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()
    nuevo_balance = transacciones.soloBalance() - monto_input
    nueva_transaccion = Transaccion(numCuenta=numCuenta_input,
                                    balance=nuevo_balance,
                                    tipo="Retiro",
                                    monto=monto_input,
                                    concepto=concepto_input,
                                    fecha= fecha_actual)
    print("Retiro realizada con éxito. Información:", nueva_transaccion.dataTransaccion())
    # Quitar de la base de datos la primera transaccion (Cuenta Creada)
    Check.transaccion_cuentaCreada(numCuenta_input)
    # Añadir a la base de datos
    SQLFuncion.añadir("transaccion", nueva_transaccion)

    # C // Volver al menu de opciones
    PatitoBank.volver("4")

# Opcion 5
def mostrar_cuentas():
    # A // Ingresar contraseña especial
    contrasena = input("Ingrese la contraseña especial para acceder a este espacio: ")
    modo_admin(contrasena, "5")

    # B // Mostrar todas las cuentas creadas
    cantidad_cuentas = local_cuentas.query(Cuenta).count()
    if cantidad_cuentas == 0:
        print("No hay cuentas en la base de datos")
    elif cantidad_cuentas == 1:
        print("\nCuenta creada hasta ahora")
        cuentas = local_cuentas.query(Cuenta).all()
        print(cuentas)

        print("Se han creado", cantidad_cuentas, "cuenta hasta ahora")
    elif cantidad_cuentas != 0:
        print("\nCuentas creadas hasta ahora")
        cuentas = local_cuentas.query(Cuenta).all()
        for cuenta in cuentas:
            print(cuenta.data_basico())

        print("Se han creado", cantidad_cuentas, "cuentas hasta ahora")

        # C // Opciones:
        opciones_avanzadas = str(input("\n¿Desea entrar a las opciones avanzadas? (Si o No): "))

        if opciones_avanzadas == "Si":
            print("1. Eliminar todas las cuentas de banco creadas hasta ahora. \n2. Eliminar todas las transacciones creadas hasta ahora")
            seleccionar = int(input("¿Que desea hacer?"))

            if seleccionar == 1:
                try:
                    eliminar_cuentas = local_cuentas.query(Cuenta).delete()
                    local_cuentas.commit()
                    print("Se han eliminado todas las cuentas de la base de datos")
                    pass
                except:
                    local_cuentas.rollback()
                    print("No se han encontrado cuentas en la base de datos")
                    pass
            elif seleccionar == 2:
                try:
                    eliminar_transacciones = local_transacciones.query(Transaccion).delete()
                    local_transacciones.commit()
                    print("Se han eliminado todas las transacciones de la base de datos")
                    pass
                except:
                    local_transacciones.rollback()
                    print("No se han encontrado transacciones en la base de datos")
                    pass

            PatitoBank.volver_opcion("5")
        elif opciones_avanzadas == "No":
            PatitoBank.volver_opcion("5")


    ## C // Volver al menu de opciones
    PatitoBank.volver("5")

# Opcion 6
def ver_cuenta_historial():
    # A // Ingresar contraseña especial
    contrasena = input("Ingrese la contraseña especial para acceder a este espacio: ")
    modo_admin(contrasena, "6")

    # B // Ingresar numero de cuenta revisar historial
    numCuenta_input = str(input("Coloque el numero de cuenta del usuario: "))
    Check.numCuenta(numCuenta_input, "6") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "6") # Si existe la cuenta

    # C // Ver historial numero de cuenta
    cantidad_transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).count()

    if cantidad_transacciones == 0:
        print("No hay cuentas en la base de datos")
    elif cantidad_transacciones == 1:
        print("\nTransaccion realizada hasta ahora")
        transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).all()
        print(transacciones)

        print("Se han hecho", cantidad_transacciones, "transaccion hasta ahora")
    elif cantidad_transacciones != 0:
        print("\nTransacciones realizadas hasta ahora")
        transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).all()
        for transaccione in transacciones:
            print(transaccione)

        print("Se han hecho", cantidad_transacciones, "transacciones hasta ahora")

    ## D // Volver al menu de opciones
    PatitoBank.volver("6")

### ------------ FrontEnd: que todo se vea bonito ###
class PatitoBank:
    def bienvenida(self):
        print("¡Sea bienvenido a PatitoBank!")

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
