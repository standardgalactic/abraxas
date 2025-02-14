import sys
import string
from collections import Counter
from nltk.corpus import stopwords

def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return filtered_words

def get_most_common_words(text, num=1000):
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = remove_stop_words(text)
    word_counts = Counter(words)
    return word_counts.most_common(num)

def main():
    if len(sys.argv) < 2:
        print("Usage: python text_analysis.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        text = file.read()

    most_common_words = get_most_common_words(text)
    print("Most common words by frequency:")
    for word, count in most_common_words:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
