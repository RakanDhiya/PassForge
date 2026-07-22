import os

import customtkinter as ctk

from modules.generator import generate_password
from modules.entropy import calculate_entropy
from modules.strength import get_strength_label
from modules.clipboard import copy_to_clipboard
from modules.checker import check_password_strength
from ui.theme import FONTS


class PassForgeApp:

    def __init__(self):
        # Tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window
        self.root = ctk.CTk()
        self.root.title("PassForge")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.set_window_icon()

        # State opsi (checkbox) - tab Generate
        self.var_upper = ctk.BooleanVar(value=True)
        self.var_lower = ctk.BooleanVar(value=True)
        self.var_digits = ctk.BooleanVar(value=True)
        self.var_symbols = ctk.BooleanVar(value=True)
        self.var_exclude_ambiguous = ctk.BooleanVar(value=False)

        self.current_password = ""

        # Main Container
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        self.create_header()

        # Tabview: Generate & Check
        self.tabview = ctk.CTkTabview(self.main_frame, width=840, height=560)
        self.tabview.pack(fill="both", expand=True)

        self.tab_generate = self.tabview.add("Generate")
        self.tab_check = self.tabview.add("Check")

        self.build_generate_tab()
        self.build_check_tab()

        # Auto generate password pertama kali dibuka
        self.generate_password_action()

    # ICON

    def set_window_icon(self):
        """
        Pasang icon window dari assets/icon.ico (Windows) atau
        assets/logo.png (fallback, macOS/Linux) kalau filenya ada.
        Gak error kalau file gak ditemukan / gagal load.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(project_root, "assets", "icon.ico")
        logo_path = os.path.join(project_root, "assets", "logo.png")

        try:
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        try:
            if os.path.exists(logo_path):
                from PIL import Image, ImageTk
                img = Image.open(logo_path)
                photo = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, photo)
                self._icon_photo_ref = photo  # simpan referensi biar gak digarbage-collect
        except Exception:
            pass

    # HEADER

    def create_header(self):
        title = ctk.CTkLabel(
            self.main_frame,
            text="PASSFORGE",
            font=FONTS["title"]
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Secure Password Generator",
            font=FONTS["subtitle"]
        )
        subtitle.pack(pady=(0, 20))


    # TAB 1: GENERATE

    def build_generate_tab(self):
        self.create_password_display(self.tab_generate)
        self.create_length_section(self.tab_generate)
        self.create_options_section(self.tab_generate)
        self.create_strength_section(self.tab_generate)
        self.create_action_buttons(self.tab_generate)
        self.create_status_label(self.tab_generate)

    def create_password_display(self, parent):
        display_frame = ctk.CTkFrame(parent)
        display_frame.pack(fill="x", pady=(10, 20))

        self.password_entry = ctk.CTkEntry(
            display_frame,
            font=FONTS["password"],
            justify="center",
            height=50
        )
        self.password_entry.pack(fill="x", padx=15, pady=15)

    def create_length_section(self, parent):
        label = ctk.CTkLabel(
            parent,
            text="Password Length",
            font=FONTS["section"]
        )
        label.pack(anchor="w")

        self.length_value = ctk.CTkLabel(
            parent,
            text="16 Characters",
            font=FONTS["body"]
        )
        self.length_value.pack(anchor="w", pady=(5, 10))

        self.slider = ctk.CTkSlider(
            parent,
            from_=4,
            to=64,
            number_of_steps=60,
            command=self.update_slider
        )
        self.slider.set(16)
        self.slider.pack(fill="x")

    def update_slider(self, value):
        self.length_value.configure(
            text=f"{int(value)} Characters"
        )
        self.generate_password_action()

    def create_options_section(self, parent):
        label = ctk.CTkLabel(
            parent,
            text="Character Options",
            font=FONTS["section"]
        )
        label.pack(anchor="w", pady=(25, 10))

        options_frame = ctk.CTkFrame(parent, fg_color="transparent")
        options_frame.pack(fill="x")

        checkboxes = [
            ("Uppercase (A-Z)", self.var_upper),
            ("Lowercase (a-z)", self.var_lower),
            ("Digits (0-9)", self.var_digits),
            ("Symbols (!@#$...)", self.var_symbols),
            ("Exclude Ambiguous (Il1O0)", self.var_exclude_ambiguous),
        ]

        for i, (text, var) in enumerate(checkboxes):
            col = i % 2
            row = i // 2
            cb = ctk.CTkCheckBox(
                options_frame,
                text=text,
                variable=var,
                font=FONTS["body"],
                command=self.generate_password_action
            )
            cb.grid(row=row, column=col, sticky="w", padx=(0, 40), pady=6)

    def create_strength_section(self, parent):
        label = ctk.CTkLabel(
            parent,
            text="Password Strength",
            font=FONTS["section"]
        )
        label.pack(anchor="w", pady=(25, 10))

        info_frame = ctk.CTkFrame(parent, fg_color="transparent")
        info_frame.pack(fill="x")

        self.strength_label = ctk.CTkLabel(
            info_frame,
            text="-",
            font=FONTS["body"]
        )
        self.strength_label.pack(side="left")

        self.entropy_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=FONTS["body"],
            text_color="#9e9e9e"
        )
        self.entropy_label.pack(side="right")

        self.strength_bar = ctk.CTkProgressBar(parent, height=14)
        self.strength_bar.pack(fill="x", pady=(8, 0))
        self.strength_bar.set(0)

    def create_action_buttons(self, parent):
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(25, 0))

        generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate Password",
            font=FONTS["button"],
            height=45,
            command=self.generate_password_action
        )
        generate_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        copy_btn = ctk.CTkButton(
            button_frame,
            text="Copy to Clipboard",
            font=FONTS["button"],
            height=45,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.copy_password_action
        )
        copy_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))

    def create_status_label(self, parent):
        self.status_label = ctk.CTkLabel(
            parent,
            text="",
            font=FONTS["body"],
            text_color="#2ecc71"
        )
        self.status_label.pack(pady=(15, 0))

    # LOGIKA - GENERATE

    def generate_password_action(self):
        length = int(self.slider.get())

        try:
            password = generate_password(
                length=length,
                use_upper=self.var_upper.get(),
                use_lower=self.var_lower.get(),
                use_digits=self.var_digits.get(),
                use_symbols=self.var_symbols.get(),
                exclude_ambiguous=self.var_exclude_ambiguous.get(),
            )
        except ValueError as e:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, "")
            self.status_label.configure(text=str(e), text_color="#e74c3c")
            self.strength_label.configure(text="-")
            self.entropy_label.configure(text="")
            self.strength_bar.set(0)
            return

        self.current_password = password

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

        self.status_label.configure(text="")
        self.update_strength_display(password)

    def update_strength_display(self, password: str):
        charset_size = 0
        if self.var_upper.get():
            charset_size += 26
        if self.var_lower.get():
            charset_size += 26
        if self.var_digits.get():
            charset_size += 10
        if self.var_symbols.get():
            charset_size += 27

        entropy_bits = calculate_entropy(len(password), max(charset_size, 1))
        strength = get_strength_label(entropy_bits)

        self.strength_label.configure(
            text=strength["label"],
            text_color=strength["color"]
        )
        self.entropy_label.configure(text=f"{entropy_bits:.1f} bits entropy")

        self.strength_bar.configure(progress_color=strength["color"])
        self.strength_bar.set(strength["progress"])

    def copy_password_action(self):
        success = copy_to_clipboard(self.current_password)

        if success:
            self.status_label.configure(
                text="Password copied to clipboard!",
                text_color="#2ecc71"
            )
        else:
            self.status_label.configure(
                text="Gagal copy (pastikan pyperclip terpasang dgn benar).",
                text_color="#e74c3c"
            )

    # TAB 2: CHECK (Password Strength Checker)

    def build_check_tab(self):
        label = ctk.CTkLabel(
            self.tab_check,
            text="Check Your Password",
            font=FONTS["section"]
        )
        label.pack(anchor="w", pady=(10, 10))

        input_frame = ctk.CTkFrame(self.tab_check, fg_color="transparent")
        input_frame.pack(fill="x")

        self.check_entry = ctk.CTkEntry(
            input_frame,
            font=FONTS["body"],
            placeholder_text="Ketik atau paste password di sini...",
            height=45,
            show="*"
        )
        self.check_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.check_entry.bind("<KeyRelease>", lambda e: self.check_password_action())

        self.var_show_check = ctk.BooleanVar(value=False)
        show_toggle = ctk.CTkCheckBox(
            input_frame,
            text="Show",
            variable=self.var_show_check,
            font=FONTS["body"],
            command=self.toggle_check_visibility
        )
        show_toggle.pack(side="left")

        # Strength result
        result_label = ctk.CTkLabel(
            self.tab_check,
            text="Result",
            font=FONTS["section"]
        )
        result_label.pack(anchor="w", pady=(25, 10))

        info_frame = ctk.CTkFrame(self.tab_check, fg_color="transparent")
        info_frame.pack(fill="x")

        self.check_strength_label = ctk.CTkLabel(
            info_frame,
            text="-",
            font=FONTS["body"]
        )
        self.check_strength_label.pack(side="left")

        self.check_entropy_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=FONTS["body"],
            text_color="#9e9e9e"
        )
        self.check_entropy_label.pack(side="right")

        self.check_bar = ctk.CTkProgressBar(self.tab_check, height=14)
        self.check_bar.pack(fill="x", pady=(8, 15))
        self.check_bar.set(0)

        self.check_crack_time_label = ctk.CTkLabel(
            self.tab_check,
            text="Estimasi waktu jebol: -",
            font=FONTS["body"],
            anchor="w",
            justify="left"
        )
        self.check_crack_time_label.pack(anchor="w", pady=(0, 10))

        self.check_feedback_label = ctk.CTkLabel(
            self.tab_check,
            text="",
            font=FONTS["body"],
            text_color="#9e9e9e",
            anchor="w",
            justify="left",
            wraplength=780
        )
        self.check_feedback_label.pack(anchor="w")

    def toggle_check_visibility(self):
        self.check_entry.configure(show="" if self.var_show_check.get() else "*")

    def check_password_action(self):
        password = self.check_entry.get()
        result = check_password_strength(password)

        self.check_strength_label.configure(
            text=result["label"],
            text_color=result["color"]
        )

        if password:
            self.check_entropy_label.configure(
                text=f"{result['entropy_bits']:.1f} bits entropy"
            )
            self.check_crack_time_label.configure(
                text=f"Estimasi waktu jebol (offline attack): {result['crack_time']}"
            )
        else:
            self.check_entropy_label.configure(text="")
            self.check_crack_time_label.configure(text="Estimasi waktu jebol: -")

        self.check_bar.configure(progress_color=result["color"])
        self.check_bar.set(result["progress"])

        feedback_parts = []
        if result["warning"]:
            feedback_parts.append(f"⚠ {result['warning']}")
        if result["suggestions"]:
            feedback_parts.extend(f"• {s}" for s in result["suggestions"])

        self.check_feedback_label.configure(text="\n".join(feedback_parts))

    def run(self):
        self.root.mainloop()
