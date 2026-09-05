# 8. Organization 與 Fork 協作（進階）

> **📌 閱讀對象：博士班學生與各組組長。**
> 碩班與大專生不需要先讀這章 —— 你只要會 [`06_git_basics.md`](06_git_basics.md) 的 pull / push 就能開始工作。
>
> **Organization 由各組自行開設與管理。** 本章提供的是共用架構與規範，各小組依自己的題目建立自己的 organization 與 repo，不共用同一個。組長負責該組的權限、review 與 main 分支的品質。
>
> 內容整理自 Notion〈lab_github_guide〉，已抽換為通用寫法。

---

## 什麼時候才需要這一套

先確認你真的需要。判準只有一個：**這個 repo 有沒有多個人同時要改？**

| 情況 | 用什麼 |
|---|---|
| 一個人的專案 | 個人 repo，直接 push，不用 fork |
| 兩三個人、彼此信任 | 一個共用 repo，各開各的 branch |
| 一組人、main 必須隨時可用 | Organization + Fork + PR（本章） |

小組只有兩個人卻硬要跑 fork + PR，只會讓大家嫌麻煩然後繞過它。**先確定痛點存在，再加流程。**

---

## 一、三層結構

```
上游原始專案（如果你們是基於某個開源專案）
        ↓ 各組基於此建立
<你們組的 Organization>/<專案名>        ← 組內 main repo（可信版本）
        ↓ 每個人 fork
<個人帳號>/<專案名>                      ← 個人開發 fork（草稿本）
```

| | 上游原始專案 | 組內 main repo | 個人 fork |
|---|---|---|---|
| 定位 | 官方原始碼 | 組內可信版本 | 個人草稿本 |
| 內容 | 原始碼 | 原始碼 + 組內自己的設定、腳本、資料規格 | 各自的實驗開發 |
| 誰能 push | 上游維護者 | 只能透過 PR + review | 自己隨便 push |
| 新成員 | 不要直接 clone | ✅ 以這個為基礎 fork | clone 自己的 fork |

**為什麼要 fork 而不是大家一起 push main：**
main 是「隨時可以拿來跑、拿來交報告」的版本。每個人直接 push，main 就會處在半成品狀態，
誰都不敢用。Fork 讓每個人有自己的草稿本，只有通過 review 的東西才進 main。

### 本機資料夾建議

```
~/<專案名>/                        ← main repo，組長管理用
~/Github_Dev_workspace/
    <專案名>/                      ← 個人日常開發工作區（每個人都有）
```

---

## 二、開設 Organization（組長做一次）

1. GitHub → 右上角頭像 → Settings → Organizations → New organization
2. 命名建議：`CCU-AISC-<組別代號>`，看得出是哪間實驗室的哪一組
3. 建立組內 main repo，把 `repo-template/` 的內容推上去當骨架
4. People → 邀請組員，權限給 **Write** 就夠（他們是透過 PR 進 main，不需要 Admin）
5. Settings → Branches → 對 `main` 加 branch protection：
   - ✅ Require a pull request before merging
   - ✅ Require approvals（至少 1 人）

> 第 5 步是整套流程真正生效的地方。沒有 branch protection，「要發 PR」只是口頭約定，
> 遲早有人趕時間就直接 push 了。

---

## 三、新成員第一次設定

假設 Git 已經裝好、身分已經設定（見 [`06_git_basics.md`](06_git_basics.md)）。

### 3-1 Fork 組內 repo

1. 去 `https://github.com/<組織名>/<專案名>`
2. 右上角按 **Fork** → 選你的個人帳號
3. repo 名稱保持不變

### 3-2 Clone 你的 fork

```bash
mkdir -p ~/Github_Dev_workspace
cd ~/Github_Dev_workspace
git clone https://github.com/<你的帳號>/<專案名>.git
cd <專案名>
```

注意 clone 的是**你的 fork**，不是組織的 repo。

### 3-3 設定 upstream

```bash
git remote add upstream https://github.com/<組織名>/<專案名>.git

git remote -v
# origin   → 你的 fork      （推送個人開發）
# upstream → 組內 main repo （拉最新版）
```

