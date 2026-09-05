# appium-agentic-self-healing-tests

[繁體中文](README.zh-TW.md) | English

Automated, agent-assisted self-healing end-to-end test suite for Android applications using Appium.

---

## Target Execution Environment: Android Emulator Only

> **This repository currently uses Android Emulator as its only supported execution target. Physical Android devices are intentionally out of scope.**

The primary goal of this project is to build a reproducible, automated, and CI-portable Android Appium test environment. An Android Emulator is the standard execution environment.

We intentionally do not consider or support:
- USB debugging or physical device authorization
- Vendor-specific Android device behavioral quirks
- USB cable connection handling
- Physical device provisioning
- Physical-device-specific Appium capabilities

---

## Phase 1 Execution Stack

Phase 1 relies on the following execution chain:

```text
pytest
  ↓
Appium Python Client
  ↓
Appium Server
  ↓
UiAutomator2 Driver
  ↓
adb
  ↓
Android Emulator
  ↓
Sauce Labs My Demo App Android (2.2.0)
```

---

## Runtime Responsibility Boundary

To ensure test portability and clean CI orchestration, responsibilities are strictly separated:

```text
Environment / Developer / CI
├── Android SDK CLI tooling & Platform Tools
├── Android AVD creation (`appium-test-api34`)
├── Android Emulator process management
├── Appium Server lifecycle (`appium`)
└── Target APK download (`apps/mda-2.2.0-238.apk`)

pytest
├── Read runtime configuration (`src/appium_self_heal/config.py`)
├── Initialize Appium WebDriver session (`tests/conftest.py`)
├── Execute smoke test verification (`tests/smoke/test_app_launch.py`)
└── Teardown WebDriver session (`driver.quit()`)
```

**Pytest does not manage infrastructure**: It does not install the Android SDK, create AVDs, launch emulators, start the Appium server, or auto-download APK files.

---

## Technology Stack & Prerequisites

