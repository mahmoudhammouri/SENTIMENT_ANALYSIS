import re
from langdetect import detect


def get_text_language(text):
    return detect(text)


def clean_text(text: str):
    """
    :param text: input string data
    :return: clean string from symbols
    """
    list_words = re.sub(r'[0-9?!-()\"#/@;:<>{}=~|.,!$%^&*_+]', "", text)
    return " ".join(list_words.split())


def get_stop_words(path):
    """

    :param path: path of (.txt) file of stop-words
    :return: list of stop-words
    """
    return open(path, encoding="utf8").read().split()


def remove_stop_words(text):
    """

    :param text: string data
    :return: string without stop-words
    """
    try:
        if len(text.strip()) == 0:
            return None

        text_lang = get_text_language(text=text)

        if text_lang == 'en' or 'af':
            list_target_stop_words = list_en_stop_words
        elif text_lang == 'ar' or text_lang == 'fa':
            list_target_stop_words = list_ar_stop_words
        else:
            return None

        list_returned_words = []
        if len(text) == 0:
            return None
        for word in text.split():
            if word not in list_target_stop_words:
                list_returned_words.append(word)
        if len(list_returned_words) == 0:
            return None
        else:
            return " ".join(list_returned_words)

    except Exception as e:
        print(e)
        print(text)


# Clean/Normalize Arabic Text
def clean_str(text):
    search = ["أ", "إ", "آ", "ة", "_", "-", "/", ".", "،", " و ", " يا ", '"', "ـ", "'", "ى", "\\", '\n', '\t',
              '&quot;', '?', '؟', '!']
    replace = ["ا", "ا", "ا", "ه", " ", " ", "", "", "", " و", " يا", "", "", "", "ي", "", ' ', ' ', ' ', ' ? ', ' ؟ ',
               ' ! ']

    # remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel, "", text)

    # remove longation
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')
    text = text.replace('اااا', 'ا')

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    # trim
    text = text.strip()

    return text


path_stop_words = "arabic_stop_words.txt"
list_ar_stop_words = get_stop_words(path=path_stop_words)
list_en_stop_words = ['each', 'isn', 'both', 've', 'hadn', 'as', 'yourselves', 'do', 'from', 'are',
                      'by', 'you', 'won', 'has', 'under', 'his', "needn't", 'very', 'other',
                      'hers', 'once', 'been', 'again', 'should', 'll', 'into', 'after', 'wasn', 'weren', 'and', 'only',
                      'my', 'ourselves', 'to', 'between', 'ain', 'who', 'doing', 'because', 'aren', 'up', 'of', 'more',
                      'over', 'yourself', 'o', 'ours', 'she', 'is', 'themselves', 'herself',
                      'don', 'with', 'were', 'shan', 'what', 'him', 'these', 'when', 'at', 'does', 'itself',
                      'have', 'why', "she's", 'their', 'while', 'her', 'the', "should've", 'just', 'was', 'below',
                      'how', 'nor', 'can', 'few', 'own', 'too', 'through', 'this', 'if', 'that', 'did', 'will',
                      're', 'where', 'they', 'd', 'its', "shan't", 'we', 'your', 'them', 'some',
                      'it', 'all', 'any', 'for', 's', "won't", 'such', 'above', 'now',
                      'whom', 'm', 'those', "you've", 'until', 'being', 'myself', "you're", 'there',
                      'yours', 'am', 'same', 'wouldn', 'down', 'during',
                      'a', 'me', 'i', 'out', 'against', 'shouldn', 'y', 'be', 'off', 'here', 'doesn',
                      "it's", 'in', 'which', 'so', 'before', 'mustn', "you'll", 'on', 'mightn', 'he', 'himself',
                      'theirs', 't', 'having', 'further', 'had', 'haven', 'our', 'hasn', "that'll",
                      'then', 'or', 'most', 'about', 'ma', 'than', "you'd", 'an', 'didn', 'needn']
