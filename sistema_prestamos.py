#Busca la posición de un libro según su código; devuelve -1 si no lo encuentra
def buscarLibroPorCodigo(codigosLibros: list, codigo: str, cantidadLibros: int) -> int:
    posicion:int = -1
    for i in range(cantidadLibros):
        if codigosLibros[i] == codigo:
            posicion = i
    return posicion


#Busca la posición de un usuario dentro de los usuarios ya registrados
def buscarUsuario(usuariosUnicos: list, usuario: str, cantidadUsuariosUnicos: int) -> int:
    posicion:int = -1
    for i in range(cantidadUsuariosUnicos):
        if usuariosUnicos[i] == usuario:
            posicion = i
    return posicion


#Registra un préstamo si el libro existe, está disponible y hay espacio en el
#arreglo de préstamos. Devuelve 1 si se registró el préstamo, o 0 si no
def registrarPrestamo(codigosLibros: list, titulosLibros: list, estadosLibros: list,
                       contadorPrestamosLibro: list, cantidadLibros: int,
                       prestamoUsuarios: list, prestamoCodigos: list,
                       totalPrestamosRegistrados: int, capacidadMaxima: int) -> int:
    if totalPrestamosRegistrados == capacidadMaxima:
        print("Se alcanzó la capacidad máxima de préstamos registrados.")
        return 0

    codigo:str = input("Código del libro: ")
    posicion:int = buscarLibroPorCodigo(codigosLibros, codigo, cantidadLibros)

    if posicion == -1:
        print("No existe un libro con ese código.")
        return 0

    if estadosLibros[posicion] == "prestado":
        print(f"'{titulosLibros[posicion]}' no está disponible.")
        return 0

    usuario:str = input("Nombre del usuario: ")

    estadosLibros[posicion] = "prestado"
    contadorPrestamosLibro[posicion] = contadorPrestamosLibro[posicion] + 1
    prestamoUsuarios[totalPrestamosRegistrados] = usuario
    prestamoCodigos[totalPrestamosRegistrados] = codigo

    print(f"Préstamo registrado: '{titulosLibros[posicion]}' para {usuario}.")
    return 1


#Registra la devolución de un libro prestado
def registrarDevolucion(codigosLibros: list, titulosLibros: list, estadosLibros: list, cantidadLibros: int):
    codigo:str = input("Código del libro a devolver: ")
    posicion:int = buscarLibroPorCodigo(codigosLibros, codigo, cantidadLibros)

    if posicion == -1:
        print("No existe un libro con ese código.")
        return

    if estadosLibros[posicion] == "disponible":
        print("Ese libro no tiene un préstamo activo.")
        return

    estadosLibros[posicion] = "disponible"
    print(f"Devolución registrada: '{titulosLibros[posicion]}'.")


#Muestra los libros que tienen el estado indicado (disponible o prestado)
def listarLibrosPorEstado(codigosLibros: list, titulosLibros: list, estadosLibros: list,
                           estadoBuscado: str, cantidadLibros: int):
    encontrados:int = 0
    for i in range(cantidadLibros):
        if estadosLibros[i] == estadoBuscado:
            print(f"- {codigosLibros[i]} | {titulosLibros[i]}")
            encontrados = encontrados + 1

    if encontrados == 0:
        print("No hay libros en ese estado.")


#Suma los préstamos de todos los libros y devuelve el total
def calcularTotal(contadorPrestamosLibro: list, cantidadLibros: int) -> int:
    total:int = 0
    for i in range(cantidadLibros):
        total = total + contadorPrestamosLibro[i]
    return total


#Calcula el promedio de préstamos por libro
def calcularPromedio(total: int, cantidadLibros: int) -> float:
    promedio:float = total / cantidadLibros
    return promedio


#Muestra la interpretación de los resultados (usa if / else)
def mostrarInterpretacion(masTitulo: str, masCantidad: int, menosTitulo: str, menosCantidad: int):
    print(f'\n=========== INTERPRETACIÓN ===========')
    if masCantidad > 50:
        print(f'El libro {masTitulo} tiene demanda MUY ALTA; conviene comprar más ejemplares.')
    else:
        print(f'El libro {masTitulo} es el más solicitado del periodo.')

    if menosCantidad < 20:
        print(f'El libro {menosTitulo} tiene BAJA demanda.')
    else:
        print(f'Todos los libros tienen una rotación aceptable.')


