# Lethe

**Cryptographic erasure via irreversible key destruction**

Lethe is a command-line security tool that implements **cryptographic erasure (crypto-shredding)**: a data destruction technique that renders information permanently unreadable by destroying the cryptographic keys used to encrypt it.

The encrypted data itself may remain on disk, but without the key, recovery is **computationally infeasible**. This approach avoids the false guarantees of traditional file overwriting on modern storage hardware.

---

## Overview

Modern storage systems (SSDs, NVMe, CoW filesystems) frequently bypass physical overwrite attempts due to wear-leveling, journaling, and snapshotting. As a result, “secure delete” utilities that rely on repeated overwrites often provide **illusory guarantees**.

Lethe addresses this by:

- Encrypting data with a unique, ephemeral key
- Permanently destroying that key in memory
- Treating file deletion as hygiene, not security

Once the key is destroyed, the data becomes mathematically unrecoverable — regardless of filesystem behavior.

---

## Threat Model & Security Guarantees

> **Core Principle**
> Lethe guarantees **future inaccessibility**, not retroactive erasure of history.

---

### Purpose

Provide a **reliable data destruction mechanism** on modern storage media where physical overwrite semantics cannot be trusted.

---

### Threats Considered

Lethe is designed to defend against the following threat classes:

| Threat Category          | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| **Forensic Recovery**    | File recovery using specialized forensic tools       |
| **Filesystem Artifacts** | Journaling, metadata, and Copy-on-Write remnants     |
| **Hardware Abstraction** | SSD wear-leveling preventing physical overwrites     |
| **Persistence**          | Recovery from backups or snapshots of encrypted data |
| **Key Reuse**            | Accidental or malicious reuse of encryption keys     |
| **Data Integrity**       | Undetected tampering with encrypted artifacts        |

---

### Explicitly Out of Scope

The following threats are **not** mitigated by Lethe:

- Access to plaintext prior to shredding
- Kernel-level or hardware-level attackers during execution
- Live memory inspection or RAM scraping
- Compromised operating systems or runtimes
- Recovery of historical plaintext remnants created before shredding

These limitations are inherent to **user-space software** and apply broadly to high-level cryptographic tools.

---

### Security Guarantees

After a successful shred operation, Lethe provides the following guarantees:

1. **Irreversibility**
   The encryption key is irreversibly destroyed in memory.

2. **Mathematical Finality**
   Encrypted artifacts cannot be decrypted without the destroyed key.

3. **Integrity Protection**
   AES-GCM ensures any modification to encrypted data is detectable.

4. **Forensic Resistance**
   Deleted plaintext cannot be reconstructed via recovery tools.

5. **Enforceable Cutoff**
   Key destruction defines a clear, auditable boundary for data accessibility.

---

## Design Principles

- **Cryptographic Honesty**
  No reliance on filesystem or hardware overwrite behavior.

- **Strict Key Lifecycle**
  Keys are generated per operation, used once, and immediately purged.

- **Fail-Loud Behavior**
  Cryptographic and file errors abort execution immediately.

- **Separation of Concerns**
  Key management, cryptography, and file handling are isolated.

- **Minimal Surface Area**
  The CLI is intentionally narrow to reduce misuse.

---

## Usage

Lethe is a command-line tool. During development, it is run inside its Poetry-managed virtual environment.

### Installation (Development)

```bash
git clone https://github.com/saadiee/lethe.git
cd lethe
poetry install
```

### Running the CLI

Use `poetry run` to execute the tool:

```bash
poetry run lethe --help
```

---

### Shred a File

Encrypts a file, destroys the encryption key, and deletes the original plaintext.

```bash
poetry run lethe shred /path/to/file
```

**Behavior:**

- A new encrypted file is created with the `.lethe` extension
- The original plaintext file is deleted
- The encryption key is destroyed in memory
- The encrypted file cannot be decrypted or restored

On success, Lethe prints the path to the encrypted artifact.

---

### Verify an Encrypted File

Checks whether a file is a structurally valid Lethe-encrypted artifact.

```bash
poetry run lethe verify /path/to/file.lethe
```

**Behavior:**

- No keys are required
- No data is modified
- Success prints `OK`
- Failure exits with an error

Verification is informational only and does not imply decryptability.

---

### Exit Codes

Lethe follows standard UNIX conventions:

- `0` — operation completed successfully
- non-zero — error or validation failure

---

### Notes & Warnings

- Lethe operates on **individual files only** (directories are intentionally unsupported)
- Shredding is **irreversible**
- Lethe does **not** attempt secure overwrites
- Plaintext remnants created prior to execution are out of scope
- Since the file is loaded in memory (f.read()), using this tool on large files can result in system crashes.

## Summary

Lethe does not attempt to erase history.
It destroys **the ability to interpret data**, which is the only reliable form of deletion on modern storage systems.

By grounding its guarantees in cryptography rather than hardware behavior, Lethe provides a defensible and honest approach to data destruction.

---

## Status

This project is intended as:

- a **security engineering portfolio project**
- a **reference implementation** of cryptographic erasure principles
- a **learning exercise** in disciplined key lifecycle management

It is not a replacement for hardware-backed secure deletion or trusted execution environments.
