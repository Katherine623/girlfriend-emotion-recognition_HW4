# 部署指南

## 📤 上傳到 GitHub

### 1. 初始化 Git Repository

在專案資料夾中開啟 PowerShell，執行：

```powershell
git init
git add .
git commit -m "Initial commit: 女朋友表情辨識器"
```

### 2. 建立 GitHub Repository

1. 前往 [GitHub](https://github.com)
2. 點擊右上角的 "+" → "New repository"
3. 填寫資訊：
   - Repository name: `emotion-recognition` 或自訂名稱
   - Description: `女朋友表情辨識器 - 使用遷移式學習辨識表情`
   - 選擇 Public（公開）或 Private（私人）
   - **不要**勾選 "Initialize this repository with a README"
4. 點擊 "Create repository"

### 3. 推送到 GitHub

複製 GitHub 提供的指令，或執行：

```powershell
git remote add origin https://github.com/your-username/emotion-recognition.git
git branch -M main
git push -u origin main
```

將 `your-username` 替換成你的 GitHub 使用者名稱。

---

## ☁️ 部署到 Streamlit Cloud

### 1. 註冊 Streamlit Cloud

1. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
2. 點擊 "Sign up" 或 "Get started"
3. 使用 GitHub 帳號登入（建議）

### 2. 部署應用程式

1. 登入後點擊 "New app"
2. 填寫部署資訊：
   - **Repository**: 選擇你的 `emotion-recognition` repository
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. 點擊 "Deploy!"

### 3. 等待部署完成

- Streamlit Cloud 會自動：
  - 讀取 `requirements.txt`
  - 安裝所有相依套件
  - 啟動應用程式
- 通常需要 3-5 分鐘
- 完成後會獲得一個公開的 URL，例如：
  - `https://your-app-name.streamlit.app`

### 4. 設定（可選）

在 Streamlit Cloud 控制台可以：
- 設定環境變數
- 查看日誌
- 重新部署
- 管理域名

---

## 🎯 使用預訓練模型（推薦）

如果你已經在本地訓練好模型：

### 選項 1：上傳模型檔案到 GitHub

```powershell
# 在 .gitignore 中註解掉這一行：
# emotion_model.h5

git add emotion_model.h5
git commit -m "Add pre-trained model"
git push
```

**注意**：GitHub 單一檔案限制 100MB，如果模型太大需要使用 Git LFS。

### 選項 2：使用 GitHub LFS（模型 > 100MB）

```powershell
# 安裝 Git LFS
# Windows: 從 https://git-lfs.github.com/ 下載安裝

# 初始化 LFS
git lfs install

# 追蹤 .h5 檔案
git lfs track "*.h5"

# 提交
git add .gitattributes
git add emotion_model.h5
git commit -m "Add model with LFS"
git push
```

### 選項 3：使用雲端儲存

將模型上傳到 Google Drive 或其他雲端空間，在程式中下載：

```python
import gdown

# 在 streamlit_app.py 中加入
if not os.path.exists("emotion_model.h5"):
    url = "https://drive.google.com/uc?id=YOUR_FILE_ID"
    gdown.download(url, "emotion_model.h5", quiet=False)
```

---

## 🐛 常見問題

### Q1: 部署失敗，顯示 "ModuleNotFoundError"
**A**: 檢查 `requirements.txt` 是否包含所有需要的套件。

### Q2: TensorFlow 安裝太慢或失敗
**A**: 在 `requirements.txt` 中使用較舊版本：
```
tensorflow==2.12.0
```

### Q3: 記憶體不足
**A**: Streamlit Cloud 免費版有記憶體限制（1GB），考慮：
- 使用更小的模型
- 減少 batch size
- 優化程式碼

### Q4: 訓練資料沒有上傳
**A**: 這是正常的（被 .gitignore 排除），用戶需要：
- 自己準備訓練資料，或
- 使用預訓練模型

### Q5: URL 想自訂
**A**: Streamlit Cloud 設定中可以修改 App URL。

---

## 📊 效能優化建議

1. **使用預訓練模型**：避免在 Streamlit Cloud 上訓練
2. **快取載入**：使用 `@st.cache_resource` 裝飾器
3. **壓縮圖片**：在上傳前先壓縮
4. **減少依賴**：只安裝必要的套件

---

## 🔒 隱私與安全

- 不要在 GitHub 上傳私人照片
- 使用 `.gitignore` 排除敏感資料
- 考慮使用 Private Repository
- Streamlit Cloud 可設定存取密碼（付費版）

---

## 📞 技術支援

- [Streamlit 官方論壇](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)
- [Streamlit 文件](https://docs.streamlit.io/)

---

完成部署後，你可以分享應用程式的 URL 給任何人使用！🎉
