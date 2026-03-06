from datetime import datetime
import os

#excepciones
class ProductoNoEncontradoError(Exception):
    """Excepción cuando no se encuentra un producto por ID"""
    pass


class CantidadInvalidaError(Exception):
    """Excepción cuando la cantidad es inválida"""
    pass

# lista de productos
productos = [
    {"id": 1, "nombre": "prod_uno", "categoria": "ropa", "precio": 20000.0},
    {"id": 2, "nombre": "prod_dos", "categoria": "manualidad", "precio": 5000.0},
    {"id": 3, "nombre": "prod_tres", "categoria": "ropa", "precio": 35000.0},
    {"id": 4, "nombre": "prod_cuatro", "categoria": "manualidad", "precio": 15000.0},
    {"id": 5, "nombre": "prod_cinco", "categoria": "manualidad", "precio": 10000.0},
]

carrito = []

#funciones generales

def encontrar_producto_id(lista_productos, id_busqueda):
    for producto in lista_productos:
        if producto["id"] == id_busqueda:
            return producto
    return None


def listado_productos(lista_productos):
    if not lista_productos:
        print("\nNo hay productos en el catálogo")
        return

    print("\nCatálogo de productos")
    print("---------------------")
    for prod in lista_productos:
        print(
            f"id: {prod['id']} | "
            f"nombre: {prod['nombre']} | "
            f"categoría: {prod['categoria']} | "
            f"precio: ${prod['precio']:.0f}"
        )

#funciones de cliente

def mostrar_menu_cliente():
    print("\n*** MENÚ CLIENTE ***")
    print("1) Ver catálogo de productos")
    print("2) Buscar producto por nombre o categoría")
    print("3) Agregar producto al carrito")
    print("4) Ver carrito y total")
    print("5) Confirmar compra")
    print("6) Vaciar carrito")
    print("0) Volver al menú de roles")


def buscar_producto(lista_productos):
    texto = input("\nIngresa nombre o categoría para buscar: ").strip().lower()

    if not texto:
        print("No se ingresó texto de búsqueda")
        return

    resultados = []
    for prod in lista_productos:
        nombre = prod["nombre"].lower()
        categoria = prod["categoria"].lower()
        if texto in nombre or texto in categoria:
            resultados.append(prod)

    if not resultados:
        print("No hay productos que coincidan con la búsqueda")
    else:
        print("\nResultados de la búsqueda")
        print("-------------------------")
        listado_productos(resultados)


def agregar_carrito(lista_productos, lista_carrito):
    try:
        id_str = input("\nIngresa el id del producto para agregar al carrito: ")
        id_producto = int(id_str)
        producto = encontrar_producto_id(lista_productos, id_producto)
    except ValueError:
        print("El id debe ser un número entero")
        return
    except ProductoNoEncontradoError as e:
        print(e)
        return

    try:
        cantidad_str = input("Ingresa la cantidad (número entero > 0): ")
        cantidad = int(cantidad_str)
        if cantidad <= 0:
            raise CantidadInvalidaError("La cantidad debe ser mayor a 0")
    except ValueError:
        print("La cantidad debe ser un número entero")
        return
    except CantidadInvalidaError as e:
        print(e)
        return

    for item in lista_carrito:
        if item["producto"]["id"] == producto["id"]:
            item["cantidad"] += cantidad
            print(
                f"Se añadieron {cantidad} unidades de '{producto['nombre']}' al carrito"
            )
            return

    lista_carrito.append({"producto": producto, "cantidad": cantidad})
    print(f"Se agregó '{producto['nombre']}' (x{cantidad}) al carrito")


def mostrar_carrito_y_total(lista_carrito):
    if not lista_carrito:
        print("\nEl carrito está vacío")
        return

    print("\nCarrito de compras")
    print("------------------")

    total = 0.0
    for item in lista_carrito:
        prod = item["producto"]
        cantidad = item["cantidad"]
        subtotal = prod["precio"] * cantidad
        total += subtotal
        print(
            f"id: {prod['id']} | "
            f"nombre: {prod['nombre']} | "
            f"cantidad: {cantidad} | "
            f"precio unitario: ${prod['precio']:.0f} | "
            f"subtotal: ${subtotal:.0f}"
        )

    print("------------------")
    print(f"TOTAL A PAGAR: ${total:.0f}")
    return total


def confirmar_compra(lista_carrito):
    if not lista_carrito:
        print("\n El carrito está vacío. No se puede confirmar la compra.")
        return

    total = mostrar_carrito_y_total(lista_carrito)
    
    print("\n" + "="*20)
    confirmar = input(f"¿Confirmar compra por ${total:.0f}? (s/n): ").strip().lower()
    
    if confirmar != "s":
        print("Compra cancelada")
        return

    try:
        ahora = datetime.now()
        fecha_hora = ahora.strftime("%Y-%m-%d %H:%M:%S")
        #se registra hora y fecha, para el registro de ordenes.txt
        
        contenido = f"\n{'='*20}\n"
        contenido += f"ORDEN DE COMPRA - {fecha_hora}\n"
        contenido += f"{'='*20}\n\n"
        
        total_final = 0.0
        for item in lista_carrito:
            prod = item["producto"]
            cantidad = item["cantidad"]
            subtotal = prod["precio"] * cantidad
            total_final += subtotal
            contenido += f"{prod['nombre']} x{cantidad} = ${subtotal:.0f}\n"
        
        contenido += f"\n{'='*20}\n"
        contenido += f"TOTAL: ${total_final:.0f}\n"
        contenido += f"{'='*20}\n"
        
        with open("ordenes.txt", mode="a", encoding="utf-8") as archivo:
            archivo.write(contenido)
    
        
        print(f"\n ¡COMPRA CONFIRMADA!")
        print(f" Detalle guardado en 'ordenes.txt'")
        print(f" Total: ${total_final:.0f}")
        
        vaciar_carrito(lista_carrito)
        
    except IOError as e:
        print(f"Error al escribir el archivo de órdenes: {e}")
    except Exception as e:
        print(f" Error inesperado: {e}")


