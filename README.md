# appium-agentic-self-healing-tests

[繁體中文](README.zh-TW.md) | English

Automated, agent-assisted self-healing end-to-end test suite for Android applications using Appium.

---

## Overview

Mobile end-to-end (E2E) test suites frequently fail due to benign UI locator drift—such as updated resource IDs, modified accessibility labels, or layout restructurings.

This repository provides an Android-first mobile test automation framework designed to:
1. Execute reliable E2E tests against native Android applications.
2. Detect locator failures and test drift during test runs.
3. Propose scoped, verifiable repairs to Screen/Page Objects using AI agents.
4. Validate proposed repairs deterministically through regression execution before human review.

## Technology Stack

- **Platform**: Android (Android-first design)
- **Language**: Python (>= 3.10)
- **Test Runner**: pytest
- **Automation Engine**: Appium with UiAutomator2 driver
- **Target Application**: [Sauce Labs My Demo App Android](https://github.com/saucelabs/my-demo-app-android/releases) (baseline release: `2.2.0`)

## Repository Structure & Agent Collaboration

This project uses a shared-source agent architecture to ensure consistent operation across Codex and Antigravity environments:

- [`AGENTS.md`](AGENTS.md): Repository-wide engineering rules, synchronization invariants, and locator guidelines.
- [`ai/agent-instructions/`](ai/agent-instructions/): Canonical instructions for dedicated agent roles (`senior-mobile-sdet`, `test-architect`, `reviewer`).
- [`.codex/agents/`](.codex/agents/): Codex runtime adapters.
- [`.agents/agents/`](.agents/agents/): Antigravity runtime adapters.
- [`.agents/skills/`](.agents/skills/): Reusable skills for Appium Android, mobile test design, and Git conventions.
- [`pyproject.toml`](pyproject.toml): Repository tooling and linter configuration.