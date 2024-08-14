import csv
import math
class Movie:
    def __init__(self, name, director, year, length, genre):
        self.name = name
        self.director = director
        self.year = year
        minute=int(length)
        self.length = f"{math.floor(minute/60)}h{minute%60}m"
        self.genre = genre
        self.rating = []
        self.play_count = 0
        self.rating_count = 0
    
    def __repr__(self):
        return f"Movie(name='{self.name}', director='{self.director}', year='{self.year}', length='{self.length}', genre='{self.genre}')"
    
    def increment_play_count(self):
        self.play_count+=1
        
    def cal_rating(self):
        try:
            avg_rating = 0
            for rating in self.rating:
                avg_rating += rating
            avg_rating /= self.rating_count
            avg_rating = round(avg_rating,1)
            return avg_rating
        except:
            return 0
    
    def add_rating(self, rating):
        self.rating.append(rating)
        self.rating_count +=1
        
    def get_name(self):
        return self.name
        
class MovieDetails:
    def __init__(self, csv_file_path):
        self.movies = []
        self.load_movies_from_csv(csv_file_path)
        
    def readlines(self, filename):
        with open(filename) as file:
            return file.readlines()

    def load_movies_from_csv(self, csv_file_path):
        try:
            contents = self.readlines(csv_file_path)
            fields = contents.pop(0).strip().split(",")
            for i, field in enumerate(fields):
                if field.lower() == "name":
                    name_column=i
                elif field.lower() == "director":
                    dir_column=i
                elif field.lower() == "year":
                    year_column=i
                elif field.lower() == "length":
                    length_column=i
                elif field.lower() == "genre":
                   genre_column=i

            for row in contents:
                cells = row.strip().split(",")
                name = cells.pop(name_column)
                dir = cells.pop(dir_column-1)
                year = cells.pop(year_column-2)
                length = cells.pop(length_column-3)
                genre = cells.pop(genre_column-4)
                movie = Movie(name, dir, year, length, genre)
                self.movies.append(movie)
                for cell in cells:
                    movie.add_rating(int(cell))
        except FileNotFoundError:
            print(f"Error: The file '{csv_file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_movies(self):
        return self.movies

    
class Playlist:
    def __init__(self, name):
        self.name = name
        self.movies = []

    def add_movie(self, movie):
        self.movies.append(movie)

    def remove_movie(self, movie):
        if movie in self.movies:
            self.movies.remove(movie)

    def clear_playlist(self):
        self.movies = []

    def get_movies(self):
       return self.movies

    #def __repr__(self):
       # return f"Playlist({self.movies})"
    
    
class PlaylistManager:
    def __init__(self):
        self.playlists = {}

    def create_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = Playlist(name)

    def get_playlist(self, name):
        return self.playlists.get(name)

    def get_all_playlists(self):
        return list(self.playlists.keys())

    def delete_playlist(self, name):
        if name in self.playlists:
            del self.playlists[name]

if __name__ == "__main__":
    csv_file_path = 'movie_list.csv'
    movies_details = MovieDetails(csv_file_path)
    movies = movies_details.get_movies()
    for movie in movies:
        print(movie)
        rating = movie.cal_rating()
        print(rating)