def vaciar_carrito(lista_carrito):
    if not lista_carrito:
        print("\nEl carrito ya está vacío")
        return

    lista_carrito.clear()
    print("El carrito ha sido vaciado")


def menu_cliente():
    while True:
        mostrar_menu_cliente()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            listado_productos(productos)
        elif opcion == "2":
            buscar_producto(productos)
        elif opcion == "3":
            agregar_carrito(productos, carrito)
        elif opcion == "4":
            mostrar_carrito_y_total(carrito)
        elif opcion == "5":
            confirmar_compra(carrito)
        elif opcion == "6":
            vaciar_carrito(carrito)
        elif opcion == "0":
            print("\nVolviendo al menú de roles...")
            break
        else:
            print("Opción no válida, elige una opción del menú")

# funciones del admin 

def mostrar_menu_admin():
    print("\n*** MENÚ ADMIN ***")
    print("1) Listar productos")
    print("2) Crear producto")
    print("3) Actualizar producto")
    print("4) Eliminar producto")
    print("5) Guardar catálogo")
    print("0) Volver al menú de roles")


def crear_producto(lista_productos):
    print("\nCrear nuevo producto")
    try:
        id_str = input("Ingresa id (entero): ")
        nuevo_id = int(id_str)
    except ValueError:
        print("El id debe ser un número entero")
        return

    if encontrar_producto_id(lista_productos, nuevo_id) is not None:
        print("Ya existe un producto con ese id")
        return

    nombre = input("Ingresa nombre: ").strip()
    categoria = input("Ingresa categoría: ").strip()

    try:
        precio_str = input("Ingresa precio (número): ")
        precio = float(precio_str)
    except ValueError:
        print("El precio debe ser numérico")
        return

    if precio <= 0:
        print("El precio debe ser mayor a 0")
        return

    nuevo_producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio
    }
    lista_productos.append(nuevo_producto)
    print(f"Producto '{nombre}' creado correctamente")


def actualizar_producto(lista_productos):
    print("\nActualizar producto")
    try:
        id_str = input("Ingresa el id del producto a actualizar: ")
        id_producto = int(id_str)
        producto = encontrar_producto_id(lista_productos, id_producto)
    except ValueError:
        print("El id debe ser un número entero")
        return
    except ProductoNoEncontradoError as e:
        print(e)
        return

    print(f"Producto actual: {producto}")

    nuevo_nombre = input("Nuevo nombre (enter para mantener): ").strip()
    nueva_categoria = input("Nueva categoría (enter para mantener): ").strip()
    nuevo_precio_str = input("Nuevo precio (enter para mantener): ").strip()

    if nuevo_nombre:
        producto["nombre"] = nuevo_nombre
    if nueva_categoria:
        producto["categoria"] = nueva_categoria
    if nuevo_precio_str:
        try:
            nuevo_precio = float(nuevo_precio_str)
            if nuevo_precio > 0:
                producto["precio"] = nuevo_precio
            else:
                print("Precio inválido, se mantiene el anterior")
        except ValueError:
            print("Precio inválido, se mantiene el anterior")

    print("Producto actualizado:", producto)


def eliminar_producto(lista_productos):
    print("\nEliminar producto")
    try:
        id_str = input("Ingresa el id del producto a eliminar: ")
        id_producto = int(id_str)
        producto = encontrar_producto_id(lista_productos, id_producto)
    except ValueError:
        print("El id debe ser un número entero")
        return
    except ProductoNoEncontradoError as e:
        print(e)
        return

    confirmar = input(
        f"¿Seguro que deseas eliminar '{producto['nombre']}'? (s/n): "
    ).strip().lower()
    if confirmar == "s":
        lista_productos.remove(producto)
        print("Producto eliminado")
    else:
        print("Operación cancelada")

#crea .txt del catalogo
def guardar_catalogo_txt(lista_productos, nombre_archivo):
    if not lista_productos:
        print("No hay productos para guardar")
        return
    try:
        with open(nombre_archivo, mode="w", encoding="utf-8") as archivo:
            archivo.write("id,nombre,categoria,precio\n")
            for producto in lista_productos:
                archivo.write(
                    f"{producto['id']},{producto['nombre']},"
                    f"{producto['categoria']},{producto['precio']}\n"
                )
        print(f"Catálogo guardado en '{nombre_archivo}'")
    except Exception as e:
        print("Error al guardar el archivo:", e)


def menu_admin():
    while True:
        mostrar_menu_admin()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            listado_productos(productos)
        elif opcion == "2":
            crear_producto(productos)
        elif opcion == "3":
            actualizar_producto(productos)
        elif opcion == "4":
            eliminar_producto(productos)
        elif opcion == "5":
            guardar_catalogo_txt(productos, "catalogo.txt")
        elif opcion == "0":
            print("\nVolviendo al menú de roles...")
            break
        else:
            print("Opción no válida")



def elegir_rol():
    while True:
        print("\n=== MI TIENDITA ===")
        print("Selecciona tu rol:")
        print("1) ADMIN")
        print("2) CLIENTE")
        print("0) Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            menu_admin()
        elif opcion == "2":
            menu_cliente()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    elegir_rol()
