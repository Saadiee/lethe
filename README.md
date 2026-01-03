# Lethe

Cryptographic erasure via irreversible key destruction

Lethe is a cryptographic erasure tool that renders data permanently unrecoverable by destroying the cryptographic keys used to encrypt it. The encrypted data may remain intact, but without the key, recovery is computationally infeasible.

Lethe demonstrates cryptographic erasure by destroying access to encryption keys at the application level. Due to Python’s memory model and garbage collection, Lethe cannot guarantee physical zeroization of key material in RAM. For high-assurance environments, lower-level languages or hardware-backed key management are required.

# 🛡️ Threat Model & Security Guarantees

> **Core Principle:** Lethe implements **cryptographic erasure (crypto-shredding)**. This is a destruction technique that renders data permanently unreadable by destroying cryptographic keys rather than attempting unreliable physical overwrites.

---

### 🎯 Purpose

To provide a reliable data destruction mechanism on modern storage media (SSDs, NVMe) where traditional "overwriting" is often bypassed by wear-leveling and controller logic.

---

### 🛡️ Threats Considered

Lethe is architected to defend against the following attack vectors:

| Threat Category          | Defense Mechanism                                       |
| ------------------------ | ------------------------------------------------------- |
| **Forensic Recovery**    | Recovery of deleted files via specialized software.     |
| **Filesystem Artifacts** | Journaling and Copy-on-Write (CoW) metadata remnants.   |
| **Hardware Abstraction** | SSD wear-leveling logic preventing physical overwrites. |
| **Persistence**          | Snapshot or backup recovery of encrypted artifacts.     |
| **Key Reuse**            | Accidental or malicious reuse of encryption keys.       |
| **Data Integrity**       | Unauthorized tampering with encrypted output.           |

---

### ⚠️ Threats Explicitly Out of Scope

The following threats are **not** mitigated by Lethe:

- **Pre-shred Access:** Attackers who accessed plaintext _before_ shredding.
- **Low-Level Access:** Kernel-level or hardware-level attackers during runtime.
- **Side-Channels:** RAM scraping attacks while the program is executing.
- **Runtime Integrity:** Malicious operating systems or compromised Python runtimes.
- **Historical Remnants:** Recovery of historical plaintext remnants prior to key destruction.

_Note: These limitations are fundamental to user-space software and common to all high-level cryptographic tools._

---

### ✅ Security Guarantees

After a successful shred operation, Lethe provides these strict guarantees:

1. **Irreversibility:** The encryption key is irreversibly destroyed in memory.
2. **Mathematical Finality:** All encrypted artifacts become mathematically unrecoverable ( security margin).
3. **Integrity:** Protection via **AES-GCM** ensures any tampering is detected during attempted decryption.
4. **Forensic Resistance:** Recovery tools cannot reconstruct plaintext without the unique, destroyed key.
5. **Enforceable Cutoffs:** Key destruction defines a clear, temporal boundary for data accessibility.

> **Lethe guarantees future inaccessibility, not retroactive erasure of history.**

---

### 🏗️ Design Principles

- **Fail-Loud Behavior:** Cryptographic failures are never silenced; they trigger immediate exceptions.
- **Strict Key Lifecycle:** Keys are generated securely, used for a single operation, and immediately purged.
- **Anti-Friction Reality:** No "secure-delete" fantasies; file deletion is treated as best-effort hygiene.
- **Modular Isolation:** Crypto-logic, key management, and file handling are strictly decoupled.
- **Honest Claims:** Zero promises dependent on opaque filesystem or hardware behavior.

---

### 📝 Summary

Lethe does not attempt to overwrite storage media. Instead, it destroys the **ability to interpret data**, which is the only reliable destruction guarantee on modern, abstracted storage systems.
