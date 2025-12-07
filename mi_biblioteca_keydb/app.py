import redis
import json
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("KEYDB_HOST")
PORT = int(os.getenv("KEYDB_PORT"))
PASSWORD = os.getenv("KEYDB_PASSWORD") or None

try:
    db = redis.Redis(
        host=HOST,
        port=PORT,
        password=PASSWORD,
        decode_responses=True
    )
    db.ping()
    print(" Conectado correctamente a KeyDB\n")
except Exception as e:
    print(" Error conectando a KeyDB:", e)
    exit()

def agregar_libro():
    print("\n📘 Agregar nuevo libro")
    id_libro = input("ID único del libro: ")

    if db.exists(f"libro:{id_libro}"):
        print(" Ya existe un libro con ese ID.")
        return

    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (pendiente/en progreso/terminado): ")

    libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    db.set(f"libro:{id_libro}", json.dumps(libro))
    print(" Libro agregado exitosamente.")


def actualizar_libro():
    print("\n Actualizar libro")
    id_libro = input("ID del libro: ")

    key = f"libro:{id_libro}"

    if not db.exists(key):
        print(" El libro no existe.")
        return

    libro = json.loads(db.get(key))

    print("\nDeja vacío para mantener el dato actual.\n")

    nuevo_titulo = input(f"Título ({libro['titulo']}): ")
    nuevo_autor = input(f"Autor ({libro['autor']}): ")
    nuevo_genero = input(f"Género ({libro['genero']}): ")
    nuevo_estado = input(f"Estado ({libro['estado']}): ")

    if nuevo_titulo:
        libro["titulo"] = nuevo_titulo
    if nuevo_autor:
        libro["autor"] = nuevo_autor
    if nuevo_genero:
        libro["genero"] = nuevo_genero
    if nuevo_estado:
        libro["estado"] = nuevo_estado

    db.set(key, json.dumps(libro))
    print(" Libro actualizado correctamente.")


def eliminar_libro():
    print("\n Eliminar libro")
    id_libro = input("ID del libro: ")

    if db.delete(f"libro:{id_libro}"):
        print(" Libro eliminado.")
    else:
        print(" Ese libro no existe.")


def listar_libros():
    print("\n Listado de libros:")

    keys = db.scan_iter("libro:*")
    hay_libros = False

    for key in keys:
        libro = json.loads(db.get(key))
        print(f"\nID: {key.split(':')[1]}")
        print(f"  Título: {libro['titulo']}")
        print(f"  Autor: {libro['autor']}")
        print(f"  Género: {libro['genero']}")
        print(f"  Estado: {libro['estado']}")
        hay_libros = True

    if not hay_libros:
        print(" No hay libros registrados.")


def buscar_libro():
    print("\n Buscar libros")
    campo = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input("Valor a buscar: ").lower()

    if campo not in ["titulo", "autor", "genero"]:
        print(" Campo inválido.")
        return

    print("\nResultados:")

    keys = db.scan_iter("libro:*")
    encontrados = False

    for key in keys:
        libro = json.loads(db.get(key))

        if valor in libro[campo].lower():
            print(f"\nID: {key.split(':')[1]}")
            print(f"  Título: {libro['titulo']}")
            print(f"  Autor: {libro['autor']}")
            print(f"  Género: {libro['genero']}")
            print(f"  Estado: {libro['estado']}")
            encontrados = True

    if not encontrados:
        print(" No se encontraron coincidencias.")


def menu():
    while True:
        print("""
==============  MENÚ BIBLIOTECA ==============
1. Agregar libro
2. Actualizar libro
3. Eliminar libro
4. Ver todos los libros
5. Buscar libros
6. Salir
================================================
        """)

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            actualizar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            listar_libros()
        elif opcion == "5":
            buscar_libro()
        elif opcion == "6":
            print(" Saliendo del programa...")
            break
        else:
            print(" Opción inválida. Intenta de nuevo.")



if __name__ == "__main__":
    menu()
