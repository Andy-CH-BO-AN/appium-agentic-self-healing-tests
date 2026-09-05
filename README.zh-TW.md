# appium-agentic-self-healing-tests

繁體中文 | [English](README.md)

基於 Appium 的 Android 應用程式 AI Agent 輔助自癒端到端（E2E）自動化測試系統。

---

## 專案概述

行動端端到端（E2E）測試常因無害的 UI locator 變更而中斷——例如 resource ID 重新命名、accessibility label 調整或畫面結構微調（locator drift）。

本專案提供以 Android 為優先（Android-first）的行動測試框架，核心目標為：
1. 對 Android 原生應用程式執行可靠且穩定的 E2E 測試。
2. 在測試執行過程中偵測定位器失效與測試漂移。
3. 透過 AI Agent 對 Screen/Page Object 提出精準、受限的自動修復建議。
4. 在交付人類審查前，透過確定性的迴歸執行驗證修復程式碼的正確性。

## 技術堆疊

- **目標平台**：Android（Android-first 設計）
- **程式語言**：Python（>= 3.10）
- **測試框架**：pytest
- **自動化引擎**：Appium 搭配 UiAutomator2 driver
- **目標展示應用程式**：[Sauce Labs My Demo App Android](https://github.com/saucelabs/my-demo-app-android/releases)（基準版本：`2.2.0`）

## 專案架構與 Agent 協作機制

本專案採用共用來源（shared-source）的 Agent 架構，確保 Codex 與 Antigravity 代理人遵循一致規範且不產生指令漂移：

- [`AGENTS.md`](AGENTS.md)：定義 repository 全域工程規範、狀態同步準則與 locator 優先階層。
- [`ai/agent-instructions/`](ai/agent-instructions/)：專責 Agent 角色的規範單一真相來源（`senior-mobile-sdet`、`test-architect`、`reviewer`）。
- [`.codex/agents/`](.codex/agents/)：Codex 執行環境轉接器。
- [`.agents/agents/`](.agents/agents/)：Antigravity 執行環境轉接器。
- [`.agents/skills/`](.agents/skills/)：行動端 Appium、測試設計與 Git 變更慣例的共用技能。
- [`pyproject.toml`](pyproject.toml)：專案工具鏈與 linter 靜態檢查設定。
