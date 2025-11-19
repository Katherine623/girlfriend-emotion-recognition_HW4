"""
女朋友表情辨識器
使用遷移式學習 (ResNet50V2) 辨識多種表情
作業：5114056002_HW4
"""

import streamlit as st

# 設定頁面配置
st.set_page_config(
    page_title="女朋友表情辨識器",
    page_icon="😊",
    layout="centered"
)

# 顯示載入進度
with st.spinner('🚀 正在載入 AI 模型...'):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2  # 改用輕量級模型
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input  # 對應的預處理
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    from tensorflow.keras.utils import to_categorical
    from PIL import Image
    import os
    import random

# 應用程式標題
st.title("💕 女朋友表情辨識器")
st.markdown("### 上傳女朋友的照片，讓AI告訴你她現在的心情，還有貼心小建議！")

# 辨識類別（增加更多表情）
categories = ["happy", "angry", "sad", "surprised", "tired", "hungry", "confused", "love"]
labels = ["開心 😊", "生氣 😠", "難過 😢", "驚訝 😲", "累了 😴", "餓了 😋", "困惑 🤔", "愛你 🥰"]

# 為每種表情準備多個可愛建議
emotion_suggestions = {
    "happy": [
        "太好了！她心情超好的！這是告白的好時機喔～ 💕",
        "哇！她笑得好開心！趁現在說什麼她都會答應的！😊",
        "她看起來心花怒放！要不要趁機約她出去玩呢？ 🎉",
        "好開心的表情！快去跟她說些甜言蜜語吧～ 💖",
        "她這麼開心，一定是因為想到你啦！繼續加油！ ✨"
    ],
    "angry": [
        "糟糕！她好像不太開心... 我去幫你買她最愛的甜點賠罪吧！ 🍰",
        "警報！警報！快道歉！我建議買花加巧克力組合包！ 🌹🍫",
        "哎呀～她生氣了！要不要說『都是我的錯，原諒我好嗎？』 🙏",
        "她看起來在生悶氣... 給她一個大大的擁抱也許會好一點？ 🤗",
        "建議你現在立刻、馬上去哄她！說不定她只是想要你的關心～ 💝"
    ],
    "sad": [
        "她看起來有點難過... 我去買你們最愛的冰淇淋，陪她一起吃！ 🍦",
        "寶貝不開心了！給她一個溫暖的擁抱，告訴她『有我在』 🫂",
        "她需要安慰！要不要看部她喜歡的電影，然後靠著你肩膀？ 🎬",
        "看起來心情低落... 陪她聊聊天，聽聽她的煩惱吧！ 💭",
        "她可能需要你的陪伴！放下手機，專心陪伴她吧～ 💕"
    ],
    "surprised": [
        "哇！她看起來很驚訝！是不是你準備了什麼驚喜呀？ 🎁",
        "她嚇一跳的樣子好可愛！趕快問問發生什麼事了～ 😲",
        "驚訝的表情！該不會是你忘記什麼重要的日子了吧？😅",
        "她看起來很意外！快去確認是好事還是壞事～ 🤔",
        "這個表情！趕快去關心她，說不定有好消息要告訴你！ ✨"
    ],
    "tired": [
        "她看起來好累喔... 我去泡杯熱可可給她，你幫她按摩肩膀！ ☕",
        "寶貝累了～讓她好好休息，你來做家事吧！💪",
        "她需要休息！準備一個舒服的枕頭，陪她睡個午覺～ 😴",
        "看起來筋疲力盡了... 今晚讓她放鬆，你來煮晚餐吧！🍳",
        "她太累了！取消所有行程，今天就在家耍廢陪她～ 🛋️"
    ],
    "hungry": [
        "她看起來餓了！我馬上去買好吃的給她！你想吃什麼？ 🍕",
        "肚子餓餓～快去準備她最愛吃的料理吧！🍜",
        "她餓了！叫個外送或是帶她去吃大餐～記得甜點也要有喔！ 🍰",
        "看這表情就知道她餓扁了！快去覓食，什麼都好就是要快！ 🍔",
        "她需要食物補充能量！買她最愛的零食或是煮碗熱騰騰的麵～ 🍲"
    ],
    "confused": [
        "她看起來有點困惑... 快去問問她在想什麼，需要你幫忙嗎？ 🤔",
        "這個表情是不懂你在說什麼！說清楚一點，慢慢解釋給她聽～ 💬",
        "她好像霧煞煞的... 耐心一點，陪她一起解決問題！ 🧩",
        "困惑模式啟動！趕快去當她的解說員，順便展現你的聰明才智！ 🤓",
        "她不明白！別再繞圈子了，直接說重點吧～ 💡"
    ],
    "love": [
        "天啊！她正在散發愛的光芒！這是表達愛意的最佳時刻！ 💖",
        "她看起來充滿愛意～快說『我也愛你』然後給她一個吻！ 💋",
        "滿滿的愛心眼神！她一定超愛你的！繼續保持這樣下去！ 🥰",
        "這個眼神～她完全被你迷住了！要好好珍惜她喔！ 💝",
        "充滿愛的表情！說些浪漫的話，讓她知道你也愛她！ 💕"
    ]
}

