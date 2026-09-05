# appium-agentic-self-healing-tests

繁體中文 | [English](README.md)

基於 Appium 的 Android 應用程式 AI Agent 輔助自癒端到端（E2E）自動化測試系統。

---

## 目標執行環境：僅限 Android 模擬器（Android Emulator Only）

> **本 repository 目前以 Android Emulator 作為唯一支援的 execution target。實體 Android 裝置明確不在支援範疇內。**

本專案的核心目標在於建立一套具高可重現性、全自動化且能無縫移植至 CI 的 Android Appium 測試環境，因此 Android Emulator 為標準且唯一的執行載體。

本專案現階段明確不考慮亦不支援：
- USB debugging 或實體裝置授權彈窗
- 特定手機廠商（OEM）客製化系統之特殊行為
- USB 線材連線不穩或斷線處理
- 實體手機之手動設定流程
- 實體裝置專屬之 Appium capabilities

---

## Phase 1 執行堆疊

Phase 1 之測試呼叫鏈由上至下依序為：

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

## 執行環境職責邊界

為確保本機開發與 CI 工作流程能一致解耦，系統職責邊界嚴格劃分如下：

```text
Environment / Developer / CI
├── Android SDK CLI 工具鏈與 Platform Tools
├── Android AVD 建立（`appium-test-api34`）
├── Android Emulator 行程啟動與生命週期管理
├── Appium Server 服務管理（`appium`）
└── 目標 APK 下載與存放（`apps/mda-2.2.0-238.apk`）

pytest
├── 讀取執行期設定（`src/appium_self_heal/config.py`）
├── 建立 Appium WebDriver session（`tests/conftest.py`）
├── 執行最小 app-launch 驗證（`tests/smoke/test_app_launch.py`）
└── 可靠釋放 WebDriver session（`driver.quit()`）
```

**pytest 嚴禁跨界管理基礎設施**：pytest 不負責安裝 Android SDK、不建立 AVD、不啟動模擬器、不啟動 Appium server，亦不負責自動下載 APK。

---

## 技術堆疊與環境需求

