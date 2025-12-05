# AutoMate Pro – Visual Automation Builder

**AutoMate Pro** is a production-grade, GUI-based workflow builder for Python's `pyautogui` library. It allows users to create, test, and export complex desktop automation scripts **without writing a single line of code manually**.

---

## 🧐 What Is It?

AutoMate Pro is a **no-code interface** for desktop automation.

Normally, using `pyautogui` requires you to manually write scripts, guess X/Y coordinates, and run the script blindly.  
AutoMate Pro solves this by providing:

1. **A Visual Stack:** Actions like Move, Click, Type appear as draggable blocks.  
2. **Integrated Tools:** Built-in coordinate pickers and image finders.  
3. **Compilability:** Generates clean `.py` scripts that work on any machine with Python.

---

## 🚀 Why Use It?

- **Speed:** Prototype macros and automation flows in minutes.  
- **Accuracy:** No need to measure pixels; the coordinate picker does it automatically.  
- **Maintainability:** Save workflows as `.json` and edit anytime.  
- **Logic Support:** Includes **loops** and **image recognition** using OpenCV.  

---

## 🛠 Installation & Prerequisites

You have two ways to run AutoMate Pro:

---

### **Option 1: Standalone Executable (No Python Required)**

1. Go to the **Releases** section of this repository  
2. Download **AutoMatePro.exe**  
3. Run it — no setup required  

---

### **Option 2: Run from Source (For Developers)**

You need **Python 3.8+** installed.

#### 1. Install Dependencies

```bash
pip install customtkinter pyautogui pillow opencv-python
```

#### 2. Run the Application

```bash
python AutomatorPro.py
```

---

## 📖 How to Use

### **1. The Interface**

- **Toolbox (Left):** Add new actions  
- **Workflow Sequence (Right):** Displays steps in execution order  
- **Console (Bottom):** Shows logs, errors, and status updates  

---

### **2. Building a Workflow**

1. Click an action (Move To, Click, Write Text, etc.) to add it  
2. Reorder using the ▲ / ▼ buttons  
3. Delete a step using the ✕ icon  

---

### **3. Using the Coordinate Picker (⌖)**

Instead of guessing coordinates:

1. Add a Move To or Click action  
2. Click the orange **Target Icon (⌖)**  
3. The app will **minimize automatically**  
4. Move your mouse to the target position (3-second window)  
5. AutoMate Pro restores and fills the X/Y values  

---

### **4. Logic & Loops**

To repeat steps (example: clicking a button 10 times):

1. Add **Loop Start** → set *iterations = 10*  
2. Add automation blocks inside  
3. Add **Loop End**  
4. Exported code automatically indents everything inside the loop  

---

### **5. Computer Vision (Find Image)**

Use this for moving buttons or dynamic UIs:

1. Screenshot the UI element and save as `.png`  
2. Add **Find & Click Image** block  
3. Select your image  
4. Adjust confidence level (0.9 = strict, 0.7 = loose)  

---

### **6. Saving & Exporting**

- **Save Project (.json):** Save and reopen workflows  
- **Generate Python (.py):** Export clean, standalone scripts  
- **Run Now:** Execute your workflow immediately  

---

## ⚠️ Safety Features

**PyAutoGUI Fail-Safe:**  
If your automation misbehaves:

➡️ Move your mouse to **any corner** of the screen  
➡️ Script stops instantly via `FailSafeException`

---

## 📝 Example Workflow

Automating a login process:

1. **Comment:** “Start Login Process”  
2. **Move To:** Username field  
3. **Click**  
4. **Write Text:** `"my_username"`  
5. **Press Key:** `"tab"`  
6. **Write Text:** `"my_password"`  
7. **Press Key:** `"enter"`  
8. **Wait:** `2.0` seconds  
9. **Screenshot:** `"login_success.png"`  

---

## 🤝 Troubleshooting

### **❓ Find Image → “Image not found”**
- Ensure the screenshot matches exactly  
- Lower confidence (0.8 or 0.7)  
- Confirm OpenCV is installed  

### **❓ GUI too small or too large**
- CustomTkinter respects system scaling  
- Check your OS display scaling settings  

---

