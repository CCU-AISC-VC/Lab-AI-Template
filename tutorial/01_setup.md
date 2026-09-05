# 1. 環境準備

目標：讓你用的 AI agent 每次開工都會先讀到 `instructions.md`。

## 為什麼要特別設定

`instructions.md` 是這個 repo 的常駐規則，但 agent 預設不會去讀它。
每個工具讀規則的方式不同，設定一次之後就不用再管。

`repo-template/` 裡已經附好各家的指向檔，複製過去就能用。

## 各工具設定

### Claude Code

已經設定好，不用做任何事。`CLAUDE.md` 內容只有一行：

```
請先閱讀 @instructions.md，並在本 repo 的所有工作中完整遵守其中的規則。
```

`@instructions.md` 這個寫法會讓 Claude Code 自動把整份規則載進來。

### GitHub Copilot

已附 `.github/copilot-instructions.md`。VS Code 需開啟設定：

```
Settings → GitHub Copilot → Use Instruction Files ✓
```

### Cursor

已附 `.cursor/rules/main.mdc`，開啟專案即生效。

### 網頁版 ChatGPT / Gemini / Claude

沒有規則檔機制，只能手動：**把 `instructions.md` 整份貼在對話的第一則訊息**，接著貼 `SPEC.md`，然後才開始講你要做什麼。

換新對話就要重貼一次。這也是為什麼建議用有規則檔機制的工具。

## 驗證有沒有生效

開一個新對話，問：

> 這個 repo 的禁止事項有哪幾條？規劃階段可以寫程式碼嗎？

正確回答應該答得出「不得修改 `data/raw/`」「不得自行產生假資料」「規劃階段不得寫程式碼」這幾條。

答不出來 → 規則沒讀到，回去檢查設定。

## Python 環境

模板預設 Python 3.11 + numpy / scipy / pandas / matplotlib：

```bash
cd my-project
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

用 MATLAB 或其他語言的話，把 `instructions.md`「二、技術環境」那一節改掉即可，流程本身不變。

---

下一步：[`02_start_project.md`](02_start_project.md)