# 建立模型函數
@st.cache_resource
def create_model():
    """創建並載入預訓練模型 - 使用 MobileNetV2 輕量級模型"""
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # 凍結基礎模型的權重
    base_model.trainable = False
    
    # 建立新模型
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(128, activation='relu'),
        Dense(len(categories), activation='softmax')
    ])
    
    return model

# 預測函數
def predict_emotion(image, model):
    """預測圖片中的表情"""
    # 調整圖片大小
    img = image.resize((224, 224))
    
    # 轉換為陣列
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # 預處理
    img_array = preprocess_input(img_array)
    
    # 預測
    predictions = model.predict(img_array, verbose=0)
    
    return predictions[0]

# 側邊欄 - 說明
with st.sidebar:
    st.header("📖 使用說明")
    st.markdown("""
    1. **設定 API Key**（可選）：啟用 AI 智慧建議
    2. **訓練模型**：點擊「開始訓練模型」按鈕
    3. **上傳照片**：上傳女朋友的照片
    4. **查看結果**：AI 會分析並顯示她的心情
    5. **AI 建議**：獲得每次都不同的貼心建議
    
    ---
    
    **支援的表情：**
    - 😊 開心
    - 😠 生氣
    - 😢 難過
    - 😲 驚訝
    - 😴 累了
    - 😋 餓了
    - 🤔 困惑
    - 🥰 愛你
    
    ---
    
    **提示：**
    - 照片建議是正面清晰的臉部照片
    - 表情越明顯，辨識效果越好
    - 設定 API Key 後每次建議都不同！
    """)
    
    st.markdown("---")
    
    # API Key 設定
    st.subheader("🤖 AI 智慧建議設定")
    st.markdown("""
    啟用後，每次辨識都會生成**全新的個性化建議**！
    
    **如何取得 API Key：**
    1. 前往 [OpenAI](https://platform.openai.com/api-keys)
    2. 註冊並建立 API Key
    3. 複製並貼到下方
    """)
    
    api_key_input = st.text_input(
        "OpenAI API Key（選填）",
        type="password",
        help="不填寫則使用預設建議",
        placeholder="sk-..."
    )
    
    if api_key_input:
        st.session_state['api_key'] = api_key_input
        st.success("✅ AI 智慧建議已啟用！")
    else:
        if 'api_key' in st.session_state:
            del st.session_state['api_key']
        st.info("💡 未設定 API Key，將使用預設建議")

# 獲取建議的函數
def get_suggestion(emotion_category):
    """根據表情類別隨機返回一個可愛的建議"""
    suggestions = emotion_suggestions.get(emotion_category, ["繼續關心她，你會做得很好的！💕"])
    return random.choice(suggestions)

