# appium-agentic-self-healing-tests

繁體中文 | [English](README.md)

基於 Appium 與 pytest 的 Android 應用程式 AI Agent 輔助自癒端到端（E2E）自動化測試系統。

---

## 這是什麼？

本專案提供一套以 Android 為核心的行動自動化測試框架，專注於原生 Android 應用程式的確定性端到端 UI 測試，並作為後續 AI 輔助定位器自癒（Self-healing）機制的基礎。

### 目標環境：僅限 Android 模擬器（Android Emulator Only）

> **本 repository 目前以 Android Emulator 作為唯一支援的執行環境。** 實體 Android 裝置明確不在支援範疇內。

將執行環境標準化於 Android 模擬器，能確保測試具備最高的環境一致性、自動化程度與 CI 可移植性，避免實體線材連接不穩、OEM 客製化系統行為差異或手動點擊授權等問題。

---

## 系統架構與執行流程

```text
pytest（測試執行器與 Driver 生命週期管理）
  ↓
Appium Python Client
  ↓
Appium Server（連接埠 4723）
  ↓
UiAutomator2 Driver
  ↓
adb
  ↓
Android Emulator（API 34, AVD: appium-test-api34）
  ↓
Sauce Labs My Demo App Android
```

### 責任邊界劃分

- **環境 / 開發者 / CI**：管理基礎設施——包含 Android SDK 工具鏈、AVD 建立、模擬器行程、Appium Server 服務與 APK 檔案下載。
- **pytest**：管理測試執行——負責讀取設定檔、建立 UiAutomator2 連線 session、透過明確狀態等待執行斷言，並於測試結束時安全釋放資源（`driver.quit()`）。

---

## 前置需求與驗證基準

### 基本需求（Requirements）
- **Python**：`>= 3.10`
- **Java JDK**：`>= 17`
- **Node.js**：`>= 20.19`
- **npm**：`>= 10`
- **Android SDK Command-line Tools**（`cmdline-tools;latest`）
- **Android Platform Tools**（`adb`）
- **Android Build Tools**（`build-tools;34.0.0`，包含 `apksigner`）
- **Android Emulator**（`emulator`）
- **Android System Image**（API 34 / Android 14）
- **Appium Server**：`>= 3.0`
- **Appium UiAutomator2 Driver**（`appium driver install uiautomator2`）

> [!NOTE]
> **Android Studio 絕非必要相依**。所有環境準備與模擬器啟動皆可純透過官方 Android SDK 命令列工具（CLI）完成。

### 實體驗證基準環境（Validated Baseline）
本專案已於以下實體主機環境完成執行驗證：
- **主機硬體架構**：Apple Silicon（macOS arm64, Darwin 25.6.0）
- **Node.js / npm**：`v26.0.0` / `11.12.1`
- **Android 目標平台**：Android 14 / API 34（`system-images;android-34;google_apis;arm64-v8a`）
- **Android Build Tools**：`34.0.0`
- **Appium Server**：`3.7.0`
- **UiAutomator2 Driver**：`8.6.1`
- **目標展示應用程式**：Sauce Labs My Demo App Android `2.2.0`（`mda-2.2.0-238.apk`）

---

## 快速上手與操作步驟

請依照以下步驟完成環境設定並執行測試套件。

### 1. 設定 Android 環境變數
於您的 Shell 設定檔（`~/.zshrc` 或 `~/.bashrc`）加入：

```bash
export ANDROID_HOME="$HOME/Library/Android/sdk" # macOS 預設路徑，或 /opt/homebrew/share/android-commandlinetools
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/build-tools/34.0.0:$PATH"
```

### 2. 安裝 Android SDK 元件並建立 AVD
接受授權並安裝指定套件：

```bash
sdkmanager --licenses

# Apple Silicon (arm64):
sdkmanager "platform-tools" "emulator" "build-tools;34.0.0" "platforms;android-34" "system-images;android-34;google_apis;arm64-v8a"
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;arm64-v8a" --force

# x86_64 主機 (Linux / Intel Mac):
sdkmanager "platform-tools" "emulator" "build-tools;34.0.0" "platforms;android-34" "system-images;android-34;google_apis;x86_64"
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;x86_64" --force
```

