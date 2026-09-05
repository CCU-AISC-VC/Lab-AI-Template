# 6. Git 基礎：pull 與 push

> 本章適用全實驗室，不分組別。只要你的工作會產生程式碼或設定檔，就需要這章。
> 內容整理自 Notion〈lab_github_guide〉，已移除特定組別與機器人專案的設定。

## 為什麼要用 Git

不用 Git 的下場，大家都遇過：

```
analysis.py
analysis_v2.py
analysis_v2_final.py
analysis_v2_final_真的最後.py
analysis_v2_final_真的最後_修正版.py
```

半年後你不知道哪個是對的，也不知道 v2 跟 v3 差在哪、為什麼要改。

Git 解決三件事：**留下每次改動的理由**、**隨時回到任何一個過去版本**、**多人改同一份不會互相覆蓋**。

## GitHub 和 Notion 各放什麼

兩個工具分工，不要混用：

| | GitHub | Notion |
|---|---|---|
| 放什麼 | 可執行的東西 | 人讀的東西 |
| 例子 | `.py` 腳本、設定檔、`SPEC.md` | 實驗紀錄、debug 筆記、安裝 SOP |
| 核心價值 | 版本控制、程式碼共享 | 知識沉澱、跨人共享思路 |
| 不適合放 | 大型資料、心得說明 | 程式碼本體 |

**整合的關鍵**：在 Notion 的每一篇實驗紀錄裡，貼上對應的 GitHub commit 或 PR 連結。
讓「結論」和「當時的程式碼版本」永遠綁在一起 —— 否則半年後你會看到一個結論，卻找不到produce它的程式。

```
## 實驗：<題目>
- 日期：2026-09-05
- 負責人：
- 對應 commit：https://github.com/<你的帳號>/<repo>/commit/a3f92b1
- 環境：Python 3.11, numpy 1.26
- 結果：
```

## 第一次設定

只做一次。

```bash
sudo apt update && sudo apt install git

git config --global user.name "你的名字"
git config --global user.email "你的學校信箱@ccu.edu.tw"
```

信箱要用你 GitHub 帳號上的那個，否則 commit 不會算在你名下。

### 設定 Token

GitHub 從 2021 年起不接受密碼，push 的時候 Password 欄位要貼 **Personal Access Token**：

1. GitHub → 右上角頭像 → Settings
2. 左側最底部 → Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token → 勾選 **repo** → 複製

存起來免得每次都要貼：

```bash
git config --global credential.helper store
```

> Token 等同密碼。不要貼進程式碼、不要貼進 Notion、不要貼給 AI agent。

## 日常循環

這五步就是 90% 的日常操作：

```
開始工作
    ↓
git pull                  ← 先拉最新版，避免衝突
    ↓
做你的修改
    ↓
git status                ← 確認到底改了哪些檔案
    ↓
git add .
git commit -m "說明這次改了什麼"
    ↓
git push
    ↓
在 Notion 更新紀錄（貼 commit 連結）
```

**`git pull` 要養成習慣在動手前先做。** 改完才發現別人也改了同一個檔案，處理起來麻煩得多。

**`git status` 是最該常按的指令。** 在 `git add .` 之前看一眼，你會發現很多本來不該進 git 的東西（暫存檔、大型資料、`.env`）。

### Commit message 怎麼寫

寫給半年後的自己看。重點是**為什麼**，不是**改了什麼**（改了什麼看 diff 就知道）。

```bash
# 好
git commit -m "Fix unit conversion: acc was in g, not m/s^2"
git commit -m "Add Butterworth lowpass, cutoff 500Hz per SPEC"

# 沒用
git commit -m "update"
git commit -m "修改"
git commit -m "aaa"

# 自己的工作區開發中，這樣也可以接受
git commit -m "WIP: testing new filter params"
```

## 什麼要進 git，什麼不要

### 要 ✅

| 類型 | 例子 |
|---|---|
| 程式碼 | `*.py`, `*.m` |
| 設定檔 | `*.yaml`, `*.json`, `*.toml` |
| 說明文件 | `README.md`, `SPEC.md`, `DEVLOG.md` |
| 需求列表 | `requirements.txt` |
| 小型結果 | `results/figures/*.png`, `results/tables/*.csv` |

