import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import threading
import json
import os
import sys

# --- Configuration & Assets ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Action Schema Definition (The Brain of the Tool)
# Defines what inputs each action requires
ACTION_SCHEMA = {
    # --- Mouse ---
    "Move To": {
        "icon": "↗", "color": "#2980b9",
        "fields": [("x", "int", "0"), ("y", "int", "0"), ("duration", "float", "0.5")]
    },
    "Click": {
        "icon": "🖱️", "color": "#2980b9",
        "fields": [("x", "int", "0"), ("y", "int", "0"), ("clicks", "int", "1"), ("button", "str", "left")]
    },
    "Drag To": {
        "icon": "✊", "color": "#2980b9",
        "fields": [("x", "int", "0"), ("y", "int", "0"), ("duration", "float", "1.0")]
    },
    "Scroll": {
        "icon": "↕", "color": "#2980b9",
        "fields": [("amount", "int", "-500")]
    },
    
    # --- Keyboard ---
    "Write Text": {
        "icon": "✎", "color": "#27ae60",
        "fields": [("text", "str", "Hello World"), ("interval", "float", "0.05")]
    },
    "Press Key": {
        "icon": "⌨️", "color": "#27ae60",
        "fields": [("key", "str", "enter")]
    },
    "Hotkey": {
        "icon": "🎹", "color": "#27ae60",
        "fields": [("keys", "str", "ctrl, c")]
    },

    # --- Logic & loops ---
    "Wait": {
        "icon": "⏳", "color": "#f39c12",
        "fields": [("seconds", "float", "1.0")]
    },
    "Loop Start": {
        "icon": "🔄", "color": "#8e44ad",
        "fields": [("iterations", "int", "5")],
        "indent_change": 1
    },
    "Loop End": {
        "icon": "⏹", "color": "#8e44ad",
        "fields": [],
        "indent_change": -1
    },

    # --- Image Recognition ---
    "Find & Click Image": {
        "icon": "🖼️", "color": "#d35400",
        "fields": [("image_path", "file", ""), ("confidence", "float", "0.9")]
    },
    
    # --- System ---
    "Screenshot": {
        "icon": "📷", "color": "#7f8c8d",
        "fields": [("filename", "str", "snap.png")]
    },
    "Comment": {
        "icon": "#", "color": "#95a5a6",
        "fields": [("note", "str", "Describe step here...")]
    }
}

