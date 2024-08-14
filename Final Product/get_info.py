import tkinter as tk
from tkinter import font as tkfont
from movies_details import Movie
        
class Info:
    def __init__(self, window, movie):
        self.movie = movie

        self.window = tk.Toplevel()
        self.window.title(f"{self.movie.name} - Details")
        self.window.geometry("400x400")
        self.window.configure(bg="darkslategray")

        self.title_font = tkfont.Font(family="Georgia", size=18, weight="bold")
        self.info_font = tkfont.Font(family="Georgia", size=14)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)

        self.display_movie_info()
        self.window.focus()
        self.window.grab_set()


    def display_movie_info(self):
        title_label = tk.Label(
            self.window,
            text=f"Title: {self.movie.name}",
            font=self.title_font,
            fg="white",
            bg="darkslategray"
        )
        title_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        year_label = tk.Label(
            self.window,
            text=f"Year: {self.movie.year}",
            font=self.info_font,
            fg="lightgray",
            bg="darkslategray"
        )
        year_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        director_label = tk.Label(
            self.window,
            text=f"Director: {self.movie.director}",
            font=self.info_font,
            fg="lightgray",
            bg="darkslategray"
        )
        director_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        rating_label = tk.Label(
            self.window,
            text=f"Rating: {self.movie.cal_rating()}",
            font=self.info_font,
            fg="lightgray",
            bg="darkslategray"
        )
        rating_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        length_label = tk.Label(
            self.window,
            text=f"Length: {self.movie.length} mins",
            font=self.info_font,
            fg="lightgray",
            bg="darkslategray"
        )
        length_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")
