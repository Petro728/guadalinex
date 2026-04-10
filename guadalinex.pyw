import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
from pathlib import Path
import copy
import json
from datetime import datetime

# ---------- Paths ----------

BASE_DIR = Path.home()
ACCOUNTS_FILE = BASE_DIR / ".guadalinex_accounts.json"
BANS_FILE = BASE_DIR / ".guadalinex_bans.json"

# ---------- Globals ----------

WALLPAPER_COLOR = "#6aa84f"
PANEL_COLOR = "#3c3c3c"
PANEL_HEIGHT = 32

CURRENT_USER = None
CURRENT_LANG = "Español"
ACCOUNTS = {}  # username -> {pin, admin, language}
BANS = {}      # username -> {reason, timestamp}

VIOLATIONS = {}  # username -> count

# ---------- Language codes & disallowed terms ----------

LANG_CODES = {
    "Español": "es",
    "Inglés": "en",
    "Catalán": "ca",
    "Gallego": "gl",
    "Pirata": "pir",
}

DISALLOWED_TERMS = {
    "en": ["prohibited_term_1", "prohibited_term_2"],
    "es": ["termino_prohibido_1", "termino_prohibido_2"],
    "ca": ["terme_prohibit_1"],
    "gl": ["termo_prohibido_1"],
    "pir": ["forbidden_phrase_1"],
}

# ---------- Translations ----------

