import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class RecommenderSystem:
    def __init__(self, csv_file):
        self.books = pd.read_csv(csv_file)
        self.books = self.books.dropna(subset=['Judul', 'Keywords'])  # Drop rows with missing 'Judul' or 'Keywords'
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.books['Judul'] + " " + self.books['Keywords'])
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        self.indices = pd.Series(self.books.index, index=self.books['Judul']).drop_duplicates()

    def get_recommendations(self, title, num_recommendations=5):
        if title not in self.indices:
            return []
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations + 1]
        book_indices = [i[0] for i in sim_scores]
        return self.books.iloc[book_indices].to_dict('records')

recommender = RecommenderSystem('Books.csv')
