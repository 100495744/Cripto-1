from Database import DatabaseMethods
from Criptografia import Criptadores
import os


# Clase de mensajes de text visibles por el usuario
class Interface:

    @staticmethod
    # Pantalla de carga
    def loading():
        print("\n-----------------------------------------------------------------------------------------------------")


    @staticmethod
    # Estado inicial del programa
    def inicial():

        # Pantalla de carga
        Interface.loading()

        # Imprimiendo mensajes de bienvenida
        print("\n¡BIENVENIDO A TU SANITARIO")
        print("\n1 - CREAR NUEVA CUENTA")
        print("\n2 - INICIAR SESIÓN")
        print("\n3 - SALIR")

        # Pantalla de carga
        Interface.loading()

        # Input del usuario
        command = input("\nINPUT: ")

        # Comprobando que el input es correcto
        while command != "1" and command != "2" and command != "3":
            command = input("\nVALOR INCORRECTO, NUEVO INPUT: ")

        # Ejecutando programa según el input introducido
        if command == "1":
            # Nueva cuenta
            Interface.new_account()
        elif command == "2":
            # Login de cuenta
            Interface.login()
        else:
            # Salir del programa
            Interface.quit_program()


    @staticmethod
    # Estado de crear nueva cuenta
    def new_account():

        # Pantalla de carga
        Interface.loading()
        print("PANTALLA DE REGISTRO")

        # Fetch por la base de datos
        database = DatabaseMethods()

        # Mensajes para el usuario
        command_u = input("\nUSUARIO: ")
        command_c = input("\nCONTRASEÑA: ")
        command_c2 = input("\nCONFIRMA CONTRASEÑA: ")

        # Comprobando que las dos contraseñas coinciden
        while command_c != command_c2:
            print("\nLAS CONTRASEÑAS NO COINCIDEN, INTENTALO DE NUEVO")
            command_c = input("\nCONTRASEÑA: ")
            command_c2 = input("\nCONFIRMA CONTRASEÑA: ")

        # Comprobando que no existe el usuario
        if database.username_existe(command_u, "DataBase/datos_principales.json") \
                or database.username_existe(command_u, "DataBase/keys.json"):
            print("YA EXISTE EL USUARIO, VUELVA A INTENTARLO DE NUEVO")
            Interface.inicial()

        # Creando el usuario e introduciéndolo en la base de datos
        hashed_password = Criptadores.hash_hmac_password(command_c2)
        database.write_json_datos_principales(command_u, hashed_password[0])
        database.write_json_keys_salt(command_u, hashed_password[1])

        print("\nCUENTA CREADA")

        # Redirigiendo a la pantalla de login
        Interface.login_done(command_u)

    @staticmethod
    # Estado de inicio de sesión
    def login():
        # Pantalla de carga
        Interface.loading()
        print("PANTALLA DE INICIO DE SESIÓN")

        # Recogiendo usuario y contraseña
        command_u = input("\nUSUARIO: ")
        command_c = input("\nCONTRASEÑA: ")

        # Fetch de la base de datos
        database = DatabaseMethods()

        # Comprobando que existe el usuario
        if database.username_existe(command_u, "DataBase/datos_principales.json") == False \
                or database.username_existe(command_u, "DataBase/keys.json") == False:
            print("NO EXISTE EL USUARIO, VUELVA A INTENTARLO DE NUEVO")
            Interface.login()

        # Valor de salt para el usuario
        salt = database.get_salt(command_u)

        # Cifrando contraseña introducido
        new_hashed_password = Criptadores.hash_hmac_password(command_c, bytes.fromhex(salt))

        # Recogiendo valor de contraseña en la base de datos
        old_hashed_password = database.get_main_password(command_u)

        # Comprobando que coinciden las contraseñas
        if new_hashed_password[0] == old_hashed_password:
            print("\nCONTRASEÑA CORRECTA, BIENVENIDO ", command_u.upper())
            Interface.login_done(command_u)

        else:
            print("\nCONTRASEÑA INCORRECTA, VUELVA A INTENTARLO DE NUEVO")
            Interface.login()

    @staticmethod
    # Estado en que el usuario ya está logged in con su información
    def login_done(username):

        # Pantalla de carga
        Interface.loading()

        # Imprimiendo las opciones
        print("\n1 - AÑADIR DATOS BANCARIOS NUEVOS A TU CUENTA ")
        print("\n2 - VER DATOS BANCARIOS ")
        print("\n3 - BORRAR CUENTA")
        print("\n4 - SALIR")

        # Input del usuario
        user_command = input("\nINPUT: ")

        # Comprobando que introduce el valor correcto
        while user_command != "1" and user_command != "2" and user_command != "3" and user_command != "4":
            user_command = input("\nVALOR INCORRECTO, NUEVO INPUT: ")

        if user_command == "1":
            # Añade datos
            Interface.add_data(username)
        elif user_command == "2":
            # Imprime todas los datos
            aux = Interface.print_data(username)
            if aux == -1:
                print("\nNO HAY NINGUN DATO BANCARIO GUARDADO")
                Interface.login_done(username)
        elif user_command == "3":
            # Recogiendo base de datos
            database = DatabaseMethods()

            # Borrando en los tres base de datos
            database.borrar_datos_usuario(username, "DataBase/keys.json")
            database.borrar_datos_usuario(username, "DataBase/datos_principales.json")
            database.borrar_datos_usuario(username, "DataBase/datos_secundarios.json")

            print("\nCUENTA BORRADA!")

            Interface.inicial()
        else:
            Interface.quit_program()

        Interface.login_done(username)


    @staticmethod
    # Función para imprimir los nombres y datos bancarios
    def print_data(username):
        # Pantalla de carga
        Interface.loading()

        # Recogiendo la base de datos y cifrador
        database = DatabaseMethods
        encryption = Encryption()

        # Base de datos como diccionario
        database_value = database.get_database("DataBase/datos_secundarios.json")

        # Comprobando que existe
        try:
            database_value = database_value[username]
        except:
            return -1

        # Recogiendo valor keyA del usuario
        keyA = database.get_keyA(username)
        index = 1
        for current in database_value:
            print("\n", index, " - ", current, " : "
                  ,encryption.descifrador_aes(bytes.fromhex(keyA)
                  ,bytes.fromhex(database_value[current][1])
                  ,bytes.fromhex(database_value[current][0])))
            index += 1

    @staticmethod
    # Función que añade nuevos datos bancarios del usuario
    def add_data(username):

        # Pantalla de carga
        Interface.loading()

        # Entidad financiera y numero de cuenta
        command_u = str(input("\nENTIDAD FINANCIERA: "))
        command_c = str(input("\nNUMERO DE CUENTA: "))

        # Recogiendo la base de datos
        database = DatabaseMethods()

        # Recogiendo valor de la key del usuario
        key = database.get_keyA(username)

        # Cifrando el numero de cuenta con aes
        iv = os.urandom(16)
        aux = Encryption.cifrador_aes(command_c, bytes.fromhex(key), iv)
        password_encrypted = aux[0]

        # Valor de iv
        iv = aux[1]

        # Añadiendo a la base de datos
        message = str.encode(str(([str(command_u), str(password_encrypted), str(iv)])))
        database.write_json_datos_secundarios(username, command_u, password_encrypted, iv)

        print("\nDATOS BANCARIOS GUARDADOS!!!")

        # Redirigiendo
        Interface.login_done(username)

    @staticmethod
    # Termina el programa
    def quit_program():
        quit()


if __name__ == '__main__':
    Interface()