import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import binascii
from cryptography.hazmat.primitives import hashes, hmac
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
import os



class Criptadores:

    @staticmethod
    def file_encription( key , file_list ):
        #use key in jsons
        buffer_size = 65536

        #Take all the names of files inside the folder


        for in_file in file_list:

            #We open de files
            input_file = open(in_file, 'rb')

            output_file = open( 'Database/EncriptedFiles/' + os.path.basename(in_file) + '.encrypted', 'wb')

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
        h = hashes.Hash(hashes.SHA256(), backend=default_backend())
        h.update(salt)
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



class FirmaDigital:
    def __init__(self):
        self.private_key = None
        self.public_key = None


    def generar_claves(self, usuario):
        """
        Genera un par de claves (privada y pública) y las guarda en carpetas específicas.
        """
        # Generar clave privada
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        # Generar clave pública
        self.public_key = self.private_key.public_key()

        # Serializar y guardar claves
        self.serializar_claves(usuario)

        print(f"Claves generadas y guardadas para el usuario: {usuario}")

    def serializar_claves(self, usuario):
        """
        Serializa y guarda las claves en las carpetas correspondientes.
        """
        # Crear carpetas si no existen
        os.makedirs("llave_priv", exist_ok=True)
        os.makedirs("llave_pub", exist_ok=True)

        # Guardar clave privada
        with open(f"llave_priv/{usuario}_private_key.pem", "wb") as private_file:
            private_file.write(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
        # Guardar clave pública
        with open(f"llave_pub/{usuario}_public_key.pem", "wb") as public_file:
            public_file.write(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

    def firmar_mensaje(self, mensaje, usuario):
        """
        Firma un mensaje con la clave privada y guarda la firma en una carpeta específica.
        """
        # Crear carpeta para firmas si no existe
        os.makedirs("firmas", exist_ok=True)

        # Cargar clave privada
        with open(f"llave_priv/{usuario}_private_key.pem", "rb") as private_file:
            private_key = serialization.load_pem_private_key(
                private_file.read(),
                password=None,
                backend=default_backend()
            )

        # Firmar el mensaje
        firma = private_key.sign(
            mensaje.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Guardar firma
        with open(f"firmas/{usuario}_firma.sig", "wb") as firma_file:
            firma_file.write(firma)

        print("Mensaje firmado y guardado en la carpeta de firmas.")
        return firma

    import base64

    def verificar_firma(self, mensaje, firma_path, usuario):
        """
        Verifica una firma en formato binario usando la clave pública.
        """
        # Cargar clave pública
        with open(f"llave_pub/{usuario}_public_key.pem", "rb") as public_file:
            public_key = serialization.load_pem_public_key(
                public_file.read(),
                backend=default_backend()
            )

        # Leer firma en formato binario
        with open(firma_path, "rb") as firma_file:
            firma = firma_file.read()

        # Verificar la firma
        try:
            public_key.verify(
                firma,
                mensaje.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("La firma es válida.")
            return True
        except Exception as e:
            print(f"La firma no es válida: {e}")
            return False