### 不要 ❌

| 類型 | 原因 |
|---|---|
| `__pycache__/`, `*.pyc` | Python 暫存 |
| `*.pt`, `*.pth`, `*.ckpt` | 模型權重太大 |
| `data/raw/`, `data/processed/` | 量測資料太大，用 NAS 共享 |
| `logs/` | 大量且無版本意義 |
| `.env` | **裡面有 API key 和密碼** |
| `venv/`, `.venv/` | 虛擬環境，用 `requirements.txt` 重建就好 |
| `.DS_Store`, `._*`, `Thumbs.db` | 作業系統雜物 |
| **任何 > 100MB 的檔案** | GitHub 硬性限制，放 NAS 或雲端，在 Notion 貼連結 |

`repo-template/.gitignore` 已經把這些設好了，複製過去就生效。

> **大檔案要在 push 前擋掉。** 一旦 commit 進去，即使之後刪掉，它還是留在 git 歷史裡，repo 會永久變肥。清除歷史的方法見 [`08_organization.md`](08_organization.md)，那是要找人幫忙的操作。

### 不確定的時候

```bash
find . -maxdepth 3 -not -path './.git/*' | sort
du -sh * | sort -h
```

把輸出貼給 AI agent，請它判斷並生成 `.gitignore`。詳見 [`07_agent_git.md`](07_agent_git.md)。

## 讓別人能重現你的環境

程式碼進了 git 不代表別人跑得起來。至少要鎖住套件版本：

```bash
pip freeze > requirements.txt      # 產出目前環境
pip install -r requirements.txt    # 別人在新電腦安裝
```

再把版本寫進 `README.md`：

```markdown
## 環境版本
| 工具 | 版本 |
|---|---|
| Python | 3.11 |
| numpy | 1.26 |
```

## 救援指令

做錯了不要慌，幾乎都救得回來。

```bash
git restore <檔案>          # 丟掉還沒 commit 的修改
git reset HEAD <檔案>       # 取消 add（檔案內容不受影響）
git revert HEAD             # 用一個新 commit 抵銷上一次 commit（安全，歷史保留）
git stash                   # 手邊改到一半，先收起來
git stash pop               # 拿回來
```

> `git reset --hard` 和 `git push --force` 會**真的刪掉東西**。不確定就先問人，不要自己試。

## 常用指令速查

```bash
# 看狀態
git status                  # 哪些檔案被改了
git log --oneline           # commit 歷史簡潔版
git diff                    # 還沒 add 的改動
git diff --staged           # 已 add、還沒 commit 的改動

# 基本操作
git pull                    # 拉最新版
git add .                   # 加入全部修改
git add <檔案>              # 只加某個檔案（比 . 安全）
git commit -m "說明"        # 建立 commit
git push                    # 推上去

# Branch
git branch                  # 看目前有哪些 branch
git checkout -b <名稱>      # 開一個新 branch 並切過去
git checkout main           # 切回 main
```

## FAQ

**Q：push 說 `rejected` 怎麼辦？**
代表遠端有你本機沒有的 commit。先 `git pull`，處理完衝突再 `git push`。

**Q：`git pull` 出現 conflict？**
打開衝突檔案，會看到 `<<<<<<<` / `=======` / `>>>>>>>` 標記。留下你要的內容、刪掉標記，然後 `git add` 該檔案再 `git commit`。不確定就把檔案內容貼給 agent 問。

**Q：不小心 commit 了密碼或 token？**
**先去 GitHub 把那個 token 撤銷（revoke）**，這是最重要的一步。改密碼比清歷史重要，因為只要推出去過就要當作已經外洩。之後再處理歷史。

**Q：`git add .` 把不該加的東西加進去了？**
還沒 commit 的話 `git reset HEAD <檔案>` 就好，然後把它加進 `.gitignore`。

---

下一步：[`07_agent_git.md`](07_agent_git.md)
