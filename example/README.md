# Example：五分鐘跑一次完整流程

> 這是**跑一次就懂**的示範。不用先讀完 tutorial，做完這個再回去讀，會比較有感覺。
>
> 需要：Python 3、`numpy`、`matplotlib`。

## 這個 example 在演什麼

一趟完整的 **plan-first 流程**，而且刻意跨兩台機器，順便演示雲端與本機的分工：

```
☁️  雲端（已完成）          💻 你的電腦（接下來）
─────────────────────      ─────────────────────
階段 1：寫 PLAN       →  git pull  →  階段 2：寫程式、執行
準備資料                                階段 3：驗證、出圖
                       ←  git push  ←
```

階段 1 已經幫你做好了：[`plans/2026-09-05_cubic_fit.md`](plans/2026-09-05_cubic_fit.md)。
你要做的是階段 2 和 3 —— **因為那需要真的把程式跑起來**，雲端做不到。

## 資料

`data/cubic_measurement.csv` —— 80 筆力與位移的量測。

```
# Synthetic demo data - NOT a real measurement
# generated 2026-09-05 | seed=20260905 | gaussian noise sigma=2.0 N
# columns: x_mm (displacement, mm), force_N (force, N)
x_mm,force_N
-3.0000,-102.3541
...
```

兩件事先講清楚：

1. **前 3 行是檔頭**，讀檔要跳過 —— 這是真實儀器資料常見的狀況，故意留著讓你踩一次
2. **這是合成資料，不是真的量測**，檔案第一行就標明了

> 第 2 點很重要。`instructions.md` 禁止 agent 自己產生假資料 ——
> 但**標明用途的練習資料**是另一回事。差別在於「有沒有誠實標示」，不在於資料是不是真的。

## 怎麼跑

### 1. 在你的電腦上取得這個 repo

```bash
git clone https://github.com/CCU-AISC-VC/Lab-AI-Template.git
cd Lab-AI-Template
```

已經有了的話：`git pull origin main`

### 2. 用 VS Code 開啟，讓 agent 讀 PLAN

```bash
code .
```

然後跟 Claude Code 說：

```
請讀 example/plans/2026-09-05_cubic_fit.md，
依照 PLAN 的步驟執行階段 2。
一次只做一步，做完回報結果，等我說繼續。
```

### 3. 一步一步跑完

PLAN 有 5 步。**每一步做完就停下來看結果**，不要讓它一口氣做完 ——
這正是 plan-first 的重點。

### 4. 驗證

跑完之後，對照 PLAN 第 4 節的驗收標準逐項確認。
這組資料的真值是已知的，所以你可以**真的檢查它有沒有算對**：

```
真值：force_N = 2.0·x³ − 5.0·x² + 3.0·x + 7.0
```

擬合出來的三次項應該很接近 2.0。如果差很多，八成是檔頭沒跳過。

### 5. 推回去

```bash
git add example/scripts example/results
git commit -m "Add cubic fit script and results"
git push
```

推上去之後，雲端的 session 就讀得到你的結果了 —— 圖和程式碼都在 git 裡。

## 跑完之後你會注意到

| 你經歷了什麼 | 對應章節 |
|---|---|
| 先有 PLAN 才動手，一步一停 | [`../tutorial/03_first_task.md`](../tutorial/03_first_task.md) |
| 用已知真值驗證程式有沒有算對 | [`../tutorial/04_verification.md`](../tutorial/04_verification.md) |
| 檔頭沒跳過會得到很離譜的係數 | [`../tutorial/00_why.md`](../tutorial/00_why.md) |
| 規劃可以在雲端，執行必須在本機 | [`../tutorial/09_claude_surfaces.md`](../tutorial/09_claude_surfaces.md) |
| commit / push 把結果送回去 | [`../tutorial/06_git_basics.md`](../tutorial/06_git_basics.md) |

## 資料夾

```
example/
├─ README.md                 你在看的這份
├─ plans/                    ✅ 階段 1 已完成
├─ data/                     ✅ 資料已備好（唯讀，不要改）
├─ scripts/                  ⬜ 階段 2：agent 在這裡寫程式
└─ results/
   ├─ figures/               ⬜ 階段 3：圖存這裡
   └─ tables/                ⬜ 階段 3：表存這裡
```
