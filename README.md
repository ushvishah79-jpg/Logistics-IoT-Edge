# OTA Firmware Edge Agent

**Member C — Edge Agent Lead**
**Project:** Logistics & IoT Edge - Secure OTA Firmware Update
**Internship:** Infotact Solutions, Bengaluru 2026

---

## Overview

This module simulates a secure IoT Edge Device Agent that:

1. Downloads signed firmware from OTA backend server
2. Verifies SHA-256 hash to detect tampering
3. Verifies RSA-2048 digital signature to authenticate source
4. Rejects invalid firmware and logs critical security alert
5. Simulates firmware installation on successful verification
6. Implements anti-rollback protection against downgrade attacks

---

## Security Pipeline
---
OTA Backend Server
|
| Download firmware + signature
v
Edge Agent
|
|-- SHA-256 Hash Verify
| (fail → REJECT + CRITICAL ALERT)
|
|-- RSA Signature Verify
| (fail → REJECT + CRITICAL ALERT)
|
|-- Anti-Rollback Version Check
| (fail → REJECT + CRITICAL ALERT)

## Threat Model

| Attack | Detection | Status |
|--------|-----------|--------|
| MITM firmware swap | SHA-256 mismatch | ✅ Protected |
| Forged unsigned firmware | RSA signature invalid | ✅ Protected |
| Corrupted download | Hash mismatch | ✅ Protected |
| Rollback attack | Version check | ✅ Protected |

---

## Cryptographic Algorithms

- Hash: SHA-256
- Signature: RSA-2048 with PKCS1v15
- Library: Python cryptography (hazmat)

---

## Folder Structure
edge_agent/
├── agent.py # Main OTA pipeline orchestrator
├── downloader.py # Firmware download + signing
├── verifier.py # Hash + signature verification
├── installer.py # Mock installation + anti-rollback
└── logger.py # Security event logging

tests/
├── test_full_pipeline.py # Complete pipeline tests
├── test_signature.py # Signature specific tests
└── create_mock_firmware.py # Test firmware generator

docs/
└── security_report.md # Threat model + test results
---

## Setup

```bash
pip install -r requirements.txt
python generate_keys.py
```

## Run Full Pipeline

```bash
cd edge_agent
python agent.py
```

## Run Tests

```bash
cd tests
python test_full_pipeline.py
```

---

## Week-wise Progress

- Week 1: Architecture + Logger + Downloader + Verifier + Installer ✅
- Week 2: Full pipeline + Anti-rollback + Mock server ✅
- Week 3: Digital signature + Error handling + Final tests ✅
- Week 4: Documentation + Integration ready ✅