TRANSLATIONS = {
    "Español": {
        "setup_title": "Configuración inicial de Guadalinex v1",
        "welcome": "Bienvenido a Guadalinex v1",
        "setup_intro": "Antes de comenzar, crea la primera cuenta.",
        "username_label": "Nombre de usuario:",
        "language_label": "Idioma:",
        "pin_label": "PIN (opcional):",
        "admin_label": "Esta cuenta es administrador",
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
        "menu_accounts": "Cuentas",
        "menu_about": "Acerca de Guadalinex",
        "menu_logout": "Cerrar sesión",
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
        "shell_help": "Comandos: listar/ls, cambiar/cd, mostrar/cat, ruta/pwd, clear, exit, help/ayuda",
        "login_title": "Inicio de sesión de Guadalinex",
        "login_select_user": "Selecciona un usuario:",
        "login_pin_prompt": "Introduce el PIN para {user}:",
        "login_pin_wrong": "PIN incorrecto.",
        "login_no_users": "No hay cuentas. Reinicia para configurar.",
        "uac_title": "Control de cuentas",
        "uac_message": "Esta acción requiere privilegios de administrador.\nIntroduce el PIN de un administrador:",
        "uac_failed": "PIN de administrador incorrecto.",
        "accounts_title": "Configuración de cuentas",
        "accounts_users": "Usuarios:",
        "accounts_create": "Crear usuario",
        "accounts_delete": "Eliminar usuario",
        "accounts_change_pin": "Cambiar PIN",
        "accounts_toggle_admin": "Alternar admin",
        "accounts_ban_user": "Banear usuario",
        "accounts_new_username": "Nuevo nombre de usuario:",
        "accounts_new_pin": "Nuevo PIN (opcional):",
        "accounts_is_admin": "¿Administrador?",
        "accounts_user_exists": "El usuario ya existe.",
        "accounts_cannot_delete_self": "No puedes eliminar tu propia cuenta mientras estás conectado.",
        "accounts_confirm_delete": "¿Eliminar la cuenta {user}?",
        "accounts_no_selection": "Selecciona un usuario.",
        "accounts_cannot_demote_last_admin": "No puedes quitar el rol de admin del último administrador.",
        "accounts_ban_reason": "Motivo del baneo:",
        "tos_title": "Términos de uso de Guadalinex v1",
        "tos_text": (
            "TÉRMINOS DE USO (SIMULADOS)\n\n"
            "Este sistema operativo es una simulación creada en Python.\n"
            "No realiza cambios reales en tu equipo, ni ofrece garantías.\n\n"
            "Al continuar, aceptas que:\n"
            "- Todo es ficticio y educativo.\n"
            "- No se almacena información sensible de forma real.\n"
            "- No se permite el uso de términos prohibidos ni lenguaje abusivo.\n"
            "- No se permiten intentos de acceso no autorizado a cuentas de administrador.\n"
            "- No se permiten intentos de eludir PINs o modificar cuentas sin permiso.\n"
            "- Las violaciones pueden resultar en la eliminación permanente de la cuenta.\n\n"
            "Firma en el recuadro inferior para aceptar estos términos."
        ),
        "tos_sign_here": "Firma aquí:",
        "tos_accept": "Aceptar y continuar",
        "tos_clear": "Borrar firma",
        "tos_must_sign": "Debes firmar antes de continuar.",
        "ban_screen_title": "Acceso denegado",
        "ban_screen_header": "ACCESO DENEGADO",
        "ban_screen_body": "Tu cuenta ha sido eliminada de este sistema simulado.",
        "ban_screen_reason": "Motivo:",
        "ban_screen_footer": "Contacta con un administrador para volver a crear una cuenta.",
        "ban_screen_back": "Volver al inicio de sesión",
        "violation_warning_title": "Aviso de TOS",
        "violation_warning_text": "Se ha detectado un comportamiento no permitido. Un nuevo intento puede resultar en baneo.",
        "violation_ban_reason_auto": "Comportamiento no permitido detectado en el sistema.",
    },
    "Inglés": {
        "setup_title": "Initial setup of Guadalinex v1",
        "welcome": "Welcome to Guadalinex v1",
        "setup_intro": "Before we begin, create the first account.",
        "username_label": "Username:",
        "language_label": "Language:",
        "pin_label": "PIN (optional):",
        "admin_label": "This account is administrator",
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
        "menu_accounts": "Accounts",
        "menu_about": "About Guadalinex",
        "menu_logout": "Log out",
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
        "shell_help": "Commands: ls, cd, cat, pwd, clear, exit, help",
        "login_title": "Guadalinex Login",
        "login_select_user": "Select a user:",
        "login_pin_prompt": "Enter PIN for {user}:",
        "login_pin_wrong": "Incorrect PIN.",
        "login_no_users": "No accounts found. Restart to run setup.",
        "uac_title": "User Account Control",
        "uac_message": "This action requires administrator privileges.\nEnter an admin PIN:",
        "uac_failed": "Admin PIN incorrect.",
        "accounts_title": "Account settings",
        "accounts_users": "Users:",
        "accounts_create": "Create user",
        "accounts_delete": "Delete user",
        "accounts_change_pin": "Change PIN",
        "accounts_toggle_admin": "Toggle admin",
        "accounts_ban_user": "Ban user",
        "accounts_new_username": "New username:",
        "accounts_new_pin": "New PIN (optional):",
        "accounts_is_admin": "Administrator?",
        "accounts_user_exists": "User already exists.",
        "accounts_cannot_delete_self": "You cannot delete the account you are logged into.",
        "accounts_confirm_delete": "Delete account {user}?",
        "accounts_no_selection": "Select a user.",
        "accounts_cannot_demote_last_admin": "You cannot remove admin role from the last administrator.",
        "accounts_ban_reason": "Ban reason:",
        "tos_title": "Guadalinex v1 Terms of Use",
        "tos_text": (
            "TERMS OF USE (SIMULATED)\n\n"
            "This operating system is a simulation built in Python.\n"
            "It does not make real changes to your machine and comes with no warranty.\n\n"
            "By continuing, you agree that:\n"
            "- Everything is fictional and educational.\n"
            "- No real sensitive data is stored.\n"
            "- Use of disallowed terms or abusive language is not permitted.\n"
            "- Unauthorized attempts to access administrator accounts are not permitted.\n"
            "- Attempts to bypass PINs or modify accounts without permission are not permitted.\n"
            "- Violations may result in permanent account removal.\n\n"
            "Sign in the box below to accept these terms."
        ),
        "tos_sign_here": "Sign here:",
        "tos_accept": "Accept and continue",
        "tos_clear": "Clear signature",
        "tos_must_sign": "You must sign before continuing.",
        "ban_screen_title": "Access denied",
        "ban_screen_header": "ACCESS DENIED",
        "ban_screen_body": "Your account has been removed from this simulated system.",
        "ban_screen_reason": "Reason:",
        "ban_screen_footer": "Contact an administrator to be recreated.",
        "ban_screen_back": "Return to login",
        "violation_warning_title": "TOS warning",
        "violation_warning_text": "Disallowed behavior detected. Another attempt may result in a ban.",
        "violation_ban_reason_auto": "Disallowed behavior detected in the system.",
    },
    # Other languages reuse previous keys; they will fall back for TOS text if missing
    "Catalán": {
        "setup_title": "Configuració inicial de Guadalinex v1",
        "welcome": "Benvingut a Guadalinex v1",
        "setup_intro": "Abans de començar, crea el primer compte.",
        "username_label": "Nom d'usuari:",
        "language_label": "Idioma:",
        "pin_label": "PIN (opcional):",
        "admin_label": "Aquest compte és administrador",
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
        "menu_accounts": "Comptes",
        "menu_about": "Quant a Guadalinex",
        "menu_logout": "Tancar sessió",
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
        "shell_help": "Comandes: llistar/ls, canviar/cd, mostrar/cat, ruta/pwd, clear, exit, ajuda/help",
        "login_title": "Inici de sessió de Guadalinex",
        "login_select_user": "Selecciona un usuari:",
        "login_pin_prompt": "Introdueix el PIN per {user}:",
        "login_pin_wrong": "PIN incorrecte.",
        "login_no_users": "No hi ha comptes. Reinicia per configurar.",
        "uac_title": "Control de comptes",
        "uac_message": "Aquesta acció requereix privilegis d'administrador.\nIntrodueix el PIN d'un administrador:",
        "uac_failed": "PIN d'administrador incorrecte.",
        "accounts_title": "Configuració de comptes",
        "accounts_users": "Usuaris:",
        "accounts_create": "Crear usuari",
        "accounts_delete": "Eliminar usuari",
        "accounts_change_pin": "Canviar PIN",
        "accounts_toggle_admin": "Alternar admin",
        "accounts_ban_user": "Banear usuari",
        "accounts_new_username": "Nou nom d'usuari:",
        "accounts_new_pin": "Nou PIN (opcional):",
        "accounts_is_admin": "Administrador?",
        "accounts_user_exists": "L'usuari ja existeix.",
        "accounts_cannot_delete_self": "No pots eliminar el compte amb el qual has iniciat sessió.",
        "accounts_confirm_delete": "Eliminar el compte {user}?",
        "accounts_no_selection": "Selecciona un usuari.",
        "accounts_cannot_demote_last_admin": "No pots treure el rol d'admin de l'últim administrador.",
        "accounts_ban_reason": "Motiu del ban:",
        "ban_screen_title": "Accés denegat",
        "ban_screen_header": "ACCÉS DENEGAT",
        "ban_screen_body": "El teu compte ha estat eliminat d'aquest sistema simulat.",
        "ban_screen_reason": "Motiu:",
        "ban_screen_footer": "Contacta amb un administrador per tornar a crear un compte.",
        "ban_screen_back": "Tornar a l'inici de sessió",
        "violation_warning_title": "Avís de TOS",
        "violation_warning_text": "S'ha detectat un comportament no permès. Un nou intent pot resultar en ban.",
        "violation_ban_reason_auto": "Comportament no permès detectat al sistema.",
    },
    "Gallego": {
        "setup_title": "Configuración inicial de Guadalinex v1",
        "welcome": "Benvido a Guadalinex v1",
        "setup_intro": "Antes de comezar, crea a primeira conta.",
        "username_label": "Nome de usuario:",
        "language_label": "Idioma:",
        "pin_label": "PIN (opcional):",
        "admin_label": "Esta conta é administrador",
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
        "menu_accounts": "Contas",
        "menu_about": "Sobre Guadalinex",
        "menu_logout": "Pechar sesión",
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
        "shell_help": "Comandos: listar/ls, cambiar/cd, mostrar/cat, ruta/pwd, clear, exit, axuda/help",
        "login_title": "Inicio de sesión de Guadalinex",
        "login_select_user": "Selecciona un usuario:",
        "login_pin_prompt": "Introduce o PIN para {user}:",
        "login_pin_wrong": "PIN incorrecto.",
        "login_no_users": "Non hai contas. Reinicia para configurar.",
        "uac_title": "Control de contas",
        "uac_message": "Esta acción require privilexios de administrador.\nIntroduce o PIN dun administrador:",
        "uac_failed": "PIN de administrador incorrecto.",
        "accounts_title": "Configuración de contas",
        "accounts_users": "Usuarios:",
        "accounts_create": "Crear usuario",
        "accounts_delete": "Eliminar usuario",
        "accounts_change_pin": "Cambiar PIN",
        "accounts_toggle_admin": "Alternar admin",
        "accounts_ban_user": "Banear usuario",
        "accounts_new_username": "Novo nome de usuario:",
        "accounts_new_pin": "Novo PIN (opcional):",
        "accounts_is_admin": "Administrador?",
        "accounts_user_exists": "O usuario xa existe.",
        "accounts_cannot_delete_self": "Non podes eliminar a conta coa que iniciaches sesión.",
        "accounts_confirm_delete": "Eliminar a conta {user}?",
        "accounts_no_selection": "Selecciona un usuario.",
        "accounts_cannot_demote_last_admin": "Non podes quitar o rol de admin do último administrador.",
        "accounts_ban_reason": "Motivo do ban:",
        "ban_screen_title": "Acceso denegado",
        "ban_screen_header": "ACCESO DENEGADO",
        "ban_screen_body": "A túa conta foi eliminada deste sistema simulado.",
        "ban_screen_reason": "Motivo:",
        "ban_screen_footer": "Contacta cun administrador para volver crear unha conta.",
        "ban_screen_back": "Volver ao inicio de sesión",
        "violation_warning_title": "Aviso de TOS",
        "violation_warning_text": "Detectouse un comportamento non permitido. Un novo intento pode resultar en ban.",
        "violation_ban_reason_auto": "Comportamento non permitido detectado no sistema.",
    },
    "Pirata": {
        "setup_title": "First riggin' o' Guadalinex v1",
        "welcome": "Ahoy! Welcome t' Guadalinex v1!",
        "setup_intro": "Before we set sail, forge the first captain.",
        "username_label": "Cap'n name:",
        "language_label": "Tongue:",
        "pin_label": "Secret code (PIN, optional):",
        "admin_label": "This cap'n commands the ship (admin)",
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
        "menu_accounts": "Crew roster",
        "menu_about": "About this vessel",
        "menu_logout": "Leave deck",
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
        "shell_help": "Commands: plunder/ls, board/cd, readscroll/cat, wherebe/pwd, clear, abandon/exit, yarr/help",
        "login_title": "Guadalinex Gangplank",
        "login_select_user": "Choose yer cap'n:",
        "login_pin_prompt": "Whisper the secret code fer {user}:",
        "login_pin_wrong": "That code be wrong, matey.",
        "login_no_users": "No crew aboard. Restart t' rig the first cap'n.",
        "uac_title": "Captain's Seal",
        "uac_message": "This deed needs a captain's blessing.\nGive the secret code o' an admin:",
        "uac_failed": "That be not a captain's code.",
        "accounts_title": "Crew roster & ranks",
        "accounts_users": "Crew:",
        "accounts_create": "Add matey",
        "accounts_delete": "Cast overboard",
        "accounts_change_pin": "Change secret code",
        "accounts_toggle_admin": "Promote/Demote captain",
        "accounts_ban_user": "Brand as mutineer",
        "accounts_new_username": "New matey's name:",
        "accounts_new_pin": "New secret code (optional):",
        "accounts_is_admin": "Make this matey a captain?",
        "accounts_user_exists": "That matey already sails here.",
        "accounts_cannot_delete_self": "Ye can't cast yerself overboard while on deck.",
        "accounts_confirm_delete": "Cast {user} overboard?",
        "accounts_no_selection": "Pick a matey first.",
        "accounts_cannot_demote_last_admin": "Ye can't demote the last captain aboard.",
        "accounts_ban_reason": "Why mark this matey a mutineer?",
        "tos_title": "Guadalinex v1 Code o' Conduct",
        "tos_text": (
            "CODE O' CONDUCT (SIMULATED)\n\n"
            "This vessel be but a Python‑forged illusion.\n"
            "She makes no real waves on yer machine.\n\n"
            "By sailin' on, ye agree:\n"
            "- All be for learnin' and fun.\n"
            "- No real treasure or secrets be stored.\n"
            "- No cursed phrases or forbidden tongue be used.\n"
            "- No sneakin' into the captain's quarters (admin) uninvited.\n"
            "- No tamperin' with secret codes or crew ranks.\n"
            "- Mutiny may see yer name struck from the crew list.\n\n"
            "Sign the log below t' accept these terms."
        ),
        "tos_sign_here": "Sign the log:",
        "tos_accept": "Swear the oath",
        "tos_clear": "Wipe the ink",
        "tos_must_sign": "Ye must sign afore we set sail.",
        "ban_screen_title": "Gangplank barred",
        "ban_screen_header": "ACCESS DENIED",
        "ban_screen_body": "Yer name's been struck from this here simulated crew.",
        "ban_screen_reason": "Charge:",
        "ban_screen_footer": "Find a captain t' sign ye back aboard.",
        "ban_screen_back": "Back t' gangplank",
        "violation_warning_title": "Code o' Conduct warning",
        "violation_warning_text": "The ship's bell rang—one more offense and ye'll be cast off.",
        "violation_ban_reason_auto": "Code o' Conduct broken in the ship's systems.",
    },
}

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

