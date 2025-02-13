from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """Retrieve all movies as a dictionary where each key is the movie title,
        and the value is a dictionary containing its details"""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Add a movie to the storage with the given title, year, rating, and poster URL """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """ Remove the movie with the given title from the storage """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """ Update the rating of the movie with the given title in the storage """
        pass

