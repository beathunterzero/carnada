# 🎣 carnada.py

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Security: AES-256-GCM](https://img.shields.io/badge/Security-AES--256--GCM-green.svg)
![Security: ChaCha20-Poly1305](https://img.shields.io/badge/Security-ChaCha20--Poly1305-orange.svg)

**Carnada** es una herramienta profesional para generar contraseñas seguras. No solo crea claves difíciles de adivinar, sino que también las protege usando tecnología de cifrado avanzada (la misma que usan los bancos y las VPNs).

---

## 🚀 Instalación

### Requisitos
- Tener instalado **Python 3.8 o superior**

### Dependencias
Instala la librería necesaria:

```bash
pip install cryptography
```

### Descarga

```bash
git clone https://github.com/tu-usuario/carnada.git
cd carnada
```

---

## 🛠️ Guía de Uso Rápido (Manual)

El uso de **Carnada** es muy sencillo. Aquí tienes los escenarios más comunes:

---

### 1. El modo más simple (Interactivo)

Si solo ejecutas el programa, este te preguntará los datos necesarios paso a paso.

```bash
python carnada.py
```

**¿Qué hace?**  
Te pedirá un nombre de usuario y una **Clave Maestra**.

**Resultado:**  
- Genera una contraseña  
- Muestra en pantalla:
  - SHA-256  
  - SHA-512  
  - AES-256  
  - ChaCha20  

**Importante:**  
No guarda nada en archivo, solo se ve en tu terminal.

---

### 2. Guardar los resultados en un archivo (`--save`)

Si quieres que la información se guarde para consultarla después:

```bash
python carnada.py -u mi_usuario --save
```

**¿Qué hace?**  
Genera la contraseña y crea (o actualiza) un archivo llamado:

```
contrasenas_generadas.txt
```

**Importante:**  
El parámetro `-s` o `--save` es lo que activa el guardado.  
Si no lo pones, solo verás los datos en consola.

---

### 3. Ver solo un tipo de cifrado (`--cipher`)

Si solo necesitas un formato específico en pantalla para copiarlo rápido:

```bash
python carnada.py -u admin --cipher chacha
```

**¿Qué hace?**  
Limpia la pantalla para mostrarte únicamente el resultado en **ChaCha20-Poly1305**.

**Opciones:**  
- `--cipher aes`  
- `--cipher chacha`  

---

## 📖 Explicación de los Comandos

| Comando | Para qué sirve |
|--------|---------------|
| `-u` o `--user` | Indica el nombre de la cuenta (ej. Facebook, Admin, SSH) |
| `-l` o `--length` | Define qué tan larga será la contraseña (ej. `-l 20`) |
| `--save` | Guarda todo en `contrasenas_generadas.txt` |
| `--cipher` | Elige qué algoritmo mostrar (`aes` o `chacha`) |
| `--no-symbols` | Genera una clave sin símbolos (solo letras y números) |

---

## 🔐 ¿Qué algoritmos utiliza Carnada?

Para que tu información sea impenetrable, el programa trabaja con cuatro estándares de la industria:

- **SHA-256 / SHA-512**  
  Crean una "huella digital" única de tu contraseña (Hashing).

- **AES-256-GCM**  
  El estándar de cifrado más utilizado en el mundo (Gobiernos y Militares).

- **ChaCha20-Poly1305**  
  Un cifrado moderno, extremadamente rápido y seguro, ideal para dispositivos móviles.

---

## ⚠️ Recordatorio Importante

La **Clave Maestra** que el programa te pide al inicio es la "llave" para tus contraseñas.

- Si guardas tus contraseñas con `--save`, necesitarás esa misma clave para descifrarlas en el futuro.  
- **¡No la pierdas!**

**Desarrollado por beathunterzero** *Entusiasta de la Caza de Amenazas*
