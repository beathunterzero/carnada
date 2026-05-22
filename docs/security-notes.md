# CARNADA Security Notes

`carnada` is designed as a local-first CLI tool for generating and checking passwords.

The main security goal is to keep the tool small, auditable, and operationally safe by avoiding unnecessary handling of secrets.

`carnada` does not store passwords, does not transmit data, does not use remote APIs, and does not act as a password manager.

---

# Security Model

`carnada` follows a minimal security model:

```text
generate or check passwords locally;
avoid persistent storage of secrets;
avoid network communication;
avoid unnecessary dependencies;
return clean terminal output;
exit after execution.
```

This model reduces operational risk and keeps the behavior predictable.

---

# Local-First Execution

All operations are executed locally on the user’s machine.

`carnada` does not:

```text
connect to external services;
send passwords to remote systems;
perform telemetry;
sync data to the cloud;
write generated passwords to disk by default.
```

This makes the tool suitable for terminal-based workflows where the user wants a simple local password generator or checker.

---

# No Password Storage

`carnada` intentionally does not store generated or checked passwords.

This is a design decision.

The tool is not a password manager and does not provide a vault, database, encrypted storage, recovery mechanism, synchronization, or credential lifecycle management.

Generated and checked passwords exist only during runtime and are printed to the terminal when requested.

Users should store permanent credentials in a dedicated password manager.

---

# No Encryption Layer

Earlier versions or experimental designs may include encryption concepts, but the current design intentionally avoids encryption features.

This is because encryption only becomes useful when the tool stores or transports secrets.

Since `carnada` does not store secrets, adding encryption would increase complexity without adding meaningful protection to the core use case.

Avoiding encryption also reduces the risk of poor key handling, unsafe file storage, accidental plaintext exposure, or misleading security assumptions.

---

# No Password Hashing

`carnada` does not generate SHA-256 or SHA-512 hashes of passwords.

This is intentional.

Fast hash functions such as SHA-256 and SHA-512 are not appropriate for secure password storage by themselves. Password storage requires dedicated password hashing or key derivation mechanisms such as Argon2id, bcrypt, scrypt, or PBKDF2 with appropriate parameters.

Because `carnada` is not a password storage system, password hashing is outside the scope of the tool.

---

# Randomness Source

Password generation uses Python’s `secrets` module.

The `secrets` module is designed for generating cryptographically strong random numbers suitable for managing secrets such as passwords, account authentication tokens, and similar values.

`carnada` does not use Python’s `random` module for password generation.

The `random` module is not suitable for cryptographic use because its output is not designed to be unpredictable against attackers.

---

# Character Set Design

`carnada` supports configurable character groups:

```text
uppercase letters;
lowercase letters;
numbers;
symbols.
```

The tool can avoid visually ambiguous characters by default.

Examples of ambiguous characters:

```text
O
0
I
1
l
o
```

Removing these characters can make generated passwords easier to read, copy, or type manually, especially when used across terminals, mobile devices, network equipment, or legacy interfaces.

This is a usability decision. It does not replace proper password length or secure storage.

---

# Password Composition

When generating a password, `carnada` should guarantee that at least one character from each active character group is included.

For example, if uppercase, lowercase, numbers, and symbols are enabled, the generated password should contain at least:

```text
one uppercase character;
one lowercase character;
one number;
one symbol.
```

The remaining characters are selected randomly from the full active character set.

The final password is shuffled before being printed.

This prevents cases where a generated password accidentally misses a selected character group.

---

# Entropy Estimation

`carnada` estimates entropy using the password length and the size of the active character set.

Conceptually:

```text
entropy = password_length × log2(character_set_size)
```

The result is shown in bits.

This is only an approximation.

Entropy estimation is useful for comparing generated passwords, but it does not guarantee real-world security.

Real-world password security also depends on:

```text
whether the password is reused;
where it is stored;
how it is transmitted;
whether it appears in logs;
whether it is exposed through clipboard history;
whether the target service has rate limiting;
whether multi-factor authentication is enabled;
whether the password has appeared in breaches.
```

