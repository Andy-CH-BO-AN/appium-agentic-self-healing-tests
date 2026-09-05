---
name: git-change-conventions
description: 在此 repository 建立或命名 branch、pull request、commit 時使用。遵守既定 type prefix，並撰寫詳盡 commit message。
---

# Git 變更與命名慣例

在建立或命名 branch、撰寫 pull request 標題與描述，或撰寫 commit message 時使用此技能。

## PR 標題格式

Pull Request 標題必須嚴格採用：
`<TYPE>: <summary>`

允許的 `<TYPE>`：
- `FEATURE:` 新增功能
- `FIX:` 修復錯誤
- `REFACTOR:` 無行為變更的程式碼重構
- `DOCS:` 僅文件變更
- `TEST:` 僅測試新增或修改
- `STYLE:` 僅格式化、排版或 lint 清理
- `PERF:` 效能改進
- `CHORE:` 維護、設定、tooling 或環境變更
- `CI:` 持續整合設定或工作流程腳本

範例：`CHORE: establish agent-ready repository foundation`

## Branch 命名格式

Git branch 不可含冒號或空白，採用：
`<type>/<summary-in-kebab-case>`

規則：
- 前綴採用小寫，且與 PR type 保持一致（如 `feat`、`fix`、`chore`、`docs`、`test`、`refactor`）。
- 摘要轉為小寫 kebab-case。

範例：`chore/phase-0-agent-foundation`

## Commit Message 規範

- **清楚且詳盡**：避免過短或語意不清的單字 commit。
- **Subject 行**：精確說明變更意圖與受影響範圍。
- **多行 Body**：非 trivial 變更必須附帶多行說明：
  - **Summary / Why**：說明為何需要此變更與所解決的問題。
  - **What Changed**：條列核心調整與變更點。
  - **Validation**：具體記錄已執行的驗證指令與結果。

範例：
```text
CHORE: establish agent-ready repository foundation

- Add AGENTS.md defining repository-wide rules for Android Appium tests
- Establish canonical role instructions in ai/agent-instructions/
- Add thin runtime adapters for Codex (.codex/agents/*.toml) and Antigravity (.agents/agents/*.md)
- Implement reusable skills in .agents/skills/ for appium-android, mobile-test-design, and git-change-conventions
- Add minimal pyproject.toml tooling configuration and update README.md
```

## Pull Request 內容結構

建立 Pull Request 時，描述應包含以下區塊：

```markdown
## Summary
<簡述此 PR 的目的與新增內容>

## Why
<為何需要此變更與背景原因>

## Changes
- <檔案/模組>: <變更說明>

## Validation
- <已執行的測試、檢查指令與結果>
```
