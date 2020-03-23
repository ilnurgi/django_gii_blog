alphabet = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'j',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ы': 'i',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    'ь': '',
    'ъ': '',
}


def cyrillic_to_latin(text):
    """
    кириллицу в латиницу
    :param text: входная строка
    :type text: str
    :rtype: str
    """
    return ''.join(alphabet.get(w, w) for w in text.lower())