class ActionBlock(ctk.CTkFrame):
    """
    A unified visual component for any action type defined in ACTION_SCHEMA.
    """
    def __init__(self, master, action_type, parent_app, data=None):
        super().__init__(master, fg_color="#212121", corner_radius=8, border_width=1, border_color="#333")
        self.parent_app = parent_app
        self.action_type = action_type
        self.schema = ACTION_SCHEMA[action_type]
        self.inputs = {}
        
        # Determine visual style
        self.accent_color = self.schema["color"]
        self.indent_level = 0 # Visual only, handled by generator logically

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.header_frame.pack(fill="x", padx=8, pady=(8, 4))

        # Icon & Title
        ctk.CTkLabel(self.header_frame, text=self.schema["icon"], font=("Arial", 16), text_color=self.accent_color).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(self.header_frame, text=action_type, font=("Roboto", 13, "bold"), text_color="#eee").pack(side="left")

        # Controls
        self.btn_del = ctk.CTkButton(self.header_frame, text="✕", width=25, height=25, fg_color="transparent", hover_color="#c0392b", command=self.delete_self)
        self.btn_del.pack(side="right")
        
        self.btn_down = ctk.CTkButton(self.header_frame, text="▼", width=25, height=25, fg_color="transparent", hover_color="#444", command=self.move_down)
        self.btn_down.pack(side="right")
        
        self.btn_up = ctk.CTkButton(self.header_frame, text="▲", width=25, height=25, fg_color="transparent", hover_color="#444", command=self.move_up)
        self.btn_up.pack(side="right")

        # --- Content / Inputs ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.build_inputs(data)

    def build_inputs(self, data):
        """Dynamically builds input fields based on schema."""
        fields = self.schema.get("fields", [])
        
        for field_name, field_type, default_val in fields:
            row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            # Label
            lbl = ctk.CTkLabel(row, text=f"{field_name}:", width=80, anchor="w", text_color="#aaa", font=("Arial", 11))
            lbl.pack(side="left")
            
            # Input Widget
            current_val = data.get(field_name, default_val) if data else default_val

            if field_type == "file":
                entry = ctk.CTkEntry(row, height=25, font=("Arial", 11))
                entry.insert(0, str(current_val))
                entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
                btn = ctk.CTkButton(row, text="...", width=30, height=25, command=lambda e=entry: self.pick_file(e))
                btn.pack(side="right")
                self.inputs[field_name] = entry
                
            else:
                entry = ctk.CTkEntry(row, height=25, font=("Arial", 11))
                entry.insert(0, str(current_val))
                entry.pack(side="left", fill="x", expand=True)
                self.inputs[field_name] = entry

            # Special case: Add coordinate picker for X/Y
            if field_name == "y" and any(f[0] == "x" for f in fields):
                btn_pick = ctk.CTkButton(row, text="⌖", width=30, height=25, fg_color="#e67e22", hover_color="#d35400", 
                                         command=self.pick_coords_logic)
                btn_pick.pack(side="right", padx=(5, 0))

    def pick_coords_logic(self):
        """Minimizes app, waits, gets coords, restores app."""
        self.parent_app.minimize_and_pick(self)

    def update_coords(self, x, y):
        if "x" in self.inputs:
            self.inputs["x"].delete(0, 'end')
            self.inputs["x"].insert(0, str(x))
        if "y" in self.inputs:
            self.inputs["y"].delete(0, 'end')
            self.inputs["y"].insert(0, str(y))

    def pick_file(self, entry_widget):
        filename = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg")])
        if filename:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, filename)

    def get_data(self):
        """Returns a dict of current input values."""
        data = {}
        for name, widget in self.inputs.items():
            data[name] = widget.get()
        return data

    # Actions
    def delete_self(self): self.parent_app.remove_block(self)
    def move_up(self): self.parent_app.move_block(self, -1)
    def move_down(self): self.parent_app.move_block(self, 1)


class AutoMateProApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoMate Pro - Workflow Builder Developed By Ansh Gautam")
        self.geometry("1100x750")
        
        # State
        self.blocks = []
        
        # --- UI Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Toolbar (Top)
        self.toolbar = ctk.CTkFrame(self, height=50, fg_color="#1a1a1a")
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.btn_save = ctk.CTkButton(self.toolbar, text="💾 Save Project", width=100, fg_color="#2c3e50", command=self.save_project)
        self.btn_save.pack(side="left", padx=10, pady=10)
        
        self.btn_load = ctk.CTkButton(self.toolbar, text="📂 Load Project", width=100, fg_color="#2c3e50", command=self.load_project)
        self.btn_load.pack(side="left", padx=5, pady=10)

        self.btn_clear = ctk.CTkButton(self.toolbar, text="🗑 Clear All", width=80, fg_color="#c0392b", command=self.clear_all)
        self.btn_clear.pack(side="left", padx=20, pady=10)

        self.btn_run = ctk.CTkButton(self.toolbar, text="▶ Run Now", width=100, fg_color="#e67e22", hover_color="#d35400", command=self.run_now_thread)
        self.btn_run.pack(side="right", padx=10, pady=10)
        
        self.btn_export = ctk.CTkButton(self.toolbar, text="⚙ Generate .py", width=120, fg_color="#27ae60", hover_color="#2ecc71", command=self.generate_script)
        self.btn_export.pack(side="right", padx=5, pady=10)

        # 2. Sidebar (Toolbox)
        self.sidebar = ctk.CTkScrollableFrame(self, width=220, label_text="Toolbox")
        self.sidebar.grid(row=1, column=0, sticky="ns", padx=5, pady=5)
        
        self.create_toolbox_category("Mouse", ["Move To", "Click", "Drag To", "Scroll"])
        self.create_toolbox_category("Keyboard", ["Write Text", "Press Key", "Hotkey"])
        self.create_toolbox_category("Logic & Flow", ["Wait", "Loop Start", "Loop End"])
        self.create_toolbox_category("Computer Vision", ["Find & Click Image"])
        self.create_toolbox_category("System", ["Screenshot", "Comment"])

        # 3. Main Workspace (Scrollable)
        self.workspace = ctk.CTkScrollableFrame(self, label_text="Workflow Sequence", fg_color="#181818")
        self.workspace.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # 4. Logger Console (Bottom)
        self.console = ctk.CTkTextbox(self, height=120, font=("Consolas", 12), fg_color="#111", text_color="#00ff00")
        self.console.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.log("Welcome to AutoMate Pro. Ready.")

    def create_toolbox_category(self, title, items):
        """Creates a collapsible group in sidebar."""
        lbl = ctk.CTkLabel(self.sidebar, text=title, font=("Arial", 12, "bold"), text_color="#bbb", anchor="w")
        lbl.pack(fill="x", pady=(15, 5))
        for item in items:
            color = ACTION_SCHEMA[item]["color"]
            btn = ctk.CTkButton(self.sidebar, text=f"+ {item}", fg_color="transparent", border_width=1, border_color="#333", 
                                anchor="w", hover_color="#333", text_color="#eee",
                                command=lambda t=item: self.add_block(t))
            btn.pack(fill="x", pady=2)

    def log(self, message):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.console.see("end")

    # --- Block Management ---
    def add_block(self, action_type, data=None):
        block = ActionBlock(self.workspace, action_type, self, data)
        block.pack(fill="x", padx=10, pady=4)
        self.blocks.append(block)
        # Scroll to bottom
        self.workspace._parent_canvas.yview_moveto(1.0)

    def remove_block(self, block):
        block.destroy()
        if block in self.blocks:
            self.blocks.remove(block)

    def move_block(self, block, direction):
        idx = self.blocks.index(block)
        new_idx = idx + direction
        if 0 <= new_idx < len(self.blocks):
            self.blocks[idx], self.blocks[new_idx] = self.blocks[new_idx], self.blocks[idx]
            self.repack_blocks()

    def repack_blocks(self):
        for b in self.blocks:
            b.pack_forget()
        for b in self.blocks:
            b.pack(fill="x", padx=10, pady=4)

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear entire workflow?"):
            for b in self.blocks: b.destroy()
            self.blocks = []

    # --- Pick Coordinate Helper ---
    def minimize_and_pick(self, block_ref):
        self.iconify() # Minimize window
        
        def _thread():
            time.sleep(0.5) # Wait for animation
            # Play a beep or visual logic could go here
            time.sleep(2.5) # Time for user to move mouse
            x, y = pyautogui.position()
            self.deiconify() # Restore
            block_ref.update_coords(x, y)
            
        threading.Thread(target=_thread, daemon=True).start()

    # --- Persistence (JSON) ---
    def get_workflow_data(self):
        workflow = []
        for b in self.blocks:
            workflow.append({
                "type": b.action_type,
                "data": b.get_data()
            })
        return workflow

    def save_project(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path: return
        try:
            with open(path, "w") as f:
                json.dump(self.get_workflow_data(), f, indent=4)
            self.log(f"Project saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_project(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path: return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            
            # Clear current
            for b in self.blocks: b.destroy()
            self.blocks = []
            
            for item in data:
                self.add_block(item["type"], item["data"])
            self.log("Project loaded.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- Compilation Logic ---
    def compile_to_python(self):
        """Converts UI blocks to a Python string."""
        lines = [
            "import pyautogui",
            "import time",
            "import os",
            "",
            "pyautogui.FAILSAFE = True",
            "",
            "def run_automation():",
            "    print('--- Starting Automation ---')"
        ]
        
        indent = 1
        
        for b in self.blocks:
            d = b.get_data()
            atype = b.action_type
            prefix = "    " * indent
            
            try:
                if atype == "Move To":
                    lines.append(f"{prefix}pyautogui.moveTo({d['x']}, {d['y']}, duration={d['duration']})")
                elif atype == "Click":
                    lines.append(f"{prefix}pyautogui.click(x={d['x']}, y={d['y']}, clicks={d['clicks']}, button='{d['button']}')")
                elif atype == "Drag To":
                    lines.append(f"{prefix}pyautogui.dragTo({d['x']}, {d['y']}, duration={d['duration']}, button='left')")
                elif atype == "Scroll":
                    lines.append(f"{prefix}pyautogui.scroll({d['amount']})")
                
                elif atype == "Write Text":
                    lines.append(f"{prefix}pyautogui.write('{d['text']}', interval={d['interval']})")
                elif atype == "Press Key":
                    lines.append(f"{prefix}pyautogui.press('{d['key']}')")
                elif atype == "Hotkey":
                    # Convert "ctrl, c" to 'ctrl', 'c'
                    keys = [k.strip() for k in d['keys'].split(',')]
                    formatted_keys = ", ".join([f"'{k}'" for k in keys])
                    lines.append(f"{prefix}pyautogui.hotkey({formatted_keys})")
                
                elif atype == "Wait":
                    lines.append(f"{prefix}time.sleep({d['seconds']})")
                
                elif atype == "Loop Start":
                    lines.append(f"{prefix}for _ in range({d['iterations']}):")
                    indent += 1
                    lines.append(f"{prefix}    print('Loop iteration...')")
                
                elif atype == "Loop End":
                    indent = max(1, indent - 1)
                    lines.append(f"{prefix}# End Loop")

                elif atype == "Find & Click Image":
                    img = d['image_path']
                    # Escape backslashes for windows paths
                    img = img.replace("\\", "\\\\")
                    conf = d['confidence']
                    lines.append(f"{prefix}loc = pyautogui.locateCenterOnScreen('{img}', confidence={conf})")
                    lines.append(f"{prefix}if loc:")
                    lines.append(f"{prefix}    pyautogui.click(loc)")
                    lines.append(f"{prefix}else:")
                    lines.append(f"{prefix}    print('Image not found: {os.path.basename(img)}')")

                elif atype == "Screenshot":
                    lines.append(f"{prefix}pyautogui.screenshot('{d['filename']}')")

                elif atype == "Comment":
                    lines.append(f"{prefix}# {d['note']}")
                    
            except Exception as e:
                lines.append(f"{prefix}print('Error generating step: {e}')")

        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    # Give user time to switch windows")
        lines.append("    time.sleep(2)")
        lines.append("    run_automation()")
        
        return "\n".join(lines)

    def generate_script(self):
        code = self.compile_to_python()
        path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python", "*.py")])
        if path:
            with open(path, "w") as f:
                f.write(code)
            self.log(f"Script generated: {path}")

    def run_now_thread(self):
        if not self.blocks: return
        self.log("Prepare for execution... (3s delay)")
        threading.Thread(target=self._run_logic, daemon=True).start()

    def _run_logic(self):
        """Executes the generated code dynamically."""
        code = self.compile_to_python()
        
        # We need to strip the '__main__' check to run it inside exec() contextually usually, 
        # but since we generated a function run_automation, we can just call that.
        
        try:
            # Setup environment
            global_env = {}
            time.sleep(3) # Initial safety delay
            exec(code, global_env) # Load definitions
            
            # Find the function and run it
            if 'run_automation' in global_env:
                global_env['run_automation']()
                self.console.after(0, lambda: self.log("Execution Complete."))
            else:
                self.console.after(0, lambda: self.log("Error: Could not find main function."))
                
        except pyautogui.FailSafeException:
            self.console.after(0, lambda: self.log("❌ FAILSAFE TRIGGERED (Mouse Corner)"))
        except Exception as e:
            self.console.after(0, lambda: self.log(f"❌ Execution Error: {e}"))

if __name__ == "__main__":
    # Check dependencies
    try:
        import pyautogui
        import cv2 # Check for opencv (needed for confidence in locateOnScreen)
    except ImportError:
        print("Missing dependencies. Please run: pip install pyautogui opencv-python pillow customtkinter")
    
    app = AutoMateProApp()
    app.mainloop()