from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


if __name__ == "__main__":
    storage = StorageJson("movies.json")
    # storage = StorageCsv('movies.csv')
    app = MovieApp(storage)
    app.run()