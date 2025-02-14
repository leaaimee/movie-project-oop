import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
print(f"Loaded API Key: {API_KEY}")


def fetch_movie_data(title):
    """ Fetch movie data from the OMDb API by title """

    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            return f"Error: {data.get('Error')}"
    else:
        return f"Error: {response.status_code}"


def extract_movie_data(raw_data):
    """ Extracts relevant fields (Title, Year, Rating) from raw movie data """

    try:
        title = raw_data.get("Title", "N/A")
        year = raw_data.get("Year", "N/A")
        rating = raw_data.get("imdbRating", "N/A")
        return {"Title": title, "Year": year, "Rating": rating}
    except Exception as e:
        return {"Error": str(e)}




if __name__ == "__main__":

    raw_data = fetch_movie_data("Titanic")

    # Extract relevant fields
    cleaned_data = extract_movie_data(raw_data)

    # Display or use the cleaned data
    print(cleaned_data)