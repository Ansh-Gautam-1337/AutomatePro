AutoMate Pro - Visual Automation Builder
========================================

**AutoMate Pro** is a production-grade, GUI-based workflow builder for Python's pyautogui library. It allows users to create, test, and export complex desktop automation scripts without writing a single line of code manually.

🧐 What is it?
--------------

AutoMate Pro is a "No-Code" interface for desktop automation.

Normally, using pyautogui requires you to write Python scripts, guess X/Y coordinates, and run the script blindly to see if it works. AutoMate Pro solves this by providing:

1.  **A Visual Stack:** specific actions (Move, Click, Type) are represented as blocks you can drag and drop.
    
2.  **Integrated Tools:** Built-in coordinate pickers and image finders.
    
3.  **Compilability:** It generates clean, standalone Python .py files that can run on any machine with Python installed.
    

🚀 Why use it?
--------------

*   **Speed:** Quickly prototype macros for data entry, gaming, or repetitive form filling.
    
*   **Accuracy:** The "Coordinate Picker" tool eliminates the need to take screenshots and measure pixels manually.
    
*   **Maintainability:** Save your workflows as JSON projects (.json) so you can edit them later.
    
*   **Logic:** Unlike simple macro recorders, this tool supports **Loops** and **Image Recognition** logic.
    

🛠 Installation & Prerequisites
-------------------------------

You have two options to run AutoMate Pro: using the standalone executable (easiest) or running from the source code.

### Option 1: Standalone Executable (No Python Required)

If you don't want to install Python or dependencies, you can use the pre-compiled .exe file.

1.  Navigate to the **Releases** section of this GitHub repository.
    
2.  Download the latest AutoMatePro.exe.
    
3.  Double-click the file to launch the application immediately.
    

### Option 2: Run from Source (For Developers)

You need **Python 3.8+** installed on your system.

#### 1\. Install Dependencies

Open your terminal or command prompt and install the required libraries.

*   customtkinter: For the modern GUI.
    
*   pyautogui: For controlling the mouse and keyboard.
    
*   pillow: For image handling.
    
*   opencv-python: **Crucial** for the "Find Image" feature (allows confidence matching).
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install customtkinter pyautogui pillow opencv-python   `

#### 2\. Running the Application

Simply run the main script:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python automator_pro.py   `

📖 How to Use
-------------

### 1\. The Interface

*   **Toolbox (Left):** Click buttons here to add actions to your workflow.
    
*   **Workflow Sequence (Right):** This is your stack of actions. They execute from top to bottom.
    
*   **Console (Bottom):** Displays logs, errors, and status updates.
    

### 2\. Building a Workflow

1.  **Add Actions:** Click items like Move To, Click, or Write Text in the toolbox.
    
2.  **Reorder:** Use the ▲ and ▼ buttons on any block to change its execution order.
    
3.  **Delete:** Click the ✕ button to remove a step.
    

### 3\. Using the Coordinate Picker (Target Icon ⌖)

Instead of guessing where to click:

1.  Add a Move To or Click block.
    
2.  Click the orange **Target Icon (⌖)** next to the X/Y fields.
    
3.  **The app will minimize automatically.**
    
4.  You have **3 seconds** to move your mouse to the desired location on your screen.
    
5.  The app will restore itself and automatically fill in the X and Y coordinates.
    

### 4\. Logic & Loops

To repeat actions (e.g., clicking a button 10 times):

1.  Add a Loop Start block. Set "Iterations" to 10.
    
2.  Add your action blocks (e.g., Click).
    
3.  Add a Loop End block.
    
4.  _Note:_ The exported code will automatically indent everything between Start and End.
    

### 5\. Computer Vision (Find Image)

To click a button that moves around:

1.  Take a small screenshot (crop) of the button you want to click. Save it as a .png.
    
2.  Add a Find & Click Image block in AutoMate Pro.
    
3.  Select your .png file.
    
4.  Set confidence (0.9 is strict, 0.7 is loose).
    

### 6\. Saving & Exporting

*   **Save Project (.json):** Saves your workflow state so you can open and edit it in AutoMate Pro later.
    
*   **Generate .py (.py):** Exports a standalone Python script. You can send this script to a colleague, and they can run it without needing the AutoMate Pro GUI.
    
*   **Run Now:** Executes the workflow immediately for testing.
    

⚠️ Safety Features
------------------

**Fail-Safe:** PyAutoGUI includes a fail-safe mode. If your automation goes rogue (mouse moving wildly):

1.  **Slam your mouse cursor into any of the four corners of the screen.**
    
2.  This will trigger a FailSafeException and immediately stop the script.
    

📝 Example Workflow
-------------------

_An example of automating a login form:_

1.  **Comment:** "Start Login Process"
    
2.  **Move To:** (Coordinate of Username field)
    
3.  **Click:** Left Button
    
4.  **Write Text:** "my\_username"
    
5.  **Press Key:** "tab"
    
6.  **Write Text:** "my\_password"
    
7.  **Press Key:** "enter"
    
8.  **Wait:** 2.0 seconds (for page load)
    
9.  **Screenshot:** "login\_success.png"
    

🤝 Troubleshooting
------------------

**Q: The "Find Image" block says "Image not found".**

*   Ensure the image on screen looks exactly like your screenshot.
    
*   Try lowering the "Confidence" to 0.8 or 0.7.
    
*   Make sure you installed opencv-python.
    

**Q: The GUI is too small/large.**

*   CustomTkinter respects system scaling. Check your OS display settings.
