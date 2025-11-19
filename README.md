# 💕 女朋友表情辨識器

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://girlfriend-emotion-recognition.streamlit.app)

使用**遷移式學習**（Transfer Learning）技術打造的智慧表情辨識器，能夠辨識女朋友照片中的 7 種表情，並提供貼心的互動建議！

## 🎯 專案特色

- 🤖 **AI 智慧辨識**：使用 MobileNetV2 輕量級神經網路
- 💬 **貼心建議**：每種表情都有多樣化的實用建議
- 🎨 **友善介面**：使用 Streamlit 打造直覺易用的 Web 介面
- ⚡ **快速部署**：可輕鬆部署到 Streamlit Cloud
- 🔄 **持續更新**：AI 建議每次都不同（可選用 OpenAI API）

## 😊 支援的表情

| 表情 | 類別 | 建議範例 |
|------|------|----------|
| 😊 | 開心 (happy) | 太好了！這是告白的好時機喔～ 💕 |
| 😠 | 生氣 (angry) | 快道歉！我建議買花加巧克力組合包！ 🌹🍫 |
| 😢 | 難過 (sad) | 給她一個溫暖的擁抱，告訴她『有我在』 🫂 |
| 😲 | 驚訝 (surprised) | 她嚇一跳的樣子好可愛！趕快問問發生什麼事了～ |
| 😴 | 累了 (tired) | 讓她好好休息，你來做家事吧！💪 |
| 😋 | 餓了 (hungry) | 快去準備她最愛吃的料理吧！🍜 |
| 🤔 | 困惑 (confused) | 耐心解釋清楚，慢慢說給她聽～ 💬 |

## 🚀 快速開始

### 線上體驗（推薦）

