# AI-GestureType: Webcam-Based Gesture Writing & System Control

AI-GestureType is an AI-powered virtual keyboard and system controller that allows users to type on a screen and control system functions in real-time using hand gestures via a standard webcam—without touching a physical keyboard or mouse.

The project features a **Python backend** powered by OpenCV and CVZone for real-time hand landmark tracking and gesture analysis, communicating via **WebSockets (Flask-SocketIO)** with a modern **React frontend** dashboard containing a dynamic matrix keyboard grid.

---

## 🚀 Features

- **Virtual Matrix Keyboard:** Control an on-screen cursor with your index finger and select letters from a 5x5 grid using a pinch gesture.
- **System Automation (PyAutoGUI):** Triggers real-time operating system keyboard events.
- **Global Gestures:** 
  - `5 Fingers Extended` -> Inserts a `Space`
  - `0 Fingers (Fist)` -> Executes a `Backspace`
  - `Index Finger Tracking + Pinch` -> Selects and types letters (A-Z)
- **Real-Time Synchronous Display:** Low-latency performance showing text output on both the React Notepad dashboard and any active system text editor.

---

## 🛠️ Tech Stack

- **Backend:** Python, OpenCV, CVZone (MediaPipe wrapper), Flask, Flask-SocketIO, PyAutoGUI
- **Frontend:** React.js, Socket.io-client, CSS3

---

## 📦 Installation & Setup

### Prerequisites
Make sure you have **Python 3.x** and **Node.js** installed on your system.

### 1. Backend Setup
Clone the repository and navigate to the project directory:

```bash
cd aidrivenproject1
```

Activate your virtual environment (`.venv`) and install the required dependencies:

```bash
pip install opencv-python cvzone flask flask-socketio flask-cors pyautogui
```

Run the Python backend server:
```bash
python app.py
```

### 2. Frontend Setup
Navigate to the frontend folder, install the packages, and start the development server:

```bash
cd gesture-frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser to view the interactive dashboard.

---

## 🎮 How To Use

1. Ensure both the **Python server** and **React app** are actively running and showing a "System Ready" status.
2. Click inside the **Smart Notepad** text area on the React web page to focus the text cursor.
3. Bring your hand into the webcam window view.
4. **Move Cursor:** Raise your **index finger** and move it around to control the red virtual cursor over the letters.
5. **Type a Letter:** Hover over a specific character box and **pinch your thumb and index finger together** to select it.
6. **Spacebar:** Show all **5 fingers** open to register a space.
7. **Backspace:** Close your hand into a **fist (0 fingers)** to delete the last typed character.

---

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).
