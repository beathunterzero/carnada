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
git clone https://github.com/beathunterzero/carnada.git
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
 
<img width="1122" height="822" alt="image" src="https://github.com/user-attachments/assets/d996b93f-bc26-4f74-b02f-3a0d60c1fa30" />

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

<img width="1139" height="819" alt="image" src="https://github.com/user-attachments/assets/86d3482e-1248-4662-9bd2-863655ccc4b9" />

<img width="907" height="441" alt="image" src="https://github.com/user-attachments/assets/67f628fe-cc6f-4d29-91bd-746e200f580f" />

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

<img width="1129" height="512" alt="image" src="https://github.com/user-attachments/assets/469ae9cd-c45d-4ccb-aeba-6267d22f645a" />

**Opciones:**  
- `--cipher aes`  
- `--cipher chacha`  

---

### 4. Definir una longitud personalizada (`--length`)

Si necesitas una contraseña más corta o mucho más larga que el estándar (18 caracteres):

```bash
python carnada.py -u mi_usuario --length 32
```

**¿Qué hace?**  
Genera una cadena de alta entropía con el tamaño exacto que indiques (ej. 32 caracteres)

<img width="1157" height="800" alt="image" src="https://github.com/user-attachments/assets/387dd0ea-eca0-42bd-85f2-9b8f6f9cc6b7" />

---

### 5. Generar claves sin símbolos (--no-symbols)

Ideal para sistemas antiguos o bases de datos que no aceptan caracteres especiales:

```bash
python carnada.py -u servicio_legacy --no-symbols
```

**¿Qué hace?**  
Filtra el generador para usar únicamente letras (mayúsculas/minúsculas) y números, manteniendo una alta entropía.

<img width="1200" height="792" alt="image" src="https://github.com/user-attachments/assets/0d205e54-fcbd-4ad1-8636-b6cd9278954d" />

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
