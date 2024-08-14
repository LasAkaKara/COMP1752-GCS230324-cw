import tkinter as tk
import tkinter.scrolledtext as tkst
import video_library as lib
import font_manager as fonts

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)
    
class UpdateVideos:
    def __init__(self, window):
        window.geometry("850x350")
        window.title("Update Videos")

        list_videos_btn = tk.Button(window, text="List All Videos", command=self.list_videos_clicked)
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)

        enter_lbl = tk.Label(window, text="Enter Video Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)
        
        rating_lbl = tk.Label(window, text="Enter New Rating")
        rating_lbl.grid(row=0, column=3, padx=10, pady=10)

        self.ratinginput_txt = tk.Entry(window, width=3)
        self.ratinginput_txt.grid(row=0, column=4, padx=10, pady=10)

        update_video_btn = tk.Button(window, text="Add rating", command=self.add_rating_clicked)
        update_video_btn.grid(row=0, column=5, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.video_txt = tk.Text(window, width=36, height=4, wrap="none")
        self.video_txt.grid(row=1, column=3, columnspan=3, sticky="NW", padx=10, pady=10)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        self.list_videos_clicked()

    def list_videos_clicked(self):
        video_list = lib.list_all()
        set_text(self.list_txt, video_list)
        self.status_lbl.configure(text="List Videos button was clicked!")
        
    def add_rating_clicked(self):
        key = self.input_txt.get()
        rating = int(self.ratinginput_txt.get())
        if key=="":
            set_text(self.video_txt, f"Please fill out the missing fields")
        name = lib.get_name(key)
        if name is not None:
            if rating in range(1,6):
                lib.add_rating(key, rating)
                lib.get_rating(key)
                play_count = lib.get_play_count(key)
                details = f"UPDATED\n{name}\nrating:{rating}\nplays:{play_count}"
                set_text(self.video_txt, details)
            else:
                set_text(self.video_txt, f"Please enter a valid rating")
        else:
            set_text(self.video_txt, f"Video {key} not found")
            

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    UpdateVideos(window)     # open the CheckVideo GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc