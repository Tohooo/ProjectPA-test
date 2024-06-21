import pandas as pd

class SearchSystem:
    def __init__(self, csv_file):
        self.books = pd.read_csv(csv_file)

    def search(self, query):
        query = query.lower()
        results = self.books[self.books['Judul'].str.contains(query, case=False, na=False)]
        return results['Judul'].tolist()

search_system = SearchSystem('Books.csv')
