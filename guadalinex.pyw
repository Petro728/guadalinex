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
CURRENT_LANG = "Español"

# ---------- Translations ----------

TRANSLATIONS = {
    "Español": {
        "setup_title": "Configuración inicial de Guadalinex v1",
        "welcome": "Bienvenido a Guadalinex v1",
        "setup_intro": "Antes de comenzar, realiza la configuración inicial.",
        "username_label": "Nombre de usuario:",
        "language_label": "Idioma:",
        "finish_setup": "Finalizar configuración",
        "error_no_username": "Debes introducir un nombre de usuario.",
        "loader_title": "Guadalinex v1",
        "loading": "Cargando el sistema...",
        "loading_status_initial": "Inicializando módulos...",
        "desktop_title": "Escritorio Guadalinex v1 (simulado)",
        "menu_main": "Guadalinex",
        "menu_browser": "Navegador",
        "menu_home": "Home",
        "menu_terminal": "Terminal",
        "menu_antivirus": "Antivirus",
        "menu_about": "Acerca de Guadalinex",
        "menu_reset_setup": "Reiniciar configuración",
        "menu_shutdown": "Apagar",
        "about_text": "Guadalinex v1 (simulado en Python)",
        "home_title": "Carpeta personal",
        "browser_title": "Navegador web",
        "browser_page_start": "Bienvenido al Navegador de Guadalinex v1.\n\nEsto es una página simulada.",
        "browser_page_guadalinex": "Guadalinex v1 fue una distribución GNU/Linux promovida por la Junta de Andalucía.",
        "browser_page_help": "Ayuda del navegador:\n- Escribe 'inicio', 'guadalinex' o 'ayuda'.",
        "browser_not_found": "Página no encontrada.",
        "terminal_title": "Terminal",
        "terminal_header": "Terminal de Guadalinex v1",
        "terminal_help": "Escribe 'help' para ayuda.",
        "antivirus_title": "Antivirus Guadalinex",
        "antivirus_scanning": "Escaneando el sistema...",
        "antivirus_no_threats": "No se encontraron amenazas.",
        "antivirus_threats_found": "Amenazas detectadas:",
        "shutdown_confirm_title": "Apagar",
        "shutdown_confirm_text": "¿Seguro que quieres apagar Guadalinex?",
        "shutdown_screen_text": "Apagando Guadalinex...",
        "reset_done": "La configuración inicial se ha restablecido.\nReinicia Guadalinex.",
        "shell_help": "Comandos: listar/ls, cambiar/cd, mostrar/cat, ruta/pwd, clear, exit, help/ayuda",
    },
    "Inglés": {
        "setup_title": "Initial setup of Guadalinex v1",
        "welcome": "Welcome to Guadalinex v1",
        "setup_intro": "Before we begin, complete the initial setup.",
        "username_label": "Username:",
        "language_label": "Language:",
        "finish_setup": "Finish setup",
        "error_no_username": "You must enter a username.",
        "loader_title": "Guadalinex v1",
        "loading": "Loading system...",
        "loading_status_initial": "Initializing modules...",
        "desktop_title": "Guadalinex v1 Desktop (simulated)",
        "menu_main": "Guadalinex",
        "menu_browser": "Browser",
        "menu_home": "Home",
        "menu_terminal": "Terminal",
        "menu_antivirus": "Antivirus",
        "menu_about": "About Guadalinex",
        "menu_reset_setup": "Reset setup",
        "menu_shutdown": "Shut down",
        "about_text": "Guadalinex v1 (simulated in Python)",
        "home_title": "Home folder",
        "browser_title": "Web Browser",
        "browser_page_start": "Welcome to the Guadalinex v1 Browser.\n\nThis is a simulated page.",
        "browser_page_guadalinex": "Guadalinex v1 was a GNU/Linux distribution promoted by the Andalusian government.",
        "browser_page_help": "Browser help:\n- Type 'inicio', 'guadalinex' or 'ayuda'.",
        "browser_not_found": "Page not found.",
        "terminal_title": "Terminal",
        "terminal_header": "Guadalinex v1 Terminal",
        "terminal_help": "Type 'help' for assistance.",
        "antivirus_title": "Guadalinex Antivirus",
        "antivirus_scanning": "Scanning system...",
        "antivirus_no_threats": "No threats found.",
        "antivirus_threats_found": "Threats detected:",
        "shutdown_confirm_title": "Shut down",
        "shutdown_confirm_text": "Are you sure you want to shut down Guadalinex?",
        "shutdown_screen_text": "Shutting down Guadalinex...",
        "reset_done": "Initial setup has been reset.\nRestart Guadalinex.",
        "shell_help": "Commands: ls, cd, cat, pwd, clear, exit, help",
    },
    "Catalán": {
        "setup_title": "Configuració inicial de Guadalinex v1",
        "welcome": "Benvingut a Guadalinex v1",
        "setup_intro": "Abans de començar, fes la configuració inicial.",
        "username_label": "Nom d'usuari:",
        "language_label": "Idioma:",
        "finish_setup": "Finalitzar configuració",
        "error_no_username": "Has d'introduir un nom d'usuari.",
        "loader_title": "Guadalinex v1",
        "loading": "Carregant el sistema...",
        "loading_status_initial": "Inicialitzant mòduls...",
        "desktop_title": "Escriptori Guadalinex v1 (simulat)",
        "menu_main": "Guadalinex",
        "menu_browser": "Navegador",
        "menu_home": "Home",
        "menu_terminal": "Terminal",
        "menu_antivirus": "Antivirus",
        "menu_about": "Quant a Guadalinex",
        "menu_reset_setup": "Reiniciar configuració",
        "menu_shutdown": "Apagar",
        "about_text": "Guadalinex v1 (simulat en Python)",
        "home_title": "Carpeta personal",
        "browser_title": "Navegador web",
        "browser_page_start": "Benvingut al Navegador de Guadalinex v1.\n\nAixò és una pàgina simulada.",
        "browser_page_guadalinex": "Guadalinex v1 va ser una distribució GNU/Linux promoguda per la Junta d'Andalusia.",
        "browser_page_help": "Ajuda del navegador:\n- Escriu 'inicio', 'guadalinex' o 'ayuda'.",
        "browser_not_found": "Pàgina no trobada.",
        "terminal_title": "Terminal",
        "terminal_header": "Terminal de Guadalinex v1",
        "terminal_help": "Escriu 'help' per ajuda.",
        "antivirus_title": "Antivirus Guadalinex",
        "antivirus_scanning": "Escanejant el sistema...",
        "antivirus_no_threats": "No s'han trobat amenaces.",
        "antivirus_threats_found": "Amenaces detectades:",
        "shutdown_confirm_title": "Apagar",
        "shutdown_confirm_text": "Segur que vols apagar Guadalinex?",
        "shutdown_screen_text": "Apagant Guadalinex...",
        "reset_done": "La configuració inicial s'ha restablert.\nReinicia Guadalinex.",
        "shell_help": "Comandes: llistar/ls, canviar/cd, mostrar/cat, ruta/pwd, clear, exit, ajuda/help",
    },
    "Gallego": {
        "setup_title": "Configuración inicial de Guadalinex v1",
        "welcome": "Benvido a Guadalinex v1",
        "setup_intro": "Antes de comezar, realiza a configuración inicial.",
        "username_label": "Nome de usuario:",
        "language_label": "Idioma:",
        "finish_setup": "Finalizar configuración",
        "error_no_username": "Debes introducir un nome de usuario.",
        "loader_title": "Guadalinex v1",
        "loading": "Cargando o sistema...",
        "loading_status_initial": "Inicializando módulos...",
        "desktop_title": "Escritorio Guadalinex v1 (simulado)",
        "menu_main": "Guadalinex",
        "menu_browser": "Navegador",
        "menu_home": "Home",
        "menu_terminal": "Terminal",
        "menu_antivirus": "Antivirus",
        "menu_about": "Sobre Guadalinex",
        "menu_reset_setup": "Reiniciar configuración",
        "menu_shutdown": "Apagar",
        "about_text": "Guadalinex v1 (simulado en Python)",
        "home_title": "Carpeta persoal",
        "browser_title": "Navegador web",
        "browser_page_start": "Benvido ao Navegador de Guadalinex v1.\n\nIsto é unha páxina simulada.",
        "browser_page_guadalinex": "Guadalinex v1 foi unha distribución GNU/Linux promovida pola Xunta de Andalucía.",
        "browser_page_help": "Axuda do navegador:\n- Escribe 'inicio', 'guadalinex' ou 'ayuda'.",
        "browser_not_found": "Páxina non atopada.",
        "terminal_title": "Terminal",
        "terminal_header": "Terminal de Guadalinex v1",
        "terminal_help": "Escribe 'help' para axuda.",
        "antivirus_title": "Antivirus Guadalinex",
        "antivirus_scanning": "Escaneando o sistema...",
        "antivirus_no_threats": "Non se atoparon ameazas.",
        "antivirus_threats_found": "Ameazas detectadas:",
        "shutdown_confirm_title": "Apagar",
        "shutdown_confirm_text": "Seguro que queres apagar Guadalinex?",
        "shutdown_screen_text": "Apagando Guadalinex...",
        "reset_done": "A configuración inicial foi restablecida.\nReinicia Guadalinex.",
        "shell_help": "Comandos: listar/ls, cambiar/cd, mostrar/cat, ruta/pwd, clear, exit, axuda/help",
    },
    "Pirata": {
        "setup_title": "First riggin' o' Guadalinex v1",
        "welcome": "Ahoy! Welcome t' Guadalinex v1!",
        "setup_intro": "Before we set sail, finish yer riggin'.",
        "username_label": "Cap'n name:",
        "language_label": "Tongue:",
        "finish_setup": "Hoist the colors!",
        "error_no_username": "Ye must give a name, matey.",
        "loader_title": "Guadalinex v1",
        "loading": "Hoistin' the sails...",
        "loading_status_initial": "Rousin' the crew...",
        "desktop_title": "Guadalinex v1 Deck (simulated)",
        "menu_main": "Guadalinex",
        "menu_browser": "Spyglass",
        "menu_home": "Quarters",
        "menu_terminal": "Ship Console",
        "menu_antivirus": "Anti‑Kraken",
        "menu_about": "About this vessel",
        "menu_reset_setup": "Reset riggin'",
        "menu_shutdown": "Scuttle ship",
        "about_text": "Guadalinex v1 (a fine vessel forged in Python)",
        "home_title": "Captain's Quarters",
        "browser_title": "Spyglass Browser",
        "browser_page_start": "Ahoy! This be the Spyglass o' Guadalinex v1.\n\nJust a mock sea chart.",
        "browser_page_guadalinex": "Guadalinex v1 be a GNU/Linux vessel once flown under Andalusian colors.",
        "browser_page_help": "Spyglass help:\n- Type 'inicio', 'guadalinex' or 'ayuda'.",
        "browser_not_found": "Nay, that page be lost at sea.",
        "terminal_title": "Ship Console",
        "terminal_header": "Guadalinex v1 Ship Console",
        "terminal_help": "Type 'yarr' or 'help' if ye be lost.",
        "antivirus_title": "Anti‑Kraken Scanner",
        "antivirus_scanning": "Searchin' fer cursed cargo...",
        "antivirus_no_threats": "No cursed cargo found. Seas be calm.",
        "antivirus_threats_found": "Cursed cargo spotted:",
        "shutdown_confirm_title": "Scuttle ship",
        "shutdown_confirm_text": "Be ye sure ye want t' sink this vessel?",
        "shutdown_screen_text": "Scuttlin' the ship...",
        "reset_done": "Riggin' reset.\nHoist her again from port.",
        "shell_help": "Commands: plunder/ls, board/cd, readscroll/cat, wherebe/pwd, clear, abandon/exit, yarr/help",
    },
}

