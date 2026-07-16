# Edge Agent Architecture

**Member C - Edge Agent Lead**
**Project:** OTA Firmware Update & Code Signing Infrastructure

---

## Overview

The Edge Agent simulates an IoT device that securely downloads
and installs firmware updates from the OTA backend server.

---

## Security Flow

OTA Backend Server
       |
       | (1) Download firmware .bin + .sig files
       v
Edge Agent (this module)
       |
       |-- (2) Calculate SHA-256 hash of downloaded firmware
       |-- (3) Compare with expected hash from server
       |-- (4) Verify digital signature using stored public key
       |
       |-- FAIL --> Drop firmware + Log CRITICAL alert + Abort
       |
       |-- PASS --> Simulate installation + Log SUCCESS

---

## Attack Scenarios Handled

| Attack | Detection Method |
|--------|-----------------|
| MITM firmware swap | SHA-256 hash mismatch |
| Forged unsigned firmware | Signature verification fail |
| Corrupted download | Hash mismatch |
| Rollback to old version | Version number check (Week 4) |

---

## Week-wise Plan

- Week 1: Architecture + structure + logger + downloader
- Week 2: Connect to Member B backend, real download
- Week 3: SHA-256 verify + signature verify + reject logic
- Week 4: Anti-rollback mechanism