#Arma el reporte completo: totales, promedio, más/menos solicitado e interpretación
def generarReportes(titulosLibros: list, contadorPrestamosLibro: list,
                     cantidadLibros: int, prestamoUsuarios: list,
                     totalPrestamosRegistrados: int, capacidadMaxima: int):
    if totalPrestamosRegistrados == 0:
        print("Todavía no se han registrado préstamos.")
        return

    total:int = calcularTotal(contadorPrestamosLibro, cantidadLibros)
    promedio:float = calcularPromedio(total, cantidadLibros)

    # Libro MÁS y MENOS solicitado (se recorre el arreglo comparando cada posición)
    posicionMax:int = 0
    posicionMin:int = 0
    for i in range(cantidadLibros):
        if contadorPrestamosLibro[i] > contadorPrestamosLibro[posicionMax]:
            posicionMax = i
        if contadorPrestamosLibro[i] < contadorPrestamosLibro[posicionMin]:
            posicionMin = i

    masTitulo:str = titulosLibros[posicionMax]
    masCantidad:int = contadorPrestamosLibro[posicionMax]
    menosTitulo:str = titulosLibros[posicionMin]
    menosCantidad:int = contadorPrestamosLibro[posicionMin]

    # Usuario más frecuente: arreglos de tamaño fijo (reservados con capacidadMaxima),
    # llenados por posición con un contador manual (sin .append)
    usuariosUnicos:list = [""] * capacidadMaxima
    cantidadPorUsuario:list = [0] * capacidadMaxima
    cantidadUsuariosUnicos:int = 0

    for i in range(totalPrestamosRegistrados):
        usuario:str = prestamoUsuarios[i]
        posicionUsuario:int = buscarUsuario(usuariosUnicos, usuario, cantidadUsuariosUnicos)
        if posicionUsuario == -1:
            usuariosUnicos[cantidadUsuariosUnicos] = usuario
            cantidadPorUsuario[cantidadUsuariosUnicos] = 1
            cantidadUsuariosUnicos = cantidadUsuariosUnicos + 1
        else:
            cantidadPorUsuario[posicionUsuario] = cantidadPorUsuario[posicionUsuario] + 1

    usuarioMasFrecuente:str = ""
    cantidadMaxUsuario:int = 0
    for i in range(cantidadUsuariosUnicos):
        if cantidadPorUsuario[i] > cantidadMaxUsuario:
            usuarioMasFrecuente = usuariosUnicos[i]
            cantidadMaxUsuario = cantidadPorUsuario[i]

    print(f'\n============== REPORTE ==============')
    for i in range(cantidadLibros):
        print(f'{titulosLibros[i]}: {contadorPrestamosLibro[i]} préstamos')
    print(f'-------------------------------------')
    print(f'Total de préstamos: {total}')
    print(f'Promedio por libro: {promedio:.1f}')
    print(f'Libro más solicitado: {masTitulo} ({masCantidad})')
    print(f'Libro menos solicitado: {menosTitulo} ({menosCantidad})')
    if cantidadMaxUsuario > 0:
        print(f'Usuario más frecuente: {usuarioMasFrecuente} ({cantidadMaxUsuario})')

    mostrarInterpretacion(masTitulo, masCantidad, menosTitulo, menosCantidad)


def mostrarMenu():
    print("\n===========================================")
    print("     GESTIÓN DE PRÉSTAMOS DE LIBROS")
    print("===========================================")
    print("   1. Registrar préstamo")
    print("   2. Registrar devolución")
    print("   3. Ver libros disponibles")
    print("   4. Ver libros prestados")
    print("   5. Generar reportes")
    print("   6. Salir")
    print("===========================================")


#VARIABLES
#Catálogo de libros representado con arreglos paralelos (misma posición = mismo libro)
CANTIDAD_LIBROS:int = 4
codigosLibros:list = ["L001", "L002", "L003", "L004"]
titulosLibros:list = ["El Principito", "Don Quijote", "Cien años de soledad", "La Odisea"]
estadosLibros:list = ["disponible", "disponible", "disponible", "disponible"]
contadorPrestamosLibro:list = [0, 0, 0, 0]

#Préstamos registrados durante la ejecución: arreglos de tamaño fijo (sin .append)
CAPACIDAD_MAXIMA_PRESTAMOS:int = 100
prestamoUsuarios:list = [""] * CAPACIDAD_MAXIMA_PRESTAMOS
prestamoCodigos:list = [""] * CAPACIDAD_MAXIMA_PRESTAMOS
totalPrestamosRegistrados:int = 0

# CICLO PRINCIPAL DEL PROGRAMA
opcion:str = ""
while opcion != "6":
    mostrarMenu()
    opcion = input("Elige una opción: ")

    if opcion == "1":
        exito:int = registrarPrestamo(codigosLibros, titulosLibros, estadosLibros,
                                       contadorPrestamosLibro, CANTIDAD_LIBROS,
                                       prestamoUsuarios, prestamoCodigos,
                                       totalPrestamosRegistrados, CAPACIDAD_MAXIMA_PRESTAMOS)
        totalPrestamosRegistrados = totalPrestamosRegistrados + exito
    elif opcion == "2":
        registrarDevolucion(codigosLibros, titulosLibros, estadosLibros, CANTIDAD_LIBROS)
    elif opcion == "3":
        listarLibrosPorEstado(codigosLibros, titulosLibros, estadosLibros, "disponible", CANTIDAD_LIBROS)
    elif opcion == "4":
        listarLibrosPorEstado(codigosLibros, titulosLibros, estadosLibros, "prestado", CANTIDAD_LIBROS)
    elif opcion == "5":
        generarReportes(titulosLibros, contadorPrestamosLibro,
                         CANTIDAD_LIBROS, prestamoUsuarios,
                         totalPrestamosRegistrados, CAPACIDAD_MAXIMA_PRESTAMOS)
    elif opcion == "6":
        print("Saliendo del sistema...")
    else:
        print("Opción no válida.")