### 3. 安裝 Appium 與 UiAutomator2 驅動
```bash
npm install -g appium
appium driver install uiautomator2
```

### 4. 安裝 Python 測試相依套件
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 或以可編輯開發模式安裝：
pip install -e ".[dev]"
```

### 5. 下載測試目標 APK
```bash
mkdir -p apps
curl -L -o apps/mda-2.2.0-238.apk https://github.com/saucelabs/my-demo-app-android/releases/download/2.2.0/mda-2.2.0-25.apk
```

### 6. 啟動模擬器並確認就緒
啟動模擬器（可加上 `-no-window` 進行 headless/CI 模式執行）：

```bash
# 在終端機 1 執行：
emulator -avd appium-test-api34 -no-window -no-audio -no-boot-anim -gpu swiftshader_indirect
```

使用專案提供的就緒檢查腳本確認模擬器已完全開機：
```bash
./scripts/wait_for_emulator.sh
```

### 7. 啟動 Appium Server
```bash
# 在終端機 2 執行：
appium --address 127.0.0.1 --port 4723
```

### 8. 執行測試
```bash
# 在終端機 3 執行（需先啟動 venv）：
# Smoke 測試（App 啟動與商品列表就緒）
pytest tests/smoke/test_app_launch.py -v

# 跨畫面 E2E 測試（選取商品並驗證商品詳情資料一致性）
pytest tests/e2e/test_product_details.py -v

# 執行全部測試
pytest tests/ -v
```

---

## 執行期設定（Configuration）

各項參數可透過環境變數彈性覆寫：

| 環境變數 | 預設值 | 說明 |
|---|---|---|
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` | Appium Server 服務連線位址 |
| `ANDROID_PLATFORM_VERSION` | `"14"` | Android 目標平台版本 |
| `ANDROID_DEVICE_NAME` | `"Android Emulator"` | Appium capabilities 裝置名稱 |
| `ANDROID_APP_PATH` | `"apps/mda-2.2.0-238.apk"` | 目標 APK 相對或絕對路徑 |
| `EXPLICIT_WAIT_TIMEOUT_SECONDS` | `10.0` | UI 狀態明確同步逾時秒數 |
| `EMULATOR_BOOT_TIMEOUT_SECONDS` | `120` | `wait_for_emulator.sh` 開機檢測逾時秒數 |

---

## 失敗診斷收集（Failure Diagnostics）

當任何測試在 `setup` 或 `call` 階段執行失敗時，pytest hook 會自動於當下仍活躍的 driver session 擷取診斷檔案並輸出至 `test-results/<test-id>/`：
- `screenshot.png`：失敗當下的畫面截圖。
- `page-source.xml`：Android UI 視圖階層樹狀 XML，供 locator 檢視與後續 self-healing 分析。

`test-results/` 已加入 `.gitignore`，不會進入版本控管，可視需要手動清理。

---

## 專案目錄結構

- [`src/appium_self_heal/`](src/appium_self_heal/)：核心執行期設定模組與共用工具。
- [`src/appium_self_heal/screens/`](src/appium_self_heal/screens/)：Screen Object 模型（`BaseScreen`、`ProductsScreen`、`ProductDetailsScreen`），封裝畫面 locators、領域操作與可重複使用的明確等待同步基元。
- [`tests/conftest.py`](tests/conftest.py)：管理 Appium WebDriver 生命週期與失敗診斷收集 hook 的 pytest fixture。
- [`tests/smoke/`](tests/smoke/)：驗證 session 建立與 App 就緒的 smoke test 測試集。
- [`tests/e2e/`](tests/e2e/)：驗證跨畫面使用者旅程與資料一致性的 E2E 測試集。
- [`scripts/wait_for_emulator.sh`](scripts/wait_for_emulator.sh)：獨立之環境就緒檢查腳本，具備逾時控制。
- [`AGENTS.md`](AGENTS.md)：定義 repository 全域工程規範、狀態同步準則與 locator 優先階層。
- [`ai/agent-instructions/`](ai/agent-instructions/)：專責 Agent 角色的規範單一真相來源（`senior-mobile-sdet`、`test-architect`、`reviewer`）。
