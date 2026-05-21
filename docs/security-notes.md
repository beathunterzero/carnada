# CARNADA Security Notes

`carnada` está diseñada como una herramienta CLI local-first para generar y revisar contraseñas.

El objetivo principal de seguridad es mantener la herramienta pequeña, auditable y operacionalmente segura, evitando el manejo innecesario de secretos.

`carnada` no almacena contraseñas, no transmite datos, no utiliza APIs remotas y no actúa como gestor de contraseñas.

---

# Modelo de seguridad

`carnada` sigue un modelo de seguridad mínimo:

```text
generar o revisar contraseñas localmente;
evitar almacenamiento persistente de secretos;
evitar comunicación de red;
evitar dependencias innecesarias;
devolver salida limpia en terminal;
finalizar después de la ejecución.
````

Este modelo reduce el riesgo operativo y mantiene un comportamiento predecible.

---

# Ejecución local-first

Todas las operaciones se ejecutan localmente en el equipo del usuario.

`carnada` no:

```text
se conecta a servicios externos;
envía contraseñas a sistemas remotos;
realiza telemetría;
sincroniza datos con la nube;
escribe contraseñas generadas en disco por defecto.
```

Esto hace que la herramienta sea adecuada para flujos de trabajo basados en terminal donde el usuario necesita un generador o revisor simple de contraseñas locales.

---

# Sin almacenamiento de contraseñas

`carnada` intencionalmente no almacena contraseñas generadas ni contraseñas revisadas.

Esta es una decisión de diseño.

La herramienta no es un gestor de contraseñas y no proporciona bóveda, base de datos, almacenamiento cifrado, mecanismo de recuperación, sincronización ni gestión del ciclo de vida de credenciales.

Las contraseñas generadas y revisadas existen únicamente durante la ejecución y se imprimen en la terminal cuando el usuario lo solicita.

Los usuarios deben almacenar credenciales permanentes en un gestor de contraseñas dedicado.

---

# Sin capa de cifrado

Versiones anteriores o diseños experimentales pueden incluir conceptos de cifrado, pero el diseño actual evita intencionalmente funciones de cifrado.

Esto se debe a que el cifrado solo aporta valor cuando la herramienta almacena o transporta secretos.

Como `carnada` no almacena secretos, agregar cifrado aumentaría la complejidad sin añadir protección significativa al caso de uso principal.

Evitar el cifrado también reduce el riesgo de manejo deficiente de claves, almacenamiento inseguro de archivos, exposición accidental en texto claro o supuestos de seguridad engañosos.

---

# Sin hashing de contraseñas

`carnada` no genera hashes SHA-256 ni SHA-512 de contraseñas.

Esto es intencional.

Funciones hash rápidas como SHA-256 y SHA-512 no son apropiadas por sí solas para almacenamiento seguro de contraseñas. El almacenamiento de contraseñas requiere mecanismos dedicados de password hashing o derivación de claves como Argon2id, bcrypt, scrypt o PBKDF2 con parámetros adecuados.

Debido a que `carnada` no es un sistema de almacenamiento de contraseñas, el hashing de contraseñas queda fuera del alcance de la herramienta.

---

# Fuente de aleatoriedad

La generación de contraseñas utiliza el módulo `secrets` de Python.

El módulo `secrets` está diseñado para generar números aleatorios criptográficamente fuertes, adecuados para gestionar secretos como contraseñas, tokens de autenticación de cuentas y valores similares.

`carnada` no utiliza el módulo `random` de Python para generar contraseñas.

El módulo `random` no es adecuado para uso criptográfico porque su salida no está diseñada para ser impredecible frente a atacantes.

---

# Diseño del conjunto de caracteres

`carnada` soporta grupos de caracteres configurables:

```text
letras mayúsculas;
letras minúsculas;
números;
símbolos.
```

La herramienta puede evitar caracteres visualmente ambiguos por defecto.

Ejemplos de caracteres ambiguos:

```text
O
0
I
1
l
o
```

Eliminar estos caracteres puede facilitar la lectura, copia o escritura manual de contraseñas, especialmente cuando se usan en terminales, dispositivos móviles, equipos de red o interfaces heredadas.

Esta es una decisión de usabilidad. No reemplaza una longitud adecuada de contraseña ni un almacenamiento seguro.

---

# Composición de contraseñas

Al generar una contraseña, `carnada` debe garantizar que se incluya al menos un carácter de cada grupo activo.

Por ejemplo, si están habilitados mayúsculas, minúsculas, números y símbolos, la contraseña generada debe contener al menos:

```text
un carácter en mayúscula;
un carácter en minúscula;
un número;
un símbolo.
```

Los caracteres restantes se seleccionan aleatoriamente desde el conjunto completo de caracteres activo.

La contraseña final se mezcla antes de imprimirse.

Esto evita casos donde una contraseña generada accidentalmente no incluya un grupo de caracteres seleccionado.

---

# Estimación de entropía

`carnada` estima la entropía usando la longitud de la contraseña y el tamaño del conjunto de caracteres activo.

Conceptualmente:

```text
entropy = password_length × log2(character_set_size)
```

El resultado se muestra en bits.

Esta es solo una aproximación.

La estimación de entropía es útil para comparar contraseñas generadas, pero no garantiza seguridad en condiciones reales.

La seguridad real de una contraseña también depende de:

```text
si la contraseña se reutiliza;
dónde se almacena;
cómo se transmite;
si aparece en logs;
si queda expuesta mediante historial del portapapeles;
si el servicio objetivo tiene rate limiting;
si la autenticación multifactor está habilitada;
si la contraseña apareció en filtraciones.
```

---

# Clasificación de fortaleza

`carnada` puede clasificar contraseñas usando umbrales aproximados de entropía.

Modelo de ejemplo:

```text
menos de 40 bits      weak
40 a 69 bits          moderate
70 a 99 bits          strong
100 bits o más        very strong
```

Esta clasificación es una guía simplificada, no una evaluación formal de seguridad.

Una contraseña clasificada como `very strong` puede seguir siendo insegura si se reutiliza, se registra en logs, se almacena de forma insegura o se comparte mediante canales inseguros.

---

# Riesgo del historial de línea de comandos

Los usuarios deben tener cuidado al pasar contraseñas sensibles directamente como argumentos de línea de comandos.

Por ejemplo:

```bash
python3 carnada.py check "MySensitivePassword"
```

Esto puede exponer la contraseña mediante el historial de la shell o inspección de procesos, dependiendo del sistema operativo y del comportamiento de la shell.

Uso recomendado:

```bash
python3 carnada.py check
```

Cuando no se proporciona una contraseña como argumento, la herramienta debe solicitarla usando entrada oculta.

---

# Riesgo de salida en terminal

Las contraseñas generadas se imprimen en la terminal.

Este es el comportamiento esperado para un generador CLI, pero los usuarios deben considerar que la salida de terminal puede ser visible mediante:

```text
grabación de pantalla;
scrollback de terminal;
sesiones compartidas;
shells remotas;
buffers de copiar/pegar;
logs de multiplexores de terminal;
herramientas de grabación de comandos.
```

Los usuarios deben limpiar el historial o scrollback de la terminal cuando sea necesario y evitar generar credenciales sensibles en entornos no confiables.

---

# Consideraciones sobre salida JSON

La salida JSON es útil para automatización.

Ejemplo:

```bash
python3 carnada.py --json
```

Sin embargo, los usuarios deben evitar redirigir salidas JSON que contienen contraseñas hacia archivos, salvo que entiendan el riesgo.

Ejemplo a evitar con credenciales reales:

```bash
python3 carnada.py --json > password.json
```

Esto crea un archivo que contiene la contraseña generada en texto claro.

Si se requiere redirección de salida, el usuario es responsable de proteger el archivo resultante.

---

# Consideraciones sobre modo silencioso

El modo silencioso imprime únicamente la contraseña generada.

Ejemplo:

```bash
python3 carnada.py --quiet
```

Esto es útil para shell scripting, pero también puede aumentar la probabilidad de exposición accidental si la salida se canaliza, registra, redirige o captura.

Ejemplo:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

Esto puede dejar la contraseña en memoria de la shell o en logs de scripts, dependiendo de cómo se utilice la variable.

El modo silencioso debe usarse con cuidado en scripts.

---

# Modelo de dependencias

`carnada` utiliza únicamente la biblioteca estándar de Python.

Esto reduce:

```text
sobrecarga de gestión de dependencias;
fricción de instalación;
riesgo de supply chain de terceros;
conflictos de versiones de paquetes.
```

Los módulos estándar relevantes incluyen:

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

No se requieren paquetes externos de Python.

---

# Comportamiento del sistema de archivos

`carnada` no crea archivos de contraseñas por defecto.

No crea:

```text
bases de datos de contraseñas;
bóvedas cifradas;
logs que contengan secretos;
archivos de configuración que contengan secretos.
```

Si el usuario redirige la salida hacia un archivo, ese comportamiento es controlado por la shell, no por `carnada`.

---

# Uso recomendado

Recomendado:

```bash
python3 carnada.py
python3 carnada.py --profile strong
python3 carnada.py --profile legacy
python3 carnada.py --count 5
python3 carnada.py --quiet
python3 carnada.py check
```

Usar el modo `check` sin pasar contraseñas reales sensibles directamente como argumentos de línea de comandos.

Recomendado:

```bash
python3 carnada.py check
```

Menos recomendado para contraseñas reales sensibles:

```bash
python3 carnada.py check "MySensitivePassword"
```

---

# Fuera de alcance

Las siguientes funcionalidades están intencionalmente fuera del alcance de `carnada`:

```text
bóvedas de contraseñas;
almacenamiento de credenciales;
sincronización de secretos;
backup en la nube;
recuperación de contraseñas;
compartición de contraseñas;
cifrado de archivos;
password hashing para sistemas de autenticación;
revisión contra bases de datos de filtraciones;
cumplimiento de políticas empresariales de contraseñas.
```

Estas funcionalidades requieren controles de seguridad más amplios y deben ser manejadas por herramientas especializadas.

---

# Prácticas seguras de desarrollo

Al mantener este proyecto:

```text
no hacer commit de contraseñas generadas;
no hacer commit de entornos virtuales locales;
no hacer commit de archivos temporales de salida;
no agregar llamadas de red salvo que el modelo de seguridad sea actualizado;
no agregar funciones de almacenamiento sin un threat model claro;
no registrar contraseñas en logs;
no imprimir valores ingresados mediante entrada oculta;
evitar dependencias innecesarias.
```

Entradas recomendadas para `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
.env
*.log
*.secret
*.key
password.json
contrasenas_generadas.txt
```

---

# Resumen

`carnada` mantiene una postura de seguridad simple al evitar almacenamiento, comunicación de red, capas de cifrado y dependencias innecesarias.

Su propósito principal es generar y revisar contraseñas localmente, proporcionar metadatos útiles y devolver una salida limpia en terminal.

La forma más segura de usar `carnada` es como una herramienta auxiliar local y temporal, no como gestor de contraseñas ni como sistema de almacenamiento de secretos a largo plazo.
