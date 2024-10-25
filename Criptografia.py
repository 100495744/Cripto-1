import hashlib

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import binascii
from cryptography.hazmat.primitives import hashes, hmac
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

class Criptadores:

    @staticmethod
    def file_encription( key ):
        #use key in jsons
        buffer_size = 65536

        #Take all the names of files inside the folder
        file_list = os.listdir('Input_Files')

        for in_file in file_list:

            #We open de files
            input_file = open('Input_files/'+ in_file, 'rb')

            output_file = open( 'Database/EncriptedFiles/' + in_file + '.encrypted', 'wb')

            #Create the cipher object
            cipher_encrypt = AES.new(key, AES.MODE_CFB)

            #Initially write iv to the output file
            output_file.write(cipher_encrypt.iv)

            #read from the input file to the buffer until it is full
            buffer = input_file.read(buffer_size)
            while len(buffer) > 0:
                ciphered_bytes = cipher_encrypt.encrypt(buffer)
                output_file.write(ciphered_bytes)
                buffer = input_file.read(buffer_size)

            input_file.close()
            output_file.close()
            return file_list
    @staticmethod
    def file_decriptor(file_names,key):
        buffer_size = 65536

        #we open de files
        for elem in file_names:
            input_file = open('Database/EncriptedFiles/' + str(elem) + '.encrypted','rb')
            output_file = open('Output_Files/' + str(elem), 'wb')


            #leemos el iv que hemos guardado en el archivo
            iv = input_file.read(16)

            #creamos el objeto de cifrado
            cipher_encrypt = AES.new(key, AES.MODE_CFB, iv = iv)

            #Leemos los datos encriptados
            buffer = input_file.read(buffer_size)
            while len(buffer) > 0:
                decrypted_bytes = cipher_encrypt.decrypt(buffer)
                output_file.write(decrypted_bytes)
                buffer = input_file.read(buffer_size)

            input_file.close()
            output_file.close()

    @staticmethod
    def file_comprobation(self,file_path):
        buffer_size = 65536
        file_hash = hashlib.sha256()
        with open(file_path,'rb') as f:
            fb = f.read(buffer_size)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(buffer_size)

        return file_hash.hexdigest()


    @staticmethod
    def string_encription(string,key, iv):
        #creamos el encriptador que genera un IV
        cipher_encrypt = AES.new(key, AES.MODE_CFB, iv = iv )
        texto = string.encode()
        ciphered_bytes = cipher_encrypt.encrypt(texto)

        ct = ciphered_bytes.hex()
        iv = iv.hex()
        key = key.hex()
        #devolvemos el dato encriptado y el iv
        return ct, iv , key

    @staticmethod
    def string_decript(key, iv , string):

        #creamos el encriptador con la key y el iv
        cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=iv)
        decrypted_bytes = cipher_encrypt.decrypt(string)


        return decrypted_bytes

    @staticmethod
    # Cifrado HMAC con SALT
    def hash_hmac_password(password, salt=os.urandom(8)):

        # Cifrando password con salt
        h = hmac.HMAC(salt, hashes.SHA256())
        h.update(str.encode(password))
        hash_pass = h.finalize()

        # Pasando a hexadecimal
        hash_pass = hash_pass.hex()
        salt = salt.hex()

        # Devolviendo valores en hexadecimal de contraseña y salt utilizado en b hexadecimal
        return hash_pass, salt

    def generar_clave_derivada(clave_acceso: str, iteraciones=1000, longitud_clave=32):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=longitud_clave,
            salt=b'',  # No se utiliza sal
            iterations=iteraciones,
            backend=default_backend()
        )
        clave_acceso_bytes = clave_acceso.encode('utf-8')
        clave_derivada = kdf.derive(clave_acceso_bytes)
        return binascii.hexlify(clave_derivada).decode('utf-8')