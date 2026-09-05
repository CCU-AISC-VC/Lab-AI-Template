# 9. 該用哪一個 Claude？

> 本章適用全實驗室。
>
> ⚠️ **這幾個產品更新很快。** 本章寫的架構性分工是穩的，但具體介面與功能位置可能已經變了 ——
> 看到跟畫面對不起來，以實際軟體為準，並回來更新這一章。

## 先分清楚兩件事

新手最常混淆的是「chat」和「agent」，這跟你用哪個 app 無關：

| | Chat | Agent（Claude Code / Cowork） |
|---|---|---|
| 誰動手 | 你 | Claude |
| 它看得到什麼 | 只有你貼進去的 | 你的檔案 |
| 它能做什麼 | 產生文字 | 讀寫檔案、執行指令 |
| 出錯的代價 | 幾乎沒有 | 檔案真的被改 |

**Chat 是對話。** 你問「這段 FFT 為什麼能量不守恆」，你要把程式貼給它，它回答，你自己回去改。

**Agent 有手。** 你說「幫我把 acc 從 g 轉成 m/s² 然後重跑」，它會自己讀檔、改檔、執行、看結果、再修。
差別不在誰比較聰明，在**它能不能直接動你的東西**。

## 四個介面

| 介面 | 形態 | 主要用途 |
|---|---|---|
| **Claude Desktop — chat** | 對話 | 問觀念、討論方法、讀論文、寫報告文字 |
| **Claude Desktop — Cowork** | Agent | 文件與資料的多步驟工作，不用開終端機 |
| **Claude Desktop — Claude Code（雲端）** | Agent | 直接讀 GitHub repo 做分析、review、規劃 |
| **VS Code extension** | Agent | 在本機改程式、配合 MATLAB／實際環境 debug |
| **CLI** | Agent | SSH 進 lab server、長時間任務 |

## 雲端還是本地？一個判準

Desktop 的 Claude Code 可以直接讀 GitHub 上的 repo 做分析，不用先 clone 到本機。很方便，但有一條硬邊界：

> **雲端 session 看得到的，只有 git 裡面的東西。**

而你們的 `.gitignore` 把這些擋在 git 外：

```
data/raw/          ← 原始量測資料
data/processed/    ← 中間資料
```

**所以雲端讀不到你的量測資料** —— 這不是限制，是設計。資料太大本來就不該進 git（見 [`06_git_basics.md`](06_git_basics.md)）。
但它直接決定了哪些工作能在雲端做：

| 工作 | 雲端可以嗎 | 為什麼 |
|---|---|---|
| 讀懂別人的分析程式 | ✅ | 程式碼在 git 裡 |
| Review PR、檢查 diff | ✅ | 都在 git 裡 |
| 寫 / 修 `SPEC.md`、`README.md` | ✅ | 都在 git 裡 |
| **寫 PLAN（階段 1）** | ✅ | 規劃階段本來就不寫程式、不碰資料 |
| 實際跑分析、產生圖表 | ❌ | 讀不到 `data/raw/` |
| 跑 MATLAB / 需要 license 的工具 | ❌ | 環境不在雲端 |
| 用實驗室 GPU、連量測儀器 | ❌ | 硬體在本地 |
| 物理合理性檢查 | ❌ | 要真的跑起來才有數字 |

### 對應到三階段流程

這條邊界剛好切在 [`03_first_task.md`](03_first_task.md) 的階段之間：

```
階段 1 規劃    → 雲端很適合（不寫程式、不需要資料，正好符合規則）
階段 2 執行    → 必須本地（要讀 data/raw/、要跑你的環境）
階段 3 驗證    → 必須本地（要真的跑出數字才能檢查）
```

出差、在家、只有平板的時候，**規劃階段可以先用雲端推進**，回到實驗室再執行。

## 本地開發：建議用 VS Code extension

回到實驗室要真的動手時，**建議用 VS Code extension，不要用 chat 貼來貼去**。三個理由：

**1. 看得到 diff。** 改動以紅綠對照呈現，你按下 accept 之前看得到它到底動了什麼。
這正好呼應 [`07_agent_git.md`](07_agent_git.md) 的「不要無腦按同意」—— 在編輯器裡你才有辦法真的看。

**2. 跑得到你的環境。** MATLAB、Python 虛擬環境、CUDA、實驗室 GPU、`data/raw/` 裡的真實資料，
全部都在你這台機器上。Agent 改完可以立刻執行、看到真的錯誤訊息，而不是猜。

**3. `CLAUDE.md` 會生效。** 見下一節。

### 配合 MATLAB 的做法

MATLAB 的程式碼（`.m`）agent 可以讀寫，但**執行要在你的機器上**（license 和 toolbox 都在本機）。
建議的循環：

```
1. 讓 agent 改 .m 檔
2. 你在 MATLAB 裡跑（或讓它用 matlab -batch "script_name" 跑）
3. 把完整錯誤訊息貼回去
4. 重複
```

錯誤訊息**整段貼**，不要只貼最後一行 —— MATLAB 的 stack trace 前面幾層通常才是原因。
另外裝 MathWorks 官方的 MATLAB extension，語法高亮和跳轉會順很多。

### 在 lab server 上跑

需要 GPU 或大量運算時，用 **VS Code + Remote-SSH** 連進 lab server，Claude Code 就跟著在 server 上工作。
本機編輯、server 運算，跟實驗室既有的 server 使用規範一致。

沒有圖形介面、或只能純終端機的情況，用 **CLI**。

## ⚠️ 重要：只有 Claude Code 會自動讀規則

這是最容易踩的坑，也是影響最大的一個：

> **`CLAUDE.md` → `instructions.md` 這套機制，只有 Claude Code（VS Code extension、CLI、Desktop 雲端）會自動生效。**

用 **chat** 的時候，那些規則**一條都不會被讀到**，包括：

- ❌ 不得修改 `data/raw/`
- ❌ 不得自行產生假資料
- ❌ 規劃階段不得寫程式碼
- ❌ 單位與座標系一律以 `SPEC.md` 為準

也就是說，**「我有用 Claude」不等於「有照實驗室的規則跑」。** 用 chat 就要自己把
`instructions.md` 和 `SPEC.md` 整份貼在對話開頭，每開新對話都要重貼一次
（設定方式見 [`01_setup.md`](01_setup.md)）。

## 實驗室建議組合

| 你要做什麼 | 用什麼 |
|---|---|
| 問觀念、討論方法、讀論文 | Desktop — chat |
| 寫 PLAN、review 別人的 PR、改文件 | Desktop — Claude Code（雲端） |
| 改分析程式、配合 MATLAB／Python debug | **VS Code extension** ← 日常主力 |
| 需要 GPU、要在 server 上跑 | VS Code + Remote-SSH，或 CLI |
| 不寫程式的文件整理工作 | Desktop — Cowork |

**一句話版本：** 想事情用 chat，動程式用 VS Code extension，出門在外先用雲端把 PLAN 寫好。