# 使用 LLM 生成個性化建議
def get_llm_suggestion(emotion_category, emotion_label, confidence):
    """使用 LLM 生成個性化的建議"""
    try:
        # 檢查是否設定了 API Key
        api_key = st.session_state.get('api_key', None)
        
        if not api_key:
            # 如果沒有 API Key，使用預設建議
            return get_suggestion(emotion_category)
        
        # 使用 OpenAI API
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # 建立提示詞
        emotion_context = {
            "happy": "她看起來很開心，心情很好",
            "angry": "她看起來有些生氣或不高興",
            "sad": "她看起來有點難過或低落",
            "surprised": "她看起來很驚訝",
            "tired": "她看起來很疲倦，需要休息",
            "hungry": "她看起來餓了，想吃東西",
            "confused": "她看起來有點困惑，不太明白某些事情",
            "love": "她的眼神充滿愛意和溫柔"
        }
        
        prompt = f"""你是一個貼心、可愛、幽默的戀愛顧問助手。

女朋友現在的表情是：{emotion_label}
辨識信心度：{confidence:.1f}%
情境說明：{emotion_context.get(emotion_category, '')}

請給出一個：
1. 非常可愛且貼心的建議（要有emoji）
2. 語氣要像是在跟好朋友聊天一樣輕鬆
3. 建議要實用且容易執行
4. 大約50-80字
5. 要幽默但不要太誇張
6. 加入一些具體的行動建議

範例風格：
- 「她看起來餓了！我馬上去買好吃的給她！你想吃什麼？🍕」
- 「寶貝累了～讓她好好休息，你來做家事吧！💪」

現在請給出你的建議："""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個專業、貼心且幽默的戀愛顧問，擅長給出實用且溫暖的建議。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.9  # 增加隨機性，讓每次回應都不一樣
        )
        
        suggestion = response.choices[0].message.content.strip()
        return suggestion
        
    except Exception as e:
        # 如果 API 調用失敗，使用預設建議
        st.warning(f"⚠️ LLM 生成失敗，使用預設建議（原因：{str(e)[:50]}...）")
        return get_suggestion(emotion_category)

# 主要區域
tab1, tab2, tab3 = st.tabs(["🎯 辨識表情", "🎓 訓練模型", "ℹ️ 關於"])

