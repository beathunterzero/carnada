# CARNADA Architecture Overview

`carnada` is designed as a small local-first command-line tool.

The architecture follows a simple flow: receive user input from the shell, resolve the execution mode, generate or analyze a password, calculate useful metadata, and return clean output to the terminal.

The tool does not use external services, does not store secrets, and does not require third-party dependencies.

---

# Design Principles

The architecture is based on the following principles:

- local execution only;
    
- no password storage;
    
- no network communication;
    
- no external dependencies;
    
- clear separation between generation, analysis, formatting, and CLI parsing;
    
- minimal operational risk;
    
- clean output suitable for terminal usage and scripting.
    

`carnada` is intentionally small in scope. It is not a password manager, not a vault, and not a secret storage system.

---

# High-Level Architecture

The tool is organized around a single executable Python script:

```text
carnada.py
```

Internally, the script is divided into logical components:

```text
CLI Parser
Profile Resolver
Charset Builder
Password Generator
Password Analyzer
Entropy Calculator
Output Formatter
```

Each component has a specific responsibility.

---

# Architecture Diagram

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

# Component Responsibilities

## 1. CLI Parser

The CLI parser receives and validates command-line arguments.

It is responsible for handling commands such as:

```bash
python3 carnada.py
python3 carnada.py --profile legacy
python3 carnada.py --count 5
python3 carnada.py --quiet
python3 carnada.py --json
python3 carnada.py check
```

Main responsibilities:

- parse command-line arguments;
    
- identify the execution mode;
    
- validate accepted options;
    
- route execution to generate mode or check mode.
    

The parser is implemented using Python’s standard `argparse` module.

---

## 2. Generate Mode

Generate mode is the default behavior of the tool.

Its purpose is to create one or more secure passwords using cryptographically secure randomness.

Example:

```bash
python3 carnada.py
```

Main responsibilities:

- load the selected profile;
    
- apply user overrides such as length or disabled character groups;
    
- build the final character set;
    
- generate the requested number of passwords;
    
- calculate entropy metadata;
    
- format the result for terminal output.
    

---

## 3. Check Mode

Check mode analyzes an existing password locally.

Example:

```bash
python3 carnada.py check
```

The password can be provided as an argument or requested interactively.

Example with direct input:

```bash
python3 carnada.py check "Password123!"
```

Example with hidden input:

```bash
python3 carnada.py check
```

Main responsibilities:

- receive a password for analysis;
    
- detect character categories;
    
- detect ambiguous characters;
    
- estimate entropy;
    
- assign a strength rating;
    
- print the result without storing the password.
    

When no password is passed as an argument, the tool should request it securely using hidden input.

---

# Generation Flow

The generation flow works as follows:

```text
1. User runs carnada from the shell.
2. CLI parser reads arguments.
3. The selected profile is loaded.
4. Optional user overrides are applied.
5. Character groups are built.
6. Password is generated using cryptographically secure randomness.
7. Entropy is estimated.
8. Result is formatted.
9. Output is printed to the terminal.
```

Example:

```bash
python3 carnada.py --profile strong -l 24
```

Expected internal flow:

```text
profile = strong
length = 24
charset = uppercase + lowercase + numbers + symbols
generator = secrets-based random selection
output = normal terminal format
```

---

# Check Flow

The check flow works as follows:

```text
1. User runs carnada in check mode.
2. CLI parser detects the check command.
3. Password is received from argument or hidden prompt.
4. Analyzer inspects password structure.
5. Entropy is estimated.
6. Strength rating is calculated.
7. Output is printed to the terminal.
```

Example:

```bash
python3 carnada.py check
```

Expected internal flow:

```text
input = hidden password prompt
analysis = length, uppercase, lowercase, numbers, symbols, ambiguous chars
output = password check report
```

---

# Password Generation Design

Password generation uses Python’s `secrets` module.

This module is designed for generating cryptographically secure random values.

The generator should ensure that at least one character from each active character group is included.

For example, if the active groups are:

```text
uppercase
lowercase
numbers
symbols
```

The generated password should contain at least one character from each group.

