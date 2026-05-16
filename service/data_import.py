import csv


def import_csv(path: str) -> list[tuple]:

    with open (path, newline = "") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # Skip header
        return [tuple(row) for row in reader]
