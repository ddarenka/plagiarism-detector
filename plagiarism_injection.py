import random

# Simulate plagiarism by injecting content from one article to another
def simulate_plagiarism(articles, injection_rate=0.05):
    sorted_articles = sorted(articles, key=lambda x: x['publication_date'])
    for i in range(1, len(sorted_articles)):
        source_article = sorted_articles[i-1]
        target_article = sorted_articles[i]
        
        source_words = source_article['text'].split()
        injection_length = int(len(source_words) * injection_rate)
        injection_start = random.randint(0, len(source_words) - injection_length)
        injection_text = source_words[injection_start:injection_start+injection_length]
        
        target_words = target_article['text'].split()
        injection_point = random.randint(0, len(target_words) - injection_length)
        target_words[injection_point:injection_point] = injection_text  # Inject
        
        target_article['text'] = ' '.join(target_words)
        target_article['plagiarism_details'] = {
            'injected_from': source_article['id'],
            'injection_rate': injection_rate,
            'injection_points': [{'start': injection_point, 'end': injection_point + len(injection_text)}]
        }
    return sorted_articles