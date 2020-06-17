

def load_dictionary(lang):
    if lang == 'EN':
        filename = 'words.txt'  # SCOWL-wl en_US word list
        db = open(filename, encoding='utf-8')
        EN_words = set(db.read().splitlines())
        db.close()
        return EN_words
    if lang == 'HU':
        filename = 'szavak.txt'  # https://sourceforge.net/projects/wordlist-hu/ hu_HU word list
        db = open(filename, encoding='utf-8')
        HU_words = set(db.read().splitlines())
        db.close()
        return HU_words


EN_words_2 = set()
EN_words_3 = set()
EN_words_4 = set()
EN_words_5 = set()
EN_words_6 = set()
EN_words_7 = set()
for i in EN_words:
    l = len(i)
    if l == 2:
        EN_words_2.add(i)
    elif l == 3:
        EN_words_3.add(i)
    elif l == 4:
        EN_words_4.add(i)
    elif l == 5:
        EN_words_5.add(i)
    elif l == 6:
        EN_words_6.add(i)
    elif l == 7:
        EN_words_7.add(i)
EN_words = {
    2: sorted(EN_words_2),
    3: sorted(EN_words_3),
    4: sorted(EN_words_4),
    5: sorted(EN_words_5),
    6: sorted(EN_words_6),
    7: sorted(EN_words_7)
    }
	
