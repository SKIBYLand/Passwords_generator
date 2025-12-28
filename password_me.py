#!/usr/bin/env python3
import os, sys, json, pathlib, webbrowser, tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import keyring
except ImportError:
    keyring = None
    print("Info: 'keyring' not available — using file/in-memory storage")

class ToolTip:
    """Simple tooltip for widgets."""
    def __init__(self, widget, text, delay=400):
        self.widget, self.text, self.delay = widget, text, delay
        self._after_id = self.tipwindow = None
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)
        widget.bind("<ButtonPress>", self.hide)
    
    def schedule(self, event=None):
        self.unschedule()
        self._after_id = self.widget.after(self.delay, self.show)
    
    def unschedule(self):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
    
    def show(self):
        if self.tipwindow or not self.text: return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        ttk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1).pack(ipadx=4, ipady=2)
    
    def hide(self, event=None):
        self.unschedule()
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

_SERVICE, _KEY, _CONTRIB_KEY = "password_gen_app", "history", "contributors"
AUTHOR_NAME = "Kanah Ngouffo Vianney Gurres"
LINKEDIN = "https://www.linkedin.com/in/vianney-kanah/"
EMAIL = "kanahvianney@icloud.com"
LICENSE_NOTE = "Free software — modifications require prior permission from the author."

def save_storage(key, data_list):
    """Save data to keyring if available, otherwise do nothing for history."""
    if keyring:
        try:
            keyring.set_password(_SERVICE, key, json.dumps(data_list))
        except Exception as e:
            print(f"Warning: failed to save {key} to keyring:", e)

def load_storage(key):
    """Load data from keyring if available, otherwise return empty list."""
    if keyring:
        try:
            data = keyring.get_password(_SERVICE, key)
            return json.loads(data) if data else []
        except Exception as e:
            print(f"Warning: failed to load {key} from keyring:", e)
    return []

def save_contributors(contrib_list):
    """Save contributors to keyring or file fallback."""
    if keyring:
        try:
            keyring.set_password(_SERVICE, _CONTRIB_KEY, json.dumps(contrib_list))
            return
        except Exception as e:
            print("Warning: failed to save contributors to keyring:", e)
    try:
        pathlib.Path.home().joinpath(".password_gen_contributors.json").write_text(json.dumps(contrib_list))
    except Exception as e:
        print("Warning: failed to save contributors to file:", e)

def load_contributors():
    """Load contributors from keyring or file fallback."""
    if keyring:
        try:
            data = keyring.get_password(_SERVICE, _CONTRIB_KEY)
            if data: return json.loads(data)
        except Exception as e:
            print("Warning: failed to load contributors from keyring:", e)
    try:
        p = pathlib.Path.home() / ".password_gen_contributors.json"
        return json.loads(p.read_text()) if p.exists() else []
    except Exception:
        return []

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Passwords_generator"))
try:
    from spec_gen import spec_gen
    from no_spec_gen import no_spec_gen
    IMPORT_OK = True
except Exception as e:
    IMPORT_OK, IMPORT_ERROR = False, str(e)

# GUI setup
root = tk.Tk()
root.title("Password Generator")
root.resizable(False, False)
main = ttk.Frame(root, padding=8)
main.grid(row=0, column=0, sticky="nsew")

# Mode selection
mode = tk.StringVar(value="spec")
ttk.Label(main, text="Generator:").grid(row=0, column=0, sticky="w")
ttk.Radiobutton(main, text="With special characters", variable=mode, value="spec").grid(row=1, column=0, sticky="w")
ttk.Radiobutton(main, text="No special characters", variable=mode, value="no_spec").grid(row=2, column=0, sticky="w")

# Length selection
length_var = tk.IntVar(value=20)
LENGTH_MIN_NO_SPEC, LENGTH_MIN_SPEC, LENGTH_MAX = 6, 7, 64

def on_mode_change():
    min_len = LENGTH_MIN_SPEC if mode.get() == "spec" else LENGTH_MIN_NO_SPEC
    length_spin.config(from_=min_len)
    if length_var.get() < min_len: length_var.set(min_len)

mode.trace_add("write", lambda *args: on_mode_change())

length_frame = ttk.Frame(main)
length_frame.grid(row=3, column=0, sticky="w", pady=(6,0))
ttk.Label(length_frame, text="Length:").grid(row=0, column=0, sticky="w")
length_spin = tk.Spinbox(length_frame, from_=LENGTH_MIN_SPEC, to=LENGTH_MAX, textvariable=length_var, width=6)
length_spin.grid(row=0, column=1, padx=6)

# Password display
password_var = tk.StringVar()
ttk.Label(main, text="Generated password:").grid(row=4, column=0, sticky="w", pady=(8,0))
pwd_entry = ttk.Entry(main, textvariable=password_var, width=36, font=("Courier", 10))
pwd_entry.grid(row=5, column=0, pady=(2,8))

# History system
history, contributors = load_storage(_KEY), load_contributors()
HISTORY_LIMIT = 20

history_frame = ttk.Frame(main)
history_frame.grid(row=6, column=0, sticky="nsew")
ttk.Label(history_frame, text="History (double-click to copy):").grid(row=0, column=0, sticky="w")
history_list = tk.Listbox(history_frame, height=8, width=40)
history_list.grid(row=1, column=0, pady=(4,6))
history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=history_list.yview)
history_list.config(yscrollcommand=history_scroll.set)
history_scroll.grid(row=1, column=1, sticky="ns", pady=(4,6))

def update_history():
    history_list.delete(0, tk.END)
    for pwd in history: history_list.insert(tk.END, pwd)

def add_to_history(pwd):
    if pwd in history: history.remove(pwd)
    history.insert(0, pwd)
    if len(history) > HISTORY_LIMIT: history.pop()
    update_history()
    save_storage(_KEY, history)

