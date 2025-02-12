import pytest
from storage_json import StorageJson

@pytest.fixture
def storage():
    return StorageJson('test_movies.json')

def test_add_movie(storage):
    storage.add_movie("The Matrix", 1999, 9.0)
    movies = storage.list_movies()
    assert "The Matrix" in movies

def test_delete_movie(storage):
    storage.add_movie("The Matrix", 1999, 9.0)
    storage.delete_movie("The Matrix")
    movies = storage.list_movies()
    assert "The Matrix" not in movies
