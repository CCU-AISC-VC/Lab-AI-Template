# 2. 建立你自己的專案

## 複製骨架

```bash
cp -r repo-template/ ../my-project
cd ../my-project
git init && git add -A && git commit -m "Init from Lab AI Template"
```

`repo-template/` 裡的空資料夾靠 `.gitkeep` 保留，複製後結構就是完整的。

## 填寫順序

**先填 `SPEC.md`，再填其他。** 這是整套流程最關鍵的一份，也是唯一填錯會讓結果全錯的一份。

### 第一優先：`SPEC.md`

必填，缺一項就可能出事：

- [ ] **單位系統** — 每個物理量用什麼單位，感測器原始輸出是什麼單位、換算係數多少
- [ ] **座標系** — 原點在哪、XYZ 各朝哪、重力方向。建議畫一張圖放 `results/figures/coordinate_system.png`
- [ ] **感測器表** — 型號、量程、取樣率、安裝位置、校正係數與校正日期
- [ ] **檔名規則與 CSV 欄位** — 包含檔頭要跳過幾行、缺值怎麼表示
- [ ] **已知問題** — 哪個試件哪次量測哪個通道壞了。這欄最容易忘，也最容易害人重跑

不知道的欄位**留白並標註「待確認」**，不要隨便填一個看起來合理的值。留白 agent 會問你，填錯它會照用。

### 第二：`instructions.md`

改「一、專案基本資訊」和「二、技術環境」兩節。其餘（禁止事項、三階段流程、物理檢查、回報格式）建議原樣保留。

想加自己的規則就往「四、禁止事項」加。規則要寫成可驗證的句子：

- 好：「不得使用 `scipy.signal.filtfilt` 以外的濾波實作」
- 壞：「請小心處理濾波」

### 第三：`README.md`

填專案名稱、負責人、原始資料放哪、怎麼跑一次。
寫給半年後的自己和接手的學弟妹看，假設對方什麼都不知道。

## 放資料

```bash
# 原始資料放進來，之後就不要再動它
cp /path/to/raw/*.csv data/raw/
```

`data/raw/` 是唯讀的。所有處理結果一律寫到 `data/processed/`。

大檔案不進 git —— `.gitignore` 已經設定好忽略 `data/raw/` 和 `data/processed/`。
在 `data/README.md` 寫清楚原始資料實際放在哪（NAS 路徑或雲端連結）。

## 檢查清單

開始第一個任務前確認：

- [ ] `SPEC.md` 的單位與座標系已填，沒有留著模板的範例值
- [ ] `data/raw/` 裡有真的資料
- [ ] agent 讀得到規則（做過 [`01_setup.md`](01_setup.md) 的驗證）
- [ ] `DEVLOG.md` 已補上一筆「建立專案」

---

下一步：[`03_first_task.md`](03_first_task.md)
