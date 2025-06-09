# ScanNest Agent
[![Build and Run Unit Tests](https://github.com/2brackets/scannest.agent/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/2brackets/scannest.agent/actions/workflows/build-and-test.yml)

**ScanNest Agent** is a cross-platform background service that monitors and reports network-connected devices to a centralized backend. It is part of the ScanNest ecosystem, designed for visibility and control over local network environments.

---

## 🚀 Features

- Auto-detects network devices (IP, MAC, hostname)
- Reports agent status (e.g. installing, running, paused, error)
- Registers agent and fetches credentials (agent ID, API key)
- Pings devices to check availability
- Detects and reports WiFi SSID
- Works on Windows, Linux, and macOS
- Modular and test-covered design (over 50 unit tests included)

---

## 🛠️ Requirements

- Python 3.12+
- `psutil`, `requests`, `pytest`, and other standard libraries

---

## 🧪 Running Tests

```bash
pytest -v tests/
```
Test coverage includes:

    Configuration
    Agent lifecycle
    Status updates
    Device and router discovery
    Network scanning and pinging
    SSID detection per OS

---

##🧩 Project Structure
```
src/
├── config/              # Configuration loading (e.g., agent ID, API key)
├── models/              # Core domain models (Agent, Device, Router, etc.)
├── reports/             # Device reporting modules
├── services/            # Main services (scanner, status reporter, etc.)
├── utils/               # Helpers: network info, WiFi SSID, OS details
tests/                   # Unit tests for all modules
version.py               # Current agent version string
main.py
````
