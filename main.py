"""
Main entry point for the Movie App.

This script initializes the application with the chosen storage (JSON or CSV)
and runs the menu-driven interface for managing the movie database
"""

from movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv


if __name__ == "__main__":
    """
    Initialize the MovieApp with the desired storage and run the application.
    You can switch between JSON and CSV storage by commenting/uncommenting
    the respective lines
    """
    storage = StorageJson("data/movies.json")
    # storage = StorageCsv('data/movies.csv')
    app = MovieApp(storage)
    app.run()