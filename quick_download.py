"""
快速下載訓練圖片 - 使用 Lorem Picsum
這個方法最快且穩定
"""

import os
import requests
import time

# 情緒列表
emotions = ['happy', 'angry', 'sad', 'surprised', 'tired', 'hungry', 'confused', 'love']

print("\n🚀 開始下載訓練圖片...\n")

total = 0
for emotion in emotions:
    # 建立資料夾
    os.makedirs(emotion, exist_ok=True)
    
    print(f"📁 {emotion}:")
    success = 0
    
    for i in range(15):  # 每個情緒下載 15 張
        try:
            # 使用 Lorem Picsum 的隨機圖片 API
            url = f"https://picsum.photos/seed/{emotion}{i}/300/300"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                filepath = os.path.join(emotion, f"{i+1:03d}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                success += 1
                print(f"  ✓ {i+1}/15", end="\r")
            
            time.sleep(0.3)  # 短暫延遲避免請求過快
            
        except Exception as e:
            print(f"  ✗ 圖片 {i+1} 失敗: {str(e)}")
    
    print(f"  ✅ 完成！下載 {success} 張圖片")
    total += success

print(f"\n{'='*50}")
print(f"🎉 全部完成！總共下載 {total} 張圖片")
print(f"{'='*50}\n")
print("下一步：")
print("1. 訪問 Streamlit 應用")
print("2. 前往「訓練模型」標籤")  
print("3. 點擊「開始訓練模型」\n")