兩個 remote 的分工要記住：**從 upstream 拉、往 origin 推。**
`git push upstream` 會失敗（也應該失敗）—— 進 main 的唯一途徑是 PR。

---

## 四、Fork 工作流程

```bash
# Step 1：同步組內最新版
git pull upstream main

# Step 2：開發、commit、推到自己的 fork
git add .
git commit -m "Add modal analysis for S03 specimen"
git push origin main

# Step 3：在 GitHub 發 Pull Request
#   → 進你的 fork 頁面
#   → 按「Contribute」→「Open pull request」
#   → 填寫說明

# Step 4：等 review → merge 進組內 main

# Step 5：merge 後同步自己的 fork
git pull upstream main
git push origin main
```

**Step 1 不要跳過。** 直接開始改，等到要發 PR 才發現落後 main 三十個 commit，衝突會很難處理。

### PR 說明範本

```
## 這個 PR 做了什麼
新增 S03 試件的模態分析流程，輸出前三階固有頻率。

## 測試方式
1. 跑 scripts/2026-09-02_modal_analysis.py
2. 確認 results/figures/2026-09-02_S03_fft.png 產生

## 物理合理性檢查
- 單位：acc 已由 g 轉 m/s²（×9.80665）
- 數量級：一階 12.1 Hz，與 FE 模型 12.4 Hz 差 2.4%
- Parseval：FFT 前後能量差 0.3%

## 相關 Notion 紀錄
https://www.notion.so/...

## 注意事項
需要 SPEC.md 中 LC-1 的校正係數已填
```

「物理合理性檢查」那一段是這個實驗室的 PR 該有、但一般軟體專案沒有的東西。
Review 的人第一個就看這段 —— 詳見 [`04_verification.md`](04_verification.md)。

### Review 該看什麼

組長或指定的 reviewer 至少確認：

- [ ] 物理合理性檢查有做，而且附了數字不是只寫「已確認」
- [ ] 沒有把 `data/raw/`、大檔案、`.env` 夾帶進來
- [ ] 單位轉換有對照 `SPEC.md`
- [ ] 有可以重跑的腳本，不是只有結果圖
- [ ] `DEVLOG.md` 有補紀錄

---

## 五、常見問題

**Q：PR 被要求修改，怎麼改？**
在你自己的 fork 上繼續 commit 再 `git push origin main`，PR 會自動更新，不用重開。

**Q：我的 fork 跟組內 main 差太多，怎麼同步？**
```bash
git fetch upstream
git merge upstream/main
git push origin main
```

**Q：什麼時候該發 PR？**
功能做完、自己測過、物理合理性檢查通過、覺得值得放進組內共用版本的時候。
做到一半不用發。

**Q：可以直接 push 到組內 main 嗎？**
不行，這是 branch protection 擋著的。真的緊急要修，找組長。

---

## 六、大檔案善後（危險操作，找人一起做）

如果已經不小心把大檔案 commit 進去了，即使之後刪掉，它還是留在 git 歷史裡，
repo 會永久變肥、clone 會很慢。清除的方法：

```bash
pip install git-filter-repo --break-system-packages
export PATH="$PATH:$HOME/.local/bin"

git filter-repo --strip-blobs-bigger-than 100M --force
git remote add origin https://github.com/<你的帳號>/<專案名>.git
git push origin main --force
```

> ⚠️ **這會重寫整個歷史。** 執行前：
> 1. 先把整個資料夾複製一份備份
> 2. 確認這個 repo 只有你一個人在用，或先通知所有人
> 3. 執行後所有人都必須重新 clone，他們手上的舊 clone 會壞掉
>
> 在組內 main repo 上做這件事，一定要組長同意並全組通知。
> 不要交給 AI agent 自己決定執行 —— 見 [`07_agent_git.md`](07_agent_git.md) 的禁止清單。

**預防遠比補救便宜。** `repo-template/.gitignore` 已經擋掉常見的大檔案來源，先確認它有生效。