# ---------- Accounts & bans management ----------

def load_accounts():
    global ACCOUNTS
    if ACCOUNTS_FILE.exists():
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                ACCOUNTS = json.load(f)
        except Exception:
            ACCOUNTS = {}
    else:
        ACCOUNTS = {}

def save_accounts():
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(ACCOUNTS, f, indent=2, ensure_ascii=False)

def load_bans():
    global BANS
    if BANS_FILE.exists():
        try:
            with open(BANS_FILE, "r", encoding="utf-8") as f:
                BANS = json.load(f)
        except Exception:
            BANS = {}
    else:
        BANS = {}

def save_bans():
    with open(BANS_FILE, "w", encoding="utf-8") as f:
        json.dump(BANS, f, indent=2, ensure_ascii=False)

def any_admin_exists():
    return any(info.get("admin") for info in ACCOUNTS.values())

def is_admin(user):
    info = ACCOUNTS.get(user, {})
    return bool(info.get("admin"))

def get_user_language(user):
    info = ACCOUNTS.get(user, {})
    return info.get("language", "Español")

def ban_user(username: str, reason: str):
    load_accounts()
    load_bans()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    BANS[username] = {
        "reason": reason,
        "timestamp": timestamp,
    }
    if username in ACCOUNTS:
        del ACCOUNTS[username]
    save_accounts()
    save_bans()

