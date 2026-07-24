# Security Report — Edge Agent
**Member C — Edge Agent Lead**
**Week 3**

---

## Threat Model

| Attack | Detection Method | Status |
|--------|-----------------|--------|
| MITM firmware swap | SHA-256 hash mismatch | ✅ Protected |
| Forged unsigned firmware | RSA signature invalid | ✅ Protected |
| Corrupted download | Hash mismatch | ✅ Protected |
| Rollback to old version | Version number check | ✅ Protected |
| Tampered firmware | Hash + Signature both fail | ✅ Protected |

---

## Cryptographic Algorithms Used

- **Hash Algorithm:** SHA-256
- **Signature Algorithm:** RSA-2048 with PKCS1v15 padding
- **Key Size:** 2048 bits
- **Library:** Python cryptography (hazmat)

---

## Verification Pipeline
---

## Test Results

| Test | Expected | Result |
|------|----------|--------|
| Genuine firmware | PASS | ✅ PASSED |
| Tampered firmware | REJECT | ✅ REJECTED |
| Wrong signature | REJECT | ✅ REJECTED |
| Rollback attack | REJECT | ✅ REJECTED |
| Normal upgrade | PASS | ✅ PASSED |

---

## Security Practices

- Private key never hardcoded — stored in `keys/` (gitignored)
- No sensitive data in GitHub repository
- All API calls have error handling
- Critical security events logged immediately