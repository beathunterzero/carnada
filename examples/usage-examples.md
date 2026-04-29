# CARNADA Usage Examples

This document provides practical examples for using `carnada` from the terminal.

`carnada` is a local-first CLI tool for generating secure passwords and checking existing passwords without storing secrets.

---

# 1. Generate a Default Password

Use the default `strong` profile:

```bash
python3 carnada.py
```

Example output:

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

Use this when you need a strong general-purpose password.

---

# 2. Generate a Longer Password

Generate a 24-character password:

```bash
python3 carnada.py -l 24
```

Equivalent command:

```bash
python3 carnada.py --length 24
```

Example output:

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

Use this when a system supports long passwords and you want stronger credentials.

---

# 3. Generate a Password for Restrictive Systems

Some legacy systems reject special characters.

Use the `legacy` profile:

```bash
python3 carnada.py --profile legacy
```

Example output:

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

Use this profile when a system only accepts letters and numbers.

---

# 4. Generate a Wi-Fi-Friendly Password

Use the `wifi` profile:

```bash
python3 carnada.py --profile wifi
```

Example output:

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

Use this when the password may need to be typed manually on phones, TVs, consoles, routers, or IoT devices.

---

# 5. Generate a Numeric PIN

Use the `pin` profile:

```bash
python3 carnada.py --profile pin
```

Example output:

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

Generate an 8-digit PIN:

```bash
python3 carnada.py --profile pin -l 8
```

Example output:

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

PINs have lower entropy than full passwords. Use them only where numeric codes are required.

---

# 6. Generate a Hexadecimal Token

Use the `hex` profile:

```bash
python3 carnada.py --profile hex
```

Example output:

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

Use this for labs, testing, or workflows that require hexadecimal values.

---

# 7. Generate Multiple Passwords

Generate five password candidates:

```bash
python3 carnada.py --count 5
```

Equivalent command:

```bash
python3 carnada.py -c 5
```

Example output:

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

Use this when you want multiple generated options.

---

# 8. Generate Only the Password

Use quiet mode:

```bash
python3 carnada.py --quiet
```

Equivalent command:

```bash
python3 carnada.py -q
```

Example output:

```text
V7#kQm92@tLx8pRz
```

Use this mode when you only want the generated password without metadata.

---

# 9. Use CARNADA in a Shell Variable

Quiet mode can be used in scripts:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

Then use the variable:

```bash
echo "$PASSWORD"
```

Security note: avoid printing secrets in real scripts. This example only demonstrates shell usage.

---

# 10. Generate JSON Output

Use JSON output:

```bash
python3 carnada.py --json
```

Example output:

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

Use JSON output when integrating `carnada` with other tools or scripts.

---

# 11. Generate Several Passwords in JSON Format

```bash
python3 carnada.py --count 3 --json
```

Example output:

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

# 12. Generate a Password Without Symbols

Some systems reject symbols.

```bash
python3 carnada.py --no-symbols
```

Example output:

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

# 13. Generate a Password Without Numbers

```bash
python3 carnada.py --no-numbers
```

Example output:

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

# 14. Allow Ambiguous Characters

By default, `carnada` avoids ambiguous characters such as:

```text
O 0 I 1 l o
```

To allow them:

```bash
python3 carnada.py --allow-ambiguous
```

Example output:

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

Use this when maximum character variety is preferred over manual readability.

---

# 15. Check a Password Safely

Run check mode without passing the password directly in the command:

```bash
python3 carnada.py check
```

The tool will ask for the password using hidden input:

```text
Password to check:
```

Example output:

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

This is the recommended method for checking real passwords.

---

# 16. Check a Test Password from the Command Line

For non-sensitive examples or testing:

```bash
python3 carnada.py check "Password123!"
```

Example output:

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

Avoid this method for real sensitive passwords because command-line arguments may be stored in shell history.

---

# 17. Check a Password with JSON Output

```bash
python3 carnada.py check --json
```

Example output:

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

You can also provide a non-sensitive test password directly:

```bash
python3 carnada.py check "Password123!" --json
```

---

# 18. View Help

Display the main help menu:

```bash
python3 carnada.py --help
```

Display help for generate mode:

```bash
python3 carnada.py generate --help
```

Display help for check mode:

```bash
python3 carnada.py check --help
```

---

# 19. View Version

```bash
python3 carnada.py --version
```

Example output:

```text
carnada 1.0.0
```

---

# 20. Run as an Executable Script

On Linux, WSL, or macOS:

```bash
chmod +x carnada.py
./carnada.py
```

Example with arguments:

```bash
./carnada.py --profile wifi -l 28
```

---

# 21. Practical Use Cases

## General password

```bash
python3 carnada.py
```

## Long password

```bash
python3 carnada.py -l 32
```

## Password for restrictive systems

```bash
python3 carnada.py --profile legacy
```

## Wi-Fi password

```bash
python3 carnada.py --profile wifi
```

## Numeric PIN

```bash
python3 carnada.py --profile pin -l 8
```

## Hex token

```bash
python3 carnada.py --profile hex
```

## Multiple candidates

```bash
python3 carnada.py --count 10
```

## Shell-friendly output

```bash
python3 carnada.py --quiet
```

## Local password check

```bash
python3 carnada.py check
```

---

# 22. Examples to Avoid with Real Passwords

Avoid checking real sensitive passwords directly from the command line:

```bash
python3 carnada.py check "MyRealPassword123!"
```

Prefer:

```bash
python3 carnada.py check
```

Avoid saving generated passwords to plaintext files:

```bash
python3 carnada.py --json > password.json
```

Avoid printing shell variables containing real passwords:

```bash
PASSWORD=$(python3 carnada.py --quiet)
echo "$PASSWORD"
```

These examples may be acceptable in a controlled lab, but they are not recommended for real credentials.

---

# Summary

These examples show how to use `carnada` for common terminal workflows:

```text
generate secure passwords
generate multiple candidates
use predefined profiles
produce quiet output
produce JSON output
check passwords locally
avoid storing secrets
```

`carnada` is intended to be simple, local, and practical for shell-based usage.