"""
carnada - Generador profesional de contraseñas seguras con hashing y cifrado.
"""

import argparse
import hashlib
import secrets
import string
import sys
from datetime import datetime
from getpass import getpass

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
import base64
import os

# ===================================================================
# CONFIGURACIÓN
# ===================================================================

CARACTERES_SEGUROS = (
    string.ascii_uppercase.replace('O', '').replace('I', '') +
    string.ascii_lowercase.replace('l', '').replace('o', '') +
    string.digits.replace('0', '').replace('1', '') +
    "!@#$%^&*()-_=+[]{};:,.<>/?"
)

DEFAULT_LENGTH = 18
KDF_ITERATIONS = 100_000
SALT_SIZE = 16
NONCE_SIZE = 12  # recomendado para AESGCM y ChaCha20Poly1305

# ===================================================================
# GENERACIÓN DE CONTRASEÑAS Y HASHES
# ===================================================================

def generar_contrasena(longitud: int, incluir_mayus: bool, incluir_minus: bool,
                       incluir_numeros: bool, incluir_simbolos: bool) -> str:
    if longitud < 8:
        longitud = 8

    chars = ""
    if incluir_mayus:
        chars += string.ascii_uppercase.replace('O', '').replace('I', '')
    if incluir_minus:
        chars += string.ascii_lowercase.replace('l', '').replace('o', '')
    if incluir_numeros:
        chars += string.digits.replace('0', '').replace('1', '')
    if incluir_simbolos:
        chars += "!@#$%^&*()-_=+[]{};:,.<>/?"

    if not chars:
        chars = CARACTERES_SEGUROS

    return ''.join(secrets.choice(chars) for _ in range(longitud))


def generar_hash_sha256(texto: str) -> str:
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()


def generar_hash_sha512(texto: str) -> str:
    return hashlib.sha512(texto.encode('utf-8')).hexdigest()

# ===================================================================
# KDF Y CIFRADO
# ===================================================================