### Prerequisites
- **Python**: `>= 3.10`
- **Java JDK**: `>= 17`
- **Node.js**: `>= 18`
- **Android SDK Command-line Tools** (`cmdline-tools;latest`)
- **Android Platform Tools** (`adb`)
- **Android Emulator** (`emulator`)
- **Android System Image** (API 34 / Android 14)
- **Configured AVD** (`appium-test-api34`)
- **Appium Server**: `>= 2.0`
- **Appium UiAutomator2 Driver** (`appium driver install uiautomator2`)
- **Target Application**: [Sauce Labs My Demo App Android 2.2.0](https://github.com/saucelabs/my-demo-app-android/releases) (`mda-2.2.0-238.apk`)

> [!NOTE]
> **Android Studio is NOT a required dependency.** All environment preparation is accomplished entirely via the Android SDK command-line tools.

---

## Baseline Emulator Configuration

- **Platform Version**: Android 14 / API 34
- **Default AVD Name**: `appium-test-api34`
- **Architecture & System Images**:
  - **Apple Silicon (macOS arm64)**: `system-images;android-34;google_apis;arm64-v8a`
  - **x86_64 Host / CI**: `system-images;android-34;google_apis;x86_64`
- **Appium `deviceName`**: Set to generic `"Android Emulator"` (AVD name belongs to setup layer, not test capabilities).

---

## CLI-First Emulator Setup Guide

### 1. Configure Android Environment Variables
Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export ANDROID_HOME="$HOME/Library/Android/sdk" # macOS default, adjust if custom
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
```

Verify `adb` is available:
```bash
adb version
```

### 2. Install Platform Tools, Emulator & System Image
Accept licenses and install baseline packages:

```bash
sdkmanager --licenses

# For Apple Silicon (arm64):
sdkmanager "platform-tools" "emulator" "platforms;android-34" "system-images;android-34;google_apis;arm64-v8a"

# For x86_64 hosts:
sdkmanager "platform-tools" "emulator" "platforms;android-34" "system-images;android-34;google_apis;x86_64"
```

### 3. Create the AVD
```bash
# Apple Silicon (arm64):
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;arm64-v8a" --force

# x86_64 hosts:
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;x86_64" --force
```

### 4. Launch the Emulator via CLI
Standard GUI launch for local development:
```bash
emulator -avd appium-test-api34
```

Headless launch (for CI or resource-constrained environments):
```bash
emulator -avd appium-test-api34 -no-window -no-audio -no-boot-anim -gpu swiftshader_indirect
```

### 5. Verify Emulator Readiness
Do not assume `adb devices` alone means Android is ready. Verify both the device attachment and the OS boot completion:

```bash
# Using the minimal repository helper script:
./scripts/wait_for_emulator.sh

# Or via direct adb one-liner:
adb wait-for-device
adb shell 'while [[ "$(getprop sys.boot_completed)" != "1" ]]; do sleep 2; done'
```

Once ready, `adb devices` will display:
```text
emulator-5554    device
```

---

## Appium Server Setup & Running Tests

### 1. Install Dependencies
```bash
# Install Appium and UiAutomator2 driver
npm install -g appium
appium driver install uiautomator2

# Install Python test dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Download Target APK
Place the target APK in `apps/`:
```bash
mkdir -p apps
# Download Sauce Labs My Demo App Android 2.2.0 release APK into apps/mda-2.2.0-238.apk
```

### 3. Start Appium Server
```bash
appium --address 127.0.0.1 --port 4723
```

### 4. Execute Smoke Test
```bash
pytest tests/smoke/test_app_launch.py -v
```

Runtime settings can be overridden via environment variables:
- `APPIUM_SERVER_URL`: Appium endpoint (default: `http://127.0.0.1:4723`)
- `ANDROID_PLATFORM_VERSION`: Target Android version (default: `"14"`)
- `ANDROID_DEVICE_NAME`: Capabilities device name (default: `"Android Emulator"`)
- `ANDROID_APP_PATH`: Relative or absolute path to APK (default: `"apps/mda-2.2.0-238.apk"`)
- `EXPLICIT_WAIT_TIMEOUT_SECONDS`: UI wait timeout (default: `10.0`)

---

## Phase 1 Non-Goals

Phase 1 deliberately excludes:
- Physical Android device support
- USB device setup and connection debugging
- Physical-device-specific Appium capabilities
- Business E2E test scenarios (login, cart, checkout)
- Screen/Page Object abstractions (kept direct for smoke test)
- AI self-healing or LLM repair logic

---

## Phase 1 Completion Criteria Checklist

Phase 1 is complete when all of the following hold:
- [x] Android Studio is not a required dependency
- [x] Android SDK CLI-first setup is fully documented
- [x] Reproducible baseline emulator configuration is documented (API 34)
- [x] AVD creation via CLI is documented
- [x] Emulator CLI launch (GUI and headless) is documented
- [x] `adb` recognizes the emulator and boot readiness is verified
- [x] Pytest fixture manages Appium driver lifecycle with reliable teardown
- [x] UiAutomator2 session connects to emulator via Appium Python Client
- [x] My Demo App launches on the emulator to a verified initial UI state
- [x] Minimal app-launch smoke test validates the end-to-end runtime chain
- [x] Zero arbitrary `time.sleep()` calls
- [x] Zero global driver state
- [x] APK binaries are not committed to Git (`.gitignore` protects `*.apk`)
- [x] Physical devices are explicitly unsupported
- [x] Complex business E2E scenarios are deferred to Phase 2
- [x] Self-healing and LLM logic are deferred to later milestones

---

## Repository Structure & Agent Collaboration

- [`AGENTS.md`](AGENTS.md): Repository-wide engineering rules, synchronization invariants, and locator guidelines.
- [`ai/agent-instructions/`](ai/agent-instructions/): Canonical instructions for dedicated agent roles (`senior-mobile-sdet`, `test-architect`, `reviewer`).
- [`.codex/agents/`](.codex/agents/): Codex runtime adapters.
- [`.agents/agents/`](.agents/agents/): Antigravity runtime adapters.
- [`.agents/skills/`](.agents/skills/): Reusable skills for Appium Android, mobile test design, and Git conventions.
- [`src/appium_self_heal/`](src/appium_self_heal/): Minimal runtime configuration.
- [`tests/`](tests/): Appium fixtures (`conftest.py`) and smoke tests (`tests/smoke/`).
- [`scripts/`](scripts/): Environment readiness scripts (`wait_for_emulator.sh`).
- [`pyproject.toml`](pyproject.toml): Repository tooling and runtime dependencies.
