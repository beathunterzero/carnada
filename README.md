# CARNADA

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

`carnada` es una herramienta CLI local para generar contraseñas seguras y revisar contraseñas existentes desde la terminal.

El proyecto sigue un principio simple: generar credenciales fuertes sin almacenar secretos, sin enviar datos a internet y sin agregar funcionalidades innecesarias que aumenten el riesgo operativo.

---

# Descripción

`carnada` genera contraseñas aleatorias utilizando mecanismos criptográficamente seguros proporcionados por Python. También incluye un modo de análisis local de contraseñas para revisar características básicas como longitud, letras mayúsculas, letras minúsculas, números, símbolos, caracteres ambiguos y entropía aproximada.

La herramienta está diseñada para uso local, laboratorios de ciberseguridad, generación temporal de credenciales, pruebas técnicas y flujos de trabajo desde la shell.

---

# Objetivo del proyecto

`carnada` no está diseñada para reemplazar un gestor de contraseñas.

Su propósito es proporcionar una herramienta pequeña, auditable y fácil de usar para:

- generar contraseñas seguras desde la terminal;

- crear contraseñas compatibles con diferentes entornos;

- revisar contraseñas de forma local;

- integrarse con scripts mediante salida limpia o JSON;

- mantener una superficie de riesgo operativo reducida.

---

# Funcionalidades principales

- Generación segura de contraseñas utilizando aleatoriedad criptográficamente segura.

- Perfiles de generación para diferentes casos de uso.

- Estimación aproximada de entropía en bits.

- Revisión local de contraseñas.

- Generación de múltiples contraseñas en una sola ejecución.

- Modo silencioso para scripting.

- Salida JSON para automatización.

- Sin almacenamiento de contraseñas.

- Sin conexión a internet requerida.

- Sin bóveda de cifrado, gestión de secretos ni sincronización remota.

---

# ¿Qué hace?

`carnada` puede:

- generar una contraseña segura usando la configuración por defecto;

- generar contraseñas con una longitud personalizada;

- generar múltiples contraseñas;

- usar perfiles como `strong`, `legacy`, `pin`, `hex` y `wifi`;

- mostrar una estimación aproximada de entropía;

- clasificar la fortaleza aproximada de una contraseña;

- revisar una contraseña ingresada por el usuario;

- devolver salida normal, silenciosa o en formato JSON.

---

# ¿Qué no hace?

`carnada` no:

- almacena contraseñas;

- administra bóvedas de contraseñas;

- cifra archivos;

- genera hashes de contraseñas;

- sincroniza secretos;

- envía información a internet;

- reemplaza un gestor de contraseñas;

- garantiza seguridad absoluta.

Esto es intencional. La herramienta está diseñada para hacer pocas cosas de forma clara, local y auditable.

---

# Requisitos

- Python 3.10 o superior.

- No requiere dependencias externas.

- Utiliza únicamente la biblioteca estándar de Python.

---

# Instalación e inicio rápido

Clonar el repositorio:

```bash
git clone https://github.com/beathunterzero/carnada.git
cd carnada
`````

Ejecutar la herramienta:

```bash
python3 carnada.py
```

Ejecución directa opcional en Linux, WSL o macOS:

```bash
chmod +x carnada.py
./carnada.py
```

En Windows PowerShell:

```powershell
python carnada.py
```

Debido a que la herramienta no utiliza dependencias externas, no es necesario instalar paquetes adicionales.

---

# Uso básico

Generar una contraseña segura usando la configuración por defecto:

```bash
python3 carnada.py
```

Generar una contraseña de 24 caracteres:

```bash
python3 carnada.py -l 24
```

Generar una contraseña usando el perfil `legacy`:

```bash
python3 carnada.py --profile legacy
```

Generar cinco contraseñas:

```bash
python3 carnada.py --count 5
```

Imprimir únicamente la contraseña generada:

```bash
python3 carnada.py --quiet
```

Generar salida en formato JSON:

```bash
python3 carnada.py --json
```

Revisar una contraseña de forma local:

```bash
python3 carnada.py check
```

