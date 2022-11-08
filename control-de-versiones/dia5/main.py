from SQLArchivo import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from SQLArchivo_utils import database_exists

import random
import re


### Cambios realizados:
##PRINCIPALES
# Cambiar de lugar el print de OP3 y OP4 (colocar datos de esta transaccion)
# Agregar condicional por si no se ha creado las bases de datos, si= pass. no= crarlas
# Mejorar el output de pedir_prestamo() y algunos procesos
# Mejorar < > >= y <= de algunos numeros

##SECUNDARIOS
#REGEX utilizado en el curp, para que nada más acepte en el siguiente patrón LLLLNNNNNNLLLLLLXN. L= Cualquier letra de la A a la Z (mayusculars). N= Cualquier número del 0 al 9. X= Puede ser cualquier letra o Numero
# Mejorar el output de diversas opciones

### TAREAS SG:
## PRINCIPAL

## SECUNDARIO
# Deglosar el main en otros archivos para dejarlo t0do un poco más limpiecito
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
            PatitoBank.volver(opcion)
    def curp(input, opcion):
        letrasMayus_numeros = "([A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][A-Z][A-Z][A-Z][A-Z][A-Z][A-Z][A-Z+0-9][0-9])"
        titular_input = input
        largo = len(titular_input)

        if largo != 18:
            print("<<El CURP solo tiene 18 caracteres. Verifique su respuesta e intente otra vez>>\n")
            PatitoBank.volver(opcion)
        else:
            if (re.search(letrasMayus_numeros, titular_input)):
                pass
            else:
                print("<<El CURP tiene solo Letras mayusculas y Números en el siguiente patrón LLLLNNNNNNLLLLLLNN (Ejemplo: BAMD040423MDFXXNA0). \nVerifique su respuesta e intente otra vez>>")
                PatitoBank.volver(opcion)
    def existe_curp(curp_input, opcion):
        buscar_curp = local_cuentas.query(Cuenta).filter(Cuenta.curp == curp_input).first()
        if buscar_curp == None:
            pass
        elif buscar_curp != None:
            print("├ El CURP que usted colocó ya esta asociado a una cuenta")
            PatitoBank.volver_al_menu(opcion)
    def numCuenta(input, opcion):
        solo_numeros = "[0-9]"
        numCuenta_input = input
        largo = len(numCuenta_input)

        if largo != 10:
            print("<<El numero de cuenta solo tiene 10 números. Verifique su respuesta e intente otra vez>>\n")
            PatitoBank.volver(opcion)
        else:
            if (re.search(solo_numeros, numCuenta_input)) and largo == 10:
                pass
            else:
                print("<<El numero de cuenta solo tiene 10 números. Verifique su respuesta e intente otra vez>>\n")
                PatitoBank.volver(opcion)
    def existe_numCuenta(numCuenta_input, opcion):
        buscar_numCuenta = local_cuentas.query(Cuenta).filter(Cuenta.numCuenta == numCuenta_input).first()
        if buscar_numCuenta == None:
            print("├ El número de cuenta que usted colocó no existe")
            print("├ Se le redigirará al menú de opciones")
            PatitoBank.menu_opcion("1")
        elif buscar_numCuenta != None:
            print("├ El número de cuenta colocado está asociado a esta cuenta: ", buscar_numCuenta)
            pass
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
    ano = int(input("¿En que año va a pagar? (Coloque un numero): "))
    mes = int(input("¿En que mes lo va a pagar? (Coloque un numero): "))
    dia = int(input("¿En que dia lo va a pagar? (Coloque un numero): "))
    # Tomar la fecha actual
    fecha_input = datetime(ano, mes, dia, 12, 0, 0)
    fecha_ahora = datetime.now()

    # Calcular fecha
    diferencia = fecha_ahora - fecha_input
    segundos_restantes = diferencia.total_seconds()
    dias_restantes = int(segundos_restantes / 86400) * -1

    if dias_restantes >= 200:
        print("Tiene más de 200 dias para realizar este pago")

    # Tasa de interes segun el monto
    interesXmonto = 0.5 # 10% de interes por el monto que se realice
    # Tasa de Interés según los dias faltantes
    interesXfecha = (dias_restantes * 0.0026)  # 8% de interes por cada 30 dias

    # Interés completo
    interesXprestamo = (interesXmonto + interesXfecha)  # cuanto porcentaje es en total
    dinero_total = int((monto_input * interesXprestamo) + monto_input)

    # Print al usuario
    print("\nSe le va a realizar un prestamo de: $", monto_input, "Debe pagarlo en", dias_restantes, "dias.")
    print("\nInteres a pagar en total:", interesXprestamo*100, "% <<Es decir, que debe pagar: $ ", dinero_total, "en total>>")

    # Pregunta:
    transaccion = input("\n ¿Desea pedir este préstamo? (Si o No): ")

    if transaccion == "Si" or transaccion == "si" or transaccion == "SI":
        transacciones = local_transacciones.query(Transaccion).filter(
            Transaccion.numCuenta == numCuenta_input).order_by(
            Transaccion.id.desc()).first()
        nuevo_balance = transacciones.soloBalance() + dinero_total
        nueva_transaccion = Transaccion(numCuenta=numCuenta_input, balance=nuevo_balance, tipo="Péstamo",
                                        monto=dinero_total,
                                        concepto="Prestamo realizado por PatitoBank")
        # Añadir a la base de datos
        SQLFuncion.añadir("transaccion", nueva_transaccion)

        print("Préstamo realizado con éxito. \nDatos: ", nueva_transaccion.dataTransaccion())
        print("Recuerde pagarlo el", datetime(ano, mes, dia, 12, 0, 0))
    elif transaccion == "No" or transaccion == "no" or transaccion == "NO":
        print("Préstamo cancelado")
        pass
    else:
        pass
