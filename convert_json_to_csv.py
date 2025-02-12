import json
import csv

def json_to_csv(json_file, csv_file):
    with open(json_file, "r") as file:
        movies = json.load(file)

    with open(csv_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "year", "rating"])
        writer.writeheader()

        for title, details in movies.items():
            writer.writerow({
                "title": title,
                "year": details["year"],
                "rating": details["rating"]
            })

json_to_csv("movies.json", "movies.csv")
print("CSV file created successfully!")