import tkinter as tk
from tkinter import filedialog

class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        
        self.title("cooltextedit")
        self.geometry('800x600')
        
        self.text_area = tk.Text(self)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Открыть файл...", command=self.open_file)
        file_menu.add_command(label="Сохранить файл...", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        self.config(menu=menu_bar)
    
    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if not filename:
            return
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, content)
    
    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if not filename:
            return
        text_to_save = self.text_area.get('1.0', tk.END).strip() + '\n'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_to_save)

if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()