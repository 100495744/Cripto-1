#Funciones para las bases de datos
import json
import os
from cryptography.hazmat.primitives import padding


class DatabaseMethods:
    @staticmethod
    # Función borra todos los datos del usuario en la base de datos elegida
    def borrar_datos_usuario(username, path):
        # Abriendo fichero de path
        f = open(path, "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Borrando elemento en dict
        try:
            del data[username]
        except:
            return -1

        # Insertando cambios
        with open(path, 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

        # Cerrando fichero
        f.close()

    @staticmethod
    # Función devuelve el valor del key que utiliza para el cifrador AES
    def get_keyA(username):
        # Abriendo fichero de keys
        f = open("DataBase/datos_principales.json", "r")

        # Recogiendo base de datos
        data = json.load(f)
        f.close()
        # Devolviendo el valor de keyA del usuario
        return data[username]["key"]

    @staticmethod
    # Función devuelve la base de datos como diccionarios
    def get_database(path):
        # Abriendo fichero
        f = open(path, "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Devolviendo toda la base de datos en forma de dict
        return data

        # Cerrando fichero
        f.close()

    @staticmethod
    # Función comprueba si existe el username
    def username_existe(username, path):
        # Abriendo fichero
        f = open(path, "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Comprobando si existe el username
        try:
            # Sí que existe el usuario
            data[username]
            return True
        except:
            # No existe el usuario en esa base de datos
            return False

        # Cerrando fichero
        f.close()

    @staticmethod
    # Función recoge el valor del salt para ese usuario
    def get_salt(username):
        # Abriendo fichero de keys
        f = open("DataBase/keys.json", "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Comprobando si existe el username
        try:
            # Devolviendo el valor de salt para el usuario
            return data[username]["salt"]
        except:
            # No existe
            return -1

        # Cerrando fichero
        f.close()

    @staticmethod
    # Función devuelve la contraseña cifrada principal del usuario
    def get_main_password(username):
        # Abriendo fichero de keys
        f = open("DataBase/datos_principales.json", "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Comprobando si existe el username
        try:
            # Devolviendo Contraseña
            return data[username]["password"]
        except:
            # No existe
            return -1

        # Cerrando fichero
        f.close()

    @staticmethod
    # Función escribe username y contraseña cifrada en primary
    def write_json_datos_principales(username, password, key):
        # Abriendo fichero de keys
        f = open("DataBase/datos_principales.json", "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Creando la variable data con lo que necesitamos y lo introducimos
        data[username] = {}
        data[username]["password"] = password
        data[username]["key"] = key
        with open('DataBase/datos_principales.json', 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

        # Cerrando fichero
        f.close()

    @staticmethod
    # Función escribe el valor de salt y iv en la base de datos
    def write_json_keys_salt(username, key):
        # Abriendo fichero de keys
        f = open("DataBase/keys.json", "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Creando la variable data con lo que necesitamos y lo introducimos
        data[username] = {}

        # Creando la variable data con lo que necesitamos y lo introducimos
        data[username]["salt"] = key


        # Abriendo el archivo para introducirlo
        with open('DataBase/keys.json', 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

        # Cerrando fichero
        f.close()

    @staticmethod
    # Función que añade nueva informacion a la cuenta del usuario
    def write_json_datos_secundarios(username, name, password, iv):
        # Abriendo fichero de keys
        f = open("DataBase/datos_secundarios.json", "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Creando la variable data con lo que necesitamos y lo introducimos
        try:
            data[username][str(name)] = [password, iv]
        except:
            data[username] = {}
            data[username][str(name)] = [password, iv]

        # Abriendo el archivo para introducirlo
        with open('DataBase/datos_secundarios.json', 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

        # Cerrando fichero
        f.close()

    @staticmethod
    def get_datos_secundarios_file(username):
        f = open("DataBase/datos_secundarios.json", "r")

        data = json.load(f)

        return data[username]["files"][0]

    @staticmethod
    def store_files( username, file_list):
        # Abriendo fichero de keys
        f = open("DataBase/datos_secundarios.json", "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Creando la variable data con lo que necesitamos y lo introducimos
        try:
            data[username]["files"].extend(file_list)
        except:
            data[username]["files"] = file_list

        # Abriendo el archivo para introducirlo
        with open('DataBase/datos_secundarios.json', 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

        # Cerrando fichero
        f.close()

    @staticmethod
    def write_json_datos_principales_key(username, key):
        # Abriendo fichero de keys
        f = open("DataBase/datos_principales.json", "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Creando la variable data con lo que necesitamos y lo introducimos
        data[username]["key"] = key
        with open('DataBase/datos_principales.json', 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

        # Cerrando fichero
        f.close()


    @staticmethod
    # Función comprueba si está vacío la base de datos
    def is_empty(path):
        f = open(path, "r")
        data = json.load(f)
        if data == {}:
            return True
        else:
            return False

    @staticmethod
    # Función vacía el fichero
    def empty_file_content(path):
        f = open(path, 'r+')
        f.truncate(0)


    def borrar_key(username, path):
        # Abriendo fichero de path
        f = open(path, "r")

        # Recogiendo base de datos
        data = json.load(f)

        # Borrando elemento en dict
        try:
            del data[username]["key"]
        except:
            return -1

        # Insertando cambios
        with open(path, 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

        # Cerrando fichero
        f.close()


DatabaseMethods.is_empty("DataBase/datos_principales.json")