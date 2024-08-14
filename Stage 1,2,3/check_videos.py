import tkinter as tk
import tkinter.scrolledtext as tkst


import video_library as lib
import font_manager as fonts


def set_text(text_area, content): #create a method to insert texts into an area
    text_area.delete("1.0", tk.END) #delete the previous texts
    text_area.insert(1.0, content) #insert the new texts


class CheckVideos(): #make the GUI functions for Checkvideos as a class for convinience
    def __init__(self, window): #initialize the GUI
        window.geometry("750x350") #set the app window dimensions
        window.title("Check Videos") #set the app window title

        list_videos_btn = tk.Button(window, text="List All Videos", command=self.list_videos_clicked) #create the "List Videos" button, link to its method when clicked
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10) #set the "List Videos" button position and paddings"

        enter_lbl = tk.Label(window, text="Enter Video Number") #create a textfield
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)#set the textfield position and paddings

        self.input_txt = tk.Entry(window, width=3) #create a textfield for input
        self.input_txt.grid(row=0, column=2, padx=10, pady=10) #adjust the input position and paddings

        check_video_btn = tk.Button(window, text="Check Video", command=self.check_video_clicked) #create the "Check Videos" button and link to its method when clicked
        check_video_btn.grid(row=0, column=3, padx=10, pady=10) #set the "Check Videos" button position and paddings"

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none") #create a scrollable textfield for the list of videos
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10) #set the textfield position, length, alignment, and paddings 

        self.video_txt = tk.Text(window, width=24, height=4, wrap="none") #create an output textfield for details of chosen video (default to none)
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10) #set the textfield position, alignment, and paddings

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10)) #set a text for the status updates of the window
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10) #set the text position, length, alignment, and paddings

        self.list_videos_clicked() #call the list videos clcked method to automatically display the video list upon opening

    def check_video_clicked(self): #create a method for when the check video button is clicked
        key = self.input_txt.get() #get the id of the inputted video
        name = lib.get_name(key) #get the name of the desired video by using the class LibraryItem
        if name is not None: #if the video exists in database
            director = lib.get_director(key) #get the director of the video with LibraryItem's method
            rating = lib.get_rating(key) #get the rating of the video with LibraryItem's method
            play_count = lib.get_play_count(key) #get the play count of the video with LibraryItem's method
            video_details = f"{name}\n{director}\nrating: {rating}\nplays: {play_count}" #set the output text for the video details
            set_text(self.video_txt, video_details) #display the  video details text in the output textfield
        else: #if the video doesnt exist in the database
            set_text(self.video_txt, f"Video {key} not found") #display the error in the output field
        self.status_lbl.configure(text="Check Video button was clicked!") #update the status text

    def list_videos_clicked(self): #create a method for when the list videos button is clicked
        video_list = lib.list_all() #create a list of all videos details using the LibraryItem's method
        set_text(self.list_txt, video_list) #display the list in the output textfield
        self.status_lbl.configure(text="List Videos button was clicked!") #update the status text

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    CheckVideos(window)     # open the CheckVideo GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
