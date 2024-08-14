import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image

class TopBar(tk.Frame):
    def __init__(self, parent, button1_callback, button2_callback, add_movie_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="darkslategray")
        self.grid(columnspan=2)
        #self.configure(height=40)
        
        self.category = ttk.Combobox(self, state="readonly", width=7)
        self.category["values"] = ["name", "director", "genre"]
        self.category.current("0")
        self.category.pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(self, width=49)
        self.search_entry.insert(0, "Search movies...")
        self.search_entry.config(fg="gray")
        self.search_entry.bind('<FocusIn>', lambda event : self.on_entry_click(event, self.search_entry, "Search movies..."))
        self.search_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, self.search_entry, "Search movies..."))
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=10)

        self.search_img = ImageTk.PhotoImage(Image.open("images/search_img.png"), width=20, height=20)
        self.search_btn = tk.Button(self, image=self.search_img,bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", command=lambda: button2_callback(self.search_entry.get(), self.category.get()))
        self.search_btn.pack(side=tk.LEFT, padx=10,pady=5)
        
        self.return_img = ImageTk.PhotoImage(Image.open("images/return_img.png"), width=20, height=20)
        self.return_btn = tk.Button(self, image=self.return_img,bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", command=button1_callback)
        self.return_btn.pack(side=tk.LEFT, padx=0, pady=5)
        
        self.add_img = ImageTk.PhotoImage(Image.open("images/add_img.png"), width=20, height=20)
        self.add_movie_button = tk.Button(self, image=self.add_img,bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", command=add_movie_callback)
        self.add_movie_button.pack(side=tk.RIGHT, padx=10, pady=5, anchor="e")

    def on_entry_click(self, event, entry, default):
        if entry.get() == default:
            entry.delete(0, "end")
            entry.insert(0, '')
            entry.config(fg = 'black')
            
    def on_focusout(self, event, entry, default):
        if entry.get() == '':
            entry.insert(0, default)
            entry.config(fg = 'grey')

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, relief="ridge", bg="darkslategray")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.scrollable_frame = tk.Frame(self.canvas, bg="darkslategray", bd=0)
        self.scrollable_frame.grid(sticky="n")
        #self.grid_propagate(False)
        #self.update()
        #print(f"initial: {self.canvas.winfo_width()}")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="center")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    
    
    def _on_canvas_configure(self, event):
        """Adjust the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def add_widget(self, widget, row):
        """Method to add a widget to the scrollable frame."""
        widget.grid(row=row, column=0, sticky="n", padx=10, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        

    def refresh(self):
        self.update()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))