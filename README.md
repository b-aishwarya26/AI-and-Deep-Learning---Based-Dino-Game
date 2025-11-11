# 🦖 Deep Learning and AI-Based Hand Gesture Dino Game

This project demonstrates an **AI-powered Dino Game** that is controlled through **real-time hand gestures** using **Deep Learning, MediaPipe, and OpenCV**.  
Instead of using a keyboard or mouse, players can interact with the game by simply moving their hands in front of a webcam — enabling a **touchless and immersive gaming experience**.

---

## 🚀 Features
- 🎮 Real-time hand gesture control using webcam.
- 🧠 Deep Learning-based hand landmark detection with **MediaPipe**.
- 👋 Recognizes gestures like open palm and closed fist.
- 🕹️ Controls Dino movement (jump/run) via hand signals.
- ⚡ Built using **Python, OpenCV, and Pygame**.
- 💡 Demonstrates the integration of **AI + Computer Vision + Game Development**.

---

## 🧠 System Overview
1. **Input Module** – Captures real-time video feed from webcam.  
2. **Gesture Detection** – Detects and tracks 21 hand landmarks using **MediaPipe Hands**.  
3. **Gesture Recognition** – Identifies open/closed hand using landmark coordinates.  
4. **Game Control** – Maps gestures to game actions in the **Pygame Dino Game**.  
5. **Output** – Displays both camera feed and game window for live interaction.

---

## 🧰 Technologies Used
| Category | Tools / Libraries |
|-----------|------------------|
| Language | Python |
| Computer Vision | OpenCV |
| Deep Learning | MediaPipe (pre-trained CNN) |
| Game Development | Pygame |
| IDE | Visual Studio Code / PyCharm |
| Hardware | Webcam |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/AI-Hand-Gesture-Dino-Game.git
cd AI-Hand-Gesture-Dino-Game

🧩 How It Works

The MediaPipe Hand module detects 21 hand landmarks using a pre-trained CNN model.

Based on the position of these landmarks, OpenCV processes the frame to identify gestures.

The detected gesture is mapped to an in-game action:

✊ Closed Fist → Jump

🖐️ Open Palm → Idle/Run

Pygame updates the Dino’s state in real time according to the gesture input.

📊 Results

Real-time gesture tracking achieved with minimal latency.

Smooth gameplay with 25–30 FPS on standard webcam.

Demonstrated effective integration of AI and HCI for interactive control.

⚠️ Limitations

Accuracy depends on lighting and camera quality.

Limited gesture vocabulary (open palm, closed fist).

May not perform well with background clutter or partial hand visibility.

🔮 Future Enhancements

Add more gestures (slide, duck, attack).

Integrate with custom-trained CNN models for higher accuracy.

Extend to Augmented Reality (AR) or VR interfaces.

Include dual-hand or multiplayer gesture support.

👩‍💻 Author

B. Aishwarya
AI/ML Enthusiast | Deep Learning Developer
📧 [aishwaryabhandari26@gmail.com]
🌐 [[LinkedIn or GitHub link here](https://www.linkedin.com/in/b-aishwarya-919396264/)]
