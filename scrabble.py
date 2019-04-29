# Check if a specific word is in the SCOWL-wl en_US word list
import random
import itertools
import timeit
from flask import Flask
from flask import render_template

app = Flask(__name__)


filename = 'words.txt'
db = open(filename, encoding='utf-8')
words = db.read().splitlines()
db.close()


def find_word(word):
    if word in words:
        return word
    else:
        return ()
    #    print('{} found in word database!'.format(word))
    # else:
    #     print('{} NOT found in word database!'.format(word))


# Build language specific tile set - without the 2 blanks
def build_tileset(lang):
    if lang == 'EN':
        tile_set = ['a']*9 + ['b']*2 + ['c']*2 + ['d']*4 + ['e']*12 + ['f']*2 + ['g']*3 + ['h']*2 + ['i']*9 + ['j'] +\
                   ['k'] + ['l']*4 + ['m']*2 + ['n']*6 + ['o']*8 + ['p']*2 + ['q'] + ['r']*6 + ['s']*4 + ['t']*6 +\
                   ['u']*4 + ['v']*2 + ['w']*2 + ['x'] + ['y']*2 + ['z']
        if len(tile_set) == 98:
            print('Tile set generated OK!')
            return tile_set
        else:
            print('ERROR: Tile set generation error with length: {}'.format(len(tile_set)))
            return len(tile_set)
    else:
        print('ERROR: Unsupported Language: {}'.format(lang))
        return 1


# Draw n number of random tiles from the tile set
def draw(tileset, n):
    if n >= 1:
        own_tiles = random.sample(tileset,k=n)
        print('Tiles drawn: {}'.format(own_tiles))
        return own_tiles
    else:
        print('ERROR: Tile number less than 1!')


# Generate possible words (tile permutations)
def word_gen(owntiles, l):
    if l >= 2:
        textperm = []
        for i in range(2,(l+1)):
            permutations = set(itertools.permutations(owntiles, r=i))
            textperm_i = []
            for element in permutations:
                textperm_i += [''.join(element)]
            print('Possible {} length words generated: {}'.format(i, len(textperm_i)))
            textperm += textperm_i
        return textperm
    else:
        print('ERROR: Word length parameter less than 2!')


# intersection test
def find_inter(ws, wc):
    results = set(ws).intersection(wc)
    if results != set():
        print(results)
        print('Number of valid words: {}'.format(len(results)))
        return results
    else:
        print('NO valid words found!')
        return 1

'''
# find test
def find_in(wc):
    results = []
    for keyword in wc:
        if find_word(keyword) != ():
            results += [''.join(find_word(keyword))]
    print(results)
    print(len(results))
    return results
'''


def score_calc(words, lang):
    if words != 1:
        if lang == 'EN':
            characters_en = dict.fromkeys(["a", "e", "i", "o", "n", "r", "t", "l", "s", "u"], 1)
            characters_en.update(dict.fromkeys(["d", "g"], 2))
            characters_en.update(dict.fromkeys(["b", "c", "m", "p"], 3))
            characters_en.update(dict.fromkeys(["f", "h", "v", "w", "y"], 4))
            characters_en.update(dict.fromkeys(["k"], 5))
            characters_en.update(dict.fromkeys(["j", "x"], 8))
            characters_en.update(dict.fromkeys(["q", "z"], 10))
            # print(characters_en)
            scores = {}
            for word in words:
                value = 0
                for character in word:
                    value += characters_en.get(character)
                scores[word] = value
            print(scores)
            return scores
        else:
            print('ERROR: Unsupported Language: {}'.format(lang))
            return 1
    else:
        print('ERROR: NO valid words given!')
        return 1


language = 'EN'

tiles = build_tileset('EN')
# print(tiles)
tile_draw = draw(tiles, 7)
# tile_draw = ['a', 'p', 'p', 'l', 'e', 'y', 's']
word_candidates = word_gen(tile_draw, 7)

# intersection test
start_time = timeit.default_timer()
valid_words = find_inter(words, word_candidates)
print(timeit.default_timer() - start_time)

'''
# in test
start_time = timeit.default_timer()
find_in(word_candidates)
print(timeit.default_timer() - start_time)
'''

#score_calc(valid_words, language)


@app.route('/index')
def index():
    user = {'username': 'Peter'}

    return render_template('index.html', title='Home', user=user, posts=score_calc(valid_words, language))
    #return "The valid {} words from draw {} are {}".format(lang, tile_draw, score_calc(valid_words, language))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
