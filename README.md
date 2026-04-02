# 🎣 carnada.py

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Security: AES-256-GCM](https://img.shields.io/badge/Security-AES--256--GCM-green.svg)
![Security: ChaCha20-Poly1305](https://img.shields.io/badge/Security-ChaCha20--Poly1305-orange.svg)

**Carnada** no es un simple generador de texto aleatorio. Es una herramienta diseñada bajo principios de **Ingeniería de Seguridad** para generar contraseñas de alta entropía, aplicar hashing criptográfico y proteger los resultados mediante cifrado simétrico de última generación.

---

## ✨ Características Principales

* **Generación de Alta Entropía:** Utiliza el módulo `secrets` de Python para aleatoriedad de grado criptográfico.
* **Anti-Confusión Visual:** Excluye caracteres ambiguos (como `O`, `0`, `I`, `l`) para minimizar errores humanos en el ingreso manual.
* **Derivación de Claves (KDF):** Implementa **PBKDF2-HMAC-SHA256** con 100,000 iteraciones y *Salt* aleatorio para robustecer tu frase maestra.
* **Cifrado Autenticado (AEAD):**
    * **AES-256-GCM:** El estándar industrial para almacenamiento seguro.
    * **ChaCha20-Poly1305:** Cifrado moderno y veloz, ideal para entornos móviles y protocolos como WireGuard.
* **Integridad y Verificación:** Genera automáticamente hashes **SHA-256** y **SHA-512** para cada contraseña creada.

---

## 🚀 Instalación

1.  **Requisitos:** Tener instalado Python 3.8 o superior.
2.  **Dependencias:** Instala la librería `cryptography`:
    ```bash
    pip install cryptography
    ```
3.  **Descarga:**
    ```bash
    git clone [https://github.com/tu-usuario/carnada.git](https://github.com/tu-usuario/carnada.git)
    cd carnada
    ```

---

## 🛠️ Guía de Uso (CLI)

El programa es sumamente flexible y permite automatizar la generación mediante argumentos.

### Ejemplos Rápidos:

* **Modo Interactivo:**
    ```bash
    python carnada.py
    ```
* **Contraseña de alta longitud para un usuario específico:**
    ```bash
    python carnada.py --user admin --length 24 --save
    ```
* **Solo cifrado AES-256-GCM:**
    ```bash
    python carnada.py -u db_root --cipher aes --save
    ```
* **Solo cifrado moderno ChaCha20:**
    ```bash
    python carnada.py -u wireguard_peer --cipher chacha --save
    ```

---

## 🛡️ Arquitectura de Seguridad



| Componente | Algoritmo / Parámetro | Propósito |
| :--- | :--- | :--- |
| **Generador** | `secrets.choice` | Aleatoriedad CSPRNG |
| **KDF** | PBKDF2-HMAC-SHA256 | Derivación de llave desde passphrase |
| **Iteraciones** | 100,000 | Resistencia contra fuerza bruta |
| **Cifrado 1** | AES-256-GCM | Confidencialidad e Integridad (Estándar) |
| **Cifrado 2** | ChaCha20-Poly1305 | Confidencialidad e Integridad (Moderno) |

---

## ⚠️ Notas de Seguridad

* **Frase Maestra:** El programa solicita una *passphrase* para derivar las llaves de cifrado. **No la olvides**, de lo contrario el contenido cifrado en `contrasenas_generadas.txt` será inaccesible.
* **Persistencia:** Al usar el flag `--save`, los datos se guardan en texto claro y cifrado. Asegúrate de restringir los permisos del archivo:
    ```bash
    chmod 600 contrasenas_generadas.txt
    ```

---

**Desarrollado por beathunterzero** *Entusiasta de la Caza de Amenazas*
