Actualización de las 5:22.
Agregar Class checker	:	
Check. Titular	:	Verifique que tenga Nombre y Apellido ()
Check.Curp	:	Verifique que tenga Letras mayusculas y numeros (y contenga 18 numeros en total)
Check.Numero de Cuenta	:	Verifique que solo tenga numeros (y contenga 10 numeros en total)
Check.Si existe numero de cuenta	:	Que verifique si ese numero de cuenta existe en la base de datos
Funcion prestamo	:	Para poder realizar todo el proceso de prestamo y los debidos calculos
Funcion calcular_prestamo	:	Para poder calcular un prestamo en intervalos de 30, 60 y 90 dias

Actualización de las 6:30.
Corregir el resto de opciones y agregarle check.numero de cuenta y check. Si existe	:	
Agregar contrasñea especial	:	Para agregarse en opcion 5.6
checker.existe_curp	:	Verificar si ya existe un dato con el mismo CURP y evitar el registro de la cuenta
mejorar checker.titular	:	Para que pueda aceptar nombres y apellidos hispanos con áéíóúñ
mejorar checker.curp	:	Para que mencione si faltan mayor longitud al texto que colocó
mejorar checker.numCuenta	:	Por lo mismo que se mencionó con checker.curp

Actualización de las 7.
Corregir opcion 5 y 6	:	En caso de que no haya cuentas o transacciones, mostrar mensaje personalizado
Actualización de las 8:45		
Eliminar "cuenta creada" de transacciones	:	Se agrego una función que quita la primera transaccion realizada (que no es una transaccion, es crear una cuenta dentr de la base de transacciones tambien). Y ya se quito eso
Editar ambas clases (cuenta, transaccion)	:	Se cambio que en transaccion era Integer, pero se cambio a String(10). 
Guardar fecha de transacciones	:	Habia un problema en la clase del archivo y no se guardaba
Mejorar Opcion 5-6	:	En caso de que solo haya 1 transaccion o 1 cuenta en la base de datos, tenga un mensaje personalizado
Cambio de nombre en los archivos	:	Para que este mas ordenad

Actualizacion 11:59.
PRINCIPALES
 OP2: Mostrar fecha actual y hacer calculos del prestamo 30/60 y 90 dias a partir de hoy
 Aceptar responder con "Si" "si" y "SI" (lo mismo con NO, no, No) buscar "(Si o No)"
 Mejorar opcion 5 y 6, no transacciones pero está la transaccion de cuenta creada
 Si el usuario coloca un numero de cuenta inexistente, se le devolverá al menu de inciio

SECUNDARIOS
 Corregir el output al llamar mostrar los datos de la cuenta y transacciones
 Corregir Output colocado (agregar Mayusculas, acentos y \n donde sea necesario)
 Mejorar las opciones con print()
 Corregir Output "redirigido a"
