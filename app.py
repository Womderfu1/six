"""
智能情绪倾听师——基于情感计算的AI心理支持系统
使用 OpenCV Haar Cascade 进行人脸检测
"""

import cv2
import numpy as np
import gradio as gr
import os

# ============================================
# 第一部分：初始化人脸检测器
# ============================================

# 使用 OpenCV 自带的人脸检测器
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

print("✅ OpenCV 人脸检测器初始化成功")

# ============================================
# 第二部分：人脸检测和关键点绘制
# ============================================

def detect_faces_opencv(frame):
    """
    使用 OpenCV 检测人脸
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    results = []
    for (x, y, w, h) in faces:
        # 生成模拟的关键点（围绕人脸框）
        landmarks = []
        for i in range(10):
            lx = x + int(w * (i + 1) / 11)
            ly = y + int(h * (i + 1) / 11)
            landmarks.append((lx, ly))
        for i in range(10):
            lx = x + int(w * (i + 1) / 11)
            ly = y + int(h * (10 - i) / 11)
            landmarks.append((lx, ly))

        results.append({
            'bbox': (x, y, x + w, y + h),
            'landmarks': landmarks
        })

    return results

def draw_face(frame, face_data):
    """
    在图像上绘制人脸框和关键点
    """
    x1, y1, x2, y2 = face_data['bbox']

    # 绘制人脸边界框（绿色）
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 绘制关键点
    landmarks = face_data['landmarks']
    for (x, y) in landmarks:
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

    return frame

# ============================================
# 第三部分：情绪识别（简化版）
# ============================================

def analyze_emotion(frame, face_bbox):
    """
    简化版情绪识别
    """
    return "neutral", 0.5

# ============================================
# 第四部分：共情回应
# ============================================

EMOJI_MAP = {
    'happy': '😊', 'sad': '😢', 'angry': '😠',
    'fear': '😨', 'disgust': '🤢', 'surprise': '😮',
    'neutral': '😐'
}

EMOTION_RESPONSE_MAP = {
    'happy': "😊 很高兴看到你这么开心！能和我分享一下让你快乐的事吗？",
    'sad': "😔 我能感受到你有些低落。如果你愿意，可以和我聊聊，我会一直在这里倾听。",
    'angry': "😠 我注意到你似乎有些烦躁。有时候说出来会让心情好一些，愿意试试吗？",
    'fear': "😨 你看起来有些不安。别担心，这里是安全的，我们可以一起面对。",
    'disgust': "🤢 我感觉到你有些不适。是什么让你有这样的感觉呢？",
    'surprise': "😮 哇，你看起来有些惊讶！发生了什么有趣的事情吗？",
    'neutral': "😐 你好，今天感觉怎么样？我随时愿意倾听你的故事。"
}

def generate_empathic_response(emotion, user_text=""):
    """
    生成共情回应
    """
    emoji = EMOJI_MAP.get(emotion, '😐')
    base_response = EMOTION_RESPONSE_MAP.get(emotion, "你好，我在这里倾听。")

    if user_text:
        return f"{emoji} 感谢你的分享。{base_response}"
    return base_response

# ============================================
# 第五部分：主程序界面
# ============================================

def process_frame(frame, state):
    """
    处理视频帧
    """
    if frame is None:
        return frame, state

    display_frame = frame.copy()
    faces = detect_faces_opencv(frame)

    current_emotion = state.get('emotion', 'neutral')

    for face_data in faces:
        display_frame = draw_face(display_frame, face_data)
        emotion, _ = analyze_emotion(frame, face_data['bbox'])
        if emotion:
            current_emotion = emotion
            x1, y1, _, _ = face_data['bbox']
            emoji = EMOJI_MAP.get(emotion, '😐')
            cv2.putText(display_frame, f"{emoji} {emotion}", (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    state['emotion'] = current_emotion

    # 在画面顶部显示当前情绪状态
    emoji = EMOJI_MAP.get(current_emotion, '😐')
    cv2.putText(display_frame, f"当前情绪: {emoji} {current_emotion}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    return display_frame, state

def on_send_message(message, state, chat_history_state):
    """
    处理用户发送的消息
    """
    if not message or not message.strip():
        return "", chat_history_state

    current_emotion = state.get('emotion', 'neutral')
    response = generate_empathic_response(current_emotion, message)
    chat_history_state.append((message, response))
    return "", chat_history_state

def start_listening(state, chat_history_state):
    """
    开始倾听
    """
    emotion = state.get('emotion', 'neutral')
    response = generate_empathic_response(emotion, "")
    chat_history_state.append(("🎧 系统", response))
    return chat_history_state, chat_history_state

def clear_chat(chat_history_state):
    """
    清空对话
    """
    chat_history_state.clear()
    return chat_history_state, chat_history_state

def update_emotion_display(state):
    """
    更新情绪显示
    """
    emotion = state.get('emotion', 'neutral')
    emoji = EMOJI_MAP.get(emotion, '😐')
    return f"{emoji} {emotion.upper()}"

def create_interface():
    """
    创建 Gradio 界面
    """
    with gr.Blocks(title="智能情绪倾听师") as demo:
        gr.Markdown("""
        # 🧠 智能情绪倾听师
        ### 基于情感计算的AI心理支持系统
        
        > 💡 **隐私保护**：所有面部数据处理均在本地完成，不上传任何数据。
        > 📷 **使用说明**：允许摄像头访问后，系统会自动检测您的面部。
        > 💬 **开始对话**：在右侧输入框中输入您的感受。
        """)

        state = gr.State({'emotion': 'neutral'})
        chat_state = gr.State([])

        with gr.Row():
            with gr.Column(scale=1):
                # 修复：使用 "webcam" 作为输入
                video_input = gr.Image(
                    label="📷 视频预览",
                    type="numpy",
                    height=350,
                    sources=["webcam"]
                )
                video_output = gr.Image(
                    label="🔍 情绪分析结果",
                    type="numpy",
                    height=350
                )
                emotion_display = gr.Textbox(
                    label="📊 当前情绪状态",
                    value="😐 NEUTRAL",
                    interactive=False
                )

            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="💬 对话记录",
                    height=420
                )
                msg_input = gr.Textbox(
                    label="✍️ 输入你的感受",
                    placeholder="输入你想说的话，然后按回车或点击发送...",
                    lines=2
                )
                with gr.Row():
                    send_btn = gr.Button("💬 发送", variant="primary")
                    listen_btn = gr.Button("🎧 开始倾听", variant="secondary")
                    clear_btn = gr.Button("🗑️ 清空记录", variant="stop")

        # 事件绑定
        video_input.stream(
            fn=process_frame,
            inputs=[video_input, state],
            outputs=[video_output, state],
            stream_every=0.1
        )

        state.change(
            fn=update_emotion_display,
            inputs=[state],
            outputs=[emotion_display]
        )

        send_btn.click(
            fn=on_send_message,
            inputs=[msg_input, state, chat_state],
            outputs=[msg_input, chat_state]
        ).then(
            fn=lambda s: s,
            inputs=[chat_state],
            outputs=[chatbot]
        )

        msg_input.submit(
            fn=on_send_message,
            inputs=[msg_input, state, chat_state],
            outputs=[msg_input, chat_state]
        ).then(
            fn=lambda s: s,
            inputs=[chat_state],
            outputs=[chatbot]
        )

        listen_btn.click(
            fn=start_listening,
            inputs=[state, chat_state],
            outputs=[chat_state, chatbot]
        )

        clear_btn.click(
            fn=clear_chat,
            inputs=[chat_state],
            outputs=[chat_state, chatbot]
        )

    return demo

# ============================================
# 第六部分：启动程序
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 智能情绪倾听师 v1.0")
    print("=" * 60)
    print("🚀 正在启动应用...")
    print("📱 访问地址: http://127.0.0.1:7860")
    print("=" * 60)

    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )