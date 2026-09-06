# appium-agentic-self-healing-tests

[繁體中文](README.zh-TW.md) | English

Automated, agent-assisted self-healing end-to-end (E2E) test suite for Android applications using Appium and pytest.

---

## What Is This?

This project provides an Android-first mobile test automation framework designed to run deterministic end-to-end UI tests against native Android apps and serve as the foundation for AI-assisted self-healing locators.

### Target Environment: Android Emulator Only

> **This repository uses Android Emulator as its only supported execution target.** Physical Android devices are intentionally out of scope.

Standardizing on the Android Emulator provides a consistent, fully automated, and CI-portable execution environment without dealing with USB cables, OEM-specific quirks, or manual device authorizations.

---

## Architecture & Execution Flow

```text
pytest (Test Runner & Driver Lifecycle)
  ↓
Appium Python Client
  ↓
Appium Server (port 4723)
  ↓
UiAutomator2 Driver
  ↓
adb
  ↓
Android Emulator (API 34, AVD: appium-test-api34)
  ↓
Sauce Labs My Demo App Android
```

### Responsibility Boundary

- **Environment / Developer / CI**: Manages infrastructure — Android SDK, AVD creation, emulator process, Appium server daemon, and APK download.
- **pytest**: Manages test execution — reads configuration, opens UiAutomator2 driver sessions, executes assertions with explicit synchronization, and cleanly tears down sessions (`driver.quit()`).

---

## Prerequisites & Baseline

### Requirements
- **Python**: `>= 3.10`
- **Java JDK**: `>= 17`
- **Node.js**: `>= 20.19`
- **npm**: `>= 10`
- **Android SDK Command-line Tools** (`cmdline-tools;latest`)
- **Android Platform Tools** (`adb`)
- **Android Build Tools** (`build-tools;34.0.0` with `apksigner`)
- **Android Emulator** (`emulator`)
- **Android System Image** (API 34 / Android 14)
- **Appium Server**: `>= 3.0`
- **Appium UiAutomator2 Driver** (`appium driver install uiautomator2`)

> [!NOTE]
> **Android Studio is NOT required.** The entire environment is established via official Android SDK command-line tools.

### Validated Baseline
Tested and verified with:
- **Host**: macOS Apple Silicon (arm64, Darwin 25.6.0)
- **Node.js / npm**: `v26.0.0` / `11.12.1`
- **Android Platform**: Android 14 / API 34 (`system-images;android-34;google_apis;arm64-v8a`)
- **Appium Server**: `3.7.0`
- **UiAutomator2 Driver**: `8.6.1`
- **Target App**: Sauce Labs My Demo App Android `2.2.0` (`mda-2.2.0-238.apk`)

---

## Quick Start / How to Run

Follow these steps to set up the environment and run the test suite from scratch.

### 1. Set Android Environment Variables
Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export ANDROID_HOME="$HOME/Library/Android/sdk" # or /opt/homebrew/share/android-commandlinetools
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/build-tools/34.0.0:$PATH"
```

### 2. Install Android SDK Packages & Create AVD
Accept licenses and install platform components:

```bash
sdkmanager --licenses

# For Apple Silicon (arm64):
sdkmanager "platform-tools" "emulator" "build-tools;34.0.0" "platforms;android-34" "system-images;android-34;google_apis;arm64-v8a"
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;arm64-v8a" --force

# For x86_64 hosts (Linux / Intel Mac):
sdkmanager "platform-tools" "emulator" "build-tools;34.0.0" "platforms;android-34" "system-images;android-34;google_apis;x86_64"
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;x86_64" --force
```

### 3. Install Appium & UiAutomator2 Driver
```bash
npm install -g appium
appium driver install uiautomator2
```

### 4. Install Python Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Or for editable development installation:
pip install -e ".[dev]"
```

### 5. Configure Test Credentials
The checkout end-to-end test requires authentication credentials. Create a local `.env` file from the provided template:

```bash
cp .env.example .env
```

Set valid test credentials in `.env`:

```env
TEST_USERNAME=bod@example.com
TEST_PASSWORD=100#$a
```

