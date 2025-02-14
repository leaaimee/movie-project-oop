from storage.istorage import IStorage
import json

class StorageJson(IStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path


    def list_movies(self):
        """ Retrieve all movies from the JSON file """
        try:
            with open(self.file_path, "r") as file:
                movies = json.load(file)
            return movies
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}


    def add_movie(self, title, year, rating, poster):
        """ Add a new movie to the JSON file """
        movies = self.list_movies()
        if title in movies:
            return f"Movie '{title}' already exists."
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        self.save_movies(movies)
        return f"Movie name {title} found & added "


    def delete_movie(self, title):
        """ Delete a movie from the JSON file """
        movies = self.list_movies()
        for stored_title in movies:
            if stored_title.lower() == title.lower():
                del movies[title]
                self.save_movies(movies)
                return None
        return f"Movie '{title}' not found."


    def update_movie(self, title, rating):
        """ Update the rating of a movie """
        movies = self.list_movies()
        for stored_title in movies:
            if stored_title.lower() == title.lower():
                movies[stored_title]["rating"] = rating
                self.save_movies(movies)
                return None
        return f"Movie '{title}' not found "


    def save_movies(self, movies):
        """ Save the movies back to the JSON file """
        with open(self.file_path, "w") as file:
            json.dump(movies, file, indent=4)
