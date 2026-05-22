# CARNADA

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

`carnada` is a local CLI tool for generating secure passwords and checking existing passwords from the terminal.

The project follows a simple principle: generate strong credentials without storing secrets, sending data to the internet, or adding unnecessary features that increase operational risk.

---

# Description

`carnada` generates random passwords using cryptographically secure mechanisms provided by Python. It also includes a local password analysis mode to inspect basic characteristics such as length, uppercase letters, lowercase letters, numbers, symbols, ambiguous characters, and approximate entropy.

The tool is designed for local usage, cybersecurity labs, temporary credential generation, technical testing, and shell-based workflows.

---

# Project Goal

`carnada` is not intended to replace a password manager.

Its purpose is to provide a small, auditable, and easy-to-use tool to:

- generate secure passwords from the terminal;
    
- create passwords compatible with different environments;
    
- check passwords locally;
    
- integrate with scripts using clean or JSON output;
    
- keep the operational risk surface small.
    

---

# Main Features

- Secure password generation using cryptographically secure randomness.
    
- Generation profiles for different use cases.
    
- Approximate entropy estimation in bits.
    
- Local password checking.
    
- Multiple password generation in a single execution.
    
- Quiet mode for scripting.
    
- JSON output for automation.
    
- No password storage.
    
- No internet connection required.
    
- No encryption vault, secret management, or remote synchronization.
    

---

# What It Does

`carnada` can:

- generate a secure password using the default configuration;
    
- generate passwords with a custom length;
    
- generate multiple passwords;
    
- use profiles such as `strong`, `legacy`, `pin`, `hex`, and `wifi`;
    
- display an approximate entropy estimate;
    
- classify the approximate password strength;
    
- check a password entered by the user;
    
- return normal, quiet, or JSON output.
    

---

# What It Does Not Do

`carnada` does not:

- store passwords;
    
- manage password vaults;
    
- encrypt files;
    
- generate password hashes;
    
- synchronize secrets;
    
- send information to the internet;
    
- replace a password manager;
    
- guarantee absolute security.
    

This is intentional. The tool is designed to do a few things clearly, locally, and auditably.

---

# Requirements

- Python 3.10 or higher.
    
- No external dependencies required.
    
- Uses only the Python standard library.
    

---

# Installation and Quick Start

Clone the repository:

```bash
git clone https://github.com/beathunterzero/carnada.git
cd carnada
```

Run the tool:

```bash
python3 carnada.py
```

Optional direct execution on Linux, WSL, or macOS:

```bash
chmod +x carnada.py
./carnada.py
```

On Windows PowerShell:

```powershell
python carnada.py
```

Because the tool has no external dependencies, no package installation is required.

---

# Basic Usage

Generate a secure password using the default configuration:

```bash
python3 carnada.py
```

Generate a 24-character password:

```bash
python3 carnada.py -l 24
```

Generate a password using the `legacy` profile:

```bash
python3 carnada.py --profile legacy
```

Generate five passwords:

```bash
python3 carnada.py --count 5
```

Print only the generated password:

```bash
python3 carnada.py --quiet
```

Generate JSON output:

```bash
python3 carnada.py --json
```

Check a password locally:

```bash
python3 carnada.py check
```

Check a password directly from the command line:

```bash
python3 carnada.py check "Password123!"
```

---

# Available Profiles

## `strong`

Recommended profile for general use. Uses uppercase letters, lowercase letters, numbers, and symbols. Designed to generate strong passwords for modern systems.

## `legacy`

Compatible profile for older or restrictive systems. Uses letters and numbers while avoiding complex symbols.

## `pin`

Numeric profile. Useful for short temporary PINs or numeric codes.

## `hex`

Hexadecimal token profile. Useful for technical testing, labs, or workflows that require hexadecimal output.

## `wifi`

Profile for long and compatible Wi-Fi passwords. Avoids complex symbols to make manual entry easier on devices.

---

# Output Examples

Normal generation example:

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

Quiet mode example:

```text
V7#kQm92@tLx8pRz
```

Password check example:

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

# Security and Design

`carnada` follows a local-first design.

All operations are performed locally on the user’s machine. The tool does not send passwords to external services, does not perform remote requests, and does not require an internet connection.

Password generation uses Python’s `secrets` module, which is suitable for generating cryptographically secure random values.

The tool avoids storing secrets by design. It does not create files containing passwords, does not store master keys, and does not maintain its own history.

---

# About Entropy

The entropy shown by `carnada` is an approximate estimate based on password length and the size of the character set used.

This metric provides a general reference for the strength of randomly generated passwords, but it should not be interpreted as an absolute security guarantee.

Real-world security also depends on usage context, system policy, secret exposure, storage practices, password reuse, and additional security controls.

---

# Important Considerations

- Do not reuse passwords across different services.
    
- Do not paste sensitive passwords into untrusted systems.
    
- Do not share passwords through insecure channels.
    
- Use a password manager to store permanent credentials.
    
- Use `carnada` as a local generator or support tool, not as a secret vault.
    

---

# Project Structure

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

# Additional Documentation

Extended documentation is available in the `docs/` directory.

Usage guide:

```text
docs/usage.md
```

Security notes:

```text
docs/security-notes.md
```

Architecture overview:

```text
docs/architecture/overview.md
```

Practical examples:

```text
examples/usage-examples.md
```

---

# Project Status

This project is intended as a personal command-line tool with an educational, practical, and defensive cybersecurity focus.

The initial version keeps the scope intentionally small and avoids features that would unnecessarily increase risk, such as secret storage, vault encryption, or remote synchronization.

---

# License

This project is distributed under the license specified in the `LICENSE` file.

---

# Author

**beathunterzero**  
Cyber Threat Hunting & Security

Personal project focused on cybersecurity, automation, and defensive command-line tooling.
