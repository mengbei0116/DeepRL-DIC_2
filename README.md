# DIC2 - Reinforcement Learning Visualizer

這是一個基於 Flask 的強化學習作業網頁設計，旨在視覺化呈現 **價值迭代 (Value Iteration)** 的演算法過程。
* DEMO網站:https://deep-rl-dic-2.vercel.app/
* 對話過程:

## 專案亮點

### 1. 現代科技感網頁設計 (Tech-Style UI)
*   **深色模式與霓虹元素**：採用深色背景搭配藍色霓虹發光效果，營造未來科技感。
*   **響應式矩陣佈局**：同時呈現 5x5 的 **價值矩陣 (Value Matrix)** 與 **策略矩陣 (Policy Matrix)**。
*   **自定義格位標示**：
    *   **起點 (S)**：左上角 (0,0)，綠色高亮。
    *   **終點 (G)**：右下角 (4,4)，紅色高亮。
    *   **障礙物**：對角線 (1,1), (2,2), (3,3) 設為純黑色區塊。

### 2. 動態價值迭代動畫 (Iterative Visualization)
*   **分步顯示**：點擊「開始價值迭代」按鈕後，網頁會以 **0.3 秒** 的間隔，逐步呈現數值更新與箭頭轉向的過程。
*   **最優路徑高亮**：迭代完成並收斂後，系統會自動選出最佳路徑，並以 **黃色光暈 (#fff700)** 標示所有路徑點（起點與終點保留原色）。

### 3. 前後端整合
*   **後端 (Flask)**：實作了標準的 Value Iteration 演算法，並負責追蹤完整的迭代歷史紀錄以供前端播放動畫。
*   **前端 (Jinja2 + JS)**：透過 Fetch API 與後端非同步通訊，實現無需重新整理的動態更新體驗。

## 運行環境
*   **Python**: Flask, NumPy
*   **Frontend**: Vanilla CSS, JavaScript (ES6+), Google Fonts (Inter, JetBrains Mono)
