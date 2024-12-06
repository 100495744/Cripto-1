from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import CertificateBuilder, BasicConstraints
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
import os


class AutoridadCertificacion:
    def __init__(self, nombre, es_raiz=True, cert_padre=None, clave_privada_padre=None):
        """
        Inicializa la AC (raíz o subordinada).
        """
        self.nombre = nombre
        self.es_raiz = es_raiz
        self.cert_padre = cert_padre
        self.clave_privada_padre = clave_privada_padre

        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.certificado = None

        if es_raiz:
            self.generar_certificado_raiz()
        else:
            self.generar_certificado_subordinado()

    def generar_certificado_raiz(self):
        """
        Genera un certificado autofirmado para la AC raíz.
        """
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.nombre),
            x509.NameAttribute(NameOID.COMMON_NAME, self.nombre),
        ])
        self.certificado = CertificateBuilder().subject_name(subject).issuer_name(subject).public_key(
            self.public_key).serial_number(x509.random_serial_number()).not_valid_before(
            datetime.datetime.utcnow()).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=3650)).add_extension(
            BasicConstraints(ca=True, path_length=None), critical=True).sign(self.private_key, hashes.SHA256())
        self.guardar_claves_y_certificado()

    def generar_certificado_subordinado(self):
        """
        Genera un certificado firmado por la AC padre.
        """
        if not self.cert_padre or not self.clave_privada_padre:
            raise ValueError(
                "Se requiere un certificado y clave privada de la AC padre para generar una AC subordinada.")

        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.nombre),
            x509.NameAttribute(NameOID.COMMON_NAME, self.nombre),
        ])
        self.certificado = CertificateBuilder().subject_name(subject).issuer_name(self.cert_padre.subject).public_key(
            self.public_key).serial_number(x509.random_serial_number()).not_valid_before(
            datetime.datetime.utcnow()).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)).add_extension(
            BasicConstraints(ca=True, path_length=0), critical=True).sign(self.clave_privada_padre, hashes.SHA256())
        self.guardar_claves_y_certificado()

    def guardar_claves_y_certificado(self):
        """
        Guarda las claves y el certificado en archivos.
        """
        os.makedirs("certificados", exist_ok=True)
        with open(f"certificados/{self.nombre}_private_key.pem", "wb") as f:
            f.write(self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                   format=serialization.PrivateFormat.PKCS8,
                                                   encryption_algorithm=serialization.NoEncryption()))
        with open(f"certificados/{self.nombre}_cert.pem", "wb") as f:
            f.write(self.certificado.public_bytes(encoding=serialization.Encoding.PEM))

    def emitir_certificado_usuario(self, nombre_usuario, public_key):
        """
        Emite un certificado para un usuario final.
        """
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.COMMON_NAME, nombre_usuario),
        ])
        cert = CertificateBuilder().subject_name(subject).issuer_name(self.certificado.subject).public_key(
            public_key).serial_number(x509.random_serial_number()).not_valid_before(
            datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).sign(
            self.private_key, hashes.SHA256())

        with open(f"certificados/{nombre_usuario}_cert.pem", "wb") as f:
            f.write(cert.public_bytes(encoding=serialization.Encoding.PEM))
        print(f"Certificado emitido para el usuario '{nombre_usuario}'.")

    @staticmethod
    def cargar_certificado_y_clave(cert_path, key_path):
        """
        Carga un certificado y su clave privada desde archivos.
        """
        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())
        with open(key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        return cert, private_key


