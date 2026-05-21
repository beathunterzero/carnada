# CARNADA Usage Examples

Este documento proporciona ejemplos prácticos para usar `carnada` desde la terminal.

`carnada` es una herramienta CLI local-first para generar contraseñas seguras y revisar contraseñas existentes sin almacenar secretos.

---

# 1. Generar una contraseña por defecto

Usar el perfil `strong` por defecto:

```bash
python3 carnada.py
````

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

Usar este comando cuando se necesite una contraseña fuerte de propósito general.

---

# 2. Generar una contraseña más larga

Generar una contraseña de 24 caracteres:

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

Usar esto cuando un sistema soporte contraseñas largas y se quieran credenciales más fuertes.

---

# 3. Generar una contraseña para sistemas restrictivos

Algunos sistemas heredados rechazan caracteres especiales.

Usar el perfil `legacy`:

```bash
python3 carnada.py --profile legacy
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : V7kQm92tLx8pRzW4
Profile  : legacy
Length   : 16
Charset  : 54 characters
Entropy  : ~92.08 bits
Rating   : strong
```

Usar este perfil cuando un sistema solo acepte letras y números.

---

# 4. Generar una contraseña compatible para Wi-Fi

Usar el perfil `wifi`:

```bash
python3 carnada.py --profile wifi
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : V7kQm92tLx8pRzW4sA6nB8
Profile  : wifi
Length   : 24
Charset  : 54 characters
Entropy  : ~138.12 bits
Rating   : very strong
```

Usar esto cuando la contraseña deba escribirse manualmente en teléfonos, televisores, consolas, routers o dispositivos IoT.

---

# 5. Generar un PIN numérico

Usar el perfil `pin`:

```bash
python3 carnada.py --profile pin
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : 583920
Profile  : pin
Length   : 6
Charset  : 10 characters
Entropy  : ~19.93 bits
Rating   : weak
```

Generar un PIN de 8 dígitos:

```bash
python3 carnada.py --profile pin -l 8
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : 84027193
Profile  : pin
Length   : 8
Charset  : 10 characters
Entropy  : ~26.58 bits
Rating   : weak
```

Los PINs tienen menor entropía que las contraseñas completas. Usarlos solo cuando se requieran códigos numéricos.

---

# 6. Generar un token hexadecimal

Usar el perfil `hex`:

```bash
python3 carnada.py --profile hex
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : a3f91c0b8e7d42f6a9c350de11b48c2f
Profile  : hex
Length   : 32
Charset  : 16 characters
Entropy  : ~128.0 bits
Rating   : very strong
```

Usar esto para laboratorios, pruebas técnicas o flujos de trabajo que requieran valores hexadecimales.

---

# 7. Generar múltiples contraseñas

Generar cinco candidatas de contraseña:

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

Usar esto cuando se quieran múltiples opciones generadas.

---

# 8. Generar solo la contraseña

Usar el modo silencioso:

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

Usar este modo cuando solo se quiera la contraseña generada sin metadatos.

---

# 9. Usar CARNADA en una variable de shell

El modo silencioso puede usarse en scripts:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

Luego usar la variable:

```bash
echo "$PASSWORD"
```

Nota de seguridad: evitar imprimir secretos en scripts reales. Este ejemplo solo demuestra el uso desde la shell.

---

# 10. Generar salida JSON

Usar salida JSON:

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

Usar salida JSON cuando se integre `carnada` con otras herramientas o scripts.

---

# 11. Generar varias contraseñas en formato JSON

```bash
python3 carnada.py --count 3 --json
```

Ejemplo de salida:

```json
{
  "profile": "strong",
  "count": 3,
  "length": 18,
  "charset_size": 82,
  "entropy_bits": 114.44,
  "rating": "very strong",
  "passwords": [
    "V7#kQm92@tLx8pRz",
    "B4!sKp81@TxQ9mVw",
    "M8#qLn73@RvX2pZa"
  ]
}
```

---

# 12. Generar una contraseña sin símbolos

Algunos sistemas rechazan símbolos.

```bash
python3 carnada.py --no-symbols
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : V7kQm92tLx8pRzW4
Profile  : strong
Length   : 18
Charset  : 54 characters
Entropy  : ~103.59 bits
Rating   : very strong
```

---

# 13. Generar una contraseña sin números

```bash
python3 carnada.py --no-numbers
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : Qm#tLx@pRzW!sA
Profile  : strong
Length   : 18
Charset  : 74 characters
Entropy  : ~111.77 bits
Rating   : very strong
```

---

# 14. Permitir caracteres ambiguos

Por defecto, `carnada` evita caracteres ambiguos como:

```text
O 0 I 1 l o
```

Para permitirlos:

```bash
python3 carnada.py --allow-ambiguous
```

Ejemplo de salida:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : O7#kQm92@tLx8pRz
Profile  : strong
Length   : 18
Charset  : 88 characters
Entropy  : ~116.31 bits
Rating   : very strong
```