# ---------- TOS violation detection ----------

def check_tos_violation(text: str, context: str, username: str):
    text_l = text.lower()
    user_lang = get_user_language(username)
    code = LANG_CODES.get(user_lang, "en")

    terms = set(DISALLOWED_TERMS.get("en", []))
    terms.update(DISALLOWED_TERMS.get(code, []))

    violated = any(term in text_l for term in terms)
    if not violated and context == "admin_attempt":
        violated = True

    if not violated:
        return

    count = VIOLATIONS.get(username, 0) + 1
    VIOLATIONS[username] = count

    if count == 1:
        messagebox.showwarning(T("violation_warning_title"), T("violation_warning_text"))
    else:
        reason = T("violation_ban_reason_auto")
        ban_user(username, reason)
        messagebox.showerror(T("ban_screen_title"), reason)

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

# ---------- Setup screen ----------

class GuadalinexSetup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(T("setup_title"))
        self.geometry("500x350")
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

        tk.Label(frame, text=T("pin_label"), fg="white", bg="#4f7fb3").grid(row=2, column=0, sticky="w")
        self.pin_entry = tk.Entry(frame, show="*")
        self.pin_entry.grid(row=2, column=1)

        self.admin_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            frame,
            text=T("admin_label"),
            variable=self.admin_var,
            fg="white",
            bg="#4f7fb3",
            selectcolor="#4f7fb3",
            activebackground="#4f7fb3"
        ).grid(row=3, column=0, columnspan=2, sticky="w")

        tk.Button(self, text=T("finish_setup"), command=self.finish_setup).pack(pady=20)

    def finish_setup(self):
        global CURRENT_USER, CURRENT_LANG

        username = self.username.get().strip()
        if not username:
            messagebox.showerror("Error", T("error_no_username"))
            return

        pin = self.pin_entry.get().strip()
        lang = self.language.get()
        admin = self.admin_var.get()

        load_accounts()
        ACCOUNTS[username] = {
            "pin": pin,
            "admin": bool(admin),
            "language": lang,
        }
        save_accounts()

        CURRENT_USER = username
        CURRENT_LANG = lang
        init_vfs_for_user(CURRENT_USER)

        self.after(100, self.launch_tos)

    def launch_tos(self):
        self.destroy()
        show_tos()

