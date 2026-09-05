# Lab AI Template

給研究室使用的 AI agent 工作流程模板。目的是讓 agent 產出的結果**可重現、可檢查、可交接**，而不是一次性的對話。

## 這個 repo 有什麼

```
├─ tutorial/           教學文件：從零開始學會這套流程
└─ repo-template/      專案骨架：直接複製到你的新專案
```

- **第一次接觸** → 從 [`tutorial/README.md`](tutorial/README.md) 開始讀
- **已經懂流程、要開新專案** → 直接複製 [`repo-template/`](repo-template/)

## 核心概念

這套模板建立在三件事上：

1. **Plan-first**：任何任務先寫 PLAN，人審過才動手寫程式。
2. **規格外置**：單位、座標系、感測器設定寫在 `SPEC.md`，agent 不准自行假設。
3. **強制驗證**：每次數值產出都要跑物理合理性檢查（單位、數量級、守恆、極端情況）。

## 快速開始

```bash
# 1. 複製骨架到你的新專案
cp -r repo-template/ ../my-project
cd ../my-project
git init

# 2. 填寫這三份檔案的空白處
#    instructions.md  專案基本資訊、技術環境
#    SPEC.md          單位、座標系、感測器、資料格式
#    README.md        專案說明

# 3. 讓 AI agent 讀規則後開工
#    Claude Code 會自動讀 CLAUDE.md，其他工具見 tutorial/01_setup.md
```

完整步驟見 [`tutorial/02_start_project.md`](tutorial/02_start_project.md)。

## 適用對象

實驗數據分析、數值模擬、訊號處理類的研究專案。範例以結構動力量測為主，但流程本身與領域無關。
