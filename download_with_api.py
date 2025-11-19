"""
簡易版訓練資料下載器
使用 Pexels 免費 API 下載照片
"""

import os
import requests
import time
from PIL import Image
from io import BytesIO

# Pexels API Key（註冊免費取得：https://www.pexels.com/api/）
# 請替換成你自己的 API Key
PEXELS_API_KEY = "YOUR_API_KEY_HERE"

# 8 種表情的搜尋關鍵字
EMOTIONS = {
    'happy': 'happy woman face portrait',
    'angry': 'angry woman face portrait',
    'sad': 'sad woman crying face',
    'surprised': 'surprised woman shocked face',
    'tired': 'tired exhausted woman face',
    'hungry': 'hungry woman wanting food',
    'confused': 'confused puzzled woman face',
    'love': 'loving affectionate woman face'
}

def download_from_pexels(query, save_folder, api_key, count=15):
    """從 Pexels 下載照片"""
    os.makedirs(save_folder, exist_ok=True)
    
    headers = {
        'Authorization': api_key
    }
    
    url = 'https://api.pexels.com/v1/search'
    params = {
        'query': query,
        'per_page': count,
        'orientation': 'portrait'
    }
    
    try:
        print(f"🔍 搜尋：{query}")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            photos = data.get('photos', [])
            
            downloaded = 0
            for idx, photo in enumerate(photos):
                try:
                    img_url = photo['src']['medium']
                    img_response = requests.get(img_url, timeout=10)
                    
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content))
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        img_path = os.path.join(save_folder, f"img_{idx+1}.jpg")
                        img.save(img_path)
                        downloaded += 1
                        print(f"  ✅ 已下載：{img_path}")
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"  ❌ 下載失敗：{str(e)}")
                    continue
            
            return downloaded
        else:
            print(f"❌ API 請求失敗：{response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ 錯誤：{str(e)}")
        return 0

def main():
    print("""
╔══════════════════════════════════════════════════╗
║     女朋友表情辨識器 - 訓練資料下載工具         ║
╚══════════════════════════════════════════════════╝
    """)
    
    # 檢查 API Key
    if PEXELS_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  請先設定 Pexels API Key！")
        print("\n如何取得 API Key：")
        print("1. 前往：https://www.pexels.com/api/")
        print("2. 註冊免費帳號")
        print("3. 取得 API Key")
        print("4. 將 API Key 貼到此腳本的 PEXELS_API_KEY 變數")
        return
    
    print("🚀 開始下載訓練資料...\n")
    
    total = 0
    for emotion, query in EMOTIONS.items():
        print(f"\n📁 {emotion.upper()}")
        count = download_from_pexels(query, emotion, PEXELS_API_KEY, count=15)
        total += count
        print(f"   完成：{count} 張照片")
    
    print(f"\n🎉 總計下載：{total} 張照片")
    print("\n✅ 下一步：")
    print("   1. python download_training_data.py  # 執行本腳本")
    print("   2. 檢查並清理不適合的照片")
    print("   3. streamlit run app.py  # 啟動應用")
    print("   4. 點擊「訓練模型」開始訓練")

if __name__ == "__main__":
    main()