with tab1:
    st.header("上傳照片進行辨識")
    
    # 檢查是否有訓練好的模型
    model_path = "emotion_model.h5"
    
    if os.path.exists(model_path):
        # 載入模型
        model = tf.keras.models.load_model(model_path)
        st.success("✅ 模型已載入！")
        
        # 上傳圖片
        uploaded_file = st.file_uploader(
            "選擇一張照片...",
            type=["jpg", "jpeg", "png"],
            help="請上傳 JPG、JPEG 或 PNG 格式的照片"
        )
        
        if uploaded_file is not None:
            # 顯示上傳的圖片
            image = Image.open(uploaded_file)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="上傳的照片", use_column_width=True)
            
            with col2:
                # 進行預測
                with st.spinner("正在分析表情..."):
                    predictions = predict_emotion(image, model)
                
                # 顯示結果
                st.subheader("分析結果")
                
                # 找出最高機率的表情
                max_idx = np.argmax(predictions)
                confidence = predictions[max_idx] * 100
                
                # 用大字體顯示主要結果
                st.markdown(f"### 她現在的心情是：**{labels[max_idx]}**")
                st.markdown(f"**信心度：{confidence:.1f}%**")
                
                # 顯示所有預測機率
                st.subheader("詳細分析")
                for i, (label, prob) in enumerate(zip(labels, predictions)):
                    percentage = prob * 100
                    st.progress(prob)
                    st.text(f"{label}: {percentage:.1f}%")
                
                # 根據結果給可愛的建議
                st.subheader("💝 貼心小建議")
                
                # 獲取對應的表情類別
                emotion_category = categories[max_idx]
                suggestion = get_llm_suggestion(emotion_category, labels[max_idx], confidence)
                
                # 根據不同表情使用不同的顯示風格
                if emotion_category == "happy":
                    st.success(f"✨ {suggestion}")
                elif emotion_category == "angry":
                    st.error(f"🚨 {suggestion}")
                elif emotion_category == "sad":
                    st.warning(f"💙 {suggestion}")
                elif emotion_category == "surprised":
                    st.info(f"😲 {suggestion}")
                elif emotion_category == "tired":
                    st.info(f"😴 {suggestion}")
                elif emotion_category == "hungry":
                    st.success(f"🍽️ {suggestion}")
                elif emotion_category == "confused":
                    st.info(f"🤔 {suggestion}")
                elif emotion_category == "love":
                    st.success(f"💖 {suggestion}")
                else:
                    st.info(f"💕 {suggestion}")
                
                # 額外的互動提示
                with st.expander("💡 更多建議"):
                    st.markdown(f"""
                    **基於她現在的心情({labels[max_idx]})，你可以：**
                    
                    """)
                    
                    # 根據不同表情給予額外建議
                    if emotion_category == "happy":
                        st.markdown("""
                        - 📸 拍張美美的照片留念
                        - 🎵 一起聽她喜歡的音樂
                        - 🌟 計劃一個驚喜約會
                        - 💌 寫張小卡片表達愛意
                        """)
                    elif emotion_category == "angry":
                        st.markdown("""
                        - 🙏 真誠地道歉
                        - 👂 耐心聽她說話
                        - 🎁 準備一個小禮物
                        - 💐 送她最愛的花
                        """)
                    elif emotion_category == "sad":
                        st.markdown("""
                        - 🫂 給她一個溫暖的擁抱
                        - 🎬 看一部療癒的電影
                        - 🍵 泡杯熱茶陪她聊天
                        - 📝 寫下你對她的愛
                        """)
                    elif emotion_category == "surprised":
                        st.markdown("""
                        - 🎉 確認是好消息還是壞消息
                        - 💬 關心她發生什麼事
                        - 🎁 如果是驚喜要假裝不知道
                        - 📱 隨時準備慶祝或安慰
                        """)
                    elif emotion_category == "tired":
                        st.markdown("""
                        - 💆 幫她按摩放鬆
                        - 🛁 準備舒服的泡澡環境
                        - 🧘 陪她做簡單的伸展
                        - 📺 一起看輕鬆的節目
                        """)
                    elif emotion_category == "hungry":
                        st.markdown("""
                        - 🍜 煮她最愛的料理
                        - 🍕 叫她最喜歡的外送
                        - 🍰 準備小點心和飲料
                        - 🍽️ 帶她去喜歡的餐廳
                        """)
                    elif emotion_category == "confused":
                        st.markdown("""
                        - 🗣️ 耐心解釋清楚
                        - 📊 用圖表或例子說明
                        - 🤝 一起找出解決方案
                        - 💡 給她時間慢慢理解
                        """)
                    elif emotion_category == "love":
                        st.markdown("""
                        - 💋 回應她的愛意
                        - 💑 來個浪漫的約會
                        - 🌹 說些甜蜜的情話
                        - 💖 好好珍惜這份愛
                        """)
                
                # 信心度提示
                if confidence < 60:
                    st.warning("⚠️ 信心度較低，建議多觀察她的其他表情或行為喔！")
    else:
        st.warning("⚠️ 尚未訓練模型，請先到「訓練模型」標籤訓練模型。")
        st.info("💡 如果您已經有訓練好的模型，請將 `emotion_model.h5` 放在專案目錄中。")