Revisar una contraseña directamente desde la línea de comandos:

```bash
python3 carnada.py check "Password123!"
```

---

# Perfiles disponibles

## `strong`

Perfil recomendado para uso general. Utiliza letras mayúsculas, letras minúsculas, números y símbolos. Está diseñado para generar contraseñas fuertes para sistemas modernos.

## `legacy`

Perfil compatible con sistemas antiguos o restrictivos. Utiliza letras y números, evitando símbolos complejos.

## `pin`

Perfil numérico. Útil para PINs temporales o códigos numéricos cortos.

## `hex`

Perfil de token hexadecimal. Útil para pruebas técnicas, laboratorios o flujos de trabajo que requieren salida hexadecimal.

## `wifi`

Perfil para contraseñas Wi-Fi largas y compatibles. Evita símbolos complejos para facilitar el ingreso manual en dispositivos.

---

# Ejemplos de salida

Ejemplo de generación normal:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : V7#kQm92@tLx8pRz
Profile  : strong
Length   : 18
Charset  : 82 characters
Entropy  : ~114.44 bits
Rating   : very strong
```

Ejemplo de modo silencioso:

```text
V7#kQm92@tLx8pRz
```

Ejemplo de revisión de contraseña:

```text
CARNADA — Password Check
------------------------------------------
Length          : 12
Uppercase       : yes
Lowercase       : yes
Numbers         : yes
Symbols         : yes
Ambiguous chars : yes
Entropy         : ~78.66 bits
Rating          : strong
```

---

# Seguridad y diseño

`carnada` sigue un diseño local-first.

Todas las operaciones se realizan localmente en el equipo del usuario. La herramienta no envía contraseñas a servicios externos, no realiza solicitudes remotas y no requiere conexión a internet.

La generación de contraseñas utiliza el módulo `secrets` de Python, adecuado para generar valores aleatorios criptográficamente seguros.

La herramienta evita almacenar secretos por diseño. No crea archivos que contengan contraseñas, no almacena claves maestras y no mantiene historial propio.

---

# Sobre la entropía

La entropía mostrada por `carnada` es una estimación aproximada basada en la longitud de la contraseña y el tamaño del conjunto de caracteres utilizado.

Esta métrica proporciona una referencia general sobre la fortaleza de contraseñas generadas aleatoriamente, pero no debe interpretarse como una garantía absoluta de seguridad.

La seguridad real también depende del contexto de uso, la política del sistema, la exposición del secreto, las prácticas de almacenamiento, la reutilización de contraseñas y controles de seguridad adicionales.

---

# Consideraciones importantes

* No reutilizar contraseñas entre diferentes servicios.

* No pegar contraseñas sensibles en sistemas no confiables.

* No compartir contraseñas mediante canales inseguros.

* Utilizar un gestor de contraseñas para almacenar credenciales permanentes.

* Usar `carnada` como generador local o herramienta de apoyo, no como bóveda de secretos.

---

# Estructura del proyecto

```text
CARNADA/
├── carnada.py
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── usage.md
│   ├── security-notes.md
│   └── architecture/
│       ├── overview.md
│       └── carnada-architecture.png
└── examples/
    └── usage-examples.md
```

---

# Documentación adicional

La documentación extendida está disponible en el directorio `docs/`.

Guía de uso:

```text
docs/usage.md
```

Notas de seguridad:

```text
docs/security-notes.md
```

Descripción de arquitectura:

```text
docs/architecture/overview.md
```

Ejemplos prácticos:

```text
examples/usage-examples.md
```

---

# Estado del proyecto

Este proyecto está pensado como una herramienta personal de línea de comandos con enfoque educativo, práctico y defensivo en ciberseguridad.

La versión inicial mantiene el alcance intencionalmente reducido y evita funcionalidades que incrementarían innecesariamente el riesgo, como almacenamiento de secretos, cifrado de bóvedas o sincronización remota.

---

# Licencia

Este proyecto se distribuye bajo la licencia especificada en el archivo `LICENSE`.

---

# Autor

**beathunterzero**
