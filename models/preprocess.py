import string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import numpy as np
import emoji


def stem(sentence):
    sno = SnowballStemmer('english')
    filtered_sentence = []

    def is_valid_word(w):
        return w.isalpha()

    for w in sentence.split():
        if is_valid_word(w):
            word_stem = sno.stem(w)
            filtered_sentence.append(word_stem)
        else:
            filtered_sentence.append(w)

    return " ".join(filtered_sentence)


def give_emoji_free_text(text):
    # https: // stackoverflow.com / a / 50602709 / 4434664
    text = text if isinstance(text, str) else text.decode('utf8')
    return emoji.get_emoji_regexp().sub(r'', text)


def preprocess_text(text, is_stem=True):
    if not text:
        return text
    if not isinstance(text, str):
        print(text, type(text))
        if np.isnan(text):
            return None

    # Removing \n
    text = text.replace("\n", "")

    # Removing deleted and removed submissions
    if text in ["[deleted]", "[removed]"]:
        return None

    # removing emoji
    text = give_emoji_free_text(text)

    # Retaining posts between 10 and 300
    max_len = 300
    if len(text) > max_len:
        return None
    min_len = 10
    if len(text) < min_len:
        return None

    # removing punctuation
    translate_table = str.maketrans('', '', string.punctuation)
    text = text.translate(translate_table)

    # lowercase
    text = text.lower()

    # removing stopwords
    english_stopwords = stopwords.words('english')
    text_split = text.split()
    text_split = [w for w in text_split
                  if w not in english_stopwords]

    # remove @mentions
    text_split = [w for w in text_split
                  if not w.startswith("@")]

    # remove hypertext links
    text_split = [w for w in text_split
                  if not w.startswith("http")]

    text = " ".join(text_split)

    # stemming
    if is_stem:
        text = stem(text)

    return text