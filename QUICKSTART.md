# 女朋友表情辨識器 - 快速開始指南

## 🚀 快速開始

### 1️⃣ 安裝相依套件

```powershell
pip install -r requirements.txt
```

### 2️⃣ 準備訓練資料

建立四個資料夾並放入對應的照片：

```
5114056002_HW4/
├── happy/          (放入開心表情的照片 10-20 張)
├── angry/          (放入生氣表情的照片 10-20 張)
├── sad/            (放入難過表情的照片 10-20 張)
└── surprised/      (放入驚訝表情的照片 10-20 張)
```

**注意**：
- 照片建議是正面清晰的臉部照片
- 表情越明顯越好
- 每個類別建議至少 10 張照片
- 支援 JPG、JPEG、PNG 格式

### 3️⃣ 執行應用程式

```powershell
streamlit run app.py
```

應用程式會在瀏覽器中自動開啟（預設是 http://localhost:8501）

### 4️⃣ 使用步驟

1. **訓練模型**：
   - 切換到「🎓 訓練模型」標籤
   - 確認資料夾和照片數量
   - 點擊「🚀 開始訓練模型」
   - 等待訓練完成（約 3-5 分鐘）

2. **辨識表情**：
   - 切換到「🎯 辨識表情」標籤
   - 上傳一張照片
   - 查看辨識結果和建議

---

## 📤 部署到 Streamlit Cloud

### 準備步驟

1. **上傳到 GitHub**：

```powershell
# 初始化 Git（如果還沒有）
git init

# 加入檔案
git add .

# 提交
git commit -m "Initial commit: 女朋友表情辨識器"

# 連接到 GitHub（替換成你的 repository URL）
git remote add origin https://github.com/你的用戶名/emotion-recognition.git

# 推送
git branch -M main
git push -u origin main
```

2. **部署到 Streamlit Cloud**：
   - 前往 https://streamlit.io/cloud
   - 用 GitHub 帳號登入
   - 點擊 "New app"
   - 選擇你的 repository
   - 主檔案選擇：`app.py`
   - 點擊 "Deploy"

3. **等待部署完成**：
   - 通常需要 3-5 分鐘
   - 完成後會獲得公開 URL

### 使用預訓練模型

如果你已經訓練好模型：

**方法 1**：直接上傳模型檔案
```powershell
git add emotion_model.h5
git commit -m "Add trained model"
git push
```

**方法 2**：使用 Git LFS（模型 > 100MB）
```powershell
git lfs install
git lfs track "*.h5"
git add .gitattributes emotion_model.h5
git commit -m "Add model with LFS"
git push
```

---

## 📁 專案結構

```
5114056002_HW4/
├── app.py                 # 主程式（Streamlit 應用）
├── requirements.txt       # Python 相依套件
├── README.md             # 專案說明
├── DEPLOY.md             # 詳細部署指南
├── .gitignore           # Git 忽略檔案
├── app_old.ipynb        # 原始 Jupyter Notebook
├── emotion_model.h5     # 訓練好的模型（訓練後產生）
├── happy/               # 開心表情訓練資料
├── angry/               # 生氣表情訓練資料
├── sad/                 # 難過表情訓練資料
└── surprised/           # 驚訝表情訓練資料
```

---

## 🎯 功能說明

### 🎯 辨識表情
- 上傳照片進行表情辨識
- 顯示四種表情的信心度
- 根據結果給予建議

### 🎓 訓練模型
- 自動載入訓練資料
- 顯示資料集資訊
- 訓練進度即時顯示
- 訓練歷史圖表視覺化
- 模型評估和建議

### ℹ️ 關於
- 專案簡介
- 技術說明
- 模型架構
- 部署指南

---

## 🔧 技術架構

- **深度學習框架**：TensorFlow/Keras
- **預訓練模型**：ResNet50V2 (ImageNet)
- **Web 框架**：Streamlit
- **影像處理**：Pillow, NumPy
- **資料分析**：Pandas, Matplotlib

### 模型架構
```
Input (224x224x3)
    ↓
ResNet50V2 (預訓練，凍結)
    ↓
GlobalAveragePooling2D
    ↓
Dense(256, ReLU) + Dropout(0.5)
    ↓
Dense(128, ReLU) + Dropout(0.3)
    ↓
Dense(4, Softmax)
    ↓
Output (4 classes)
```

---

## ❓ 常見問題

### Q: 訓練需要多久時間？
**A**: 約 3-5 分鐘（取決於資料量和電腦效能）

### Q: 為什麼辨識不準確？
**A**: 可能原因：
- 訓練資料太少
- 照片品質不佳
- 表情不夠明顯
- 資料不平衡

建議：增加訓練資料，每類至少 15-20 張清晰照片。

### Q: 可以辨識其他表情嗎？
**A**: 可以！修改 `categories` 和 `labels` 變數，並準備對應的訓練資料。

### Q: 模型檔案太大無法上傳 GitHub？
**A**: 使用 Git LFS 或將模型放在雲端儲存（Google Drive、Dropbox 等）。

### Q: 部署後如何更新模型？
**A**: 重新訓練後提交新的 `emotion_model.h5`，Streamlit Cloud 會自動重新部署。

---

## 📊 效能優化建議

1. **增加訓練資料**：每類 20+ 張照片
2. **資料平衡**：確保每類照片數量相近
3. **資料增強**：翻轉、旋轉、調整亮度等
4. **調整超參數**：學習率、batch size、epochs
5. **微調模型**：解凍部分基礎模型層進行訓練

---

## 📝 作業資訊

- **課程**：資訊處理
- **學號**：5114056002
- **作業**：HW4 - 遷移式學習
- **主題**：女朋友表情辨識器

---

## 📞 需要幫助？

- 查看 `DEPLOY.md` 了解詳細部署步驟
- 查看 `README.md` 了解專案詳情
- 檢查 Streamlit 官方文件：https://docs.streamlit.io/

---

祝您使用愉快！🎉
