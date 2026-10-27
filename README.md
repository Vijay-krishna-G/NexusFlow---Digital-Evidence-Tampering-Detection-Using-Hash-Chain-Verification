
# NexusFlow — Digital Evidence Integrity & Chain-of-Custody System

NexusFlow is a digital forensics project designed to verify digital evidence integrity, detect unauthorized modifications, and maintain a traceable chain of custody using SHA-256 hashing and hash-chain verification.

## Features

- **Evidence Integrity Verification** — Verify evidence files using SHA-256 hashes.
- **Tampering Detection** — Identify changes by comparing calculated hashes with stored hash values.
- **Chain-of-Custody Tracking** — Maintain evidence records and track evidence handling.
- **Case Management** — Register and organize digital forensic cases.
- **Role-Based Access** — Support different user roles, including Admin, Officer, and User.
- **Evidence Management** — Upload and manage digital evidence files.

## Technology Stack

- Python
- Django
- MySQL
- HTML, CSS, JavaScript
- SHA-256 Hashing

## How It Works

1. A case is registered in the system.
2. Digital evidence is uploaded and assigned a SHA-256 hash.
3. Hash information is stored for integrity verification and hash-chain tracking.
4. The verification process recalculates the evidence hash and compares it with the stored value.
5. A mismatch indicates that the evidence may have been modified.

## Security Note

This project demonstrates digital evidence integrity verification and chain-of-custody management. Its protection depends on the security of the application and its stored records. Database-backed hash records are not inherently immutable.

## Project Status

Developed as an academic project in digital forensics.

## Disclaimer

This project is intended for educational and research purposes. Use only authorized digital evidence and test data.