# ---------- TOS screen with signature ----------

class TOSScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(T("tos_title"))
        self.geometry("700x500")
        self.configure(bg="#2b3e50")
        self.resizable(False, False)

        self.signed = False
        self.last_x = None
        self.last_y = None

        title = tk.Label(
            self,
            text=T("tos_title"),
            font=("Sans", 18, "bold"),
            fg="white",
            bg="#2b3e50"
        )
        title.pack(pady=10)

        frame_text = tk.Frame(self, bg="#2b3e50")
        frame_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        text = tk.Text(frame_text, wrap="word", height=10)
        text.insert("1.0", T("tos_text"))
        text.config(state="disabled")
        text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_text, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)

        sig_label = tk.Label(self, text=T("tos_sign_here"), fg="white", bg="#2b3e50")
        sig_label.pack(anchor="w", padx=20)

        self.canvas = tk.Canvas(self, bg="white", height=150, cursor="pencil")
        self.canvas.pack(fill="x", padx=20, pady=5)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

        btn_frame = tk.Frame(self, bg="#2b3e50")
        btn_frame.pack(pady=10)

        self.accept_btn = tk.Button(btn_frame, text=T("tos_accept"), state="disabled", command=self.accept)
        self.accept_btn.pack(side="left", padx=10)

        clear_btn = tk.Button(btn_frame, text=T("tos_clear"), command=self.clear_signature)
        clear_btn.pack(side="left", padx=10)

    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="black", width=2)
            self.signed = True
            self.accept_btn.config(state="normal")
        self.last_x = event.x
        self.last_y = event.y

    def clear_signature(self):
        self.canvas.delete("all")
        self.signed = False
        self.accept_btn.config(state="disabled")

    def accept(self):
        if not self.signed:
            messagebox.showwarning(T("tos_title"), T("tos_must_sign"))
            return
        self.after(100, self.launch_login)

    def launch_login(self):
        self.destroy()
        show_login()

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

