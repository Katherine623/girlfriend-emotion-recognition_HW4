# 女朋友表情辨識器 😊

使用遷移式學習技術打造的表情辨識器，能夠辨識女朋友照片中的四種基本表情：開心、生氣、難過、驚訝。

## 🎯 專案簡介

這個專案使用 **ResNet50V2** 預訓練模型，搭配遷移式學習技術，只需要少量訓練資料就能建立一個準確的表情辨識器。

## 🚀 支援的表情

- 😊 **開心** (Happy)
- 😠 **生氣** (Angry)  
- 😢 **難過** (Sad)
- 😲 **驚訝** (Surprised)

## 📦 安裝與執行

### 本地執行

1. **Clone 專案**
```bash
git clone https://github.com/your-username/emotion-recognition.git
cd emotion-recognition
```

2. **安裝相依套件**
```bash
pip install -r requirements.txt
```

3. **準備訓練資料** (可選)
在專案目錄下建立四個資料夾，並放入對應的照片：
```
project/
├── happy/          (放入開心的照片)
├── angry/          (放入生氣的照片)
├── sad/            (放入難過的照片)
└── surprised/      (放入驚訝的照片)
```

建議每個類別至少放入 10-20 張照片以獲得更好的辨識效果。

4. **執行應用程式**
```bash
streamlit run streamlit_app.py
```

應用程式會在瀏覽器中自動開啟（通常是 http://localhost:8501）

## ☁️ 部署到 Streamlit Cloud

### 方法一：透過 GitHub（推薦）

1. **上傳到 GitHub**
   - 建立新的 GitHub Repository
   - 將專案檔案 push 到 GitHub

2. **連接 Streamlit Cloud**
   - 前往 [Streamlit Cloud](https://streamlit.io/cloud)
   - 使用 GitHub 帳號登入
   - 點擊 "New app"
   - 選擇你的 Repository、分支和主檔案 (`streamlit_app.py`)
   - 點擊 "Deploy"

3. **等待部署完成**
   - Streamlit Cloud 會自動安裝相依套件
   - 部署完成後會獲得一個公開的 URL

### 方法二：使用預訓練模型

如果已經有訓練好的模型：

1. 將 `emotion_model.h5` 檔案放在專案根目錄
2. 上傳到 GitHub
3. 部署到 Streamlit Cloud
4. 可以直接使用辨識功能，不需要重新訓練

## 🔧 技術架構

- **深度學習框架**: TensorFlow/Keras
- **預訓練模型**: ResNet50V2 (ImageNet)
- **Web 框架**: Streamlit
- **影像處理**: Pillow, NumPy

### 模型架構
```
ResNet50V2 (預訓練，凍結權重)
    ↓
GlobalAveragePooling2D
    ↓
Dense(128, activation='relu')
    ↓
Dense(4, activation='softmax')
```

## 📁 專案結構

```
emotion-recognition/
├── streamlit_app.py       # Streamlit 應用程式主檔
├── requirements.txt       # Python 相依套件
├── README.md             # 專案說明文件
├── .gitignore           # Git 忽略檔案
├── emotion_model.h5     # 訓練好的模型（可選）
├── happy/               # 開心表情訓練資料
├── angry/               # 生氣表情訓練資料
├── sad/                 # 難過表情訓練資料
└── surprised/           # 驚訝表情訓練資料
```

## 💡 使用說明

### 訓練模型

1. 在應用程式中切換到「🎓 訓練模型」標籤
2. 準備好訓練資料（每個類別的資料夾中放入照片）
3. 點擊「開始訓練模型」按鈕
4. 等待訓練完成（通常需要幾分鐘）

### 辨識表情

1. 切換到「🎯 辨識表情」標籤
2. 上傳一張照片（JPG、JPEG 或 PNG 格式）
3. 查看辨識結果和信心度
4. 根據建議採取行動 😊

## 🎓 作業資訊

- **課程**: 資訊處理
- **學號**: 5114056002
- **作業**: HW4 - 遷移式學習
- **主題**: 女朋友表情辨識器

## 📝 注意事項

- 照片建議是正面清晰的臉部照片
- 表情越明顯，辨識效果越好
- 訓練資料越多且越平衡，模型越準確
- 建議每個類別至少準備 10-20 張照片
- 首次訓練需要下載 ResNet50V2 權重（約 100MB）

## 🤝 貢獻

歡迎提出 Issue 或 Pull Request！

## 📄 授權

MIT License

## 🔗 相關連結

- [Streamlit 官方文件](https://docs.streamlit.io/)
- [TensorFlow 官方文件](https://www.tensorflow.org/)
- [ResNet50V2 論文](https://arxiv.org/abs/1603.05027)

---

Made with ❤️ using Streamlit | 5114056002_HW4
