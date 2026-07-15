def buscarLibroPorCodigo(codigosLibros: list, codigo: str, cantidadLibros: int) -> int:
    posicion:int = -1
    for i in range(cantidadLibros):
        if codigosLibros[i] == codigo:
            posicion = i
    return posicion


def buscarUsuario(usuariosUnicos: list, usuario: str, cantidadUsuariosUnicos: int) -> int:
    posicion:int = -1
    for i in range(cantidadUsuariosUnicos):
        if usuariosUnicos[i] == usuario:
            posicion = i
    return posicion


def registrarPrestamo(codigosLibros: list, titulosLibros: list, estadosLibros: list,
                       contadorPrestamosLibro: list, cantidadLibros: int,
                       prestamoUsuarios: list, prestamoCodigos: list,
                       usuarioActualLibro: list, dniActualLibro: list, telefonoActualLibro: list,
                       totalPrestamosRegistrados: int) -> int:
    codigo:str = input("Código del libro: ")
    posicion:int = buscarLibroPorCodigo(codigosLibros, codigo, cantidadLibros)

    if posicion == -1:
        print("No existe un libro con ese código.")
        return 0
    else:
        if estadosLibros[posicion] == "prestado":
            print(f"'{titulosLibros[posicion]}' no está disponible.")
            return 0
        else:
            usuario:str = input("Nombre del usuario: ")
            dni:str = input("DNI del usuario: ")
            telefono:str = input("Teléfono del usuario: ")

            estadosLibros[posicion] = "prestado"
            contadorPrestamosLibro[posicion] = contadorPrestamosLibro[posicion] + 1
            prestamoUsuarios[totalPrestamosRegistrados] = usuario
            prestamoCodigos[totalPrestamosRegistrados] = codigo
            usuarioActualLibro[posicion] = usuario
            dniActualLibro[posicion] = dni
            telefonoActualLibro[posicion] = telefono

            print(f"Préstamo registrado: '{titulosLibros[posicion]}' para {usuario}.")
            return 1


def registrarDevolucion(codigosLibros: list, titulosLibros: list, estadosLibros: list,
                         usuarioActualLibro: list, dniActualLibro: list, telefonoActualLibro: list,
                         cantidadLibros: int):
    codigo:str = input("Código del libro a devolver: ")
    posicion:int = buscarLibroPorCodigo(codigosLibros, codigo, cantidadLibros)

    if posicion == -1:
        print("No existe un libro con ese código.")
    else:
        if estadosLibros[posicion] == "disponible":
            print("Ese libro no tiene un préstamo activo.")
        else:
            estadosLibros[posicion] = "disponible"
            usuarioActualLibro[posicion] = ""
            dniActualLibro[posicion] = ""
            telefonoActualLibro[posicion] = ""
            print(f"Devolución registrada: '{titulosLibros[posicion]}'.")


def listarLibrosPorEstado(codigosLibros: list, titulosLibros: list, estadosLibros: list,
                           estadoBuscado: str, cantidadLibros: int):
    encontrados:int = 0
    for i in range(cantidadLibros):
        if estadosLibros[i] == estadoBuscado:
            print(f"- {codigosLibros[i]} | {titulosLibros[i]}")
            encontrados = encontrados + 1

    if encontrados == 0:
        print("No hay libros en ese estado.")


def listarLibrosPrestados(codigosLibros: list, titulosLibros: list, estadosLibros: list,
                           usuarioActualLibro: list, dniActualLibro: list, telefonoActualLibro: list,
                           cantidadLibros: int):
    encontrados:int = 0
    for i in range(cantidadLibros):
        if estadosLibros[i] == "prestado":
            print(f"- {codigosLibros[i]} | {titulosLibros[i]} | Usuario: {usuarioActualLibro[i]} | DNI: {dniActualLibro[i]} | Tel: {telefonoActualLibro[i]}")
            encontrados = encontrados + 1

    if encontrados == 0:
        print("No hay libros prestados actualmente.")


#Suma los préstamos de los libros y devuelve el total
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


def generarReportes(titulosLibros: list, contadorPrestamosLibro: list,
                     cantidadLibros: int, prestamoUsuarios: list, totalPrestamosRegistrados: int):
    if totalPrestamosRegistrados == 0:
        print("Todavía no se han registrado préstamos.")
    else:
        total:int = calcularTotal(contadorPrestamosLibro, cantidadLibros)
        promedio:float = calcularPromedio(total, cantidadLibros)

        # Libro MÁS y MENOS solicitado
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

        # Usuario más frecuente
        usuariosUnicos:list = [""] * 100
        cantidadPorUsuario:list = [0] * 100
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


