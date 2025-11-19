# 訓練資料準備指南

## 🎯 目標
為每種表情收集 10-20 張照片

## 📂 需要建立的資料夾
```
5114056002_HW4/
├── happy/      (開心的表情)
├── angry/      (生氣的表情)
├── sad/        (難過的表情)
├── surprised/  (驚訝的表情)
├── tired/      (疲倦的表情)
├── hungry/     (飢餓的表情)
├── confused/   (困惑的表情)
└── love/       (充滿愛意的表情)
```

## 🔍 照片來源（免費無版權）

### 方法 1：Unsplash（推薦）
1. 前往：https://unsplash.com/
2. 搜尋關鍵字：
   - `happy woman face`
   - `angry woman expression`
   - `sad woman crying`
   - `surprised shocked face`
   - `tired exhausted woman`
   - `hungry woman`
   - `confused puzzled face`
   - `loving woman smile`
3. 下載照片到對應資料夾

### 方法 2：Pexels
1. 前往：https://www.pexels.com/
2. 搜尋相同關鍵字
3. 下載免費照片

### 方法 3：Pixabay
1. 前往：https://pixabay.com/
2. 搜尋表情關鍵字
3. 下載免費圖片

## 📋 照片要求

✅ **好的照片：**
- 清晰的正面照
- 單一人物
- 表情明顯
- 光線充足
- JPG/PNG 格式

❌ **避免：**
- 模糊不清
- 多人照片
- 側臉或背面
- 表情不明顯
- 太暗或過曝

## 🚀 快速開始

### 使用自動下載腳本（需要 API Key）
```bash
# 1. 安裝依賴
pip install requests pillow

# 2. 執行下載腳本
python download_with_api.py
```

### 手動下載
1. 在專案目錄建立 8 個資料夾
2. 從上述網站下載照片
3. 每個資料夾放 10-20 張照片
4. 執行應用並訓練

## 📝 訓練步驟

1. **準備完資料後：**
   ```bash
   streamlit run app.py
   ```

2. **在應用中：**
   - 切換到「訓練模型」標籤
   - 檢查資料集概況
   - 點擊「開始訓練模型」
   - 等待 5-10 分鐘完成訓練

3. **訓練完成後：**
   - 切換到「辨識表情」標籤
   - 上傳照片測試
   - 查看辨識結果和建議

## 💡 小技巧

- **最少數量**：每類至少 10 張
- **建議數量**：每類 15-20 張
- **最佳數量**：每類 30+ 張（準確度更高）
- **照片品質 > 數量**：寧缺毋濫

## 🎓 作業展示重點

即使沒有訓練完成的模型，也可以展示：
1. ✅ 完整的應用架構
2. ✅ 遷移式學習設計（MobileNetV2）
3. ✅ 8 種表情分類系統
4. ✅ LLM 整合（OpenAI GPT-3.5）
5. ✅ 完整的訓練流程介面
6. ✅ 詳細的文檔說明

## 📞 需要幫助？

如果遇到問題，可以：
1. 查看 README.md
2. 查看 EMOTIONS_GUIDE.md（詳細的表情指南）
3. 查看 AI_GUIDE.md（LLM 設定指南）
