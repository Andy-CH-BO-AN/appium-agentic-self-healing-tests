# 專案協作與 Agent 工程規範

本文件定義本 repository 的工程規範與 AI Agent / 開發者的協作準則。

## 專案核心

- **專案範疇**：以 Android 為優先（Android-first）的行動端自動化測試。
- **技術堆疊**：Python、pytest、Appium 與 UiAutomator2。
- **簡單為先**：優先採用簡單且明確的實作，避免過早抽象化。在沒有明確需求前，不引入通用的包裝框架。
- **人類主導**：人類工程師保有最終架構決策與程式碼合併權限。

## 行動端測試工程原則

- **測試獨立性**：測試案例必須隔離且可獨立執行。嚴禁依賴測試執行順序或跨測試共享可變狀態。
- **明確狀態同步**：嚴禁使用任意固定 `sleep`。一律採用基於狀態的明確等待機制（例如 `WebDriverWait` 搭配 expected conditions）。
- **穩定 Locator 策略**：遵守 Android 定位器優先順序：
  1. Accessibility ID（`content-desc`）
  2. 穩定的 Android resource-id
  3. Android UIAutomator（`AppiumBy.ANDROID_UIAUTOMATOR`，如文字比對或滾動容器）
  4. 窄範圍 Scoped XPath（僅作為最後手段）
  避免使用絕對 XPath、深層階層 XPath、脆弱的 index 選擇器或硬編碼螢幕座標。
- **職責分離**：UI 互動細節與 locator 定義封裝於 Screen/Page Object 中；測試案例本身只專注表達使用者旅程、業務意圖與結果驗證。
- **具實質意義的 Assertion**：斷言必須驗證使用者可感知的實際結果與應用程式真實狀態，而非僅僅確認操作執行未拋出例外。
- **禁止掩蓋 Flaky**：嚴禁以 retry 迴圈或隨意拉長 timeout 掩蓋非預期的 flaky 行為，必須追查並修正根本原因。

## 驗證與誠實回報

- **強制執行驗證**：任何程式碼變更必須透過現有工具進行最相關的驗證（linters、formatters、語法檢查、目標測試）。
- **誠實回報結果**：嚴禁宣稱未實際執行的驗證。清楚回報已驗證項目與環境限制。

## 專責 Agent 角色

共用角色規範位於 `ai/agent-instructions/`：

- `senior-mobile-sdet`（[`ai/agent-instructions/senior-mobile-sdet.md`](ai/agent-instructions/senior-mobile-sdet.md)）：負責 Python、pytest、Appium、Android、UiAutomator2、driver 生命週期、locators 與 Screen Object 的技術實作決策。
- `test-architect`（[`ai/agent-instructions/test-architect.md`](ai/agent-instructions/test-architect.md)）：負責測試策略、情境設計、覆蓋率評估、風險優先級與測試獨立性設計。
- `reviewer`（[`ai/agent-instructions/reviewer.md`](ai/agent-instructions/reviewer.md)）：唯讀審查程式碼正確性、flaky 風險、locator 穩定度、隱藏 sleep、過度抽象與驗證缺口。

執行環境轉接器（Runtime Adapters）：
- **Codex**：`.codex/agents/*.toml`
- **Antigravity**：`.agents/agents/*.md`

## Repository Skills

共用技能位於 `.agents/skills/`：
- `appium-android`：Android 與 Appium 實作慣例、UiAutomator2 locator 策略與生命週期管理。
- `mobile-test-design`：設計高價值、隔離且可獨立執行的行動端 E2E 測試情境指南。
- `git-change-conventions`：Branch、commit 與 pull request 命名標準。
