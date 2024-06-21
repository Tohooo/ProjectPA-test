from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from recommender import recommender
from search import search_system

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/books')
def books():
    books_data = recommender.books.to_dict('records')
    return render_template('books.html', books=books_data)

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    try:
        recommendations = recommender.get_recommendations(title)
        return jsonify(recommendations)
    except KeyError:
        return jsonify({"error": "Title not found"}), 404

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    suggestions = search_system.search(query)
    return jsonify(suggestions)

@app.route('/details', methods=['GET'])
def details():
    title = request.args.get('title')
    book = recommender.books[recommender.books['Judul'] == title].to_dict('records')
    if book:
        return jsonify(book[0])
    else:
        return jsonify({"error": "Title not found"}), 404

@app.route('/api/books', methods=['GET'])
def api_books():
    books_data = recommender.books.to_dict('records')
    return jsonify(books_data)

@app.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('query')
    query_words = query.lower().split()
    books = recommender.books[recommender.books['Judul'].apply(lambda x: all(word in x.lower() for word in query_words))]
    additional_books = recommender.books[recommender.books['Judul'].apply(lambda x: any(word in x.lower() for word in query_words))]
    results = pd.concat([books, additional_books]).drop_duplicates().to_dict('records')
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
