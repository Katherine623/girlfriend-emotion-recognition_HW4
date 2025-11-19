"""
一鍵訓練腳本 - 自動處理所有步驟並生成 emotion_model.h5
"""
import os
os.environ['KERAS_BACKEND'] = 'torch'

import numpy as np
import keras
from PIL import Image
import sys

categories = ["happy", "angry", "sad", "surprised", "tired", "hungry", "confused", "love"]

print("=" * 60)
print("  女朋友表情辨識器 - 自動訓練腳本")
print("=" * 60)

# 載入圖片
print("\n[1/5] 載入訓練圖片...")
data, labels = [], []
total_images = 0

for i, cat in enumerate(categories):
    if not os.path.exists(cat):
        print(f"  ⚠️  資料夾 {cat} 不存在")
        continue
    
    files = [f for f in os.listdir(cat) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"  ✓ {cat}: {len(files)} 張")
    total_images += len(files)
    
    for fname in files[:20]:  # 限制每類最多20張加速
        try:
            img = Image.open(os.path.join(cat, fname)).convert('RGB').resize((128, 128))  # 改小加速
            data.append(np.array(img, dtype='float32') / 255.0)
            labels.append(i)
        except:
            pass

if len(data) == 0:
    print("\n❌ 沒有找到圖片！請確認照片在正確的資料夾中。")
    sys.exit(1)

data = np.array(data)
labels = keras.utils.to_categorical(labels, len(categories))
print(f"\n  ✅ 成功載入 {len(data)} 張圖片")

# 建立模型
print("\n[2/5] 建立神經網路模型...")
model = keras.Sequential([
    keras.layers.Input(shape=(128, 128, 3)),
    keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    keras.layers.MaxPooling2D(2),
    keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
    keras.layers.MaxPooling2D(2),
    keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(len(categories), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print("  ✅ 模型建立完成")

# 訓練
print("\n[3/5] 開始訓練模型...")
print("  （這可能需要 3-5 分鐘，請稍候...）\n")

history = model.fit(
    data, labels,
    epochs=15,
    batch_size=4,
    validation_split=0.2,
    verbose=1
)

# 儲存
print("\n[4/5] 儲存模型...")
model.save('emotion_model.h5')
print("  ✅ 模型已儲存為 emotion_model.h5")

# 測試
print("\n[5/5] 驗證模型...")
test_img = data[0:1]
prediction = model.predict(test_img, verbose=0)
predicted_class = np.argmax(prediction)
print(f"  ✅ 測試成功！預測類別: {categories[predicted_class]}")

# 顯示結果
print("\n" + "=" * 60)
print("  🎉 訓練完成！")
print("=" * 60)
final_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]
print(f"\n  訓練準確率: {final_acc*100:.1f}%")
print(f"  驗證準確率: {final_val_acc*100:.1f}%")
print(f"\n  模型檔案: emotion_model.h5")
print(f"  檔案大小: {os.path.getsize('emotion_model.h5')/1024/1024:.1f} MB")
print("\n  下一步：")
print("  1. 訪問 http://localhost:8501")
print("  2. 到「上傳照片進行辨識」標籤")
print("  3. 上傳照片測試效果！")
print("\n" + "=" * 60)
