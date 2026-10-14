import tkinter as tk

def xor_logic(char, key_char):
    char_code = ord(char)
    key_code = ord(key_char)
    cipher_code = char_code ^ key_code
    return char_code, key_code, cipher_code, chr(cipher_code)

class XorAnimator:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация XOR Шифрования")
        self.root.geometry("750x700")  
        self.root.configure(bg="#1e1e1e")

        # Дефолтные значения
        self.message = "Hello, World!"
        self.secret_key = "CODE"
        
        # Динамические состояния
        self.current_text = self.message
        self.is_encrypting = True
        self.index = 0
        self.result_chars = list()       
        self.visual_positions = list()   
        
        # Флаги управления анимацией
        self.is_paused = True  
        self.after_id = None  

        # ШРИФТЫ
        self.title_font = ("Courier New", 18, "bold")
        self.mono_font = ("Courier New", 14, "bold")
        self.bit_font = ("Courier New", 22, "bold")
        self.hint_font = ("Courier New", 11, "italic")

        self.create_widgets()
        self.prepare_visual_text()
        
        # БИНДИНГ КЛАВИШ
        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("<r>", self.restart_animation)
        self.root.bind("<R>", self.restart_animation)
        self.root.bind("<KeyPress>", self.handle_global_key)

    def create_widgets(self):
        # Панель ввода данных
        self.input_frame = tk.Frame(self.root, bg="#252526", bd=1, relief="solid")
        self.input_frame.pack(pady=10, fill="x", padx=40)

        tk.Label(self.input_frame, text="Введите текст:", font=self.hint_font, fg="#ffffff", bg="#252526").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.ent_text = tk.Entry(self.input_frame, font=self.mono_font, bg="#3c3c3c", fg="#ffffff", insertbackground="white", width=25)
        self.ent_text.grid(row=0, column=1, padx=10, pady=5)
        self.ent_text.insert(0, self.message)

        tk.Label(self.input_frame, text="Введите ключ:", font=self.hint_font, fg="#ffffff", bg="#252526").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.ent_key = tk.Entry(self.input_frame, font=self.mono_font, bg="#3c3c3c", fg="#ffffff", insertbackground="white", width=25)
        self.ent_key.grid(row=1, column=1, padx=10, pady=5)
        self.ent_key.insert(0, self.secret_key)

        self.btn_start = tk.Button(self.input_frame, text="Запустить анимацию", font=("Courier New", 11, "bold"), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", command=self.apply_user_input)
        self.btn_start.grid(row=0, column=2, rowspan=2, padx=15, pady=5, sticky="ns")

        # Заголовок режима
        self.lbl_mode = tk.Label(self.root, text="ОЖИДАНИЕ СТАРТА", font=self.title_font, fg="#ffb74d", bg="#1e1e1e")
        self.lbl_mode.pack(pady=10)

        # Фрейм для строк текста и ключа
        self.txt_frame = tk.Frame(self.root, bg="#2d2d2d", bd=2, relief="groove")
        self.txt_frame.pack(pady=10, fill="x", padx=40)

        tk.Label(self.txt_frame, text="Текст: ", font=self.mono_font, fg="#aaaaaa", bg="#2d2d2d").grid(row=0, column=0, padx=(10, 0), pady=5, sticky="w")
        self.lbl_text_flow = tk.Label(self.txt_frame, text=self.message, font=self.mono_font, fg="#ffffff", bg="#2d2d2d")
        self.lbl_text_flow.grid(row=0, column=1, pady=5, sticky="w")

        self.lbl_pointer = tk.Label(self.txt_frame, text="▲", font=self.mono_font, fg="#ffffff", bg="#2d2d2d")
        self.lbl_pointer.grid(row=1, column=1, sticky="w")

        tk.Label(self.txt_frame, text="Ключ:  ", font=self.mono_font, fg="#aaaaaa", bg="#2d2d2d").grid(row=2, column=0, padx=(10, 0), pady=5, sticky="w")
        self.lbl_key_flow = tk.Label(self.txt_frame, text=self.secret_key, font=self.mono_font, fg="#ffb74d", bg="#2d2d2d")
        self.lbl_key_flow.grid(row=2, column=1, pady=5, sticky="w")

        # Основная зона анимации битов
        self.bit_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.bit_frame.pack(pady=20)

        tk.Label(self.bit_frame, text="Символ текста: ", font=self.mono_font, fg="#ffffff", bg="#1e1e1e").grid(row=0, column=0, sticky="e")
        self.lbl_char_bit = tk.Label(self.bit_frame, text="00000000", font=self.bit_font, fg="#81c784", bg="#1e1e1e")
        self.lbl_char_bit.grid(row=0, column=1, padx=10, sticky="w")

        tk.Label(self.bit_frame, text="Символ ключа:  ", font=self.mono_font, fg="#ffb74d", bg="#1e1e1e").grid(row=1, column=0, sticky="e")
        self.lbl_key_bit = tk.Label(self.bit_frame, text="00000000", font=self.bit_font, fg="#ffb74d", bg="#1e1e1e")
        self.lbl_key_bit.grid(row=1, column=1, padx=10, sticky="w")

        self.lbl_xor_line = tk.Label(self.bit_frame, text="^ (XOR) -----------------", font=self.mono_font, fg="#e0e0e0", bg="#1e1e1e")
        self.lbl_xor_line.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

        tk.Label(self.bit_frame, text="Итог (Символ):  ", font=self.mono_font, fg="#64b5f6", bg="#1e1e1e").grid(row=3, column=0, sticky="e")
        self.lbl_res_bit = tk.Label(self.bit_frame, text="00000000", font=self.bit_font, fg="#64b5f6", bg="#1e1e1e")
        self.lbl_res_bit.grid(row=3, column=1, padx=10, sticky="w")

        # Строка числового результата
        self.lbl_full_result = tk.Label(self.root, text="Текущий сбор (коды шифра): ", font=self.mono_font, fg="#e0e0e0", bg="#1e1e1e", wraplength=700)
        self.lbl_full_result.pack(pady=10)

        # Подсказка по горячим клавишам
        self.lbl_status = tk.Label(self.root, text="⌨️ [Пробел] — Пауза/Старт | [R] — Сбросить заново", font=self.hint_font, fg="#888888", bg="#1e1e1e")
        self.lbl_status.pack(side="bottom", pady=15)

    def apply_user_input(self):
        user_text = self.ent_text.get()
        user_key = self.ent_key.get()

        if not user_text:
            user_text = "Hello, World!"
        if not user_key:
            user_key = "CODE"

        self.message = user_text
        self.secret_key = user_key
        
        self.lbl_key_flow.config(text=self.secret_key)
        self.restart_animation()

    def prepare_visual_text(self):
        self.visual_positions = list()
        current_spaces = 0
        for char in self.current_text:
            self.visual_positions.append(current_spaces)
            current_spaces += 4 if not char.isprintable() else 1

    def cancel_timer(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def schedule_next_step(self, delay_ms):
        self.cancel_timer()
        self.after_id = self.root.after(delay_ms, self.animate_step)

    def handle_global_key(self, event):
        if event.char in ('к', 'К'):
            self.restart_animation()

    def animate_step(self):
        if self.is_paused:
            return

        if self.index < len(self.current_text):
            char = self.current_text[self.index]
            key_char = self.secret_key[self.index % len(self.secret_key)]

            char_code, key_code, cipher_code, cipher_char = xor_logic(char, key_char)
            self.result_chars.append(cipher_char)

            display_char = char if char.isprintable() else f"\\x{ord(char):02x}"

            self.lbl_char_bit.config(text=f"{char_code:08b} ('{display_char}')")
            self.lbl_key_bit.config(text=f"{key_code:08b} ('{key_char}')")
            self.lbl_res_bit.config(text=f"{cipher_code:08b}")

            indent = self.visual_positions[self.index]
            self.lbl_pointer.config(text=" " * indent + "▲")

            codes_str = " ".join([str(ord(c)) for c in self.result_chars])
            prefix_lbl = "Текущий сбор (коды шифра): " if self.is_encrypting else "Расшифровка (коды текста): "
            self.lbl_full_result.config(text=f"{prefix_lbl}[{codes_str}]")

            self.index += 1
            self.schedule_next_step(800)
        else:
            self.cancel_timer()
            self.switch_mode()

    def switch_mode(self):
        if self.is_encrypting:
            self.is_encrypting = False
            self.current_text = "".join(self.result_chars)
            self.result_chars = list() 
            self.index = 0
            
            self.lbl_mode.config(text="РЕЖИМ: РАСШИФРОВАНИЕ", fg="#2196F3")
            
            printable_text = "".join([c if c.isprintable() else f"\\x{ord(c):02x}" for c in self.current_text])
            self.lbl_text_flow.config(text=printable_text)
            
            self.prepare_visual_text()
            self.root.after(1000, self.animate_step)
        else:
            self.lbl_mode.config(text="ГОТОВО!", fg="#4CAF50")
            final_str = "".join(self.result_chars)
            self.lbl_full_result.config(text=f"Итоговый текст: {final_str}")
            self.lbl_pointer.config(text="")

    def toggle_pause(self, event=None):
        if "ГОТОВО!" in self.lbl_mode.cget("text") or "ОЖИДАНИЕ СТАРТА" in self.lbl_mode.cget("text"):
            return 
            
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.cancel_timer()
            current_mode = self.lbl_mode.cget("text").replace(" (ПАУЗА)", "")
            self.lbl_mode.config(text=f"{current_mode} (ПАУЗА)", fg="#e57373")
        else:
            color = "#4CAF50" if self.is_encrypting else "#2196F3"
            mode_text = "РЕЖИМ: ШИФРОВАНИЕ" if self.is_encrypting else "РЕЖИМ: РАСШИФРОВАНИЕ"
            self.lbl_mode.config(text=mode_text, fg=color)
            self.animate_step()

    def restart_animation(self, event=None):
        self.cancel_timer()
        
        self.current_text = self.message
        self.is_encrypting = True
        self.index = 0
        self.result_chars = list()       
        self.is_paused = False
        self.lbl_mode.config(text="РЕЖИМ: ШИФРОВАНИЕ", fg="#4CAF50")
        self.lbl_text_flow.config(text=self.message)
        self.lbl_pointer.config(text="▲")
        self.lbl_char_bit.config(text="00000000")
        self.lbl_key_bit.config(text="00000000")
        self.lbl_res_bit.config(text="00000000")
        self.lbl_full_result.config(text="Текущий сбор (коды шифра): ")
        self.prepare_visual_text()
        self.schedule_next_step(1000)

if __name__ == "__main__":
    root = tk.Tk()
    app = XorAnimator(root)
    root.mainloop()