def calcular_prestamo(monto_input):
    interesFecha = 0.08 #8% por 30 dias
    interesMonto = 0.05 #5% por el prestamo que se pida
    interesX30dias = int((interesFecha + interesMonto)*100)
    interesX60dias = int((interesFecha * 2 + interesMonto)*100)
    interesX90dias = int((interesFecha * 3 + interesMonto)*100)

    fecha_actual = datetime.now()
    treintaDias = fecha_actual + relativedelta(months=1)
    sesentaDias = fecha_actual + relativedelta(months=2)
    noventaDias = fecha_actual + relativedelta(months=3)

    print("<<Si lo paga en 30 días: (", treintaDias.strftime("20%y-%m-%d"), ") es %", interesX30dias, "de interes", "| 60 dias: (", sesentaDias.strftime("20%y-%m-%d"), ") es %", interesX60dias, "de interés", "| 90 días: (", noventaDias.strftime("20%y-%m-%d"), ") es %", interesX90dias, "de interes")

def modo_admin(input, opcion):
    contrasena = input
    respuesta = "PatosPatos"

    if contrasena == respuesta:
        print("├ Usted ha accedido al modo administrador\n")
        pass
    else:
        print("╰─Contraseña de administrador incorrecta. Se le redirigirá al menú de opciones")
        PatitoBank.menu_opcion(1)

### --- OPCIONES DE SELECCION
# Opcion 1: Crear una cuenta
def crear_cuenta():
    print("├ Coloque los datos que se le indiquen para poder crear una cuenta")
    ## A // Crear la cuenta: Nombre del titular
    titular_input = str(input("• Nombre del titular: "))
    Check.titular(titular_input, "1")

    ## B// Curp: Ingresar Clave Unica de Registro Poblacional
    curp_input = str(input("• CURP del titular: "))
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
    print("\n¡Cuenta creada con éxito!", nueva_cuenta, "\n<<Guarde estos datos en un lugar seguro>>")

    ## E // Volver al menu de opciones
    PatitoBank.volver_al_menu("1")

