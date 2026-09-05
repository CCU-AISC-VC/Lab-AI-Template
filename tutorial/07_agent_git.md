# 7. 讓 AI agent 幫你操作 Git

> 本章適用全實驗室。前提是先讀過 [`06_git_basics.md`](06_git_basics.md) —— 你要看得懂 agent 在做什麼，才有辦法判斷它做得對不對。

Git 指令記不起來很正常。與其背，不如讓 agent 幫你產生指令，你負責看懂再按下去。

## 兩種用法

| | 你用的工具 | 誰執行指令 |
|---|---|---|
| **A. Agent 直接執行** | Claude Code、Cursor 等有終端機權限的 | Agent 自己跑 |
| **B. Agent 只給指令** | 網頁版 ChatGPT / Claude / Gemini | 你自己複製貼上 |

新手建議先從 **B** 開始。你會看到每一條指令、知道自己按了什麼；等到看得懂了再換 A。

---

## 用法 A：讓 agent 直接執行

Claude Code 這類工具可以直接跑 git 指令。你只要用中文描述：

```
我改完濾波參數了，幫我 commit 並 push。
```

Agent 會做的事：看 `git status` 和 `git diff` → 判斷哪些該加 → 寫 commit message → push。

### 你必須看的兩件事

Agent 執行前會顯示指令，**不要無腦按同意**。至少確認：

1. **`git add` 的範圍** —— 有沒有把 `data/raw/`、`.env`、大檔案加進去？
2. **push 的目標** —— 是不是推到你以為的地方？

### 好用的指示方式

```
先給我 git status 的結果，說明每個檔案為什麼該進或不該進 git，
我確認後再 commit。
```

```
幫我看 .gitignore 有沒有漏掉什麼，先不要動手改。
```

```
這次的改動幫我寫 commit message，英文、動詞開頭、50 字以內，
說明「為什麼改」而不是「改了什麼」。
```

---

## 用法 B：Agent 給指令，你自己執行

### 策略 1：Git 助理 prompt（最推薦新人）

貼這段給 agent，之後每次只要描述情況：

```
你是我的 Git 操作助理。我在做實驗數據分析的研究開發。
Repo 結構：scripts/、src/、data/、results/。
data/raw/ 是原始量測資料，絕對不能進 git。

請根據我描述的情況給我：
1. 應執行的 git 指令（可直接複製貼上）
2. commit message 建議
3. 是否需要更新 .gitignore

我的情況是：[描述你做了什麼]
```

### 策略 2：讓它讀 git status

```bash
git status
```

貼給 agent：「以上是我的 git status，請幫我判斷哪些要 add、哪些要 ignore，給我完整操作指令。」

### 策略 3：讓它寫 commit message

```bash
git diff --staged
```

貼給 agent：「請幫我寫一個清楚的 commit message，英文、動詞開頭、50 字以內。」

### 策略 4：讓它生成 .gitignore

```bash
find . -maxdepth 3 -not -path './.git/*' | sort
du -sh * | sort -h
```

貼給 agent：「請幫我判斷哪些要 push、哪些要 ignore，並生成 .gitignore。」

### 策略 5：解錯誤訊息

Git 的錯誤訊息對新手不友善，但對 agent 很好懂。**整段貼上**，不要只貼最後一行 —— 前面幾行通常才是原因。

---

## 絕對不要讓 agent 自己決定的事

這幾條無論用法 A 還是 B 都一樣。它們的共同點是**做錯了救不回來**：

| 操作 | 為什麼危險 |
|---|---|
| `git push --force` | 覆蓋遠端歷史，別人的工作可能消失 |
| `git reset --hard` | 直接丟掉未 commit 的修改，沒有回收桶 |
| `git filter-repo` / `filter-branch` | 重寫整個歷史，所有人都要重新 clone |
| 刪 branch、刪 tag | 尤其是別人的 |
| 動 `data/raw/` | 原始量測資料不可逆，這也是 `instructions.md` 的第一條禁令 |
| 把 token / 密碼寫進檔案 | 一旦 push 就當作外洩 |

Agent 提議做這幾件事的時候，**停下來問人**。這不是 agent 會不會出錯的問題，是這些操作本來就該有第二個人看過。

## Agent 常見的失誤

| 徵兆 | 怎麼處理 |
|---|---|
| `git add .` 一次加了 200 個檔案 | 退回去，先看 `git status`，補 `.gitignore` |
| commit message 寫「update files」 | 要求它說明「為什麼改」 |
| push 失敗就改用 `--force` | 停。正確做法是 `git pull` 再 push |
| 把 `data/raw/` 也加進去 | 這是硬性禁令，退回並檢查 `.gitignore` |
| 一個 commit 混了五件不相干的事 | 要求拆開分次 commit |

## 一個實際的例子

```
你：我改了三個檔案，幫我整理一下要不要分開 commit。

Agent：git status 顯示：
  M  src/filters.py       ← 修正 Butterworth 階數
  M  SPEC.md              ← 更新截止頻率 500Hz
  ?? data/processed/tmp.csv ← 中間輸出

建議：
1. tmp.csv 不該進 git，已在 .gitignore 的 data/processed/* 範圍內
2. 另外兩個是同一件事（濾波參數變更），可以一起 commit

  git add src/filters.py SPEC.md
  git commit -m "Set lowpass cutoff to 500Hz per updated SPEC"

你：好，執行。
```

重點在 agent **說明了每個檔案為什麼這樣處理**，而不是直接 `git add .`。
養成要求它解釋的習慣，你會順便學會 git。

---

下一步：[`08_organization.md`](08_organization.md)（進階，博士班與各組組長閱讀）