# Shell command mapping: canonical -> localized
SHELL_COMMANDS = {
    "Español": {
        "ls": ["ls", "listar"],
        "cd": ["cd", "cambiar"],
        "cat": ["cat", "mostrar"],
        "pwd": ["pwd", "ruta"],
        "help": ["help", "ayuda"],
        "clear": ["clear"],
        "exit": ["exit"],
    },
    "Inglés": {
        "ls": ["ls"],
        "cd": ["cd"],
        "cat": ["cat"],
        "pwd": ["pwd"],
        "help": ["help"],
        "clear": ["clear"],
        "exit": ["exit"],
    },
    "Catalán": {
        "ls": ["ls", "llistar"],
        "cd": ["cd", "canviar"],
        "cat": ["cat", "mostrar"],
        "pwd": ["pwd", "ruta"],
        "help": ["help", "ajuda"],
        "clear": ["clear"],
        "exit": ["exit"],
    },
    "Gallego": {
        "ls": ["ls", "listar"],
        "cd": ["cd", "cambiar"],
        "cat": ["cat", "mostrar"],
        "pwd": ["pwd", "ruta"],
        "help": ["help", "axuda"],
        "clear": ["clear"],
        "exit": ["exit"],
    },
    "Pirata": {
        "ls": ["ls", "plunder"],
        "cd": ["cd", "board"],
        "cat": ["cat", "readscroll"],
        "pwd": ["pwd", "wherebe"],
        "help": ["help", "yarr"],
        "clear": ["clear"],
        "exit": ["exit", "abandon"],
    },
}

