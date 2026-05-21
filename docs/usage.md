# CARNADA Usage Guide

`carnada` es una herramienta local-first de línea de comandos para generar contraseñas seguras y revisar contraseñas existentes desde la terminal.

Esta guía explica los principales modos de uso, perfiles disponibles, opciones de comandos y ejemplos prácticos.

---

# Requisitos

`carnada` requiere:

```text
Python 3.10 o superior
````

No requiere dependencias externas.

La herramienta utiliza únicamente la biblioteca estándar de Python.

---

# Ejecutar la herramienta

Desde el directorio del proyecto, ejecutar:

```bash
python3 carnada.py
```

En Windows PowerShell:

```powershell
python carnada.py
```

En Linux, WSL o macOS, opcionalmente se puede asignar permiso de ejecución al script:

```bash
chmod +x carnada.py
./carnada.py
```

---

# Generación básica de contraseñas

Generar una contraseña segura usando el perfil por defecto:

```bash
python3 carnada.py
```

Ejemplo de salida:

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

Por defecto, `carnada` utiliza el perfil `strong`.

---

# Longitud personalizada de contraseña

Usar `-l` o `--length` para definir una longitud personalizada.

```bash
python3 carnada.py -l 24
```

Comando equivalente:

```bash
python3 carnada.py --length 24
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : N9#rVx28@LmQ7sKpT4zW!a
Profile  : strong
Length   : 24
Charset  : 82 characters
Entropy  : ~152.59 bits
Rating   : very strong
```

---

# Perfiles de generación

Los perfiles proporcionan configuraciones predefinidas para diferentes escenarios de uso.

Usar un perfil con:

```bash
python3 carnada.py --profile <profile_name>
```

Perfiles disponibles:

```text
strong
legacy
pin
hex
wifi
```

---

## strong

Perfil por defecto para uso general.

Utiliza:

```text
letras mayúsculas
letras minúsculas
números
símbolos
```

Ejemplo:

```bash
python3 carnada.py --profile strong
```

---

## legacy

Perfil compatible con sistemas restrictivos o antiguos.

Utiliza:

```text
letras mayúsculas
letras minúsculas
números
```

No utiliza símbolos.

Ejemplo:

```bash
python3 carnada.py --profile legacy
```

Este perfil es útil cuando un sistema rechaza caracteres especiales o tiene restricciones antiguas de política de contraseñas.

---

## pin

Perfil numérico.

Utiliza:

```text
solo números
```

Ejemplo:

```bash
python3 carnada.py --profile pin
```

También se puede definir una longitud personalizada para el PIN:

```bash
python3 carnada.py --profile pin -l 8
```

---

## hex

Perfil de token hexadecimal.

Utiliza:

```text
0123456789abcdef
```

Ejemplo:

```bash
python3 carnada.py --profile hex
```

Este perfil es útil para laboratorios, pruebas técnicas o flujos de trabajo que requieren valores hexadecimales.

---

## wifi

Perfil para contraseñas Wi-Fi largas y compatibles.

Utiliza:

```text
letras mayúsculas
letras minúsculas
números
```

Ejemplo:

```bash
python3 carnada.py --profile wifi
```

Este perfil evita símbolos complejos para facilitar la escritura manual en teléfonos, routers, televisores inteligentes, consolas y dispositivos IoT.

---

# Generar múltiples contraseñas

Usar `-c` o `--count` para generar más de una contraseña.

```bash
python3 carnada.py --count 5
```

Comando equivalente:

```bash
python3 carnada.py -c 5
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Profile  : strong
Count    : 5
Length   : 18
Entropy  : ~114.44 bits each
Rating   : very strong
------------------------------------------
1. V7#kQm92@tLx8pRz
2. B4!sKp81@TxQ9mVw
3. M8#qLn73@RvX2pZa
4. K5@wTr49#LpQ8nXs
5. Z9!vMc61@HsT3qRb
```

Esto es útil cuando se necesitan varias credenciales temporales o se desea elegir entre múltiples opciones generadas.

---

# Modo silencioso

El modo silencioso imprime únicamente la contraseña generada.

Uso:

```bash
python3 carnada.py --quiet
```

Comando equivalente:

```bash
python3 carnada.py -q
```

Ejemplo de salida:

```text
V7#kQm92@tLx8pRz
```

El modo silencioso es útil para shell scripting.

Ejemplo:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

Usar esto con cuidado. Las contraseñas almacenadas en variables de shell aún pueden quedar expuestas mediante logs, salida de depuración o comandos posteriores.

---

# Salida JSON

Usar `--json` para imprimir salida estructurada.

```bash
python3 carnada.py --json
```

Ejemplo de salida:

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

La salida JSON es útil para automatización o integración con otras herramientas.

Evitar redirigir contraseñas reales hacia archivos, salvo que se entienda el riesgo.

Ejemplo a evitar con credenciales sensibles:

```bash
python3 carnada.py --json > password.json
```

Esto crea un archivo en texto plano que contiene la contraseña generada.

---

# Opciones de grupos de caracteres

`carnada` permite deshabilitar grupos específicos de caracteres.

Opciones disponibles:

```text
--no-upper
--no-lower
--no-numbers
--no-symbols
```

Ejemplos:

Generar una contraseña sin símbolos:

```bash
python3 carnada.py --no-symbols
```

Generar una contraseña solo con letras minúsculas y números:

```bash
python3 carnada.py --no-upper --no-symbols
```

Generar una contraseña sin números:

```bash
python3 carnada.py --no-numbers
```

Debe permanecer habilitado al menos un grupo de caracteres.

---

# Caracteres ambiguos

Por defecto, `carnada` evita caracteres visualmente ambiguos.

Ejemplos:

```text
O
0
I
1
l
o
```

Esto facilita la lectura y escritura manual de contraseñas.

Para permitir caracteres ambiguos, usar:

```bash
python3 carnada.py --allow-ambiguous
```

Esto puede aumentar ligeramente el conjunto de caracteres disponible.

---

# Modo de revisión de contraseña

`carnada` puede revisar una contraseña existente de forma local.

Uso:

```bash
python3 carnada.py check
```

La herramienta solicitará la contraseña usando entrada oculta.

Ejemplo:

```text
Password to check:
```

Este es el método recomendado porque la contraseña no se pasa directamente por la línea de comandos de la shell.

Ejemplo de salida:

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

# Revisar una contraseña desde la línea de comandos

También se puede proporcionar la contraseña directamente como argumento:

```bash
python3 carnada.py check "Password123!"
```

Esto es menos recomendable para contraseñas reales sensibles porque puede almacenarse en el historial de la shell o quedar visible mediante inspección de procesos.

Usar esta forma principalmente para pruebas, ejemplos o valores no sensibles.

---

# Salida JSON en modo check

Usar `--json` con el modo `check`:

```bash
python3 carnada.py check --json
```

Ejemplo de salida:

```json
{
  "length": 12,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "symbols": true,
  "ambiguous_chars": true,
  "entropy_bits": 78.66,
  "rating": "strong"
}
```

También se puede revisar un valor proporcionado directamente:

```bash
python3 carnada.py check "Password123!" --json
```

---

# Menú de ayuda

Para mostrar el menú principal de ayuda:

```bash
python3 carnada.py --help
```

Para mostrar ayuda del modo generate:

```bash
python3 carnada.py generate --help
```

Para mostrar ayuda del modo check:

```bash
python3 carnada.py check --help
```

---

# Versión

Para mostrar la versión de la herramienta:

```bash
python3 carnada.py --version
```

Ejemplo de salida:

```text
carnada 1.0.0
```

---

# Patrones comunes de uso

Generar una contraseña fuerte:

```bash
python3 carnada.py
```

Generar una contraseña más larga:

```bash
python3 carnada.py -l 32
```

Generar una contraseña para un sistema restrictivo:

```bash
python3 carnada.py --profile legacy
```

Generar una contraseña compatible para Wi-Fi:

```bash
python3 carnada.py --profile wifi
```

Generar un PIN numérico:

```bash
python3 carnada.py --profile pin -l 6
```

Generar un token hexadecimal:

```bash
python3 carnada.py --profile hex
```

Generar múltiples candidatos:

```bash
python3 carnada.py --count 10
```

Usar la salida en una variable de shell:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

Revisar una contraseña de forma segura usando entrada oculta:

```bash
python3 carnada.py check
```

---

# Prácticas recomendadas

Usar el perfil `strong` por defecto para contraseñas generales.

Usar `legacy` solo cuando un sistema rechace símbolos.

Usar `wifi` cuando la contraseña deba escribirse manualmente en varios dispositivos.

Usar el modo `check` sin pasar contraseñas reales sensibles directamente como argumentos de línea de comandos.

Usar `--quiet` con cuidado en scripts.

Evitar redirigir contraseñas generadas hacia archivos en texto plano.

Almacenar credenciales de largo plazo en un gestor de contraseñas dedicado.

---

# Comportamiento de salida

`carnada` se ejecuta, imprime la salida solicitada y finaliza.

No mantiene procesos en segundo plano.

No almacena contraseñas generadas.

No crea logs.

No requiere acceso a internet.

---

# Solución de problemas

## Comando Python no encontrado

Probar con:

```bash
python carnada.py
```

o:

```bash
python3 carnada.py
```

dependiendo del sistema operativo y de la instalación de Python.

---

## Permiso denegado al ejecutar `./carnada.py`

Dar permisos de ejecución al script:

```bash
chmod +x carnada.py
```

Luego ejecutar:

```bash
./carnada.py
```

---

## Perfil inválido

Usar uno de los perfiles disponibles:

```text
strong
legacy
pin
hex
wifi
```

Ejemplo:

```bash
python3 carnada.py --profile strong
```

---

## Sin grupos de caracteres habilitados

Esto puede ocurrir si todos los grupos de caracteres están deshabilitados:

```bash
python3 carnada.py --no-upper --no-lower --no-numbers --no-symbols
```

Debe permanecer habilitado al menos un grupo de caracteres.

---

# Resumen

`carnada` proporciona un flujo local simple:

```text
generar contraseñas;
revisar contraseñas;
estimar entropía;
imprimir una salida limpia en terminal;
evitar almacenar secretos.
```

Está diseñada para ser pequeña, práctica y segura para uso local desde terminal.
