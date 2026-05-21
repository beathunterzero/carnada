# CARNADA Architecture Overview

`carnada` está diseñada como una herramienta pequeña de línea de comandos con enfoque local-first.

La arquitectura sigue un flujo simple: recibir la entrada del usuario desde la shell, resolver el modo de ejecución, generar o analizar una contraseña, calcular metadatos útiles y devolver una salida limpia en la terminal.

La herramienta no utiliza servicios externos, no almacena secretos y no requiere dependencias de terceros.

---

# Principios de diseño

La arquitectura se basa en los siguientes principios:

- ejecución únicamente local;

- sin almacenamiento de contraseñas;

- sin comunicación de red;

- sin dependencias externas;

- separación clara entre generación, análisis, formateo y parsing de CLI;

- riesgo operativo mínimo;

- salida limpia adecuada para uso en terminal y scripting.

`carnada` tiene un alcance intencionalmente reducido. No es un gestor de contraseñas, no es una bóveda y no es un sistema de almacenamiento de secretos.

---

# Arquitectura de alto nivel

La herramienta está organizada alrededor de un único script ejecutable de Python:

```text
carnada.py
````

Internamente, el script se divide en componentes lógicos:

```text
CLI Parser
Profile Resolver
Charset Builder
Password Generator
Password Analyzer
Entropy Calculator
Output Formatter
```

Cada componente tiene una responsabilidad específica.

---

# Diagrama de arquitectura

```text
User / Shell
     |
     v
Command-line Arguments
     |
     v
CLI Parser
     |
     +-------------------------+
     |                         |
     v                         v
Generate Mode              Check Mode
     |                         |
     v                         v
Profile Resolver           Password Input
     |                         |
     v                         v
Charset Builder            Password Analyzer
     |                         |
     v                         v
Secure Password Generator  Entropy Calculator
     |                         |
     v                         v
Entropy Calculator         Output Formatter
     |                         |
     +-----------+-------------+
                 |
                 v
          Terminal Output
       normal / quiet / JSON
