from istorage import IStorage
import csv

class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path


    def list_movies(self):
        """ Retrieve all movies from the CSV file """
        movies = {}
        try:
            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row["title"]
                    movies[title] = {
                        "year": int(row["year"]),
                        "rating": float(row["rating"]),
                        "poster": row.get("poster", "N/A")
                    }
            return movies
        except FileNotFoundError:
            return {}


    def add_movie(self, title, year, rating, poster):
        """ Add a new movie to the csv file """
        movies = self.list_movies()
        if title in movies:
            return f"Movie '{title}' already exists."

        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "year", "rating", "poster"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({"title": title, "year": year, "rating": rating, "poster": poster})

        return f"Movie '{title}' added successfully."


    def delete_movie(self, title):
        """ Delete a movie from the csv file """
        movies = self.list_movies()
        if title in movies:
            del movies[title]

            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["title", "year", "rating", "poster"])
                writer.writeheader()
                for movie_title, movie_data in movies.items():
                    writer.writerow({
                        "title": movie_title,
                        "year": movie_data["year"],
                        "rating": movie_data["rating"],
                        "poster": movie_data["poster"]
                    })

            return f"Movie '{title}' deleted successfully "
        return f"Movie '{title}' not found "


    def update_movie(self, title, rating):
        """ Update the rating of a movie in the CSV file """
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self.save_movies(movies)  # Delegate file saving
            return f"Movie '{title}' updated successfully."
        return f"Movie '{title}' not found."


    def save_movies(self, movies):
        """ Save the movies back to the csv file """
        with open (self.file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "year", "rating", "poster"])
            writer.writeheader()
            for title, data in movies.items():
                writer.writerow({
                    "title": title,
                    "year": data["year"],
                    "rating": data["rating"],
                    "poster": data["poster"]
                })