# ---------- Ban screen (BS2, red with big X) ----------

class BanScreen(tk.Tk):
    def __init__(self, username: str, reason: str):
        super().__init__()
        self.title(T("ban_screen_title"))
        self.geometry("600x350")
        self.configure(bg="#cc0000")
        self.resizable(False, False)

        tk.Label(
            self,
            text="✖",
            font=("Sans", 72, "bold"),
            fg="white",
            bg="#cc0000"
        ).pack(pady=10)

        tk.Label(
            self,
            text=T("ban_screen_header"),
            font=("Sans", 24, "bold"),
            fg="white",
            bg="#cc0000"
        ).pack(pady=5)

        tk.Label(
            self,
            text=T("ban_screen_body"),
            font=("Sans", 12),
            fg="white",
            bg="#cc0000"
        ).pack(pady=10)

        frame = tk.Frame(self, bg="#cc0000")
        frame.pack(pady=5)

        tk.Label(
            frame,
            text=T("ban_screen_reason"),
            font=("Sans", 11, "bold"),
            fg="white",
            bg="#cc0000"
        ).pack(side="left")

        tk.Label(
            frame,
            text=reason or "-",
            font=("Sans", 11),
            fg="white",
            bg="#cc0000",
            wraplength=450,
            justify="left"
        ).pack(side="left")

        tk.Label(
            self,
            text=T("ban_screen_footer"),
            font=("Sans", 11),
            fg="white",
            bg="#cc0000"
        ).pack(pady=15)

        tk.Button(
            self,
            text=T("ban_screen_back"),
            command=self.back_to_login,
            bg="#ffffff",
            fg="#cc0000"
        ).pack(pady=10)

    def back_to_login(self):
        self.destroy()
        show_login()

# ---------- Login screen (B1: icon grid) ----------

