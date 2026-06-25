# 🧠 智能情绪倾听师（Intelligent Emotional Listener）

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Gradio-3.50%2B-orange.svg" alt="Gradio">
  <img src="https://img.shields.io/badge/OpenCV-4.5%2B-green.svg" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  基于情感计算的 AI 心理支持系统 —— 实时人脸检测 + 共情回应，零数据上传，隐私安全。
</p>

---

## 📖 项目简介

**智能情绪倾听师** 是一个基于情感计算的 AI 心理支持系统，通过摄像头实时检测用户面部情绪，并生成温暖、共情的文字回应。

### 🎯 核心功能

| 功能 | 说明 |
|------|------|
| 👤 **实时人脸检测** | 使用 OpenCV Haar Cascade 检测人脸并标注关键点 |
| 😊 **情绪识别** | 识别 7 种基础情绪（快乐、悲伤、愤怒、恐惧、厌恶、惊讶、中性） |
| 💬 **共情回应** | 根据情绪状态生成个性化共情对话 |
| 🔒 **隐私保护** | 所有数据本地处理，不上传任何面部信息 |

### 🛠️ 技术栈

- **人脸检测**：OpenCV Haar Cascade
- **界面框架**：Gradio
- **数值计算**：NumPy
- **大语言模型**：DashScope / 通义千问（可选）
- **部署平台**：魔搭社区创空间

---

## 🚀 快速开始

### 本地运行

#### 1. 克隆仓库omderfu

```bash
git clone https://github.com/Womderfu1/intelligent-emotional-listener.git
cd intelligent-emotional-listener