> [!NOTE]
> `.env` is gitignored and must never be committed. Test credentials are automatically loaded via `python-dotenv` in `config.py`. If credentials are unset when executing checkout tests, the execution fails fast with an explicit `ValueError`. Non-secret deterministic test data (shipping addresses, mock payment cards) are defined directly within testcases rather than in `.env`.

### 6. Download Target APK
```bash
mkdir -p apps
curl -L -o apps/mda-2.2.0-238.apk https://github.com/saucelabs/my-demo-app-android/releases/download/2.2.0/mda-2.2.0-25.apk
```

### 7. Start the Emulator & Verify Readiness
Start the emulator (use `-no-window` for headless/CI mode):

```bash
# In Terminal 1:
emulator -avd appium-test-api34 -no-window -no-audio -no-boot-anim -gpu swiftshader_indirect
```

Wait until the emulator is attached and fully booted using the helper script:
```bash
./scripts/wait_for_emulator.sh
```

### 8. Start Appium Server
```bash
# In Terminal 2:
appium --address 127.0.0.1 --port 4723
```

### 9. Run Tests
```bash
# In Terminal 3 (with venv active):
# Smoke test (app launch and Products screen readiness)
pytest tests/smoke/test_app_launch.py -v

# E2E test (cross-screen product selection and details validation)
pytest tests/e2e/test_product_details.py -v

# E2E test (add product to cart and verify cart consistency)
pytest tests/e2e/test_cart.py -v

# E2E test (complete checkout flow with authentication)
pytest tests/e2e/test_checkout.py -v

# Run all tests
pytest tests/ -v
```

---

## Configuration

Settings can be customized via environment variables or `.env`:

| Variable | Default | Description |
|---|---|---|
| `TEST_USERNAME` | *(None)* | Required for checkout E2E test; fails fast if unset |
| `TEST_PASSWORD` | *(None)* | Required for checkout E2E test; fails fast if unset |
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` | Appium server connection URL |
| `ANDROID_PLATFORM_VERSION` | `"14"` | Android platform version |
| `ANDROID_DEVICE_NAME` | `"Android Emulator"` | Appium capabilities device name |
| `ANDROID_APP_PATH` | `"apps/mda-2.2.0-238.apk"` | Path to target APK file |
| `EXPLICIT_WAIT_TIMEOUT_SECONDS` | `10.0` | Default timeout for UI state synchronization |
| `EMULATOR_BOOT_TIMEOUT_SECONDS` | `120` | Timeout for `wait_for_emulator.sh` boot check |

---

## Failure Diagnostics

When any test fails during `setup` or `call` execution, pytest automatically captures failure artifacts to `test-results/<test-id>/`:
- `screenshot.png`: Visual snapshot of the screen at the moment of failure.
- `page-source.xml`: Current Android UI view hierarchy tree for locator inspection and self-healing analysis.
- `failure.json`: Minimal JSON metadata containing test `nodeid`, `test_name`, and execution `phase`.

`test-results/` is gitignored and can be manually cleaned up as needed.

---

## Repository Structure

- [`src/appium_self_heal/`](src/appium_self_heal/): Core runtime configuration and utilities.
- [`src/appium_self_heal/screens/`](src/appium_self_heal/screens/): Screen Object models (`BaseScreen`, `ProductsScreen`, `ProductDetailsScreen`, `CartScreen`, `LoginScreen`, `CheckoutAddressScreen`, `CheckoutPaymentScreen`, `CheckoutReviewScreen`, `CheckoutCompleteScreen`) encapsulating locators, domain actions, and explicit wait synchronization.
- [`tests/conftest.py`](tests/conftest.py): Pytest fixture managing Appium driver lifecycle and failure diagnostics hook.
- [`tests/smoke/`](tests/smoke/): Smoke test suite verifying session creation and app readiness.
- [`tests/e2e/`](tests/e2e/): Cross-screen E2E test suite validating user journeys (`test_product_details.py`, `test_cart.py`, `test_checkout.py`).
- [`scripts/wait_for_emulator.sh`](scripts/wait_for_emulator.sh): Standalone script verifying emulator attachment and boot completion.
- [`AGENTS.md`](AGENTS.md): Repository engineering standards, synchronization rules, and locator priorities.
- [`ai/agent-instructions/`](ai/agent-instructions/): Canonical agent role definitions (`senior-mobile-sdet`, `test-architect`, `reviewer`).