# Opcion 2: Ver el balance de una cuenta
def ver_cuenta_balance():
    print("├ Coloque los datos que se le indiquen para poder ver el balance de una cuenta")
    ## A // Ingresar numero de cuenta para ver el balance
    numCuenta_input = str(input("• Numero de cuenta del titular: "))
    Check.numCuenta(numCuenta_input, "2") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "2") # Si existe la cuenta

    ## B // Mostrar balance de la cuenta
    cuenta_balance = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).order_by(
        Transaccion.id.desc()).first()

    if cuenta_balance.soloBalance() == 0:
        print("\n<<Esta cuenta no tiene dinero>>")
    elif cuenta_balance.soloBalance() >= 1:
        print("\nEl balance es cuenta es: $", cuenta_balance.soloBalance(), "\n")

        ## C // Pedir préstamo
        posible_prestamo = int(cuenta_balance.soloBalance() * 0.8) # Solo se puede prestar hasta el 80% del balance de la cuenta
        print("<<Puede pedir hasta $", posible_prestamo, "como préstamo>>")
        calcular_prestamo(posible_prestamo)
        prestamo = input("\n¿Desea pedir un préstamo? (Si o No): ")

        if prestamo == "Si" or prestamo == "si" or prestamo == "SI":
            monto_input = int(input("¿Cuanto dinero necesita?: $ "))
            if monto_input > posible_prestamo:
                print("<<Disculpe, el monto colocado es más del que le podemos prestar>>")
                pass
            elif monto_input <= posible_prestamo:
                pedir_prestamo(monto_input, numCuenta_input)
        elif prestamo == "No" or prestamo == "no" or prestamo == "NO":
            pass
        else:
            PatitoBank.volver("4")

    ## D // Volver al menu de opciones
    PatitoBank.volver_al_menu("2")

# Opcion 3
def depositar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = str(input("├ Coloque el numero de cuenta del usuario: "))
    Check.numCuenta(numCuenta_input, "3") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "3") # Si existe la cuenta

    # ¿Desea depositar dinero a esa cuenta?
    esta_cuenta = input("\n├ ¿Desea depositar dinero a esta cuenta? (Si o No): ")
    if esta_cuenta == "Si" or esta_cuenta == "si" or esta_cuenta == "SI":
        pass
    elif esta_cuenta == "No" or esta_cuenta == "no" or esta_cuenta == "NO":
        PatitoBank.volver_al_menu("4")
    else:
        PatitoBank.volver_al_menu("4")

    print("├ Coloque los datos para el depósito:")
    # B // Ingresar datos del depósito (Monto / Fecha y Hora / Concepto)
    monto_input = int(input("• Dinero a depositar: $ "))
    fecha_input = print("• Fecha y hora: (se coloca de manera automática)", datetime.now())
    # SG: seleccionar si se quiere o no la fecha así
    concepto_input = str(input("• Concepto: "))

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
    print("\n├ Depósito realizado con éxito. Datos: \n", nueva_transaccion.dataTransaccion())
    # Quitar de la base de datos la primera transaccion (Cuenta Creada)
    Check.transaccion_cuentaCreada(numCuenta_input)
    # Añadir a la base de datos
    SQLFuncion.añadir("transaccion", nueva_transaccion)

    # C // Volver al menu de opciones
    PatitoBank.volver_al_menu("3")

# Opcion 4
def retirar_dinero():
    # A // Ingresar numero de cuenta a depositar dinero
    numCuenta_input = str(input("├ Coloque el numero de cuenta del usuario: "))
    Check.numCuenta(numCuenta_input, "3") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "3") # Si existe la cuenta

    # ¿Desea depositar dinero a esa cuenta?
    esta_cuenta = input("\n├ ¿Desea retirar dinero de esta cuenta? (Si o No): ")
    if esta_cuenta == "Si" or esta_cuenta == "si" or esta_cuenta == "SI":
        pass
    elif esta_cuenta == "No" or esta_cuenta == "no" or esta_cuenta == "NO":
        PatitoBank.volver_al_menu("4")
    else:
        PatitoBank.volver_al_menu("4")

    print("├ Coloque los datos para el retiro:")
    # B // Ingresar datos del depósito (Monto / Fecha y Hora / Concepto)
    monto_input = int(input("• Dinero a retirar: $ "))
    fecha_input = print("• Fecha y hora: (se coloca de manera automática)", datetime.now())
    # SG: seleccionar si se quiere o no la fecha así
    concepto_input = str(input("• Concepto: "))

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
    print("\n├ Retiro realizado con éxito. Datos: \n", nueva_transaccion.dataTransaccion())
    # Quitar de la base de datos la primera transaccion (Cuenta Creada)
    Check.transaccion_cuentaCreada(numCuenta_input)
    # Añadir a la base de datos
    SQLFuncion.añadir("transaccion", nueva_transaccion)

    # C // Volver al menu de opciones
    PatitoBank.volver_al_menu("4")

