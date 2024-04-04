import os
import re
import json
import argparse

from plagiarism_injection import simulate_plagiarism

# Load text files as books
def load_books(folder_path):
    books = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                books.append({'title': filename, 'text': file.read()})
    return books

# Split books into articles
def split_into_articles(books, words_per_article=2000):
    articles = []
    for book in books:
        words = book['text'].split()
        for i in range(0, len(words), words_per_article):
            articles.append({
                'id': f"{book['title'].replace('.txt', '')}_{i//words_per_article}",
                'title': book['title'],
                'text': ' '.join(words[i:i+words_per_article]),
                'source_book': book['title'],
                'publication_date': '2024-01-01',  # Example, adjust as needed
                'plagiarism_details': None
            })
    return articles



# Save dataset to JSON
def save_dataset_as_json(articles, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({"articles": articles}, file, indent=4, ensure_ascii=False)

# Combine steps
def create_and_save_dataset(folder_path, output_file_path, words_per_article=20000, injection_rate=0.05):
    books = load_books(folder_path)
    articles = split_into_articles(books, words_per_article)
    simulated_articles = simulate_plagiarism(articles, injection_rate)
    save_dataset_as_json(simulated_articles, output_file_path)

# Adding argparse functionality
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and save a dataset simulating plagiarism from a set of text files.")
    parser.add_argument('--folder_path', type=str, required=True, help='Path to the folder containing book text files.')
    parser.add_argument('--output_file_path', type=str, required=True, help='Path where the JSON dataset will be saved.')
    parser.add_argument('--words_per_article', type=int, default=2000, help='Number of words per article (default: 2000).')
    parser.add_argument('--injection_rate', type=float, default=0.05, help= 'Koeficient for plagiarism injecton.')
    args = parser.parse_args()

    # Use the arguments
    create_and_save_dataset(args.folder_path, args.output_file_path, args.words_per_article, args.injection_rate)

    print("Dataset creation and saving complete.")