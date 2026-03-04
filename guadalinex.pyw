import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from pathlib import Path
import copy

# ---------- Global config ----------

SETUP_FILE = Path.home() / ".guadalinex_setup_done"

WALLPAPER_COLOR = "#6aa84f"
PANEL_COLOR = "#3c3c3c"
PANEL_HEIGHT = 32

CURRENT_USER = None
CURRENT_LANG = None

# Base template for a user's home
BASE_USER_FS = {
    "Documentos": {
        "bienvenida.txt": "Bienvenido a Guadalinex v1 simulado.\nEste es tu directorio personal."
    },
    "Imágenes": {},
    "Descargas": {}
}

# Global VFS, initialized after we know the user
VFS = {}


def init_vfs_for_user(username: str):
    global VFS
    # Deep-ish copy of BASE_USER_FS
    user_home = {}
    for folder, content in BASE_USER_FS.items():
        user_home[folder] = copy.deepcopy(content)
    VFS = {
        "home": {
            username: user_home
        }
    }


def load_setup_config():
    global CURRENT_USER, CURRENT_LANG
    if not SETUP_FILE.exists():
        return
    data = {}
    with open(SETUP_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                data[k] = v
    CURRENT_USER = data.get("username", "usuario")
    CURRENT_LANG = data.get("language", "Español")
    init_vfs_for_user(CURRENT_USER)


# ---------- Setup screen ----------

class GuadalinexSetup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuración inicial de Guadalinex v1")
        self.geometry("500x300")
        self.configure(bg="#4f7fb3")
        self.resizable(False, False)

        tk.Label(
            self,
            text="Bienvenido a Guadalinex v1",
            font=("Sans", 22, "bold"),
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=20)

        tk.Label(
            self,
            text="Antes de comenzar, realiza la configuración inicial.",
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=10)

        frame = tk.Frame(self, bg="#4f7fb3")
        frame.pack(pady=10)

        tk.Label(frame, text="Nombre de usuario:", fg="white", bg="#4f7fb3").grid(row=0, column=0, sticky="w")
        self.username = tk.Entry(frame)
        self.username.grid(row=0, column=1)

        tk.Label(frame, text="Idioma:", fg="white", bg="#4f7fb3").grid(row=1, column=0, sticky="w")
        self.language = tk.StringVar(value="Español")
        tk.OptionMenu(frame, self.language, "Español").grid(row=1, column=1)

        tk.Button(self, text="Finalizar configuración", command=self.finish_setup).pack(pady=20)

    def finish_setup(self):
        global CURRENT_USER, CURRENT_LANG

        username = self.username.get().strip()
        if not username:
            messagebox.showerror("Error", "Debes introducir un nombre de usuario.")
            return

        CURRENT_USER = username
        CURRENT_LANG = self.language.get()

        with open(SETUP_FILE, "w", encoding="utf-8") as f:
            f.write("setup_done=1\n")
            f.write(f"username={CURRENT_USER}\n")
            f.write(f"language={CURRENT_LANG}\n")

        init_vfs_for_user(CURRENT_USER)

        self.after(100, self.launch_loader)

    def launch_loader(self):
        self.destroy()
        show_loader()


# ---------- Loader screen ----------

class GuadalinexLoader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guadalinex v1")
        self.resizable(False, False)
        self.geometry("500x300")
        self.configure(bg="#4f7fb3")

        container = tk.Frame(self, bg="#4f7fb3")
        container.pack(expand=True, fill="both")

        tk.Label(
            container,
            text="Guadalinex v1",
            font=("Sans", 28, "bold"),
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=40)

        tk.Label(
            container,
            text="Cargando el sistema...",
            font=("Sans", 12),
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=10)

        self.progress = ttk.Progressbar(container, orient="horizontal", mode="determinate", length=300)
        self.progress.pack(pady=30)

        self.status_label = tk.Label(
            container,
            text="Inicializando módulos...",
            font=("Sans", 10),
            fg="white",
            bg="#4f7fb3"
        )
        self.status_label.pack()

        threading.Thread(target=self.fake_boot, daemon=True).start()

    def fake_boot(self):
        steps = [
            "Cargando kernel...",
            "Montando sistema de archivos...",
            "Iniciando servicios básicos...",
            "Configurando entorno de usuario...",
            "Preparando escritorio Guadalinex..."
        ]
        for i, msg in enumerate(steps, start=1):
            time.sleep(0.8)
            self.progress["value"] = i * (100 / len(steps))
            self.status_label.config(text=msg)

        time.sleep(0.8)
        self.after(500, self.finish)

    def finish(self):
        self.destroy()
        show_desktop()


# ---------- Apps: Home ----------

def open_home_app(parent):
    win = tk.Toplevel(parent)
    win.title(f"Carpeta personal de {CURRENT_USER}")
    win.geometry("500x380")
    win.configure(bg="#dcdcdc")

    left = tk.Frame(win, bg="#ececec", width=160)
    left.pack(side="left", fill="y")

    right = tk.Frame(win, bg="#ffffff")
    right.pack(side="right", fill="both", expand=True)

    folder_list = tk.Listbox(left)
    folder_list.pack(fill="y", expand=True, padx=5, pady=5)

    file_list = tk.Listbox(right)
    file_list.pack(fill="both", expand=True, padx=5, pady=5)

    user_home = VFS["home"][CURRENT_USER]

    for folder in user_home:
        folder_list.insert("end", folder)

    def show_files(event):
        if not folder_list.curselection():
            return
        file_list.delete(0, "end")
        folder = folder_list.get(folder_list.curselection())
        for f in user_home[folder]:
            file_list.insert("end", f)

    def open_file(event):
        if not folder_list.curselection() or not file_list.curselection():
            return
        folder = folder_list.get(folder_list.curselection())
        filename = file_list.get(file_list.curselection())
        content = user_home[folder][filename]

        viewer = tk.Toplevel(win)
        viewer.title(filename)
        text = tk.Text(viewer, wrap="word")
        text.insert("1.0", content)
        text.config(state="disabled")
        text.pack(fill="both", expand=True)

    folder_list.bind("<<ListboxSelect>>", show_files)
    file_list.bind("<Double-Button-1>", open_file)


# ---------- Apps: Navegador ----------

def open_browser_app(parent):
    win = tk.Toplevel(parent)
    win.title("Navegador web")
    win.geometry("600x400")
    win.configure(bg="#dcdcdc")

    toolbar = tk.Frame(win, bg="#bbbbbb")
    toolbar.pack(fill="x")

    url = tk.Entry(toolbar)
    url.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    page = tk.Text(win, wrap="word", bg="white")
    page.pack(fill="both", expand=True)

    PAGES = {
        "inicio": "Bienvenido al Navegador de Guadalinex v1.\n\nEsto es una página simulada.",
        "guadalinex": "Guadalinex v1 fue una distribución GNU/Linux promovida por la Junta de Andalucía.",
        "ayuda": "Ayuda del navegador:\n- Escribe 'inicio', 'guadalinex' o 'ayuda'.",
        "que-paso-con-este-OS": "Desafortunamente, en 2018, era discontinuado. Pero, como esto es una simulación, no pasaría nada."
    }

    def load_page():
        key = url.get().strip().lower()
        page.delete("1.0", "end")
        page.insert("1.0", PAGES.get(key, "Página no encontrada."))

    tk.Button(toolbar, text="Ir", command=load_page).pack(side="right", padx=5)

    url.insert(0, "inicio")
    load_page()


# ---------- Mini shell ----------

class MiniShell:
    def __init__(self, username: str):
        self.username = username
        # cwd as list of path components, starting at ["home", username]
        self.cwd = ["home", username]

    def get_cwd_node(self):
        node = VFS
        for part in self.cwd:
            node = node[part]
        return node

    def get_pwd(self):
        # Build /home/<user>/...
        if self.cwd == ["home", self.username]:
            return f"/home/{self.username}"
        sub = "/".join(self.cwd[2:])
        return f"/home/{self.username}/" + sub

    def get_prompt_path(self):
        # Show ~ for home, ~/subdir for others
        if self.cwd == ["home", self.username]:
            return "~"
        sub = "/".join(self.cwd[2:])
        return f"~/{sub}"

    def run(self, cmd: str):
        if not cmd:
            return ""
        parts = cmd.split()
        c = parts[0]
        args = parts[1:]

        if c == "help":
            return "Comandos: help, ls, cd, cat, pwd, clear, exit"
        if c == "pwd":
            return self.get_pwd()
        if c == "ls":
            return self.cmd_ls()
        if c == "cd":
            return self.cmd_cd(args)
        if c == "cat":
            return self.cmd_cat(args)
        if c == "clear":
            return "\f"
        if c == "exit":
            return "Cierra la ventana para salir."
        return "Comando no reconocido."

    def cmd_ls(self):
        node = self.get_cwd_node()
        items = list(node.keys())
        return "\n".join(items)

    def cmd_cd(self, args):
        if not args:
            self.cwd = ["home", self.username]
            return ""
        target = args[0]
        if target == "/":
            self.cwd = ["home", self.username]
            return ""
        if target == "..":
            if len(self.cwd) > 2:
                self.cwd.pop()
            return ""
        node = self.get_cwd_node()
        if target in node and isinstance(node[target], dict):
            self.cwd.append(target)
            return ""
        return "Directorio no encontrado."

    def cmd_cat(self, args):
        if not args:
            return "Uso: cat <archivo>"
        filename = args[0]
        node = self.get_cwd_node()
        if filename in node and isinstance(node[filename], str):
            return node[filename]
        return "Archivo no encontrado."


# ---------- Terminal app ----------

def open_terminal_app(parent, shell: MiniShell):
    win = tk.Toplevel(parent)
    win.title("Terminal")
    win.geometry("600x350")
    win.configure(bg="#000000")

    text = tk.Text(win, bg="black", fg="white", insertbackground="white")
    text.pack(fill="both", expand=True)

    def write_prompt():
        path = shell.get_prompt_path()
        prompt = f"{shell.username}@guadalinex:{path}$ "
        text.insert("end", prompt)
        text.see("end")

    text.insert("end", "Guadalinex v1 Terminal\nEscribe 'help' para ayuda.\n\n")
    write_prompt()

    def on_enter(event):
        line_start = text.search(r"\n", "insert linestart", backwards=True)
        if not line_start:
            line_start = "insert linestart"
        line = text.get(line_start, "end-1c")
        if "$" in line:
            cmd = line.split("$", 1)[-1].strip()
        else:
            cmd = line.strip()

        output = shell.run(cmd)

        if output == "\f":
            text.delete("1.0", "end")
            text.insert("end", "Guadalinex v1 Terminal\nEscribe 'help' para ayuda.\n\n")
        else:
            text.insert("end", "\n" + output + "\n")
        write_prompt()
        return "break"

    text.bind("<Return>", on_enter)


# ---------- Desktop ----------

class GuadalinexDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guadalinex v1 Desktop (simulado)")
        self.geometry("800x600")
        self.minsize(640, 480)

        self.shell = MiniShell(CURRENT_USER)

        self.desktop = tk.Frame(self, bg=WALLPAPER_COLOR)
        self.desktop.pack(fill="both", expand=True)

        self.panel = tk.Frame(self.desktop, bg=PANEL_COLOR, height=PANEL_HEIGHT)
        self.panel.pack(side="bottom", fill="x")

        self.left_panel = tk.Frame(self.panel, bg=PANEL_COLOR)
        self.left_panel.pack(side="left", padx=4)

        tk.Button(
            self.left_panel,
            text="Guadalinex",
            fg="white",
            bg="#2b2b2b",
            command=self.open_main_menu
        ).pack(side="left", padx=2)

        tk.Button(
            self.left_panel,
            text="Navegador",
            fg="white",
            bg="#555555",
            command=self.open_browser
        ).pack(side="left", padx=2)

        tk.Button(
            self.left_panel,
            text="Home",
            fg="white",
            bg="#555555",
            command=self.open_home
        ).pack(side="left", padx=2)

        self.right_panel = tk.Frame(self.panel, bg=PANEL_COLOR)
        self.right_panel.pack(side="right", padx=6)

        self.clock_label = tk.Label(self.right_panel, text="", fg="white", bg=PANEL_COLOR)
        self.clock_label.pack(side="right")

        self.update_clock()
        self.create_desktop_icons()

    def update_clock(self):
        self.clock_label.config(text=time.strftime("%H:%M"))
        self.after(1000, self.update_clock)

    def create_desktop_icons(self):
        frame = tk.Frame(self.desktop, bg=WALLPAPER_COLOR)
        frame.place(x=20, y=40)

        self.make_icon(frame, "Home", self.open_home, 0)
        self.make_icon(frame, "Navegador", self.open_browser, 1)
        self.make_icon(frame, "Terminal", self.open_terminal, 2)

    def make_icon(self, parent, text, command, row):
        tk.Button(parent, text=text, width=12, height=2, command=command).grid(row=row, pady=10)

    def open_main_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Navegador", command=self.open_browser)
        menu.add_command(label="Home", command=self.open_home)
        menu.add_command(label="Terminal", command=self.open_terminal)
        menu.add_separator()
        menu.add_command(label=f"Acerca de Guadalinex ({CURRENT_USER})", command=self.show_about)
        menu.add_separator()
        menu.add_command(label="Salir de la sesión", command=self.quit)
        menu.tk_popup(self.winfo_rootx() + 10, self.winfo_rooty() + 10)

    def open_browser(self):
        open_browser_app(self)

    def open_home(self):
        open_home_app(self)

    def open_terminal(self):
        open_terminal_app(self, self.shell)

    def show_about(self):
        messagebox.showinfo(
            "Acerca de Guadalinex",
            f"Guadalinex v1 (simulado en Python)\nUsuario: {CURRENT_USER}\nIdioma: {CURRENT_LANG}"
        )


# ---------- Entry points ----------

def show_loader():
    GuadalinexLoader().mainloop()


def show_desktop():
    GuadalinexDesktop().mainloop()


def show_setup():
    GuadalinexSetup().mainloop()


# ---------- Main ----------

if __name__ == "__main__":
    if SETUP_FILE.exists():
        load_setup_config()
        show_loader()
    else:
        show_setup()