After selecting the required characters, the remaining characters are selected randomly from the full character pool. The final list is shuffled before being returned.

This avoids generating passwords that accidentally miss an enabled category.

---

# Character Groups

`carnada` uses configurable character groups:

```text
uppercase letters
lowercase letters
numbers
symbols
```

The tool can also remove visually ambiguous characters by default.

Examples of ambiguous characters:

```text
O
0
I
1
l
o
```

This improves readability when passwords need to be copied manually or typed into another device.

---

# Profiles

Profiles define default generation behavior for specific use cases.

Current profiles:

```text
strong
legacy
pin
hex
wifi
```

## strong

Default profile for general usage.

Uses:

```text
uppercase
lowercase
numbers
symbols
```

## legacy

Designed for older or restrictive systems.

Uses:

```text
uppercase
lowercase
numbers
```

## pin

Designed for numeric codes.

Uses:

```text
numbers
```

## hex

Designed for hexadecimal tokens.

Uses:

```text
0123456789abcdef
```

## wifi

Designed for long Wi-Fi passwords that are easier to type manually.

Uses:

```text
uppercase
lowercase
numbers
```

---

# Entropy Estimation

`carnada` estimates entropy using password length and character set size.

Conceptually:

```text
entropy = password_length × log2(character_set_size)
```

The result is shown in bits.

This value is an approximation. It is useful for comparing generated passwords, but it is not a complete security guarantee.

The final strength rating is derived from the estimated entropy.

Example rating model:

```text
less than 40 bits      weak
40 to 69 bits          moderate
70 to 99 bits          strong
100 bits or more       very strong
```

---

# Output Layer

The output layer formats results for different usage scenarios.

Supported output modes:

```text
normal
quiet
JSON
```

## Normal Output

Human-readable terminal output.

Example:

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

Prints only the generated password.

This is useful for shell scripting.

Example:

```bash
python3 carnada.py --quiet
```

Output:

```text
V7#kQm92@tLx8pRz
```

## JSON Output

Provides structured output for automation.

Example:

```bash
python3 carnada.py --json
```

Output:

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

# Security Boundaries

`carnada` does not cross the following boundaries:

```text
no password storage
no local vault
no encryption layer
no remote API
no telemetry
no cloud synchronization
no database
```

This boundary is intentional.

The tool generates or checks passwords locally and then exits.

---

# Data Handling

`carnada` does not persist generated or checked passwords.

Data exists only during execution.

The tool does not create output files by default.

Password input in check mode should use hidden input when no password is provided as an argument.

Users should avoid passing sensitive real passwords directly in the command line because shell history may store them.

Recommended:

```bash
python3 carnada.py check
```

Less recommended:

```bash
python3 carnada.py check "MySensitivePassword"
```

---

# Dependency Model

`carnada` uses only the Python standard library.

Main modules:

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

No external dependencies are required.

This keeps installation simple and reduces supply chain risk.

---

# Execution Model

The tool can be executed directly with Python:

```bash
python3 carnada.py
```

On Linux, WSL, or macOS, it can also be executed directly if the file has executable permissions:

```bash
chmod +x carnada.py
./carnada.py
```

The script includes a shebang line:

```python
#!/usr/bin/env python3
```

This allows the system to locate the appropriate Python interpreter.

---

# Architecture Scope

The current architecture is intentionally simple.

`carnada` does not need a package layout or complex module separation at this stage because the project is small and has no external dependencies.

A single-file architecture is acceptable while the tool remains focused on:

```text
password generation
password checking
entropy estimation
terminal output
```

If the project grows significantly, it could later be separated into modules such as:

```text
cli.py
profiles.py
generator.py
analyzer.py
formatter.py
```

For now, keeping everything in `carnada.py` improves portability and makes the tool easier to audit.

---

# Summary

`carnada` follows a minimal local-first architecture.

The tool receives input from the shell, routes execution through a CLI parser, performs either password generation or password analysis, estimates entropy, and prints the result in a clean format.

Its main security decision is to avoid storing, transmitting, or managing secrets.

This keeps the project small, auditable, and practical for terminal-based workflows.