with tab2:
    st.header("訓練表情辨識模型")
    
    st.markdown("""
    ### 📝 訓練步驟
    
    1. **準備訓練資料**：
       - 在專案目錄建立八個資料夾：`happy`、`angry`、`sad`、`surprised`、`tired`、`hungry`、`confused`、`love`
       - 在每個資料夾中放入對應表情的照片（建議每類 15-20 張）
    
    2. **開始訓練**：
       - 點擊下方按鈕開始訓練
       - 訓練完成後模型會自動儲存為 `emotion_model.h5`
    
    3. **使用提示**：
       - 照片建議是正面清晰的臉部照片
       - 表情越明顯，辨識效果越好
       - 建議每個類別的照片數量要平衡
       - 現在支援 8 種表情，訓練時間可能會稍長一些
    """)
    
    # 檢查資料夾是否存在
    folders_exist = all(os.path.exists(cat) for cat in categories)
    
    if folders_exist:
        st.success("✅ 已找到所有訓練資料夾")
        
        # 顯示每個資料夾的圖片數量
        st.subheader("📊 資料集概況")
        
        total_images = 0
        dataset_info = []
        
        for cat, label in zip(categories, labels):
            if os.path.exists(cat):
                num_images = len([f for f in os.listdir(cat) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                total_images += num_images
                dataset_info.append({
                    '表情': label,
                    '資料夾': cat,
                    '照片數': num_images
                })
        
        df = pd.DataFrame(dataset_info)
        st.dataframe(df, use_container_width=True)
        
        st.info(f"📸 總計：{total_images} 張照片")
        
        # 資料集品質檢查
        if total_images < 20:
            st.error("⚠️ 訓練資料太少！建議至少準備 40 張照片（每類 10 張）以獲得較好的效果。")
        elif total_images < 40:
            st.warning("⚠️ 訓練資料偏少。建議每類準備 15-20 張照片以提升準確度。")
        else:
            st.success("✅ 訓練資料充足！")
        
        # 檢查資料平衡度
        counts = [item['照片數'] for item in dataset_info]
        if max(counts) > min(counts) * 2 and min(counts) > 0:
            st.warning("⚠️ 資料不平衡！某些類別的照片數量差異較大，可能影響訓練效果。")
        
        # 顯示樣本圖片（可選）
        with st.expander("🖼️ 預覽訓練資料"):
            cols = st.columns(4)
            for idx, (cat, label) in enumerate(zip(categories, labels)):
                if os.path.exists(cat):
                    files = [f for f in os.listdir(cat) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                    if files:
                        sample_img_path = os.path.join(cat, files[0])
                        try:
                            img = Image.open(sample_img_path)
                            with cols[idx]:
                                st.image(img, caption=label, use_column_width=True)
                        except:
                            pass
        
        st.markdown("---")
        
        # 訓練按鈕
        if total_images >= 12:  # 至少每類3張
            if st.button("🚀 開始訓練模型", type="primary", use_container_width=True):
                train_model()
        else:
            st.error("❌ 訓練資料不足！請至少在每個資料夾中放入 3 張照片。")
    else:
        st.warning("⚠️ 請先建立訓練資料夾並放入照片")
        st.code("""
建立資料夾結構：
project/
├── happy/          (放入開心的照片)
├── angry/          (放入生氣的照片)
├── sad/            (放入難過的照片)
├── surprised/      (放入驚訝的照片)
├── tired/          (放入累了的照片)
├── hungry/         (放入餓了的照片)
├── confused/       (放入困惑的照片)
└── love/           (放入愛你的照片)
        """)
        
        # 提供建立資料夾按鈕
        if st.button("📁 自動建立資料夾", type="secondary"):
            try:
                for cat in categories:
                    os.makedirs(cat, exist_ok=True)
                st.success("✅ 資料夾建立完成！請在各資料夾中放入對應的照片。")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 建立資料夾失敗：{str(e)}")

with tab3:
    st.header("關於這個應用")
    
    st.markdown("""
    ### 🎯 專案簡介
    
    這是一個使用**遷移式學習**（Transfer Learning）技術打造的表情辨識器，
    能夠辨識女朋友照片中的八種表情。
    
    ### 🔬 技術說明
    
    - **基礎模型**：MobileNetV2（在 ImageNet 上預訓練，輕量快速）
    - **框架**：TensorFlow/Keras
    - **介面**：Streamlit
    - **辨識類別**：8 種表情
    - **AI 建議**：OpenAI GPT-3.5（選用）
    
    ### 📊 模型架構
    
    ```
    MobileNetV2 (預訓練，輕量級)
    ↓
    GlobalAveragePooling2D
    ↓
    Dense(128, ReLU)
    ↓
    Dense(8, Softmax)
    ```
    
    ### 💡 使用建議
    
    - 照片建議是正面清晰的臉部照片
    - 表情越明顯，辨識效果越好
    - 訓練資料越多，模型越準確
    
    ### 🚀 部署到 Streamlit Cloud
    
    1. 將專案上傳到 GitHub
    2. 到 [Streamlit Cloud](https://streamlit.io/cloud) 註冊
    3. 連接 GitHub 倉庫並部署
    
    ---
    
    **開發者**：資工在職專班  
    **學號**：5114056002  
    **作業**：HW4 - 遷移式學習
    """)

def train_model():
    """訓練模型的函數 - 完整訓練流程"""
    st.subheader("🎓 訓練進度")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 步驟 1: 載入訓練資料
        status_text.text("步驟 1/6: 載入訓練資料...")
        progress_bar.progress(15)
        
        data = []
        target = []
        
        for i, category in enumerate(categories):
            if not os.path.exists(category):
                st.error(f"❌ 找不到資料夾：{category}")
                return
                
            files = [f for f in os.listdir(category) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if len(files) == 0:
                st.warning(f"⚠️ 資料夾 {category} 中沒有圖片檔案")
                continue
                
            for fname in files:
                try:
                    img_path = os.path.join(category, fname)
                    img = load_img(img_path, target_size=(224, 224))
                    x = img_to_array(img)
                    data.append(x)
                    target.append(i)
                except Exception as e:
                    st.warning(f"無法載入圖片 {fname}: {str(e)}")
                    continue
        
        if len(data) == 0:
            st.error("❌ 沒有找到任何訓練資料！請確認資料夾中有圖片檔案。")
            return
            
        data = np.array(data)
        target = np.array(target)
        
        st.success(f"✅ 成功載入 {len(data)} 張照片")
        
        # 顯示資料集資訊
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("總圖片數", len(data))
        with info_col2:
            st.metric("圖片尺寸", "224x224x3")
        
        # 顯示每個類別的數量
        unique, counts = np.unique(target, return_counts=True)
        data_dist = pd.DataFrame({
            '表情': [labels[i] for i in unique],
            '數量': counts
        })
        st.dataframe(data_dist, use_container_width=True)
        
        # 步驟 2: 資料預處理
        status_text.text("步驟 2/6: 資料預處理...")
        progress_bar.progress(30)
        
        # 使用 ResNet50V2 的預處理函數
        data = preprocess_input(data)
        
        # 將標籤轉換為 one-hot encoding
        target = to_categorical(target, len(categories))
        
        st.success("✅ 資料預處理完成")
        
        # 步驟 3: 建立模型
        status_text.text("步驟 3/6: 建立 MobileNetV2 輕量級模型...")
        progress_bar.progress(45)
        
        # 載入預訓練的 MobileNetV2 模型（輕量快速）
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # 凍結基礎模型的權重
        base_model.trainable = False
        
        # 建立完整模型
        model = Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(128, activation='relu'),
            Dropout(0.3),
            Dense(len(categories), activation='softmax')
        ])
        
        # 編譯模型
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        st.success("✅ 模型建立完成")
        
        # 顯示模型摘要
        with st.expander("📊 查看模型架構"):
            # 獲取模型摘要
            stringlist = []
            model.summary(print_fn=lambda x: stringlist.append(x))
            model_summary = "\n".join(stringlist)
            st.code(model_summary)
        
        # 步驟 4: 訓練模型
        status_text.text("步驟 4/6: 訓練模型（這可能需要幾分鐘）...")
        progress_bar.progress(60)
        
        # 使用 Streamlit 的進度條顯示訓練過程
        epoch_text = st.empty()
        metrics_placeholder = st.empty()
        
        # 訓練參數
        epochs = 15
        batch_size = 8
        
        history = model.fit(
            data, target,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0
        )
        
        progress_bar.progress(80)
        st.success("✅ 模型訓練完成")
        
        # 步驟 5: 顯示訓練結果
        status_text.text("步驟 5/6: 分析訓練結果...")
        
        # 顯示訓練歷史圖表
        st.subheader("📈 訓練過程")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # 準確率圖表
        ax1.plot(history.history['accuracy'], label='訓練準確率', marker='o')
        ax1.plot(history.history['val_accuracy'], label='驗證準確率', marker='s')
        ax1.set_title('模型準確率')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('準確率')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 損失圖表
        ax2.plot(history.history['loss'], label='訓練損失', marker='o')
        ax2.plot(history.history['val_loss'], label='驗證損失', marker='s')
        ax2.set_title('模型損失')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('損失')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 步驟 6: 儲存模型
        status_text.text("步驟 6/6: 儲存模型...")
        progress_bar.progress(95)
        
        model.save("emotion_model.h5")
        
        progress_bar.progress(100)
        status_text.text("✅ 訓練完成！")
        
        st.success("🎉 訓練完成！模型已儲存為 emotion_model.h5")
        
        # 顯示最終結果
        st.subheader("📊 訓練結果")
        
        final_accuracy = history.history['accuracy'][-1] * 100
        final_val_accuracy = history.history['val_accuracy'][-1] * 100
        final_loss = history.history['loss'][-1]
        final_val_loss = history.history['val_loss'][-1]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("訓練準確率", f"{final_accuracy:.1f}%")
        with col2:
            st.metric("驗證準確率", f"{final_val_accuracy:.1f}%")
        with col3:
            st.metric("訓練損失", f"{final_loss:.4f}")
        with col4:
            st.metric("驗證損失", f"{final_val_loss:.4f}")
        
        # 評估模型品質
        st.subheader("🎯 模型評估")
        if final_val_accuracy >= 90:
            st.success("✨ 優秀！模型表現非常好！")
        elif final_val_accuracy >= 80:
            st.info("👍 不錯！模型表現良好！")
        elif final_val_accuracy >= 70:
            st.warning("⚠️ 尚可。建議增加訓練資料或調整參數。")
        else:
            st.error("❌ 表現不佳。建議增加更多訓練資料。")
        
        # 給予建議
        st.subheader("💡 建議")
        
        if final_val_accuracy < final_accuracy - 20:
            st.warning("⚠️ 檢測到過擬合（Overfitting）！訓練準確率遠高於驗證準確率。\n建議：\n- 增加更多訓練資料\n- 使用資料增強（Data Augmentation）\n- 增加 Dropout 比例")
        
        if len(data) < 40:
            st.info("💡 訓練資料較少，建議每個類別準備至少 15-20 張照片以提升模型準確度。")
        
        st.info("💡 現在可以到「辨識表情」標籤測試模型了！")
        
        # 儲存訓練歷史
        history_df = pd.DataFrame(history.history)
        st.download_button(
            label="📥 下載訓練歷史資料",
            data=history_df.to_csv(index=False),
            file_name="training_history.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"❌ 訓練過程發生錯誤：{str(e)}")
        st.exception(e)
        st.info("""
        請確認：
        - 訓練資料夾存在且包含照片（happy, angry, sad, surprised）
        - 照片格式正確（JPG/JPEG/PNG）
        - 每個類別至少有 5 張照片
        - 系統有足夠的記憶體
        """)

# 頁尾
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>"
    "<p>Made with ❤️ using Streamlit | 5114056002_HW4</p>"
    "</div>",
    unsafe_allow_html=True
)
