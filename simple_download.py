"""
簡易訓練資料下載工具
使用 Google Images 搜尋結果直接下載
"""

import os
import requests
from pathlib import Path
import time

# 定義情緒類別和搜尋關鍵字
EMOTIONS = {
    'happy': ['happy woman face', 'joyful woman', 'smiling lady'],
    'angry': ['angry woman face', 'mad woman', 'frustrated lady'],
    'sad': ['sad woman face', 'crying woman', 'depressed lady'],
    'surprised': ['surprised woman face', 'shocked woman', 'amazed lady'],
    'tired': ['tired woman face', 'exhausted woman', 'sleepy lady'],
    'hungry': ['hungry woman face', 'woman eating', 'food craving woman'],
    'confused': ['confused woman face', 'puzzled woman', 'uncertain lady'],
    'love': ['loving woman face', 'woman in love', 'romantic woman']
}

# 使用 Lorem Picsum (隨機圖片) 作為範例圖片
def download_sample_images(emotion_folder, count=10):
    """下載範例圖片"""
    os.makedirs(emotion_folder, exist_ok=True)
    
    successful = 0
    for i in range(count):
        try:
            # 使用 Lorem Picsum 提供的隨機圖片
            # 每次使用不同的 seed 來獲取不同圖片
            url = f"https://picsum.photos/seed/{emotion_folder}{i}/400/400"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                filepath = os.path.join(emotion_folder, f"{i+1:03d}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ 下載 {filepath}")
                successful += 1
            
            time.sleep(0.5)  # 避免請求過快
            
        except Exception as e:
            print(f"  ✗ 下載失敗: {str(e)}")
    
    return successful

def download_from_thispersondoesnotexist(emotion_folder, count=10):
    """從 This Person Does Not Exist 下載 AI 生成的人臉"""
    os.makedirs(emotion_folder, exist_ok=True)
    
    successful = 0
    for i in range(count):
        try:
            # 這個網站每次訪問都會生成一個新的 AI 人臉
            url = "https://thispersondoesnotexist.com/image"
            
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                filepath = os.path.join(emotion_folder, f"person_{i+1:03d}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ 下載 {filepath}")
                successful += 1
            
            time.sleep(2)  # 這個網站需要較長間隔
            
        except Exception as e:
            print(f"  ✗ 下載失敗: {str(e)}")
    
    return successful

def main():
    print("\n" + "="*60)
    print("  女朋友表情辨識器 - 簡易訓練資料下載工具")
    print("="*60)
    print("\n選擇下載方式：")
    print("1. 使用 AI 生成人臉 (This Person Does Not Exist) - 推薦")
    print("2. 使用隨機圖片 (Lorem Picsum) - 快速測試")
    print("3. 手動下載指南")
    print()
    
    choice = input("請選擇 (1-3): ").strip()
    
    if choice == "1":
        print("\n🤖 使用 AI 生成人臉...")
        print("注意：每個情緒下載 10 張，總共約需 3-5 分鐘\n")
        
        for emotion in EMOTIONS.keys():
            print(f"\n📁 下載 {emotion} 表情圖片...")
            count = download_from_thispersondoesnotexist(emotion, count=10)
            print(f"✅ {emotion}: 成功下載 {count} 張")
    
    elif choice == "2":
        print("\n📸 使用隨機圖片...")
        print("注意：這些圖片不是人臉，僅供測試\n")
        
        for emotion in EMOTIONS.keys():
            print(f"\n📁 下載 {emotion} 表情圖片...")
            count = download_sample_images(emotion, count=10)
            print(f"✅ {emotion}: 成功下載 {count} 張")
    
    elif choice == "3":
        print("\n" + "="*60)
        print("  📖 手動下載指南")
        print("="*60)
        print("\n建議網站：")
        print("1. Pexels - https://www.pexels.com/")
        print("2. Unsplash - https://unsplash.com/")
        print("3. Pixabay - https://pixabay.com/")
        print("\n搜尋關鍵字：")
        for emotion, keywords in EMOTIONS.items():
            print(f"\n{emotion}:")
            for keyword in keywords:
                print(f"  - {keyword}")
        print("\n步驟：")
        print("1. 到上述網站搜尋關鍵字")
        print("2. 下載至少 10 張符合該情緒的照片")
        print("3. 將照片放到對應的資料夾 (happy/, angry/, 等)")
        print("4. 每個資料夾至少需要 3 張照片才能訓練")
        print()
    
    else:
        print("無效的選擇！")
        return
    
    if choice in ["1", "2"]:
        print("\n" + "="*60)
        print("  ✅ 下載完成！")
        print("="*60)
        print("\n下一步：")
        print("1. 訪問 Streamlit 應用")
        print("2. 前往「訓練模型」標籤")
        print("3. 點擊「開始訓練模型」")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  下載已中斷")
    except Exception as e:
        print(f"\n❌ 發生錯誤: {str(e)}")