直接訪問已部署的應用：
👉 **[girlfriend-emotion-recognition.streamlit.app](https://girlfriend-emotion-recognition.streamlit.app)**

### 本地執行

```bash
# 1. Clone 專案
git clone https://github.com/Katherine623/girlfriend-emotion-recognition_HW4.git
cd girlfriend-emotion-recognition_HW4

# 2. 安裝相依套件
pip install -r requirements.txt

# 3. 執行應用程式
streamlit run app.py
```

應用程式將在瀏覽器自動開啟（http://localhost:8501）

## 📦 技術架構

### 核心技術
- **深度學習框架**：TensorFlow/Keras
- **基礎模型**：MobileNetV2（ImageNet 預訓練）
- **Web 框架**：Streamlit 1.28+
- **影像處理**：Pillow, NumPy
- **AI 建議**：OpenAI GPT-3.5（選用）

### 模型架構

```
Input (224×224×3)
    ↓
MobileNetV2 (預訓練，輕量級)
    ↓
GlobalAveragePooling2D
    ↓
Dense(128, ReLU)
    ↓
Dense(7, Softmax) ← 7 種表情分類
```

**模型大小**：約 1.2 MB（超輕量！）

## 📁 專案結構

```
girlfriend-emotion-recognition_HW4/
├── app.py                  # 主應用程式（核心）
├── auto_train.py          # 自動訓練腳本
├── requirements.txt       # Python 相依套件
├── emotion_model.h5       # 訓練好的模型（1.2 MB）
├── README.md             # 專案說明（本檔案）
├── .gitignore            # Git 忽略設定
│
├── happy/                # 訓練資料：開心表情照片
├── angry/                # 訓練資料：生氣表情照片
├── sad/                  # 訓練資料：難過表情照片
├── surprised/            # 訓練資料：驚訝表情照片
├── tired/                # 訓練資料：累了表情照片
├── hungry/               # 訓練資料：餓了表情照片
└── confused/             # 訓練資料：困惑表情照片
```

## 💡 使用指南

### 1️⃣ 辨識表情（主要功能）

1. 開啟應用程式
2. 點擊「🎯 辨識表情」標籤
3. 上傳女朋友的照片（JPG/PNG 格式）
4. 查看 AI 分析結果：
   - 辨識出的表情
   - 信心度百分比
   - 詳細的機率分布
   - 💝 貼心小建議
   - 💡 更多互動建議

### 2️⃣ 訓練自己的模型（本地）

如果想用自己的照片訓練模型：

```bash
# 1. 準備訓練資料
# 在每個資料夾中放入對應表情的照片
# 建議每個類別 15-20 張

# 2. 執行訓練腳本
python auto_train.py

# 3. 等待訓練完成（約 3-5 分鐘）
# 會生成新的 emotion_model.h5
```

### 3️⃣ 啟用 AI 智慧建議（選用）

1. 前往 [OpenAI](https://platform.openai.com/api-keys) 取得 API Key
2. 在側邊欄輸入 API Key
3. 每次辨識都會生成全新的個性化建議！

## ☁️ 部署到 Streamlit Cloud

### 部署步驟

1. **Fork 或 Clone 本專案到你的 GitHub**
   ```bash
   git clone https://github.com/Katherine623/girlfriend-emotion-recognition_HW4.git
   ```

2. **前往 [Streamlit Cloud](https://streamlit.io/cloud)**
   - 使用 GitHub 帳號登入
   - 點擊 "New app"

3. **設定部署參數**
   - Repository: `your-username/girlfriend-emotion-recognition_HW4`
   - Branch: `main`
   - Main file path: `app.py`

4. **點擊 Deploy**
   - 等待 2-3 分鐘自動部署
   - 完成後獲得公開 URL

### 重要提示

- ✅ `emotion_model.h5` 會自動上傳（已在 repo 中）
- ✅ 訓練照片不會上傳（在 `.gitignore` 中）
- ✅ 應用可直接使用預訓練模型進行辨識
- ❌ Cloud 上無法訓練模型（需在本地訓練）

## 🎓 作業資訊

- **課程**：資訊處理 (w3)
- **學號**：5114056002
- **作業編號**：HW4
- **主題**：遷移式學習 - 女朋友表情辨識器
- **技術重點**：Transfer Learning, MobileNetV2, Streamlit

## 📊 模型效能

- **訓練資料**：75 張照片（本地）
- **訓練時間**：約 3-5 分鐘
- **模型大小**：1.18 MB
- **推論速度**：< 1 秒
- **準確率**：根據訓練資料而異（建議 >80%）

## 📝 開發紀錄

### v3.0 (2024-11-20) - 大幅優化
- ✅ 移除 `love` 類別（7 種表情更精簡）
- ✅ 刪除訓練功能（Cloud 上無法執行）
- ✅ 簡化 UI（移除混淆訊息）
- ✅ 加強錯誤處理（模型載入失敗保護）
- ✅ 清理不必要檔案（減少 18 個檔案）
- ✅ 優化程式碼（從 827 行 → 514 行）

### v2.0 - 功能完善
- ✅ 修復 Streamlit progress 類型錯誤
- ✅ 修復 AI 建議重複問題
- ✅ 優化訓練頁面顯示

### v1.0 - 初始版本
- ✅ 基本表情辨識功能
- ✅ 8 種表情支援
- ✅ Streamlit Cloud 部署

## 💻 開發環境

```
Python 3.8+
tensorflow-cpu 2.x
streamlit 1.28+
pillow 10.x
numpy 1.24+
```

## 🤔 常見問題

<details>
<summary><b>Q: 為什麼辨識不準確？</b></summary>

A: 可能原因：
- 照片不夠清晰
- 表情不夠明顯
- 光線不佳
- 臉部角度太偏

建議使用正面清晰的照片。
</details>

<details>
<summary><b>Q: 可以訓練自己的模型嗎？</b></summary>

A: 可以！在本地執行 `python auto_train.py`。準備每個表情 15-20 張照片會有更好效果。
</details>

<details>
<summary><b>Q: 為什麼 Cloud 上無法訓練？</b></summary>

A: 因為訓練照片沒有上傳到 GitHub（在 .gitignore 中）。請在本地訓練後，將生成的 `emotion_model.h5` 推送到 GitHub。
</details>

<details>
<summary><b>Q: AI 建議需要付費嗎？</b></summary>

A: 不填寫 API Key 時使用免費的預設建議。填寫 OpenAI API Key 後使用 AI 生成建議（會產生少量費用）。
</details>

## 🙏 致謝

- **Streamlit** - 優秀的 Web 框架
- **TensorFlow** - 強大的深度學習框架
- **MobileNetV2** - 輕量高效的 CNN 架構
- **OpenAI** - GPT-3.5 API

## 📜 授權

MIT License - 歡迎學習與分享！

## 🔗 相關連結

- 📱 [線上 Demo](https://girlfriend-emotion-recognition.streamlit.app)
- 💻 [GitHub Repository](https://github.com/Katherine623/girlfriend-emotion-recognition_HW4)
- 📚 [Streamlit 文件](https://docs.streamlit.io/)
- 🧠 [MobileNetV2 論文](https://arxiv.org/abs/1801.04381)

---

<div align="center">
  <p><b>Made with ❤️ for girlfriend by 5114056002</b></p>
  <p>資工在職專班 | HW4 - 遷移式學習</p>
</div>
