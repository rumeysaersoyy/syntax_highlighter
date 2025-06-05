import tkinter as tk
import tkinter.messagebox as messagebox
from lexer import tokenize
from parser import Parser

HIGHLIGHT_COLORS = {
    'KEYWORD': 'blue',
    'IDENTIFIER': 'black',
    'NUMBER': 'orange',
    'STRING': 'green',
    'BOOL': 'purple',
    'OPERATOR': 'red',
    'DELIMITER': 'brown',
    'COMMENT': 'gray'
}

class SyntaxHighlighter:
    def __init__(self, root):
        self.root = root
        self.text = tk.Text(root, font=("Consolas", 12), wrap="word")
        self.text.pack(expand=True, fill='both')
        self.text.bind('<KeyRelease>', self.on_key_release)

        for token_type, color in HIGHLIGHT_COLORS.items():
            self.text.tag_config(token_type, foreground=color)

        # Alt kısımdaki hata mesajı label'ı artık boş, gösterim yok
        self.error_label = tk.Label(root, text="", fg="red", anchor="w", justify="left")
        self.error_label.pack(fill='x')

        # Hata Ayıkla butonu
        self.error_button = tk.Button(root, text="Hata Ayıkla", command=self.show_error)
        self.error_button.pack(fill='x')

        self.last_error = ""  # Son hata mesajını tutmak için

        self._after_id = None  # debounce için

    def on_key_release(self, event=None):
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(300, self.process_code)

    def process_code(self):
        code = self.text.get("1.0", tk.END)
        try:
            tokens = tokenize(code)
        except Exception as e:
            self.last_error = f"Lexer hatası: {str(e)}"
            self.clear_highlighting()
            return

        self.highlight_code(tokens)

        try:
            parser = Parser(tokens)
            parser.parse_program()
            self.last_error = ""  # Hata yok
        except Exception as e:
            self.last_error = f"Parser hatası: {str(e)}"

    def clear_highlighting(self):
        for tag in HIGHLIGHT_COLORS:
            self.text.tag_remove(tag, "1.0", tk.END)

    def highlight_code(self, tokens):
        self.clear_highlighting()
        idx = 0
        for token_type, token_value, line, col in tokens:
            if token_type in ('WHITESPACE', 'NEWLINE', 'INDENT', 'DEDENT', 'EOF'):
                continue
            start = f"1.0 + {idx} chars"
            end = f"1.0 + {idx + len(token_value)} chars"
            if token_type in HIGHLIGHT_COLORS:
                self.text.tag_add(token_type, start, end)
            idx += len(token_value)

    def show_error(self):
        if self.last_error:
            messagebox.showerror("Hata Mesajı", self.last_error)
        else:
            messagebox.showinfo("Hata Mesajı", "Hata yok.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Real-Time Grammar-Based Syntax Highlighter")
    app = SyntaxHighlighter(root)
    root.mainloop()