### 前置需求（Prerequisites）
- **Python**：`>= 3.10`
- **Java JDK**：`>= 17`
- **Node.js**：`>= 18`
- **Android SDK Command-line Tools**（`cmdline-tools;latest`）
- **Android Platform Tools**（`adb`）
- **Android Emulator**（`emulator`）
- **Android System Image**（API 34 / Android 14）
- **已設定之 AVD**（`appium-test-api34`）
- **Appium Server**：`>= 2.0`
- **Appium UiAutomator2 Driver**（`appium driver install uiautomator2`）
- **目標展示應用程式**：[Sauce Labs My Demo App Android 2.2.0](https://github.com/saucelabs/my-demo-app-android/releases)（`mda-2.2.0-238.apk`）

> [!NOTE]
> **Android Studio 絕非必要相依**。所有環境建置皆可純透過 Android SDK command-line tooling（CLI）完成。

---

## 基準模擬器設定（Emulator Baseline）

- **Android 版本**：Android 14 / API 34
- **預設 AVD 名稱**：`appium-test-api34`
- **硬體架構與 System Image 選擇**：
  - **Apple Silicon（macOS arm64）**：`system-images;android-34;google_apis;arm64-v8a`
  - **x86_64 主機 / CI 環境**：`system-images;android-34;google_apis;x86_64`
- **Appium `deviceName`**：設定為通用名稱 `"Android Emulator"`（AVD 名稱屬於環境啟動層，不硬編碼為測試業務邏輯）。

---

## CLI-First 模擬器環境建立指南

### 1. 設定 Android 環境變數
於 Shell 設定檔（`~/.zshrc` 或 `~/.bashrc`）加入：

```bash
export ANDROID_HOME="$HOME/Library/Android/sdk" # macOS 預設路徑，可依實際位置調整
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
```

驗證 `adb` 指令可用：
```bash
adb version
```

### 2. 安裝 Platform Tools、Emulator 與系統映像檔
接受 SDK 授權並安裝指定套件：

```bash
sdkmanager --licenses

# Apple Silicon (arm64):
sdkmanager "platform-tools" "emulator" "platforms;android-34" "system-images;android-34;google_apis;arm64-v8a"

# x86_64 主機:
sdkmanager "platform-tools" "emulator" "platforms;android-34" "system-images;android-34;google_apis;x86_64"
```

### 3. 透過 CLI 建立 AVD
```bash
# Apple Silicon (arm64):
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;arm64-v8a" --force

# x86_64 主機:
avdmanager create avd -n appium-test-api34 -k "system-images;android-34;google_apis;x86_64" --force
```

### 4. 透過 CLI 啟動模擬器
本機開發可啟動具視窗之一般模擬器：
```bash
emulator -avd appium-test-api34
```

CI 或無桌面環境可使用無介面（headless）啟動：
```bash
emulator -avd appium-test-api34 -no-window -no-audio -no-boot-anim -gpu swiftshader_indirect
```

### 5. 驗證模擬器就緒狀態（Readiness）
不要只執行 `adb devices` 就假設系統已準備就緒。請確認系統屬性 `sys.boot_completed`：

```bash
# 使用 repository 提供的輕量檢查腳本：
./scripts/wait_for_emulator.sh

# 或直接使用 adb 一行指令檢查：
adb wait-for-device
adb shell 'while [[ "$(getprop sys.boot_completed)" != "1" ]]; do sleep 2; done'
```

當就緒時，`adb devices` 會顯示：
```text
emulator-5554    device
```

---

## Appium Server 與測試執行

### 1. 安裝套件相依
```bash
# 安裝 Appium 與 UiAutomator2 驅動程式
npm install -g appium
appium driver install uiautomator2

# 安裝 Python 測試環境相依
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. 下載測試目標 APK
將 APK 放置於專案根目錄的 `apps/`：
```bash
mkdir -p apps
# 下載 Sauce Labs My Demo App Android 2.2.0 release APK 並命名為 apps/mda-2.2.0-238.apk
```

### 3. 啟動 Appium Server
```bash
appium --address 127.0.0.1 --port 4723
```

### 4. 執行 Smoke Test
```bash
pytest tests/smoke/test_app_launch.py -v
```

執行期參數可透過環境變數覆寫：
- `APPIUM_SERVER_URL`：Appium 連線位址（預設：`http://127.0.0.1:4723`）
- `ANDROID_PLATFORM_VERSION`：Android 目標版本（預設：`"14"`）
- `ANDROID_DEVICE_NAME`：Capabilities 裝置名稱（預設：`"Android Emulator"`）
- `ANDROID_APP_PATH`：APK 相對或絕對路徑（預設：`"apps/mda-2.2.0-238.apk"`）
- `EXPLICIT_WAIT_TIMEOUT_SECONDS`：UI 明確等待逾時秒數（預設：`10.0`）

---

## Phase 1 明確排除事項（Non-Goals）

Phase 1 明確不做以下項目：
- 實體 Android 裝置支援
- USB 連線除錯與實體裝置授權邏輯
- 實體裝置專屬之 capabilities
- 業務性 E2E 測試情境（如登入、購物車、結帳流程）
- Screen/Page Object 抽象化（smoke test 保持單純直接）
- AI 自癒（self-healing）或 LLM 修復邏輯

---

## Phase 1 完成標準檢核清單

必須符合以下所有項目，Phase 1 方視為完成：
- [x] Android Studio 不是必要 dependency
- [x] Android SDK CLI-first setup 已完整文件化
- [x] 明確且可重現的模擬器 baseline 已文件化（API 34）
- [x] AVD CLI 建立方式已文件化
- [x] 模擬器 CLI 啟動方式（GUI 與 headless）已文件化
- [x] `adb` 能識別模擬器且 boot readiness 機制已實作
- [x] pytest fixture 正確管理 Appium driver lifecycle 且落實 teardown
- [x] UiAutomator2 session 透過 Appium Python Client 連線至模擬器
- [x] My Demo App 能於模擬器中成功啟動至已知 UI 狀態
- [x] 具備一個驗證完整 runtime chain 的最小 app-launch smoke test
- [x] 程式碼中無任意 `time.sleep()`
- [x] 不存在全域 driver 共享狀態
- [x] APK 二進位檔未被 commit（由 `.gitignore` 保護 `*.apk`）
- [x] 排除實體裝置支援
- [x] 業務 E2E 情境延後至 Phase 2
- [x] Self-healing 與 LLM 邏輯延後至後續里程碑

---

## 專案架構與 Agent 協作機制

- [`AGENTS.md`](AGENTS.md)：定義 repository 全域工程規範、狀態同步準則與 locator 優先階層。
- [`ai/agent-instructions/`](ai/agent-instructions/)：專責 Agent 角色的規範單一真相來源（`senior-mobile-sdet`、`test-architect`、`reviewer`）。
- [`.codex/agents/`](.codex/agents/)：Codex 執行環境轉接器。
- [`.agents/agents/`](.agents/agents/)：Antigravity 執行環境轉接器。
- [`.agents/skills/`](.agents/skills/)：行動端 Appium、測試設計與 Git 變更慣例的共用技能。
- [`src/appium_self_heal/`](src/appium_self_heal/)：最小執行期環境設定模組。
- [`tests/`](tests/): Appium driver fixture（`conftest.py`）與最小測試案例（`tests/smoke/`）。
- [`scripts/`](scripts/): 環境就緒檢查腳本（`wait_for_emulator.sh`）。
- [`pyproject.toml`](pyproject.toml)：專案工具鏈與執行期相依設定。
