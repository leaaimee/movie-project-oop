from omdb_fetcher import fetch_movie_data

class MovieApp:
    def __init__(self, storage):
        """ Initialize the MovieApp with a storage instance """
        self._storage = storage

    def _command_list_movies(self):
        """ List all movies currently stored in the database """
        movies = self._storage.list_movies()

        movie_count = len(movies)
        print(f"\nOur database currently stores {movie_count} movies\n")
        if movies:
            for title, movie_data in movies.items():
                year = movie_data["year"]
                rating = movie_data["rating"]
                print(f"{title}, ({year}) with a rating of: {rating}")
        else:
            print("No movies found in the database.")

    # Part of the project when fetching data from csv or json - obsolete when working with OMDB
    # def _command_add_movie(self):
    #     title = input("Enter movie title: ").strip().capitalize()
    #     year = int(input("Enter release year: "))
    #     rating = float(input("Enter rating (1-10): "))
    #
    #     message = self._storage.add_movie(title, year, rating)
    #     if message:
    #         print(message)
    #     else:
    #         print(f"Movie '{title}' added successfully!")

    def _command_add_movie(self):
        """ Add a new movie by fetching data from the OMDb API """
        title = input("Enter the movie title: ")
        movie_data = fetch_movie_data(title)

        if isinstance(movie_data, str):
            print(movie_data)
            return

        year = int(movie_data["Year"])
        rating = float(movie_data.get("imdbRating", 0))
        poster = movie_data.get("Poster", "N/A")

        message = self._storage.add_movie(title, year, rating, poster)
        print(message)


    def _command_delete_movie(self):
        """ Delete a movie from the database by title """
        title = input("Enter movie title: ").strip()

        message = self._storage.delete_movie(title)
        if message:
            print(message)
        else:
            print(f"Movie '{title}' was deleted successfully!")


    def _command_update_movie(self):
        """ Update the rating of a movie in the database """
        title = input("Enter the movie you want to update: ").strip()
        rating = float(input("Enter a new rating (1-10): "))

        message = self._storage.update_movie(title, rating)
        if message:
            print(message)
        else:
            print(f"Movie '{title}' was updated successfully to the new rating of: {rating} !")


    def _command_list_movie_stats(self):
        """ Display statistics about the movie ratings,
               including average, median, best, and worst ratings """
        movies = self._storage.list_movies()

        if not movies:
            print("No movies found in the database.")
            return

        print("\nMovie Statistics\n")

        # Calculate average rating
        average_rating = sum(movie_data["rating"] for movie_data in movies.values()) / len(movies)
        print(f"The average rating of movies in this database is: {average_rating:.1f}")

        # Calculate median rating
        ratings = [movie_data["rating"] for movie_data in movies.values()]
        ratings.sort()
        n = len(ratings)
        if n % 2 == 0:
            median = (ratings[n // 2 - 1] + ratings[n // 2]) / 2
        else:
            median = ratings[n // 2]

        median = round(median, 1)
        print(f"The median rating is: {median}")

        # provides the best movie(s)
        best_rating = 0
        best_movie = []
        for title, movie_data in movies.items():
            rating = movie_data["rating"]
            if rating > best_rating:
                best_rating = rating
                best_movie = [title]
            elif rating == best_rating:
                best_movie.append(title)
        print(f"The best movie(s) in our database with a rating of {best_rating}: " + ", ".join(
            best_movie))

        # provides the worst movie(s)
        worst_rating = 10
        worst_movie = []
        for title, movie_data in movies.items():
            rating = movie_data["rating"]
            if rating < worst_rating:
                worst_rating = rating
                worst_movie = [title]
            elif rating == worst_rating:
                worst_movie.append(title)
        print(f"The worst movie(s) our database with a rating of {worst_rating}: " + ", ".join(
            worst_movie))


    def _command_search_movies(self):
        """ Search for movies by title """
        search_title = input("Enter the title to search for: ").strip()
        movies = self._storage.list_movies()
        found_movies = [
            (title, movie_data["year"], movie_data["rating"])
            for title, movie_data in movies.items()
            if search_title.lower() in title.lower()
        ]

        if found_movies:
            print("\nFound Movies:")
            for title, year, rating in found_movies:
                print(f"{title} ({year}) - Rating: {rating}")
        else:
            print("No movies found matching the search criteria ")


    def _command_sort_by_rating(self):
        """ Sort movies by rating in ascending or descending order """
        order = input("Enter '1' for ascending order or '2' for descending order: ").strip()
        if order not in ["1", "2"]:
            print("Invalid input. Please enter '1' or '2'.")
            return

        sorted_movies = sorted(self._storage.list_movies().items(), key=lambda item: item[1]["rating"],
                               reverse=(order == "2"))
        if sorted_movies:
            print("\nMovies sorted by rating:\n")
            for title, movie_data in sorted_movies:
                print(f"{title} ({movie_data['year']}): {movie_data['rating']}")
        else:
            print("No movies found to sort ")


    def _command_sorted_by_year(self):
        """ Display all movies sorted by year """
        order = input("Sort by year: 1 (Ascending) or 2 (Descending): ").strip()
        sorted_movies = self.sorted_by_year(order)

        if isinstance(sorted_movies, str):
            print(sorted_movies)
        else:
            print("\nMovies sorted by year:")
            for title, year, rating in sorted_movies:
                print(f"{title} ({year}), Rating: {rating}")


    def sorted_by_year(self, order):
        """Display all movies sorted by the year of release, ascending or descending"""
        movies = self._storage.list_movies()  # Adjust to use storage correctly

        if order == "1":
            movies_years = sorted(movies.items(), key=lambda item: item[1]["year"])
        elif order == "2":
            movies_years = sorted(movies.items(), key=lambda item: item[1]["year"], reverse=True)
        else:
            return "Invalid input. Please enter '1' or '2'"

        return [(title, movie_data["year"], movie_data["rating"]) for title, movie_data in movies_years]


    def _command_generate_website(self):
        """ Generate an HTML website displaying all movies from the database """
        movies = self._storage.list_movies()

        if not movies:
            print("No movies found in the database.")
            return

        movie_grid = ""
        for title, movie_data in movies.items():
            movie_grid += f"""
            <div class="movie">
                <img src="{movie_data['poster']}" alt="{title}" class="movie-poster"/>
                <h2>{title}</h2>
                <p>Year: {movie_data['year']}</p>
                <p>Rating: {movie_data['rating']}</p>
            </div>
            """

        with open("_static/index_template.html", "r") as template_file:
            template_content = template_file.read()

        template_content = template_content.replace("__TEMPLATE_TITLE__", "My Movie Database")
        template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        with open("index.html", "w") as output_file:
            output_file.write(template_content)

        print("Website generated successfully as 'index.html'.")


    def _command_exit(self):
        """ Exiting the program """
        print("Goodbye!")
        exit()


    def run(self):

        menu_actions = {
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_list_movie_stats,
            "6": self._command_search_movies,
            "7": self._command_sort_by_rating,
            "8": self._command_sorted_by_year,
            "9": self._command_generate_website,
            "0": self._command_exit,
        }

        while True:
            print("\n***** Movie Database App *****")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie")
            print("5. Movie Statistics")
            print("6. Search Movies")
            print("7. Sort Movies By Rating")
            print("8. Sort Movies By Year")
            print("9. Generate Website")
            print("0. Exit")

            choice = input("Choose an option: ")

            action = menu_actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again")