---

# Strength Rating

`carnada` may classify passwords using approximate entropy thresholds.

Example model:

```text
less than 40 bits      weak
40 to 69 bits          moderate
70 to 99 bits          strong
100 bits or more       very strong
```

This rating is a simplified guide, not a formal security assessment.

A password rated as `very strong` can still be unsafe if it is reused, logged, stored insecurely, or shared through insecure channels.

---

# Command-Line History Risk

Users should be careful when passing sensitive passwords directly as command-line arguments.

For example:

```bash
python3 carnada.py check "MySensitivePassword"
```

This may expose the password through shell history or process inspection depending on the operating system and shell behavior.

Recommended usage:

```bash
python3 carnada.py check
```

When no password is provided as an argument, the tool should request it using hidden input.

---

# Terminal Output Risk

Generated passwords are printed to the terminal.

This is expected behavior for a CLI generator, but users should be aware that terminal output may be visible through:

```text
screen recording;
terminal scrollback;
shared sessions;
remote shells;
copy/paste buffers;
logs from terminal multiplexers;
command recording tools.
```

Users should clear terminal history or scrollback when needed and avoid generating sensitive credentials in untrusted environments.

---

# JSON Output Considerations

JSON output is useful for automation.

Example:

```bash
python3 carnada.py --json
```

However, users should avoid redirecting JSON output containing passwords into files unless they understand the risk.

Example to avoid with real credentials:

```bash
python3 carnada.py --json > password.json
```

This creates a file containing the generated password in plaintext.

If output redirection is required, the user is responsible for protecting the resulting file.

---

# Quiet Mode Considerations

Quiet mode prints only the generated password.

Example:

```bash
python3 carnada.py --quiet
```

This is useful for shell scripting, but it can also increase the chance of accidental exposure if the output is piped, logged, redirected, or captured.

Example:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

This may leave the password in shell memory or script logs depending on how the variable is used.

Quiet mode should be used carefully in scripts.

---

# Dependency Model

`carnada` uses only the Python standard library.

This reduces:

```text
dependency management overhead;
installation friction;
third-party supply chain risk;
package version conflicts.
```

The relevant standard modules include:

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

No external Python packages are required.

---

# File System Behavior

`carnada` does not create password files by default.

It does not create:

```text
password databases;
encrypted vaults;
logs containing secrets;
configuration files containing secrets.
```

If a user redirects output to a file, that behavior is controlled by the shell, not by `carnada`.

---

# Recommended Usage

Recommended:

```bash
python3 carnada.py
python3 carnada.py --profile strong
python3 carnada.py --profile legacy
python3 carnada.py --count 5
python3 carnada.py --quiet
python3 carnada.py check
```

Use `check` mode without passing real sensitive passwords directly as command-line arguments.

Recommended:

```bash
python3 carnada.py check
```

Less recommended for sensitive real passwords:

```bash
python3 carnada.py check "MySensitivePassword"
```

---

# Out of Scope

The following features are intentionally outside the scope of `carnada`:

```text
password vaults;
credential storage;
secret synchronization;
cloud backup;
password recovery;
password sharing;
file encryption;
password hashing for authentication systems;
breach database checks;
enterprise password policy enforcement.
```

These features require broader security controls and should be handled by specialized tools.

---

# Safe Development Practices

When maintaining this project:

```text
do not commit generated passwords;
do not commit local virtual environments;
do not commit temporary output files;
do not add network calls unless the security model is updated;
do not add storage features without a clear threat model;
do not log passwords;
do not print hidden input values;
avoid unnecessary dependencies.
```

Recommended `.gitignore` entries:

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

# Summary

`carnada` keeps its security posture simple by avoiding storage, networking, encryption layers, and unnecessary dependencies.

Its main purpose is to generate and check passwords locally, provide useful metadata, and return clean terminal output.

The safest way to use `carnada` is as a temporary local helper, not as a password manager or long-term secret storage system.