class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(T("login_title"))
        self.geometry("600x400")
        self.configure(bg="#2b3e50")
        self.resizable(False, False)

        tk.Label(
            self,
            text=T("login_title"),
            font=("Sans", 22, "bold"),
            fg="white",
            bg="#2b3e50"
        ).pack(pady=20)

        self.users_frame = tk.Frame(self, bg="#2b3e50")
        self.users_frame.pack(expand=True)

        tk.Label(
            self,
            text=T("login_select_user"),
            fg="white",
            bg="#2b3e50"
        ).pack(pady=5)

        self.draw_users()

    def draw_users(self):
        for w in self.users_frame.winfo_children():
            w.destroy()

        load_accounts()
        load_bans()

        users = list(ACCOUNTS.keys())
        banned_users = list(BANS.keys())

        if not users and not banned_users:
            tk.Label(
                self.users_frame,
                text=T("login_no_users"),
                fg="white",
                bg="#2b3e50"
            ).pack()
            return

        all_users = [(u, False) for u in users] + [(u, True) for u in banned_users]

        cols = 3
        for idx, (user, is_banned) in enumerate(all_users):
            row = idx // cols
            col = idx % cols
            frame = tk.Frame(self.users_frame, bg="#2b3e50")
            frame.grid(row=row, column=col, padx=20, pady=20)

            color = "#4f7fb3" if not is_banned else "#7f0000"
            icon = tk.Canvas(frame, width=80, height=80, bg=color, highlightthickness=0)
            icon.create_oval(10, 10, 70, 70, fill="#87aade" if not is_banned else "#ff6666", outline="#ffffff")
            icon.pack()
            label_text = user + (" (ban)" if is_banned else "")
            tk.Label(frame, text=label_text, fg="white", bg="#2b3e50").pack(pady=5)

            if is_banned:
                icon.bind("<Button-1>", lambda e, u=user: self.show_ban(u))
                frame.bind("<Button-1>", lambda e, u=user: self.show_ban(u))
            else:
                icon.bind("<Button-1>", lambda e, u=user: self.login_user(u))
                frame.bind("<Button-1>", lambda e, u=user: self.login_user(u))

    def show_ban(self, user):
        reason = BANS.get(user, {}).get("reason", "")
        self.destroy()
        BanScreen(user, reason).mainloop()

    def login_user(self, user):
        info = ACCOUNTS.get(user, {})
        pin = info.get("pin", "")
        if pin:
            prompt = T("login_pin_prompt").format(user=user)
            entered = simpledialog.askstring(T("login_title"), prompt, show="*", parent=self)
            if entered is None:
                return
            if entered != pin:
                messagebox.showerror(T("login_title"), T("login_pin_wrong"))
                return
        global CURRENT_USER, CURRENT_LANG
        CURRENT_USER = user
        CURRENT_LANG = get_user_language(user)
        init_vfs_for_user(CURRENT_USER)
        self.after(100, self.launch_loader)

    def launch_loader(self):
        self.destroy()
        show_loader()

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
        return cmd

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

        check_tos_violation(cmd, "terminal", shell.username)

        output = shell.run(cmd)

        if output == "\f":
            text.delete("1.0", "end")
            text.insert("end", f"{T('terminal_header')}\n{T('terminal_help')}\n\n")
        else:
            text.insert("end", "\n" + output + "\n")
        write_prompt()
        return "break"

    text.bind("<Return>", on_enter)

# ---------- Home app ----------

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

# ---------- Browser app ----------

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

# ---------- Antivirus app (admin-only via UAC) ----------

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

# ---------- UAC (admin prompt) ----------

def require_admin(parent, action_callback):
    if is_admin(CURRENT_USER):
        action_callback()
        return

    load_accounts()
    admins = [u for u, info in ACCOUNTS.items() if info.get("admin")]
    if not admins:
        messagebox.showerror(T("uac_title"), T("uac_failed"))
        return

    pin = simpledialog.askstring(T("uac_title"), T("uac_message"), show="*", parent=parent)
    if pin is None:
        return

    for u in admins:
        if ACCOUNTS[u].get("pin") == pin:
            action_callback()
            return

    check_tos_violation("unauthorized_admin_access", "admin_attempt", CURRENT_USER)
    messagebox.showerror(T("uac_title"), T("uac_failed"))

# ---------- Account settings app (admin-only) ----------