# Opcion 5
def mostrar_cuentas():
    # A // Ingresar contraseña especial
    contrasena = input("├ Ingrese contraseña de administrador: ")
    modo_admin(contrasena, "5")

    # B // Mostrar todas las cuentas creadas
    cantidad_cuentas = local_cuentas.query(Cuenta).count()
    if cantidad_cuentas == 0:
        print("No se han creado cuentas")
    elif cantidad_cuentas == 1:
        print("\nCuenta creada:")
        cuentas = local_cuentas.query(Cuenta).all()
        print(cuentas)

        print("<<Se han creado", cantidad_cuentas, "cuenta hasta ahora>>")
    elif cantidad_cuentas != 0:
        print("\nCuentas creadas: ")
        cuentas = local_cuentas.query(Cuenta).all()
        for cuenta in cuentas:
            print(cuenta.data_basico())

        print("<<Se han creado", cantidad_cuentas, "cuentas hasta ahora>>")

        # C // Opciones:
        opciones_avanzadas = str(input("\n\n¿Desea entrar a las opciones avanzadas? (Si o No): "))

        if opciones_avanzadas == "Si" or opciones_avanzadas == "si" or opciones_avanzadas == "SI":
            print("1. Eliminar todas las cuentas de banco creadas hasta ahora (incluyendo las transacciones realizadas). \n0. Salir de las opciones avanzadas")
            seleccionar = int(input("\n├ ¿Que elige?: "))

            if seleccionar == 1:
                try:
                    eliminar_cuenta = local_cuentas.query(Cuenta).delete()
                    local_cuentas.commit()
                    print("<<Cuentas eliminadas con éxito>>")
                    eliminar_transacciones = local_transacciones.query(Transaccion).delete()
                    local_transacciones.commit()
                    print("<<Transacciones eliminadas con éxito>>")
                    pass
                except:
                    local_cuentas.rollback()
                    pass
            elif seleccionar == 0:
                print("<<Used ha salido de las opciones avanzadas>>")
                pass
            else:
                pass
        elif opciones_avanzadas == "No" or opciones_avanzadas == "no" or opciones_avanzadas == "NO":
            pass
        else:
            pass

    ## C // Volver al menu de opciones
    PatitoBank.volver_al_menu("5")

# Opcion 6
def ver_cuenta_historial():
    # A // Ingresar contraseña especial
    contrasena = input("├ Ingrese la contraseña de administrador: ")
    modo_admin(contrasena, "6")

    # B // Ingresar numero de cuenta revisar historial
    numCuenta_input = str(input("Coloque el numero de cuenta del usuario: "))
    Check.numCuenta(numCuenta_input, "6") # Si los datos son correctos
    Check.existe_numCuenta(numCuenta_input, "6") # Si existe la cuenta

    # C // Ver historial numero de cuenta
    cantidad_transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).count()

    if cantidad_transacciones == 0:
        print("No se ha encontrado transacciones realizadas por esta cuenta")
    elif cantidad_transacciones == 1:
        usuario_CuentaCreada = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input,
                                                                       Transaccion.tipo == "Cuenta Creada").first()
        if usuario_CuentaCreada != None: # si hay
            print("No se ha encontrado transacciones hechas por esta cuenta")
        elif usuario_CuentaCreada == None: # sino hay
            print("\nTransaccion realizada hasta ahora")
            transacciones = local_transacciones.query(Transaccion).filter(
                Transaccion.numCuenta == numCuenta_input).all()
            print(transacciones)

            print("<<Se ha hecho", cantidad_transacciones, "transaccion hasta ahora>>")
    elif cantidad_transacciones >= 2:
        print("\nTransacciones realizadas:")
        transacciones = local_transacciones.query(Transaccion).filter(Transaccion.numCuenta == numCuenta_input).all()
        for transaccione in transacciones:
            print(transaccione)

        print("<<Se han hecho", cantidad_transacciones, "transacciones hasta ahora>>")

    ## D // Volver al menu de opciones
    PatitoBank.volver_al_menu("6")

