# OTA Firmware Edge Agent — Final Project Summary

**Member C — Ushvi Shah (Edge Agent Lead)**
**Internship:** Infotact Solutions, Bengaluru 2026
**Project:** Logistics & IoT Edge - Secure OTA Firmware Update

---

## What I Built

A complete IoT Edge Device Agent that securely downloads,
verifies and installs firmware updates using cryptographic
techniques to prevent attacks.

---

## Week-wise Work Done

### Week 1 — Foundation
- Created complete project structure
- Built logger.py — security event logging system
- Built downloader.py — firmware download module
- Built verifier.py — SHA-256 hash verification
- Built installer.py — mock installation simulation
- Created mock firmware for testing

### Week 2 — Pipeline Integration
- Connected downloader + verifier + installer in agent.py
- Added anti-rollback protection (blocks older versions)
- Built mock server for local testing
- Complete OTA pipeline working end-to-end

### Week 3 — Cryptographic Security
- Integrated RSA-2048 digital signature verification
- Fixed generate_keys.py (IndentationError bug)
- Added comprehensive error handling and edge cases
- Built test_full_pipeline.py with 4 test scenarios
- Built test_signature.py for signature specific tests

### Week 4 — Documentation & Final
- Security report with threat model
- Final README with setup instructions
- Project summary documentation

---

## Security Features Implemented

| Feature | Technology | Status |
|---------|-----------|--------|
| Hash verification | SHA-256 | ✅ Done |
| Signature verification | RSA-2048 | ✅ Done |
| Anti-rollback protection | Version comparison | ✅ Done |
| Security event logging | Python logging | ✅ Done |
| Error handling | try/except | ✅ Done |
| Mock installation | Simulation | ✅ Done |

---

## Test Results

| Test Case | Expected | Result |
|-----------|----------|--------|
| Genuine firmware v1.0.0 | INSTALL | ✅ INSTALLED |
| Genuine firmware v2.0.0 | INSTALL | ✅ INSTALLED |
| Tampered firmware | REJECT | ✅ REJECTED |
| Wrong signature | REJECT | ✅ REJECTED |
| Rollback v0.5.0 | BLOCK | ✅ BLOCKED |
| Missing firmware file | ERROR | ✅ HANDLED |
| Empty firmware file | ERROR | ✅ HANDLED |

---

## Key Learnings

- RSA asymmetric cryptography — how public/private keys work
- SHA-256 hashing — how tampering is detected
- Anti-rollback security — why version checks matter
- Secure software engineering — never hardcode keys
- Git workflow — branches, PRs, conflict resolution
- Team collaboration — working with Member A, B, D

---

## Files Created
edge_agent/
├── agent.py # Main OTA pipeline
├── downloader.py # Firmware download + sign
├── verifier.py # Hash + signature verify
├── installer.py # Install + anti-rollback
└── logger.py # Security logging

tests/
├── test_full_pipeline.py # All scenario tests
├── test_signature.py # Signature tests
└── create_mock_firmware.py # Mock firmware creator

docs/
├── edge_agent_architecture.md # System design
├── security_report.md # Threat model
└── final_summary.md # This file
---

## GitHub Stats

- Branch: ushvi
- Total commits: 15+
- Files created: 10+
- Tests passing: 7/7