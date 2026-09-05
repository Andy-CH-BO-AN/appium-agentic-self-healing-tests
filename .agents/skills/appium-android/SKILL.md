---
name: appium-android
description: Android 與 Appium 實作最佳實踐、UiAutomator2 locator 策略、同步等待與 driver 生命週期管理。
---

# Appium Android 行動端工程準則

在實作、重構或審查 Appium Android 自動化測試、定位器（locators）、driver fixture 或 Screen/Page Object 時使用此技能。

## 1. Android Locator 策略

Android 視圖元件辨識與 Web DOM 有本質上的不同。請一律遵守 Android 優先定位階層：

### 推薦優先順序
1. **Accessibility ID（`AppiumBy.ACCESSIBILITY_ID`）**：
   - 對應 Android 的 `content-desc` 屬性。
   - 具可感知性、語意清楚且穩定，為第一優先考量。
2. **Resource ID（`AppiumBy.ID`）**：
   - 對應 Android 的 `package:id/view_id`。
   - 當 ID 穩定且在當前畫面具唯一性時使用。
3. **Android UIAutomator（`AppiumBy.ANDROID_UIAUTOMATOR`）**：
   - Android 原生 UiSelector 語法（例如 `new UiSelector().text("...")` 或 `new UiScrollable(...)`）。
   - 適合文字比對或滾動容器操作。
4. **窄範圍 Scoped XPath（`AppiumBy.XPATH`）**：
   - 僅在無任何語意識別碼或原生 UIAutomator 查詢無法達成時，作為最後手段。
   - 必須嚴格限縮在已知、明確的父容器範圍內。

### 禁止之反模式
- **嚴禁絕對 XPath**：例如 `/hierarchy/android.widget.FrameLayout/...`。
- **嚴禁深層階層 XPath**：避免脆弱的祖先節點串聯。
- **避免 Index 選擇器**：除非操作的是已驗證的同質清單，否則避免 `//android.widget.TextView[3]`。
- **嚴禁任意螢幕座標點擊**：標準 UI 元件不得使用固定 `(x, y)` 座標點擊。
- **不可套用 Web 慣例**：勿將 Playwright/CSS 選擇器模式直接套用至 Android 原生視圖。

## 2. 同步與等待機制

- **僅採用明確狀態等待**：一律使用 `WebDriverWait` 搭配 expected conditions（如可見性、可點擊性）。
- **嚴禁使用任意固定 Sleep**：禁止使用 `time.sleep()`，這會拖慢測試且無法保證穩定性。
- **禁止以 Retry 迴圈掩蓋 Flaky**：不可把不穩定的操作包進 retry 迴圈中，必須排查是否為畫面動畫、狀態未就緒或 locator 缺陷。

## 3. Driver 與 Session 生命週期

- **明確的 Driver 擁有權**：Appium driver 的建立與釋放一律透過 pytest fixture 管理，確保 teardown 必然執行。
- **乾淨且可預期的初始狀態**：每個測試案例必須從已知狀態開始（全新啟動、重置或明確初始導航）。
- **無跨測試隱式狀態**：測試絕不可依賴前一個測試留下的狀態或暫存。

## 4. Screen / Page Objects

- **封裝 Locator 與操作細節**：原始 locator 與 driver 呼叫集中在 Screen Object 中。
- **避免多餘的 Framework 包裝**：不包裝沒有額外領域語意的 wrapper（如無意義的 `custom_click`）。
- **主要斷言保留在測試案例中**：驗證使用者結果的核心 assertion 寫在測試函式中，維持測試表達力。

## 5. 失敗診斷

測試失敗時應能自動擷取：
- 失敗當下的螢幕截圖（Screenshot）。
- 完整的畫面 XML 原始碼（Page Source）以便排查視圖階層。
- 相關的 device logcat 記錄片段。
- 絕不無聲吞下 exception，確保保留完整 traceback。