### ------------ FrontEnd: que todo se vea bonito ###
class PatitoBank:
    def bienvenida(self):
        print("╭───────────────────────────────────────────╮\n|   PatitoBank. El mejor banco de Python.   |\n╰───────────────────────────────────────────╯")

    def base_de_datos(self):
        # Create database if it does not exist.
        if not database_exists(Link1):
            print("...Estamos creando la base de datos...")
            # Crear la base de datos para las cuentas
            Base.metadata.create_all(engine_cuentas)
            # Crear la base de datos para las transacciones
            Base.metadata.create_all(engine_transacciones)
            print("...Se ha creado la base de datos exitosamente...")
            PatitoBank.salir("inicie")
        else:
            pass

    def menu_opcion(self):
        print("\n╭─────── Menu de opciones:\n├──> ¿Qué desee hacer?\n├ 1. Crear una cuenta de banco\n├ 2. Ver el balance de una cuenta\n├ 3. Depositar dinero a una cuenta\n├ 4. Retirar dinero a una cuenta\n├ 5. Ver todas las cuentas de banco creadas\n├ 6. Ver el historial de transacciones de una cuenta\n╰─ 0. Salir de Patito Bank")
        opcion = str(input("\n╭───Seleccione una opción: "))

        if opcion == "1":
            print("├ Crear una cuenta de banco\n")
            crear_cuenta()
        elif opcion == "2":
            print("├ Ver el balance de una cuenta\n")
            ver_cuenta_balance()
        elif opcion == "3":
            print("├ Depositar dinero a una cuenta\n")
            depositar_dinero()
        elif opcion == "4":
            print("├ Retirar dinero a una cuenta\n")
            retirar_dinero()
        elif opcion == "5":
            print("├ Ver todas las cuentas de banco creadas\n")
            mostrar_cuentas()
        elif opcion == "6":
            print("├ Ver el historial de transacciones de una cuenta\n")
            ver_cuenta_historial()
        elif opcion == "0":
            PatitoBank.salir("gracias")
        else:
            print("├ La opción que seleccionó es inválida ┤")
            PatitoBank.menu_opcion(1)

    def volver(opcion):
        if opcion == "1":
            print("╭────────")
            print("├ Crear una cuenta de banco\n")
            crear_cuenta()
        elif opcion == "2":
            print("╭────────")
            print("├ Ver el balance de una cuenta\n")
            ver_cuenta_balance()
        elif opcion == "3":
            print("╭────────")
            print("├ Depositar dinero a una cuenta\n")
            depositar_dinero()
        elif opcion == "4":
            print("╭────────")
            print("├ Retirar dinero a una cuenta\n")
            retirar_dinero()
        elif opcion == "5":
            print("╭────────")
            print("├ Ver todas las cuentas de banco creadas\n")
            mostrar_cuentas()
        elif opcion == "6":
            print("╭────────")
            print("├ Ver el historial de transacciones de una cuenta\n")
            ver_cuenta_historial()
        else:
            print("├ La opción que seleccionó es inválida ┤")
            PatitoBank.menu_opcion(1)

    def volver_al_menu(opcion):
        pregunta = input("\n├ ¿Desea volver al menu de opciones? (Si o No): ")

        if pregunta == "Si" or pregunta == "si" or pregunta == "SI":
            print("╰────────")
            PatitoBank.menu_opcion(1)
        elif pregunta == "No" or pregunta == "no" or pregunta == "NO":
            print("╰────────")
            PatitoBank.volver(opcion)
        else:
            print("╰────────")
            PatitoBank.volver(opcion)

    def salir(mensaje):
        if mensaje == "gracias":
            print("╭─────────────────────────────────────╮\n|  Gracias por utilizar PatitoBank.   |\n╰─────────────────────────────────────╯")
        elif mensaje == "inicie":
            print("╭───────────────────────────────────────────╮\n|  Por favor, inicie PatitoBank otra vez.   |\n╰───────────────────────────────────────────╯")

        exit()

### ------------ SetUp: que el usuario lo pueda utilizar ###
PatitoBank.bienvenida("1")
PatitoBank.base_de_datos("1")
PatitoBank.menu_opcion("1")