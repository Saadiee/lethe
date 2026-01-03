# Lethe

Cryptographic erasure via irreversible key destruction

Lethe is a cryptographic erasure tool that renders data permanently unrecoverable by destroying the cryptographic keys used to encrypt it. The encrypted data may remain intact, but without the key, recovery is computationally infeasible.

Lethe demonstrates cryptographic erasure by destroying access to encryption keys at the application level. Due to Python’s memory model and garbage collection, Lethe cannot guarantee physical zeroization of key material in RAM. For high-assurance environments, lower-level languages or hardware-backed key management are required.