def T(key: str) -> str:
    lang = TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["Español"])
    return lang.get(key, TRANSLATIONS["Español"].get(key, key))


# ---------- VFS ----------

BASE_USER_FS = {
    "Documentos": {
        "bienvenida.txt": "Bienvenido a Guadalinex v1 simulado.\nEste es tu directorio personal."
    },
    "Imágenes": {},
    "Descargas": {}
}

VFS = {}


def init_vfs_for_user(username: str):
    global VFS
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


def reset_setup():
    if SETUP_FILE.exists():
        SETUP_FILE.unlink()
    messagebox.showinfo("Reset", T("reset_done"))


# ---------- Setup screen ----------

class GuadalinexSetup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(T("setup_title"))
        self.geometry("500x300")
        self.configure(bg="#4f7fb3")
        self.resizable(False, False)

        tk.Label(
            self,
            text=T("welcome"),
            font=("Sans", 22, "bold"),
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=20)

        tk.Label(
            self,
            text=T("setup_intro"),
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=10)

        frame = tk.Frame(self, bg="#4f7fb3")
        frame.pack(pady=10)

        tk.Label(frame, text=T("username_label"), fg="white", bg="#4f7fb3").grid(row=0, column=0, sticky="w")
        self.username = tk.Entry(frame)
        self.username.grid(row=0, column=1)

        tk.Label(frame, text=T("language_label"), fg="white", bg="#4f7fb3").grid(row=1, column=0, sticky="w")
        self.language = tk.StringVar(value="Español")
        tk.OptionMenu(frame, self.language, "Español", "Inglés", "Catalán", "Gallego", "Pirata").grid(row=1, column=1)

        tk.Button(self, text=T("finish_setup"), command=self.finish_setup).pack(pady=20)

    def finish_setup(self):
        global CURRENT_USER, CURRENT_LANG

        username = self.username.get().strip()
        if not username:
            messagebox.showerror("Error", T("error_no_username"))
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
        self.title(T("loader_title"))
        self.resizable(False, False)
        self.geometry("500x300")
        self.configure(bg="#4f7fb3")

        container = tk.Frame(self, bg="#4f7fb3")
        container.pack(expand=True, fill="both")

        tk.Label(
            container,
            text=T("welcome"),
            font=("Sans", 28, "bold"),
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=40)

        tk.Label(
            container,
            text=T("loading"),
            font=("Sans", 12),
            fg="white",
            bg="#4f7fb3"
        ).pack(pady=10)

        self.progress = ttk.Progressbar(container, orient="horizontal", mode="determinate", length=300)
        self.progress.pack(pady=30)

        self.status_label = tk.Label(
            container,
            text=T("loading_status_initial"),
            font=("Sans", 10),
            fg="white",
            bg="#4f7fb3"
        )
        self.status_label.pack()

        threading.Thread(target=self.fake_boot, daemon=True).start()

    def fake_boot(self):
        steps = [
            T("loading_status_initial"),
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
    win.title(f"{T('home_title')} - {CURRENT_USER}")
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


# ---------- Apps: Browser ----------

def open_browser_app(parent):
    win = tk.Toplevel(parent)
    win.title(T("browser_title"))
    win.geometry("600x400")
    win.configure(bg="#dcdcdc")

    toolbar = tk.Frame(win, bg="#bbbbbb")
    toolbar.pack(fill="x")

    url = tk.Entry(toolbar)
    url.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    page = tk.Text(win, wrap="word", bg="white")
    page.pack(fill="both", expand=True)

    PAGES = {
        "inicio": T("browser_page_start"),
        "guadalinex": T("browser_page_guadalinex"),
        "ayuda": T("browser_page_help"),
    }

    def load_page():
        key = url.get().strip().lower()
        page.delete("1.0", "end")
        page.insert("1.0", PAGES.get(key, T("browser_not_found")))

    tk.Button(toolbar, text="Ir", command=load_page).pack(side="right", padx=5)

    url.insert(0, "inicio")
    load_page()


# ---------- Mini shell ----------

class MiniShell:
    def __init__(self, username: str):
        self.username = username
        self.cwd = ["home", username]

    def get_cwd_node(self):
        node = VFS
        for part in self.cwd:
            node = node[part]
        return node

    def get_pwd(self):
        if self.cwd == ["home", self.username]:
            return f"/home/{self.username}"
        sub = "/".join(self.cwd[2:])
        return f"/home/{self.username}/" + sub

    def get_prompt_path(self):
        if self.cwd == ["home", self.username]:
            return "~"
        sub = "/".join(self.cwd[2:])
        return f"~/{sub}"

    def resolve_command(self, cmd: str) -> str:
        mapping = SHELL_COMMANDS.get(CURRENT_LANG, SHELL_COMMANDS["Español"])
        for canonical, aliases in mapping.items():
            if cmd in aliases:
                return canonical
        return cmd  # unknown

    def run(self, cmd: str):
        if not cmd:
            return ""
        parts = cmd.split()
        raw_c = parts[0]
        args = parts[1:]

        c = self.resolve_command(raw_c)

        if c == "help":
            return T("shell_help")
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
    win.title(T("terminal_title"))
    win.geometry("600x350")
    win.configure(bg="#000000")

    text = tk.Text(win, bg="black", fg="white", insertbackground="white")
    text.pack(fill="both", expand=True)

    def write_prompt():
        path = shell.get_prompt_path()
        prompt = f"{shell.username}@guadalinex:{path}$ "
        text.insert("end", prompt)
        text.see("end")

    text.insert("end", f"{T('terminal_header')}\n{T('terminal_help')}\n\n")
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
            text.insert("end", f"{T('terminal_header')}\n{T('terminal_help')}\n\n")
        else:
            text.insert("end", "\n" + output + "\n")
        write_prompt()
        return "break"

    text.bind("<Return>", on_enter)


# ---------- Antivirus app ----------

def open_antivirus_app(parent):
    win = tk.Toplevel(parent)
    win.title(T("antivirus_title"))
    win.geometry("400x250")
    win.configure(bg="#dcdcdc")

    label = tk.Label(win, text=T("antivirus_scanning"), bg="#dcdcdc")
    label.pack(pady=10)

    progress = ttk.Progressbar(win, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20)

    result = tk.Label(win, text="", bg="#dcdcdc")
    result.pack(pady=10)

    def scan():
        suspicious = []
        total = 0

        user_home = VFS["home"][CURRENT_USER]
        for folder, content in user_home.items():
            for filename in content:
                total += 1

        if total == 0:
            total = 1

        scanned = 0
        for folder, content in user_home.items():
            for filename in list(content.keys()):
                scanned += 1
                progress["value"] = (scanned / total) * 100
                win.update_idletasks()
                time.sleep(0.2)

                if "virus" in filename.lower() or "malware" in filename.lower():
                    suspicious.append(f"{folder}/{filename}")

        if suspicious:
            result.config(text=T("antivirus_threats_found") + "\n" + "\n".join(suspicious), fg="red")
        else:
            result.config(text=T("antivirus_no_threats"), fg="green")

    threading.Thread(target=scan, daemon=True).start()


# ---------- Shutdown screen ----------

def show_shutdown_screen():
    win = tk.Toplevel()
    win.title(T("shutdown_confirm_title"))
    win.geometry("400x200")
    win.configure(bg="#000000")
    tk.Label(win, text=T("shutdown_screen_text"), fg="white", bg="black", font=("Sans", 16)).pack(expand=True)
    win.after(2000, quit)


# ---------- Desktop ----------

class GuadalinexDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(T("desktop_title"))
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
            text=T("menu_main"),
            fg="white",
            bg="#2b2b2b",
            command=self.open_main_menu
        ).pack(side="left", padx=2)

        tk.Button(
            self.left_panel,
            text=T("menu_browser"),
            fg="white",
            bg="#555555",
            command=self.open_browser
        ).pack(side="left", padx=2)

        tk.Button(
            self.left_panel,
            text=T("menu_home"),
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

        self.make_icon(frame, T("menu_home"), self.open_home, 0)
        self.make_icon(frame, T("menu_browser"), self.open_browser, 1)
        self.make_icon(frame, T("menu_terminal"), self.open_terminal, 2)
        self.make_icon(frame, T("menu_antivirus"), self.open_antivirus, 3)

    def make_icon(self, parent, text, command, row):
        tk.Button(parent, text=text, width=14, height=2, command=command).grid(row=row, pady=10)

    def open_main_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label=T("menu_browser"), command=self.open_browser)
        menu.add_command(label=T("menu_home"), command=self.open_home)
        menu.add_command(label=T("menu_terminal"), command=self.open_terminal)
        menu.add_command(label=T("menu_antivirus"), command=self.open_antivirus)
        menu.add_separator()
        menu.add_command(label=T("menu_about"), command=self.show_about)
        menu.add_command(label=T("menu_reset_setup"), command=reset_setup)
        menu.add_separator()
        menu.add_command(label=T("menu_shutdown"), command=self.shutdown)
        menu.tk_popup(self.winfo_rootx() + 10, self.winfo_rooty() + 10)

    def open_browser(self):
        open_browser_app(self)

    def open_home(self):
        open_home_app(self)

    def open_terminal(self):
        open_terminal_app(self, self.shell)

    def open_antivirus(self):
        open_antivirus_app(self)

    def show_about(self):
        messagebox.showinfo(
            T("menu_about"),
            f"{T('about_text')}\nUsuario: {CURRENT_USER}\nIdioma: {CURRENT_LANG}"
        )

    def shutdown(self):
        if messagebox.askyesno(T("shutdown_confirm_title"), T("shutdown_confirm_text")):
            show_shutdown_screen()
            self.destroy()


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