def derivar_clave_desde_passphrase(passphrase: str, salt: bytes) -> bytes:
    """
    Deriva una clave de 32 bytes (256 bits) desde una passphrase usando PBKDF2-HMAC-SHA256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(passphrase.encode('utf-8'))


def cifrar_con_aes256(plaintext: str, key: bytes, salt: bytes) -> dict:
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)

    return {
        "algoritmo": "AES-256-GCM",
        "salt": base64.b64encode(salt).decode('utf-8'),
        "nonce": base64.b64encode(nonce).decode('utf-8'),
        "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
    }


def cifrar_con_chacha20(plaintext: str, key: bytes, salt: bytes) -> dict:
    chacha = ChaCha20Poly1305(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = chacha.encrypt(nonce, plaintext.encode('utf-8'), None)

    return {
        "algoritmo": "ChaCha20-Poly1305",
        "salt": base64.b64encode(salt).decode('utf-8'),
        "nonce": base64.b64encode(nonce).decode('utf-8'),
        "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
    }

# ===================================================================
# GUARDADO EN ARCHIVO
# ===================================================================

def guardar_en_archivo_modo_todo(usuario: str, contrasena: str,
                                 hash256: str, hash512: str,
                                 aes_info: dict, chacha_info: dict,
                                 passphrase: str):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("contrasenas_generadas.txt", "a", encoding="utf-8") as f:
        f.write(f"[{fecha}]\n")
        f.write(f"Usuario        : {usuario}\n")
        f.write(f"Contraseña     : {contrasena}\n")
        f.write(f"Clave maestra  : {passphrase}\n")
        f.write(f"Hash SHA-256   : {hash256}\n")
        f.write(f"Hash SHA-512   : {hash512}\n")
        f.write("AES-256-GCM:\n")
        f.write(f"  Salt (base64)  : {aes_info['salt']}\n")
        f.write(f"  Nonce (base64) : {aes_info['nonce']}\n")
        f.write(f"  Ciphertext     : {aes_info['ciphertext']}\n")
        f.write("ChaCha20-Poly1305:\n")
        f.write(f"  Salt (base64)  : {chacha_info['salt']}\n")
        f.write(f"  Nonce (base64) : {chacha_info['nonce']}\n")
        f.write(f"  Ciphertext     : {chacha_info['ciphertext']}\n")
        f.write("-" * 70 + "\n")


def guardar_en_archivo_solo_aes(usuario: str, aes_info: dict, passphrase: str):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("contrasenas_generadas.txt", "a", encoding="utf-8") as f:
        f.write(f"[{fecha}]\n")
        f.write(f"Usuario        : {usuario}\n")
        f.write(f"Clave maestra  : {passphrase}\n")
        f.write("AES-256-GCM:\n")
        f.write(f"  Salt (base64)  : {aes_info['salt']}\n")
        f.write(f"  Nonce (base64) : {aes_info['nonce']}\n")
        f.write(f"  Ciphertext     : {aes_info['ciphertext']}\n")
        f.write("-" * 70 + "\n")


def guardar_en_archivo_solo_chacha(usuario: str, chacha_info: dict, passphrase: str):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("contrasenas_generadas.txt", "a", encoding="utf-8") as f:
        f.write(f"[{fecha}]\n")
        f.write(f"Usuario        : {usuario}\n")
        f.write(f"Clave maestra  : {passphrase}\n")
        f.write("ChaCha20-Poly1305:\n")
        f.write(f"  Salt (base64)  : {chacha_info['salt']}\n")
        f.write(f"  Nonce (base64) : {chacha_info['nonce']}\n")
        f.write(f"  Ciphertext     : {chacha_info['ciphertext']}\n")
        f.write("-" * 70 + "\n")

# ===================================================================
# ARGUMENTOS CLI
# ===================================================================

def configurar_argumentos():
    parser = argparse.ArgumentParser(
        description="🎣 carnada — Generador de contraseñas seguras con hashing y cifrado",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python carnada.py --user rhodyn\n"
            "  python carnada.py -u juan -l 20 --save\n"
            "  python carnada.py -u admin --cipher aes --save\n"
            "  python carnada.py -u root --cipher chacha --save"
        )
    )

    parser.add_argument("--user", "-u", type=str, default=None,
                        help="Nombre de usuario (si no se proporciona, se pedirá)")
    
    parser.add_argument("--length", "-l", type=int, default=DEFAULT_LENGTH,
                        help=f"Longitud de la contraseña (default: {DEFAULT_LENGTH})")
    
    parser.add_argument("--no-mayus", action="store_true", help="No incluir mayúsculas")
    parser.add_argument("--no-minus", action="store_true", help="No incluir minúsculas")
    parser.add_argument("--no-numbers", action="store_true", help="No incluir números")
    parser.add_argument("--no-symbols", action="store_true", help="No incluir símbolos")
    
    parser.add_argument("--save", "-s", action="store_true",
                        help="Guardar en archivo contrasenas_generadas.txt")

    parser.add_argument(
        "--cipher",
        choices=["none", "aes", "chacha"],
        default="none",
        help="Modo de salida: none = todo, aes = solo AES, chacha = solo ChaCha20"
    )

    return parser.parse_args()

# ===================================================================
# PROGRAMA PRINCIPAL
# ===================================================================

def main():
    args = configurar_argumentos()

    # Usuario
    if not args.user:
        while True:
            usuario = input("Ingrese el nombre de usuario: ").strip()
            if usuario:
                break
            print("❌ El nombre de usuario no puede estar vacío.")
    else:
        usuario = args.user

    if args.length < 8:
        print("⚠️ Longitud mínima recomendada: 8. Se ajustará automáticamente.")

    # Clave maestra (siempre)
    print("\nSe requiere una clave maestra para derivar la clave de cifrado.")
    passphrase = getpass("Ingrese clave maestra: ")
    passphrase_confirm = getpass("Confirme clave maestra: ")

    if passphrase != passphrase_confirm:
        print("❌ Las claves maestras no coinciden. Abortando.")
        sys.exit(1)

    # Generar contraseña
    contrasena = generar_contrasena(
        longitud=args.length,
        incluir_mayus=not args.no_mayus,
        incluir_minus=not args.no_minus,
        incluir_numeros=not args.no_numbers,
        incluir_simbolos=not args.no_symbols
    )

    # Hashes
    hash256 = generar_hash_sha256(contrasena)
    hash512 = generar_hash_sha512(contrasena)

    # Derivar UNA sola clave para AES y ChaCha
    salt = os.urandom(SALT_SIZE)
    key = derivar_clave_desde_passphrase(passphrase, salt)

    aes_info = None
    chacha_info = None

    # Cifrado según modo
    if args.cipher == "none":
        aes_info = cifrar_con_aes256(contrasena, key, salt)
        chacha_info = cifrar_con_chacha20(contrasena, key, salt)
    elif args.cipher == "aes":
        aes_info = cifrar_con_aes256(contrasena, key, salt)
    elif args.cipher == "chacha":
        chacha_info = cifrar_con_chacha20(contrasena, key, salt)

    # Salida en pantalla
    print("\n" + "="*70)
    print("                 🎣 CARNADA — PASSWORD TOOL")
    print("="*70)
    print(f"Usuario               : {usuario}")
    print(f"Contraseña            : {contrasena}")
    print(f"Longitud              : {len(contrasena)} caracteres")
    print(f"Clave maestra         : {passphrase}")

    if args.cipher == "none":
        print("-" * 70)
        print("SHA-256 — Hash criptográfico usado en blockchain, firmas digitales y verificación de integridad.")
        print(f"Hash SHA-256          : {hash256}")
        print()
        print("SHA-512 — Variante más robusta de SHA-2, usada en sistemas de alta seguridad.")
        print(f"Hash SHA-512          : {hash512}")
        print("-" * 70)
        print("AES-256-GCM — Cifrado autenticado usado en HTTPS, VPNs y almacenamiento seguro.")
        print(f"Salt (base64)         : {aes_info['salt']}")
        print(f"Nonce (base64)        : {aes_info['nonce']}")
        print(f"Ciphertext (base64)   : {aes_info['ciphertext']}")
        print("-" * 70)
        print("ChaCha20-Poly1305 — Cifrado moderno usado en TLS 1.3, WireGuard y dispositivos móviles.")
        print(f"Salt (base64)         : {chacha_info['salt']}")
        print(f"Nonce (base64)        : {chacha_info['nonce']}")
        print(f"Ciphertext (base64)   : {chacha_info['ciphertext']}")
    elif args.cipher == "aes":
        print("-" * 70)
        print("AES-256-GCM — Cifrado autenticado usado en HTTPS, VPNs y almacenamiento seguro.")
        print(f"Salt (base64)         : {aes_info['salt']}")
        print(f"Nonce (base64)        : {aes_info['nonce']}")
        print(f"Ciphertext (base64)   : {aes_info['ciphertext']}")
    elif args.cipher == "chacha":
        print("-" * 70)
        print("ChaCha20-Poly1305 — Cifrado moderno usado en TLS 1.3, WireGuard y dispositivos móviles.")
        print(f"Salt (base64)         : {chacha_info['salt']}")
        print(f"Nonce (base64)        : {chacha_info['nonce']}")
        print(f"Ciphertext (base64)   : {chacha_info['ciphertext']}")

    print("="*70)

    # Guardado según modo
    if args.save:
        if args.cipher == "none":
            guardar_en_archivo_modo_todo(
                usuario, contrasena, hash256, hash512,
                aes_info, chacha_info, passphrase
            )
        elif args.cipher == "aes":
            guardar_en_archivo_solo_aes(usuario, aes_info, passphrase)
        elif args.cipher == "chacha":
            guardar_en_archivo_solo_chacha(usuario, chacha_info, passphrase)
        print("✅ Resultado guardado correctamente en 'contrasenas_generadas.txt'")

    print("¡Mantén esta información en un lugar seguro!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