def pedirTipoUsuario() -> str:
    print("\n===========================================")
    print("              INICIO DE SESIÓN")
    print("===========================================")
    print("   1. Cliente (alquilar y devolver libros)")
    print("   2. Gerente (acceso completo)")
    print("   3. Registrar usuario")
    print("===========================================")
    opcion:str = input("Elige tu tipo de usuario: ")

    if opcion == "2":
        return "gerente"
    else:
        return "cliente"


def mostrarMenuCliente():
    print("\n===========================================")
    print("     GESTIÓN DE PRÉSTAMOS DE LIBROS")
    print("                (CLIENTE)")
    print("===========================================")
    print("   1. Registrar préstamo")
    print("   2. Registrar devolución")
    print("   3. Ver libros disponibles")
    print("   4. Salir")
    print("===========================================")


def mostrarMenuGerente():
    print("\n===========================================")
    print("     GESTIÓN DE PRÉSTAMOS DE LIBROS")
    print("                (GERENTE)")
    print("===========================================")
    print("   1. Registrar préstamo")
    print("   2. Registrar devolución")
    print("   3. Ver libros disponibles")
    print("   4. Ver libros prestados")
    print("   5. Generar reportes")
    print("   6. Salir")
    print("===========================================")


#VARIABLES
#Mini BD
CANTIDAD_LIBROS:int = 4
codigosLibros:list = ["L01", "L02", "L03", "L04"]
titulosLibros:list = ["El Principito", "Don Quijote", "Cien años de soledad", "La Odisea"]
estadosLibros:list = ["disponible", "disponible", "disponible", "disponible"]
contadorPrestamosLibro:list = [0, 0, 0, 0]

# Reservamos espacio para los préstamos que se vayan registrando
prestamoUsuarios:list = [""] * 100
prestamoCodigos:list = [""] * 100
totalPrestamosRegistrados:int = 0

# Datos del usuario que tiene actualmente cada libro (mismo índice que codigosLibros)
usuarioActualLibro:list = [""] * CANTIDAD_LIBROS
dniActualLibro:list = [""] * CANTIDAD_LIBROS
telefonoActualLibro:list = [""] * CANTIDAD_LIBROS

# CICLO PRINCIPAL DEL PROGRAMA
tipoUsuario:str = pedirTipoUsuario()

if tipoUsuario == "cliente":
    opcion:str = ""
    while opcion != "4":
        mostrarMenuCliente()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            exito:int = registrarPrestamo(codigosLibros, titulosLibros, estadosLibros,
                                           contadorPrestamosLibro, CANTIDAD_LIBROS,
                                           prestamoUsuarios, prestamoCodigos,
                                           usuarioActualLibro, dniActualLibro, telefonoActualLibro,
                                           totalPrestamosRegistrados)
            totalPrestamosRegistrados = totalPrestamosRegistrados + exito
        else:
            if opcion == "2":
                registrarDevolucion(codigosLibros, titulosLibros, estadosLibros,
                                     usuarioActualLibro, dniActualLibro, telefonoActualLibro,
                                     CANTIDAD_LIBROS)
            else:
                if opcion == "3":
                    listarLibrosPorEstado(codigosLibros, titulosLibros, estadosLibros, "disponible", CANTIDAD_LIBROS)
                else:
                    if opcion == "4":
                        print("Saliendo del sistema...")
                    else:
                        print("Opción no válida.")
else:
    opcion:str = ""
    while opcion != "6":
        mostrarMenuGerente()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            exito:int = registrarPrestamo(codigosLibros, titulosLibros, estadosLibros,
                                           contadorPrestamosLibro, CANTIDAD_LIBROS,
                                           prestamoUsuarios, prestamoCodigos,
                                           usuarioActualLibro, dniActualLibro, telefonoActualLibro,
                                           totalPrestamosRegistrados)
            totalPrestamosRegistrados = totalPrestamosRegistrados + exito
        else:
            if opcion == "2":
                registrarDevolucion(codigosLibros, titulosLibros, estadosLibros,
                                     usuarioActualLibro, dniActualLibro, telefonoActualLibro,
                                     CANTIDAD_LIBROS)
            else:
                if opcion == "3":
                    listarLibrosPorEstado(codigosLibros, titulosLibros, estadosLibros, "disponible", CANTIDAD_LIBROS)
                else:
                    if opcion == "4":
                        listarLibrosPrestados(codigosLibros, titulosLibros, estadosLibros,
                                               usuarioActualLibro, dniActualLibro, telefonoActualLibro,
                                               CANTIDAD_LIBROS)
                    else:
                        if opcion == "5":
                            generarReportes(titulosLibros, contadorPrestamosLibro,
                                             CANTIDAD_LIBROS, prestamoUsuarios, totalPrestamosRegistrados)
                        else:
                            if opcion == "6":
                                print("Saliendo del sistema...")
                            else:
                                print("Opción no válida.")
