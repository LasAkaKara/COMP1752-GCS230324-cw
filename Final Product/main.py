from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
import csv
from frames import ScrollableFrame, TopBar
from movies_details import PlaylistManager, Movie, MovieDetails
from get_info import Info
from login import Login
import fonts

import os

class MainApp:
    def __init__(self, window, movies, playlist_manager, user_file_path):
        self.window = window
        self.window.title("Movie Player App")
        self.window.geometry("1536x864")

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        fonts.configure()
        
        self.playlist_manager = playlist_manager
        self.current_playlist = None
        self.star_outlined_img = ImageTk.PhotoImage(Image.open("images/star_outlined.png"), width=20, height=20)
        self.star_filled_img = ImageTk.PhotoImage(Image.open("images/star_filled.png"), width=20, height=20)
        self.add_img = ImageTk.PhotoImage(Image.open("images/add_img.png"), width=20, height=20)
        self.info_img = ImageTk.PhotoImage(Image.open("images/info_img.png"), width=20, height=20)
        self.rate_img = ImageTk.PhotoImage(Image.open("images/rate_img.png"), width=20, height=20)
        self.remove_img = ImageTk.PhotoImage(Image.open("images/remove_img.png"), width=20, height=20)
        
        self.top_bar = TopBar(
            self.main_frame,
            button1_callback=self.return_clicked, 
            button2_callback=self.search_clicked,
            add_movie_callback=self.open_add_movie_window,
        )
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        
        self.videolist_frame = ScrollableFrame(self.main_frame)
        self.videolist_frame.grid(row=1, column=0, sticky="nsew")
        self.videolist_frame.configure(bg="darkslategray")

        self.right_frame = tk.Frame(self.main_frame, background="white")
        self.right_frame.grid(row=1, column=1, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=2)
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.watch_frame = tk.Frame(self.right_frame, bg="gray19", bd=5, highlightthickness=15, highlightbackground="darkgoldenrod3", relief=tk.SUNKEN)
        self.watch_frame.grid(row=0, column=0, sticky="nsew")
        self.watch_frame.update()
        
        self.play_button = tk.Button(
            self.watch_frame,
            text="Play",
            command=self.play_top_movie,
            bg="salmon4", fg="wheat1", activebackground="salmon3", activeforeground="wheat1"
        )
        self.play_button.pack(side=tk.BOTTOM, pady=10)

        self.current_movie_label = tk.Label(
            self.watch_frame,
            text="No movie playing",
            bg="gray19",
            fg="wheat1",
            font=("Georgia", 18)
        )
        self.current_movie_label.pack(side=tk.TOP, pady=10)
        
        self.playlist_btn_frame = tk.Frame(self.right_frame, height=65, bd=0, relief=tk.SUNKEN, bg="darkslategray")
        self.playlist_btn_frame.grid(row=1, column=0, sticky="nsew")
        
        self.clear_btn = tk.Button(self.playlist_btn_frame, text="CLEAR", font=("Futura", 15, "bold"), bg="salmon4", fg="wheat1", command=self.clear_current_playlist, anchor="w", activebackground="salmon3", activeforeground="wheat1")
        self.clear_btn.grid(row=0, column=0, pady=10, padx=10, sticky = "news")
        
        self.playlist_combobox = ttk.Combobox(
            self.playlist_btn_frame,
            values=self.playlist_manager.get_all_playlists(),
            state="readonly"
        )
        self.playlist_combobox.grid(row=0, column=1, pady=10, padx=60, sticky = "W")
        self.playlist_combobox.bind("<<ComboboxSelected>>", self.load_playlist)
        
        self.new_playlist_button = tk.Button(
            self.playlist_btn_frame,
            image=self.add_img,
            command=self.create_new_playlist,
            bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4"
        )
        
        self.new_playlist_button.grid(row=0, column=2, pady=10, padx=10, sticky = "e")
        
        self.playlist_frame = ScrollableFrame(self.right_frame)
        self.playlist_frame.grid(row=2, column=0, sticky="nsew")
        
        self.main_frame.update()
        self.movies = movies
        self.display_movies(self.movies)

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        Login(tk.Toplevel(self.window), user_file_path)
        

        

    def display_movies(self, movies):
        for widget in self.videolist_frame.scrollable_frame.winfo_children():
            widget.destroy()
        
        for i, movie in enumerate(movies):
            self.add_movie_frame(movie, i)
        self.videolist_frame.refresh()
    
    def add_movie_frame(self, movie, row):
        #toto: fix shrinking of frames
        movie_frame = tk.Frame(self.videolist_frame.scrollable_frame, width=800, height=125, bd=1, relief=tk.RAISED, padx=10, pady=3, bg="darkseagreen")
        movie_frame.grid_propagate(False)
        movie_frame.grid(sticky="n")
        movie_frame.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(movie_frame, text=f"{movie.name}", font=("Georgia", 30, "bold"),bg="darkseagreen", fg="sienna4")
        title_label.grid(row=0, column=0, sticky="w")

        rate_btn = tk.Button(movie_frame, image=self.rate_img,bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", command=lambda:self.rate_movie(movie))
        rate_btn.grid(row=0, column=1, sticky="e",pady =5, padx=5)
        
        info_btn = tk.Button(movie_frame, image=self.info_img,bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", command=lambda:self.get_info(movie))
        info_btn.grid(row=0, column=2, sticky="e",pady =5, padx=5)

        info_label = tk.Label(movie_frame, text=f"    {movie.year}\t         {movie.length}\t         {movie.director}", font=("Georgia", 15, "italic"),bg="darkseagreen", fg='wheat2')
        info_label.grid(row=1, column=0, sticky="w", padx=5)
        
        add_btn = tk.Button(movie_frame, image=self.add_img,bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", command=lambda:self.add_to_playlist(movie))
        add_btn.grid(row=1, column=2, sticky="e",pady=5, padx=5)

        self.videolist_frame.add_widget(movie_frame, row)

    def get_info(self, movie):
        Info(tk.Toplevel, movie)
        
    def add_to_playlist(self, movie):
        try:
            if movie not in self.current_playlist.get_movies():
                self.current_playlist.add_movie(movie)
                self.display_playlist_movies()
                self.playlist_frame.refresh()
            else:
                tk.messagebox.showerror(message="This movie is already in the playlist!")
        except:
            tk.messagebox.showerror(message="Please choose a playlist first!")
    
    def load_playlist(self, event):
        """Load the selected playlist and display its movies."""
        playlist_name = self.playlist_combobox.get()
        self.current_playlist = self.playlist_manager.get_playlist(playlist_name)
        self.display_playlist_movies()

    def create_new_playlist(self):
        """Create a new playlist and add it to the selection combobox."""
        new_playlist_name = tk.simpledialog.askstring("New Playlist", "Enter the name of the new playlist:")
        if new_playlist_name:
            self.playlist_manager.create_playlist(new_playlist_name)
            self.playlist_combobox['values'] = self.playlist_manager.get_all_playlists()
            self.playlist_combobox.set(new_playlist_name)
            self.load_playlist(None)

    def display_playlist_movies(self):
        """Display the movies in the current playlist."""
        for widget in self.playlist_frame.scrollable_frame.winfo_children():
            widget.destroy()

        if self.current_playlist:
            for i, movie in enumerate(self.current_playlist.movies):
                self.add_playlist_item(movie, i)

    def clear_current_playlist(self):
        self.current_playlist.clear_playlist()
        self.display_playlist_movies()

    def add_playlist_item(self, item, row):
        item_frame = tk.Frame(self.playlist_frame.scrollable_frame, width=700, height=70 , bd=2, relief=tk.RAISED, padx=10, pady=10, bg="darkseagreen")
        item_frame.grid_propagate(False)
        item_frame.grid(sticky="n")
        item_frame.grid_columnconfigure(0, weight=1)

        item_label = tk.Label(item_frame, text=f"{item.name}", font=("Georgia", 18, "bold"),bg="darkseagreen", fg="sienna4")
        item_label.grid(row=0, column=0, sticky="news")

        remove_btn = tk.Button(item_frame, image=self.remove_img, bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", command = lambda: self.remove_movie(item))
        remove_btn.grid(row=0, column=1, sticky="e")
        
        self.playlist_frame.add_widget(item_frame, row+1)

    def remove_movie(self, movie):
        self.current_playlist.remove_movie(movie)
        self.display_playlist_movies()
        
    def return_clicked(self):
        self.display_movies(self.movies)

    def search_clicked(self, keyword, type):
        if keyword == "Search movies..." or keyword == "":
            tk.messagebox.showerror(message="Please insert keywords!")
        else:
            self.movieslist2=[]
            if type == "name":
                for movie in movies.get_movies():
                    if keyword in movie.name.lower().replace(" ",""):
                        self.movieslist2.append(movie)
            elif type == "genre":
                for movie in movies.get_movies():
                    if keyword in movie.genre.lower().replace(" ",""):
                        self.movieslist2.append(movie)
            elif type == "director":
                for movie in movies.get_movies():
                    if keyword in movie.director.lower().replace(" ",""):
                        self.movieslist2.append(movie)
            self.display_movies(self.movieslist2)
            self.videolist_frame.refresh()

    def rate_movie(self, movie):
        rating_window = tk.Toplevel(self.window)
        rating_window.title(f"Rate {movie.name}")
        rating_window.geometry("300x250")
        rating_window.configure(bg="darkslategray")
        if movie.cal_rating() != 0:
            ratetext=f"Current Rating: {movie.cal_rating()} / 5"
        else:
            ratetext="This movie hasn't been rated!"
        current_rating_label = tk.Label(
            rating_window, 
            text=ratetext, 
            font=("Helvetica", 14), 
            bg="darkslategray", 
            fg="white"
        )
        current_rating_label.pack(pady=20)

        stars_frame = tk.Frame(rating_window, bg="darkslategray")
        stars_frame.pack()

        self.star_buttons = []
        self.new_rating = movie.cal_rating()
        for i in range(5):
            button = tk.Button(
                stars_frame, 
                bd=0, 
                highlightthickness=0,
                image=self.star_outlined_img, 
                bg="darkslategray", 
                activebackground="darkslategray", 
                command=lambda i=i: self.update_stars(i, self.star_filled_img, self.star_outlined_img)
            )
            button.grid(row=0, column=i, padx=5)
            self.star_buttons.append(button)

        self.update_stars(movie.cal_rating() - 1, self.star_filled_img, self.star_outlined_img)

        submit_button = tk.Button(
            rating_window, 
            text="Submit", 
            command=lambda: self.submit_rating(movie, rating_window), 
            bg="darkorange4", 
            fg="white"
        )
        submit_button.pack(pady=20)

    def update_stars(self, index, star_filled, star_outline):
        self.new_rating = index + 1
        for i, button in enumerate(self.star_buttons):
            if i <= index:
                button.config(image=star_filled)
            else:
                button.config(image=star_outline)

    def submit_rating(self, movie, rating_window):
        movie.add_rating(self.new_rating)
        tk.messagebox.showinfo("Rating Submitted", f"{movie.name} is now rated at {movie.cal_rating()}/5 stars!")
        rating_window.destroy()
        
    def on_entry_click(self, event, entry, default):
        if entry.get() == default:
            entry.delete(0, "end")
            entry.insert(0, '')
            entry.config(fg = 'black')
            
    def on_focusout(self, event, entry, default):
        if entry.get() == '':
            entry.insert(0, default)
            entry.config(fg = 'grey')

    def open_add_movie_window(self):
        #todo: make better looking GUI
        add_movie_window = tk.Toplevel(self.window)
        add_movie_window.title("Add New Movie")
        add_movie_window.geometry("400x500")
        add_movie_window.configure(bg="darkslategray")
        add_movie_window.focus()
        add_movie_window.grab_set()
        
        title_label = tk.Label(add_movie_window, text=f"ADD A NEW VIDEO", font=("Georgia", 20, "bold"),bg="darkslategray", fg="wheat1")
        title_label.pack(pady=25)
        
        movie_name_entry = tk.Entry(add_movie_window, width=20)
        movie_name_entry.insert(0, "movie name")
        movie_name_entry.config(fg="gray")
        movie_name_entry.bind('<FocusIn>', lambda event : self.on_entry_click(event, movie_name_entry, "movie name"))
        movie_name_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, movie_name_entry, "movie name"))
        movie_name_entry.pack(pady=15)

        movie_year_entry = tk.Entry(add_movie_window, width=20)
        movie_year_entry.insert(0, "release year")
        movie_year_entry.config(fg="gray")
        movie_year_entry.bind('<FocusIn>', lambda event : self.on_entry_click(event, movie_year_entry, "release year"))
        movie_year_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, movie_year_entry, "release year"))
        movie_year_entry.pack(pady=15)

        movie_director_entry = tk.Entry(add_movie_window, width=20)
        movie_director_entry.insert(0, "directed by")
        movie_director_entry.config(fg="gray")
        movie_director_entry.bind('<FocusIn>', lambda event : self.on_entry_click(event, movie_director_entry, "directed by"))
        movie_director_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, movie_director_entry, "directed by"))
        movie_director_entry.pack(pady=15)



        movie_length_entry = tk.Entry(add_movie_window, width=20)
        movie_length_entry.insert(0, "movie length (in minutes)")
        movie_length_entry.config(fg="gray")
        movie_length_entry.bind('<FocusIn>', lambda event : self.on_entry_click(event, movie_length_entry, "movie length (in minutes)"))
        movie_length_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, movie_length_entry, "movie length (in minutes)"))
        movie_length_entry.pack(pady=15)
        
        genre_combobox = ttk.Combobox(add_movie_window, state="readonly", values=["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-fi"], width=18)
        genre_combobox.set("select genre")
        genre_combobox.pack(pady=15)
               
        add_button = tk.Button(add_movie_window, text="ADD", font=("Helvetica", 18, "bold"), command=lambda: self.add_new_movie(movie_name_entry.get(), movie_director_entry.get(), movie_year_entry.get(),  movie_length_entry.get(), genre_combobox.get(),  add_movie_window), bd=2, highlightthickness=3, relief="raised", highlightbackground="brown4",bg="lightsalmon4", highlightcolor="brown4",activebackground="sienna4", fg="wheat1")
        add_button.pack(pady=20)

    def add_new_movie(self, name, director,  year, length,genre,  window):
        addable = True
        if not year.isdigit() or 1600>int(year) or 2050<int(year):
            tk.messagebox.showerror(message="Please enter a valid year!")
            addable = False
        if not length.isdigit():
            tk.messagebox.showerror(message="Please enter a number for movie length!")
            addable = False
        for movie in self.movies:
            if name.lower() == movie.get_name().lower():
                tk.messagebox.showerror(message="This movie is already in the list")
                addable = False
                break
        
        if addable == True:
            new_movie = Movie(name, director, year, length, genre)
            self.movies.append(new_movie)
            self.display_movies(self.movies)

            with open('movie_list.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name,director,year,length,genre])

            window.destroy()
            messagebox.showinfo("Success", "Movie added successfully!")

    def play_top_movie(self):
        """Play the top movie in the current playlist queue."""
        if self.current_playlist and self.current_playlist.movies:
            top_movie = self.current_playlist.movies[0]
            top_movie.increment_play_count()
            self.current_movie_label.config(text=f"Playing: {top_movie.name}")
            tk.messagebox.showinfo(message=f"{top_movie.name} play count: {top_movie.play_count}")
            self.current_playlist.movies.pop(0)
            self.display_playlist_movies() 

        else:
            self.current_movie_label.config(text="No movie playing")
            tk.messagebox.showerror(message="There is no movie in the playlist")
            
if __name__ == "__main__":
    movies_file_path='csv/movie_list.csv'
    movies = MovieDetails(movies_file_path)
    movieslist = movies.get_movies()

    playlist_manager = PlaylistManager()

    user_file_path = 'csv/users.csv'
    window = tk.Tk()
    app = MainApp(window, movieslist, playlist_manager, user_file_path)
    
    window.mainloop()