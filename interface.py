from Database import DatabaseMethods
from Criptografia import Criptadores
from Criptografia import FirmaDigital
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
    def new_account( command_u , command_c , command_c2):

        # Fetch por la base de datos
        database = DatabaseMethods()

        # Creando el usuario e introduciéndolo en la base de datos
        hashed_password = Criptadores.hash_hmac_password(command_c2)
        database.write_json_datos_principales(command_u, hashed_password[0], Criptadores.generar_clave_derivada(command_c2))
        database.write_json_keys_salt(command_u, hashed_password[1])

    @staticmethod
    # Estado de inicio de sesión
    def login( command_u , command_c):

        # Recogiendo usuario y contraseña
        command_u = input("\nUSUARIO: ")
        command_c = input("\nCONTRASEÑA: ")

        if  command_u == "0" :
            Interface.inicial()


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
            database.write_json_datos_principales_key(command_u, Criptadores.generar_clave_derivada(command_c))
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
        print("\n1 - AÑADIR DATOS DE SEGURO A TU CUENTA ")
        print("\n2 - VER DATOS DEL SEGURO ")
        print("\n3 - GUARDAR ARCHIVOS MEDICOS ")
        print("\n4 - RECUPERAR ARCHIVOS MEDICOS")
        print("\n5 - BORRAR CUENTA")
        print("\n6 - FIRMA DIGITAL Y CERTIFICADOS")
        print("\n7 - SALIR")

        # Input del usuario
        user_command = input("\nINPUT: ")

        # Comprobando que introduce el valor correcto
        while user_command != "1" and user_command != "2" and user_command != "3" and user_command != "4" and user_command != "5" and user_command != "6" and user_command != "7":
            user_command = input("\nVALOR INCORRECTO, NUEVO INPUT: ")

        if user_command == "1":
            # Añade datos
            Interface.add_data(username)
        elif user_command == "2":
            # Imprime todas los datos
            aux = Interface.print_data(username)
            if aux == -1:
                print("\nNO HAY NINGUN DATO DEL SEGURO GUARDADO")
                Interface.login_done(username)
        elif user_command == "3":
            database = DatabaseMethods()
            key = database.get_keyA(username)
            lista_files = Criptadores.file_encription(bytes.fromhex(key))
            aux = database.store_files(username , lista_files)

            if type(lista_files) == "NoneType":
                print("\n NO HAY ARCHIVOS PARA GUARDAR")

            else:
                for elem in lista_files:
                    if elem != "null":
                        print("\n TUS ARCHIVOS HAN SIDO GUARDADOS")
                        os.remove("Input_Files/" + elem)
                    else:
                        print("\n NO HAY ARCHIVOS PARA GUARDAR")

        elif user_command == "4":
            database = DatabaseMethods()
            key = database.get_keyA(username)
            file_list = database.get_datos_secundarios_file(username)
            if len(file_list) > 0 :
                Criptadores.file_decriptor(file_list, bytes.fromhex(key))
                print("\n ARCHIVOS RECUPERADOS")
            else:
                print("\n NO TIENES ARCHIVOS GUARDADOS")


        elif user_command == "5":
            # Recogiendo base de datos
            database = DatabaseMethods()

            # Borrando en los tres base de datos
            database.borrar_datos_usuario(username, "DataBase/keys.json")
            database.borrar_datos_usuario(username, "DataBase/datos_principales.json")
            database.borrar_datos_usuario(username, "DataBase/datos_secundarios.json")

            print("\nCUENTA BORRADA!")

            Interface.inicial()


        elif user_command == "6":
            Interface.firma_digital_menu()

        elif user_command == "7":
            DatabaseMethods.borrar_key(username, "Database/datos_principales.json")
            Interface.quit_program()

        Interface.login_done(username)

    @staticmethod
    def firma_digital_menu():
        """
        Menú para la funcionalidad de firma digital.
        """
        firma_digital = FirmaDigital()
        firma_digital.inicializar_ac()

        while True:
            Interface.loading()
            print("\n1 - GENERAR CLAVES")
            print("2 - FIRMAR MENSAJE")
            print("3 - VERIFICAR FIRMA")
            print("4 - GENERAR CERTIFICADO DE USUARIO")
            print("5 - VERIFICAR CERTIFICADO")
            print("6 - VOLVER AL MENÚ PRINCIPAL")
            Interface.loading()

            opcion = input("\nSelecciona una opción: ")

            if opcion == "1":
                usuario = input("Introduce el nombre del usuario: ")
                firma_digital.generar_claves(usuario)
                firma_digital.serializar_claves(usuario)

            elif opcion == "2":
                usuario = input("Introduce el nombre del usuario: ")
                mensaje = input("Introduce el mensaje a firmar: ")
                firma_digital.firmar_mensaje(mensaje, usuario)

            elif opcion == "3":
                usuario = input("Introduce el nombre del usuario: ")
                mensaje = input("Introduce el mensaje original: ")
                firma_path = input("Introduce la ruta de la firma (archivo .sig): ")
                firma_digital.verificar_firma(mensaje, firma_path, usuario)

            elif opcion == "4":
                usuario = input("Introduce el nombre del usuario: ")
                firma_digital.emitir_certificado_usuario(usuario)

            elif opcion == "5":
                cert_path = input("Ruta del certificado a verificar: ")
                ac_raiz_cert_path = "certificados/AC1_cert.pem"
                firma_digital.verificar_certificado(cert_path, ac_raiz_cert_path)

            elif opcion == "6":
                break




            else:
                print("Opción no válida.")

    @staticmethod
    # Función para imprimir los nombres y datos bancarios
    def print_data(username):

        # Recogiendo la base de datos y cifrador
        database = DatabaseMethods
        encryption = Criptadores()

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
        text = ""
        for current in database_value:
            text += ("\n" + str(index), " - " + str(current) + " : " +
                     str(encryption.string_decript(bytes.fromhex(keyA)
                        ,bytes.fromhex(database_value[current][1]) ,
                        bytes.fromhex(database_value[current][0]))))
            index += 1
        return text

    @staticmethod
    # Función que añade nuevos datos bancarios del usuario
    def add_data(username , command_u, command_c):


        # Recogiendo la base de datos
        database = DatabaseMethods()

        # Recogiendo valor de la key del usuario
        key = database.get_keyA(username)

        # Cifrando el numero de cuenta con aes
        iv = os.urandom(16)
        aux = Criptadores.string_encription(command_c, bytes.fromhex(key), iv )
        password_encrypted = aux[0]

        # Valor de iv
        iv = aux[1]

        # Añadiendo a la base de datos
        database.write_json_datos_secundarios(username, command_u, password_encrypted, iv)


    @staticmethod
    # Termina el programa
    def quit_program():
        quit()


if __name__ == '__main__':
    Interface()