from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

class Criptadores:

    def file_encription(self, key ):
        #use key in jsons
        buffer_size = 65536

        #Take all the names of files inside the folder
        file_list = os.listdir('Input_Archivos')

        for in_file in file_list:

            #We open de files
            input_file = open('Input_Archivos/'+ in_file, 'rb')

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


    def file_decriptor(self,file_names,key):
        buffer_size = 65536

        #we open de files
        for elem in file_names:
            input_file = open('Database/EncriptedFiles/' + elem + '.encrypted','rb')
            output_file = open('Output_Files/' + elem, 'wb')


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


