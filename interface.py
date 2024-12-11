from Database import DatabaseMethods
from Criptografia import Criptadores
from Criptografia import FirmaDigital
from AutoridadCertificacion import Certificados
import os


# Clase de mensajes de text visibles por el usuario
class Interface:


    @staticmethod
    # Estado de crear nueva cuenta - NO BORRAR
    def new_account( command_u , command_c , command_c2):

        # Fetch por la base de datos
        database = DatabaseMethods()

        # Creando el usuario e introduciéndolo en la base de datos
        hashed_password = Criptadores.hash_hmac_password(command_c2)
        database.write_json_datos_principales(command_u, hashed_password[0], Criptadores.generar_clave_derivada(command_c2))
        database.write_json_keys_salt(command_u, hashed_password[1])


    #SE PUEDE BORRAR

    @staticmethod
    def firma_digital_menu():
        """
        Menú para la funcionalidad de firma digital.
        """
        firma_digital = FirmaDigital()
        certificado = Certificados()

        while True:
            Interface.loading()
            print("\n1 - GENERAR CLAVES")
            print("2 - FIRMAR MENSAJE")
            print("3 - VERIFICAR FIRMA")
            print("4 - VERIFICAR CERTIFICADO")
            print("5 - VOLVER AL MENÚ PRINCIPAL")
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
                cert = certificado.solicitar_certificado(usuario)
                if certificado.verificar_certificado(cert):
                    print("Certificado válido")
                else:
                    print("Certificado no válido")

            elif opcion == "5":
                break




            else:
                print("Opción no válida.")

    @staticmethod
    # Función para imprimir los nombres y datos bancarios - NO BORRAR
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
        wehavefiles = False
        for current in database_value:
            if current != "files":
                text +=  "\n" + str(index) + " - " + str(current) + " : " + str(encryption.string_decript(bytes.fromhex(keyA)
                        ,bytes.fromhex(database_value[current][1]),
                        bytes.fromhex(database_value[current][0])))
                index += 1
            else:
                wehavefiles = True
        if wehavefiles:
            text += "\n Files: "
            for filesnames in database_value["files"]:
                text = text + "\n -" + filesnames
            return text
        else:
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