def open_accounts_app(parent):
    win = tk.Toplevel(parent)
    win.title(T("accounts_title"))
    win.geometry("500x380")
    win.configure(bg="#dcdcdc")

    left = tk.Frame(win, bg="#dcdcdc")
    left.pack(side="left", fill="y", padx=10, pady=10)

    right = tk.Frame(win, bg="#dcdcdc")
    right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    tk.Label(left, text=T("accounts_users"), bg="#dcdcdc").pack(anchor="w")
    user_list = tk.Listbox(left, height=15)
    user_list.pack(fill="y", expand=True)

    def refresh_users():
        user_list.delete(0, "end")
        load_accounts()
        for u, info in ACCOUNTS.items():
            tag = " (admin)" if info.get("admin") else ""
            user_list.insert("end", u + tag)

    refresh_users()

    def get_selected_user():
        if not user_list.curselection():
            messagebox.showwarning(T("accounts_title"), T("accounts_no_selection"))
            return None
        text = user_list.get(user_list.curselection())
        if " (admin)" in text:
            return text.replace(" (admin)", "")
        return text

    def create_user():
        username = simpledialog.askstring(T("accounts_title"), T("accounts_new_username"), parent=win)
        if not username:
            return
        username = username.strip()
        if not username:
            return
        load_accounts()
        if username in ACCOUNTS:
            messagebox.showerror(T("accounts_title"), T("accounts_user_exists"))
            return
        pin = simpledialog.askstring(T("accounts_title"), T("accounts_new_pin"), show="*", parent=win)
        is_adm = messagebox.askyesno(T("accounts_title"), T("accounts_is_admin"))
        ACCOUNTS[username] = {
            "pin": pin or "",
            "admin": bool(is_adm),
            "language": CURRENT_LANG,
        }
        save_accounts()
        refresh_users()

    def delete_user():
        user = get_selected_user()
        if not user:
            return
        if user == CURRENT_USER:
            messagebox.showerror(T("accounts_title"), T("accounts_cannot_delete_self"))
            return
        if not messagebox.askyesno(T("accounts_title"), T("accounts_confirm_delete").format(user=user)):
            return
        load_accounts()
        if user in ACCOUNTS:
            del ACCOUNTS[user]
            save_accounts()
        refresh_users()

    def change_pin():
        user = get_selected_user()
        if not user:
            return
        pin = simpledialog.askstring(T("accounts_title"), T("accounts_new_pin"), show="*", parent=win)
        if pin is None:
            return
        load_accounts()
        if user in ACCOUNTS:
            ACCOUNTS[user]["pin"] = pin
            save_accounts()
        refresh_users()

    def toggle_admin():
        user = get_selected_user()
        if not user:
            return
        load_accounts()
        if user not in ACCOUNTS:
            return
        if ACCOUNTS[user].get("admin") and sum(1 for u in ACCOUNTS.values() if u.get("admin")) == 1:
            messagebox.showerror(T("accounts_title"), T("accounts_cannot_demote_last_admin"))
            return
        ACCOUNTS[user]["admin"] = not ACCOUNTS[user].get("admin")
        save_accounts()
        refresh_users()

    def ban_selected_user():
        user = get_selected_user()
        if not user:
            return
        if user == CURRENT_USER:
            messagebox.showerror(T("accounts_title"), T("accounts_cannot_delete_self"))
            return
        reason = simpledialog.askstring(T("accounts_title"), T("accounts_ban_reason"), parent=win)
        if reason is None:
            return
        ban_user(user, reason)
        refresh_users()

    tk.Button(right, text=T("accounts_create"), command=create_user).pack(fill="x", pady=5)
    tk.Button(right, text=T("accounts_delete"), command=delete_user).pack(fill="x", pady=5)
    tk.Button(right, text=T("accounts_change_pin"), command=change_pin).pack(fill="x", pady=5)
    tk.Button(right, text=T("accounts_toggle_admin"), command=toggle_admin).pack(fill="x", pady=5)
    tk.Button(right, text=T("accounts_ban_user"), command=ban_selected_user).pack(fill="x", pady=5)

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
        self.make_icon(frame, T("menu_accounts"), self.open_accounts, 4)

    def make_icon(self, parent, text, command, row):
        tk.Button(parent, text=text, width=14, height=2, command=command).grid(row=row, pady=10)

    def open_main_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label=T("menu_browser"), command=self.open_browser)
        menu.add_command(label=T("menu_home"), command=self.open_home)
        menu.add_command(label=T("menu_terminal"), command=self.open_terminal)
        menu.add_command(label=T("menu_antivirus"), command=self.open_antivirus)
        menu.add_command(label=T("menu_accounts"), command=self.open_accounts)
        menu.add_separator()
        menu.add_command(label=T("menu_about"), command=self.show_about)
        menu.add_separator()
        menu.add_command(label=T("menu_logout"), command=self.logout)
        menu.add_command(label=T("menu_shutdown"), command=self.shutdown)
        menu.tk_popup(self.winfo_rootx() + 10, self.winfo_rooty() + 10)

    def open_browser(self):
        open_browser_app(self)

    def open_home(self):
        open_home_app(self)

    def open_terminal(self):
        open_terminal_app(self, self.shell)

    def open_antivirus(self):
        require_admin(self, lambda: open_antivirus_app(self))

    def open_accounts(self):
        require_admin(self, lambda: open_accounts_app(self))

    def show_about(self):
        messagebox.showinfo(
            T("menu_about"),
            f"{T('about_text')}\nUsuario: {CURRENT_USER}\nIdioma: {CURRENT_LANG}\nAdmin: {is_admin(CURRENT_USER)}"
        )

    def logout(self):
        self.destroy()
        show_login()

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

def show_login():
    load_accounts()
    load_bans()
    global CURRENT_LANG
    if ACCOUNTS:
        first_user = next(iter(ACCOUNTS.keys()))
        CURRENT_LANG = get_user_language(first_user)
    LoginScreen().mainloop()

def show_tos():
    TOSScreen().mainloop()

# ---------- Main ----------

if __name__ == "__main__":
    load_accounts()
    load_bans()
    if ACCOUNTS_FILE.exists() and ACCOUNTS:
        show_login()
    else:
        show_setup()