Usar esto cuando se prefiera máxima variedad de caracteres por encima de legibilidad manual.

---

# 15. Revisar una contraseña de forma segura

Ejecutar el modo `check` sin pasar la contraseña directamente en el comando:

```bash
python3 carnada.py check
```

La herramienta solicitará la contraseña usando entrada oculta:

```text
Password to check:
```

Ejemplo de salida:

```text
CARNADA — Password Check
------------------------------------------
Length          : 18
Uppercase       : yes
Lowercase       : yes
Numbers         : yes
Symbols         : yes
Ambiguous chars : no
Entropy         : ~114.44 bits
Rating          : very strong
```

Este es el método recomendado para revisar contraseñas reales.

---

# 16. Revisar una contraseña de prueba desde la línea de comandos

Para ejemplos no sensibles o pruebas:

```bash
python3 carnada.py check "Password123!"
```

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

Evitar este método para contraseñas reales sensibles porque los argumentos de línea de comandos pueden almacenarse en el historial de la shell.

---

# 17. Revisar una contraseña con salida JSON

```bash
python3 carnada.py check --json
```

Ejemplo de salida:

```json
{
  "length": 18,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "symbols": true,
  "ambiguous_chars": false,
  "entropy_bits": 114.44,
  "rating": "very strong"
}
```

También se puede proporcionar directamente una contraseña de prueba no sensible:

```bash
python3 carnada.py check "Password123!" --json
```

---

# 18. Ver ayuda

Mostrar el menú principal de ayuda:

```bash
python3 carnada.py --help
```

Mostrar ayuda del modo `generate`:

```bash
python3 carnada.py generate --help
```

Mostrar ayuda del modo `check`:

```bash
python3 carnada.py check --help
```

---

# 19. Ver versión

```bash
python3 carnada.py --version
```

Ejemplo de salida:

```text
carnada 1.0.0
```

---

# 20. Ejecutar como script ejecutable

En Linux, WSL o macOS:

```bash
chmod +x carnada.py
./carnada.py
```

Ejemplo con argumentos:

```bash
./carnada.py --profile wifi -l 28
```

---

# 21. Casos de uso prácticos

## Contraseña general

```bash
python3 carnada.py
```

## Contraseña larga

```bash
python3 carnada.py -l 32
```

## Contraseña para sistemas restrictivos

```bash
python3 carnada.py --profile legacy
```

## Contraseña Wi-Fi

```bash
python3 carnada.py --profile wifi
```

## PIN numérico

```bash
python3 carnada.py --profile pin -l 8
```

## Token hexadecimal

```bash
python3 carnada.py --profile hex
```

## Múltiples candidatas

```bash
python3 carnada.py --count 10
```

## Salida compatible con shell

```bash
python3 carnada.py --quiet
```

## Revisión local de contraseña

```bash
python3 carnada.py check
```

---

# 22. Ejemplos a evitar con contraseñas reales

Evitar revisar contraseñas reales sensibles directamente desde la línea de comandos:

```bash
python3 carnada.py check "MyRealPassword123!"
```

Preferir:

```bash
python3 carnada.py check
```

Evitar guardar contraseñas generadas en archivos de texto plano:

```bash
python3 carnada.py --json > password.json
```

Evitar imprimir variables de shell que contengan contraseñas reales:

```bash
PASSWORD=$(python3 carnada.py --quiet)
echo "$PASSWORD"
```

Estos ejemplos pueden ser aceptables en un laboratorio controlado, pero no se recomiendan para credenciales reales.

---

# Resumen

Estos ejemplos muestran cómo usar `carnada` para flujos comunes desde terminal:

```text
generar contraseñas seguras
generar múltiples candidatas
usar perfiles predefinidos
producir salida silenciosa
producir salida JSON
revisar contraseñas localmente
evitar almacenar secretos
```

`carnada` está pensada para ser simple, local y práctica para uso basado en shell.
