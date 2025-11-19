"""
自動下載訓練資料集
從網路上下載表情照片作為訓練資料
"""

import os
import requests
from PIL import Image
from io import BytesIO
import time

# 8 種表情的搜尋關鍵字
emotions = {
    'happy': ['happy face', 'smiling woman', 'joyful expression'],
    'angry': ['angry face', 'mad expression', 'upset woman'],
    'sad': ['sad face', 'crying woman', 'upset expression'],
    'surprised': ['surprised face', 'shocked expression', 'amazed woman'],
    'tired': ['tired face', 'exhausted woman', 'sleepy expression'],
    'hungry': ['hungry face', 'craving food', 'wanting to eat'],
    'confused': ['confused face', 'puzzled expression', 'thinking woman'],
    'love': ['loving face', 'affectionate expression', 'adoring woman']
}

def download_from_unsplash(query, save_folder, count=15):
    """
    從 Unsplash 下載照片（免費無版權）
    """
    os.makedirs(save_folder, exist_ok=True)
    
    # Unsplash API（使用公開存取）
    base_url = "https://source.unsplash.com/800x600/?"
    
    downloaded = 0
    for i in range(count):
        try:
            # 添加隨機參數避免快取
            url = f"{base_url}{query}&sig={i}"
            
            print(f"下載 {query} 照片 {i+1}/{count}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                # 轉換為 RGB（避免 RGBA 問題）
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 儲存
                img_path = os.path.join(save_folder, f"{query.replace(' ', '_')}_{i+1}.jpg")
                img.save(img_path)
                downloaded += 1
                print(f"✅ 已儲存：{img_path}")
            
            # 避免請求過快
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ 下載失敗：{str(e)}")
            continue
    
    return downloaded

def download_all_training_data():
    """
    下載所有表情的訓練資料
    """
    print("🚀 開始下載訓練資料...")
    print("=" * 50)
    
    total_downloaded = 0
    
    for emotion, keywords in emotions.items():
        print(f"\n📁 處理表情：{emotion}")
        folder = emotion
        
        for keyword in keywords:
            count = download_from_unsplash(keyword, folder, count=5)
            total_downloaded += count
            
        print(f"✅ {emotion} 完成！")
    
    print("\n" + "=" * 50)
    print(f"🎉 完成！總共下載 {total_downloaded} 張照片")
    print("\n下一步：")
    print("1. 檢查各資料夾中的照片")
    print("2. 刪除不合適的照片")
    print("3. 執行 Streamlit 應用：streamlit run app.py")
    print("4. 在「訓練模型」標籤訓練模型")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════╗
║     女朋友表情辨識器 - 訓練資料下載工具         ║
║                                                  ║
║  這個腳本會從 Unsplash 下載免費無版權照片       ║
║  作為訓練資料。每種表情約下載 15 張照片。       ║
╚══════════════════════════════════════════════════╝
    """)
    
    input("按 Enter 開始下載...")
    download_all_training_data()
