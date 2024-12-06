from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from Database import DatabaseMethods
from cryptography.hazmat.backends import default_backend
import datetime
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


class Certificados:
    def __init__(self):
        self.database = DatabaseMethods()
        self.guardar_certificado = self.database.guardar_certificado
        self.deserializar_privada = self.database.deserializar_llave_privada
        self.deserializar_publica = self.database.deserializar_llave_publica

    def solicitar_certificado(self, user):
        privada = self.deserializar_privada(user)
        self.publica = self.deserializar_publica(user)
        # Generar certificado
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Leganés"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Universidad Carlos III de Madrid"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"uc3m.es"),
        ])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.publica
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 10 days
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).sign(privada, hashes.SHA256())
        # serializamos el certificado y lo guardamos
        self.guardar_certificado(user, cert.public_bytes(serialization.Encoding.PEM))
        return cert

    def verificar_certificado(self, cert):
        try:
            self.publica.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm,
            )
            return True
        except InvalidSignature:
            return False