```

---

# Responsabilidades de los componentes

## 1. CLI Parser

El parser de CLI recibe y valida los argumentos de línea de comandos.

Es responsable de manejar comandos como:

```bash
python3 carnada.py
python3 carnada.py --profile legacy
python3 carnada.py --count 5
python3 carnada.py --quiet
python3 carnada.py --json
python3 carnada.py check
```

Responsabilidades principales:

* interpretar argumentos de línea de comandos;

* identificar el modo de ejecución;

* validar opciones aceptadas;

* enrutar la ejecución hacia el modo de generación o el modo de revisión.

El parser está implementado usando el módulo estándar `argparse` de Python.

---

## 2. Generate Mode

El modo de generación es el comportamiento por defecto de la herramienta.

Su propósito es crear una o más contraseñas seguras utilizando aleatoriedad criptográficamente segura.

Ejemplo:

```bash
python3 carnada.py
```

Responsabilidades principales:

* cargar el perfil seleccionado;

* aplicar modificaciones del usuario, como longitud o grupos de caracteres deshabilitados;

* construir el conjunto final de caracteres;

* generar la cantidad solicitada de contraseñas;

* calcular metadatos de entropía;

* formatear el resultado para salida en terminal.

---

## 3. Check Mode

El modo de revisión analiza una contraseña existente de forma local.

Ejemplo:

```bash
python3 carnada.py check
```

La contraseña puede proporcionarse como argumento o solicitarse de forma interactiva.

Ejemplo con entrada directa:

```bash
python3 carnada.py check "Password123!"
```

Ejemplo con entrada oculta:

```bash
python3 carnada.py check
```

Responsabilidades principales:

* recibir una contraseña para análisis;

* detectar categorías de caracteres;

* detectar caracteres ambiguos;

* estimar entropía;

* asignar una clasificación de fortaleza;

* imprimir el resultado sin almacenar la contraseña.

Cuando no se pasa una contraseña como argumento, la herramienta debe solicitarla de forma segura usando entrada oculta.

---

# Flujo de generación

El flujo de generación funciona de la siguiente manera:

```text
1. El usuario ejecuta carnada desde la shell.
2. El CLI parser lee los argumentos.
3. Se carga el perfil seleccionado.
4. Se aplican modificaciones opcionales del usuario.
5. Se construyen los grupos de caracteres.
6. La contraseña se genera usando aleatoriedad criptográficamente segura.
7. Se estima la entropía.
8. Se formatea el resultado.
9. La salida se imprime en la terminal.
```

Ejemplo:

```bash
python3 carnada.py --profile strong -l 24
```

Flujo interno esperado:

```text
profile = strong
length = 24
charset = uppercase + lowercase + numbers + symbols
generator = secrets-based random selection
output = normal terminal format
```

---

# Flujo de revisión

El flujo de revisión funciona de la siguiente manera:

```text
1. El usuario ejecuta carnada en modo check.
2. El CLI parser detecta el comando check.
3. La contraseña se recibe desde argumento o prompt oculto.
4. El analizador inspecciona la estructura de la contraseña.
5. Se estima la entropía.
6. Se calcula la clasificación de fortaleza.
7. La salida se imprime en la terminal.
```

Ejemplo:

```bash
python3 carnada.py check
```

Flujo interno esperado:

```text
input = hidden password prompt
analysis = length, uppercase, lowercase, numbers, symbols, ambiguous chars
output = password check report
```

---

# Diseño de generación de contraseñas

La generación de contraseñas utiliza el módulo `secrets` de Python.

Este módulo está diseñado para generar valores aleatorios criptográficamente seguros.

El generador debe asegurar que se incluya al menos un carácter de cada grupo de caracteres activo.

Por ejemplo, si los grupos activos son:

```text
uppercase
lowercase
numbers
symbols
```

La contraseña generada debe contener al menos un carácter de cada grupo.

Después de seleccionar los caracteres requeridos, los caracteres restantes se eligen aleatoriamente desde el conjunto completo de caracteres. La lista final se mezcla antes de devolverse.

Esto evita generar contraseñas que accidentalmente no incluyan una categoría habilitada.

---

# Grupos de caracteres

`carnada` utiliza grupos de caracteres configurables:

```text
uppercase letters
lowercase letters
numbers
symbols
```

La herramienta también puede remover caracteres visualmente ambiguos por defecto.

Ejemplos de caracteres ambiguos:

```text
O
0
I
1
l
o
```

Esto mejora la legibilidad cuando las contraseñas deben copiarse manualmente o escribirse en otro dispositivo.

---

# Perfiles

Los perfiles definen el comportamiento de generación por defecto para casos de uso específicos.

Perfiles actuales:

```text
strong
legacy
pin
hex
wifi
```

## strong

Perfil por defecto para uso general.

Utiliza:

```text
uppercase
lowercase
numbers
symbols
```

## legacy

Diseñado para sistemas antiguos o restrictivos.

Utiliza:

```text
uppercase
lowercase
numbers
```

## pin

Diseñado para códigos numéricos.

Utiliza:

```text
numbers
```

## hex

Diseñado para tokens hexadecimales.

Utiliza:

```text
0123456789abcdef
```

## wifi

Diseñado para contraseñas Wi-Fi largas y más fáciles de escribir manualmente.

Utiliza:

```text
uppercase
lowercase
numbers
```

---

# Estimación de entropía

`carnada` estima la entropía usando la longitud de la contraseña y el tamaño del conjunto de caracteres.

Conceptualmente:

```text
entropy = password_length × log2(character_set_size)
```

El resultado se muestra en bits.

Este valor es una aproximación. Es útil para comparar contraseñas generadas, pero no representa una garantía completa de seguridad.

La clasificación final de fortaleza se deriva de la entropía estimada.

Modelo de clasificación de ejemplo:

```text
less than 40 bits      weak
40 to 69 bits          moderate
70 to 99 bits          strong
100 bits or more       very strong
```

---

# Capa de salida

La capa de salida formatea los resultados para diferentes escenarios de uso.

Modos de salida soportados:

```text
normal
quiet
JSON
```

## Normal Output

Salida legible para humanos en la terminal.

Ejemplo:

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

## Quiet Output

Imprime únicamente la contraseña generada.

Esto es útil para shell scripting.

Ejemplo:

```bash
python3 carnada.py --quiet
```

Salida:

```text
V7#kQm92@tLx8pRz
```

## JSON Output

Proporciona una salida estructurada para automatización.

Ejemplo:

```bash
python3 carnada.py --json
```

Salida:

```json
{
  "profile": "strong",
  "count": 1,
  "length": 18,
  "charset_size": 82,
  "entropy_bits": 114.44,
  "rating": "very strong",
  "passwords": [
    "V7#kQm92@tLx8pRz"
  ]
}
```

---

# Límites de seguridad

`carnada` no cruza los siguientes límites:

```text
no password storage
no local vault
no encryption layer
no remote API
no telemetry
no cloud synchronization
no database
```

Este límite es intencional.

La herramienta genera o revisa contraseñas localmente y luego finaliza su ejecución.

---

# Manejo de datos

`carnada` no persiste contraseñas generadas ni contraseñas revisadas.

Los datos existen únicamente durante la ejecución.

La herramienta no crea archivos de salida por defecto.

La entrada de contraseña en modo check debe usar entrada oculta cuando no se proporciona una contraseña como argumento.

Los usuarios deben evitar pasar contraseñas reales sensibles directamente en la línea de comandos, porque el historial de la shell podría almacenarlas.

Recomendado:

```bash
python3 carnada.py check
```

Menos recomendado:

```bash
python3 carnada.py check "MySensitivePassword"
```

---

# Modelo de dependencias

`carnada` utiliza únicamente la biblioteca estándar de Python.

Módulos principales:

```text
argparse
json
math
secrets
string
sys
dataclasses
getpass
```

No se requieren dependencias externas.

Esto mantiene la instalación simple y reduce el riesgo de supply chain.

---

# Modelo de ejecución

La herramienta puede ejecutarse directamente con Python:

```bash
python3 carnada.py
```

En Linux, WSL o macOS, también puede ejecutarse directamente si el archivo tiene permisos de ejecución:

```bash
chmod +x carnada.py
./carnada.py
```

El script incluye una línea shebang:

```python
#!/usr/bin/env python3
```

Esto permite que el sistema ubique el intérprete de Python adecuado.

---

# Alcance de la arquitectura

La arquitectura actual es intencionalmente simple.

`carnada` no necesita una estructura de paquete ni separación compleja por módulos en esta etapa, porque el proyecto es pequeño y no tiene dependencias externas.

Una arquitectura de archivo único es aceptable mientras la herramienta se mantenga enfocada en:

```text
password generation
password checking
entropy estimation
terminal output
```

Si el proyecto crece significativamente, más adelante podría separarse en módulos como:

```text
cli.py
profiles.py
generator.py
analyzer.py
formatter.py
```

Por ahora, mantener todo en `carnada.py` mejora la portabilidad y facilita la auditoría de la herramienta.

---

# Resumen

`carnada` sigue una arquitectura mínima con enfoque local-first.

La herramienta recibe entrada desde la shell, enruta la ejecución mediante un parser de CLI, realiza generación o análisis de contraseñas, estima entropía y muestra el resultado en un formato limpio.

Su principal decisión de seguridad es evitar almacenar, transmitir o gestionar secretos.

Esto mantiene el proyecto pequeño, auditable y práctico para flujos de trabajo basados en terminal.