update_history()

def generate_password():
    if not IMPORT_OK:
        messagebox.showerror("Import error", f"Cannot generate: {IMPORT_ERROR}")
        return
    try:
        pwd = spec_gen(length=length_var.get()) if mode.get() == "spec" else no_spec_gen(length=length_var.get())
    except ValueError as ve:
        messagebox.showerror("Invalid length", str(ve))
        return
    password_var.set(pwd)
    add_to_history(pwd)
    copy_btn["state"] = "normal"

def copy_to_clipboard():
    if not (pwd := password_var.get()):
        messagebox.showinfo("No password", "Generate a password first.")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard")

btn_frame = ttk.Frame(main)
btn_frame.grid(row=7, column=0, pady=(0,6))
gen_btn = ttk.Button(btn_frame, text="Generate", command=generate_password)
copy_btn = ttk.Button(btn_frame, text="Copy current", command=copy_to_clipboard, state="disabled")
gen_btn.grid(row=0, column=0, padx=(0,8))
copy_btn.grid(row=0, column=1)

ToolTip(gen_btn, "Generate a password (Enter)")
ToolTip(copy_btn, "Copy the currently displayed password to clipboard (Ctrl+C)")

# History interactions
def on_history_double_click(event):
    if not (sel := history_list.curselection()): return
    pwd = history_list.get(sel[0])
    password_var.set(pwd)
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Selected history password copied to clipboard")

history_list.bind("<Double-Button-1>", on_history_double_click)

def copy_selected_history():
    if not (sel := history_list.curselection()):
        messagebox.showinfo("No selection", "Select an entry in history first.")
        return
    pwd = history_list.get(sel[0])
    password_var.set(pwd)
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Selected history password copied to clipboard")

def clear_history():
    if messagebox.askyesno("Clear history", "Clear all saved passwords from history?"):
        history.clear()
        update_history()
        save_storage(_KEY, history)

hist_btns = ttk.Frame(main)
hist_btns.grid(row=8, column=0, pady=(4,0))
ttk.Button(hist_btns, text="Copy selected", command=copy_selected_history).grid(row=0, column=0, padx=(0,6))
ttk.Button(hist_btns, text="Clear history", command=clear_history).grid(row=0, column=1)
ttk.Button(hist_btns, text="About / Credits", command=lambda: show_about()).grid(row=0, column=2, padx=6)

# About window
def show_about():
    top = tk.Toplevel(root)
    top.title("About / Credits")
    top.resizable(False, False)
    frm = ttk.Frame(top, padding=8)
    frm.grid(row=0, column=0, sticky="nsew")
    
    ttk.Label(frm, text=f"Author: {AUTHOR_NAME}").grid(row=0, column=0, sticky="w")
    
    # LinkedIn row
    link_row = ttk.Frame(frm)
    link_row.grid(row=1, column=0, columnspan=3, sticky="w")
    ttk.Label(link_row, text="LinkedIn:").pack(side="left")
    link_label = ttk.Label(link_row, text="Vianney Kanah", foreground="blue", cursor="hand2")
    link_label.pack(side="left", padx=(4,0))
    link_label.bind("<Button-1>", lambda e: webbrowser.open(LINKEDIN))
    ToolTip(link_label, LINKEDIN)
    
    # Email row
    email_row = ttk.Frame(frm)
    email_row.grid(row=2, column=0, columnspan=3, sticky="w")
    ttk.Label(email_row, text="Email:").pack(side="left")
    email_label = ttk.Label(email_row, text=EMAIL, foreground="blue", cursor="hand2")
    email_label.pack(side="left", padx=(4,0))
    email_label.bind("<Button-1>", lambda e: webbrowser.open(f"mailto:{EMAIL}"))
    ToolTip(email_label, EMAIL)
    
    ttk.Button(email_row, text="Copy", width=6, 
              command=lambda: (root.clipboard_clear(), root.clipboard_append(EMAIL),
                              messagebox.showinfo("Copied", "Email address copied to clipboard"))).pack(side="left", padx=6)
    
    ttk.Label(frm, text=LICENSE_NOTE).grid(row=3, column=0, sticky="w", pady=(4,6))
    ttk.Label(frm, text="Contributors:").grid(row=4, column=0, sticky="w")
    
    contrib_list = tk.Listbox(frm, height=6, width=40)
    contrib_list.grid(row=5, column=0, pady=(4,6))
    
    def refresh_contribs():
        contrib_list.delete(0, tk.END)
        for c in contributors: contrib_list.insert(tk.END, c)
    refresh_contribs()
    
    def add_contributor():
        if not (name := simpledialog.askstring("Add contributor", "Enter your name:", parent=top)): return
        if (name := name.strip()) in contributors:
            messagebox.showinfo("Already listed", "You're already in the contributors list.")
            return
        contributors.insert(0, name)
        save_contributors(contributors)
        refresh_contribs()
        messagebox.showinfo("Thanks!", "Your name was added to contributors.")
    
    btn_frame = ttk.Frame(frm)
    btn_frame.grid(row=6, column=0, pady=(6,0))
    ttk.Button(btn_frame, text="Add my name", command=add_contributor).grid(row=0, column=0, padx=(0,6))
    ttk.Button(btn_frame, text="Close", command=top.destroy).grid(row=0, column=1)

if not IMPORT_OK:
    ttk.Label(main, text=f"Warning: generator import failed: {IMPORT_ERROR}", 
              foreground="red").grid(row=9, column=0, pady=(8,0))

root.bind("<Return>", lambda e: generate_password())
root.bind("<Control-c>", lambda e: copy_to_clipboard())

def on_close():
    save_storage(_KEY, history)
    save_contributors(contributors)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
gen_btn.focus()
root.mainloop()
