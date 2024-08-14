import math
class LibraryItem:
    def __init__(self, name, director):
        self.name = name
        self.director = director
        self.rating = [5]
        self.play_count = 0
        self.rating_count=0
        
    def addrating(self, rating):
        self.rating_count+=1
        self.rating.append(rating)
            
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

    def info(self):
        return f"{self.name} - {self.director} {self.stars()}"

    def stars(self):
        stars = ""
        for i in range(self.cal_rating()):
            stars += "*"
        return stars
