import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text, custom_stopwords=['abstract', 'keywords']):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'\W+|\d+', ' ', text)
    # Tokenization
    tokens = word_tokenize(text)
    # Remove stopwords (default + custom) and apply stemming
    stop_words = set(stopwords.words('english')).union(set(custom_stopwords))

    stemmer = PorterStemmer()
    processed_text = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return " ".join(processed_text)