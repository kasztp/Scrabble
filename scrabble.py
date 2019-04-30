import random
import itertools
import timeit
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired
#from flask_bootstrap import Bootstrap


filename = 'words.txt'  # SCOWL-wl en_US word list
score = {}
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
def word_gen(owntiles, l, s):
    if l >= 2:
        textperm = []
        if s:
            permutations = set(itertools.permutations(owntiles, r=l))
            textperm = []
            for element in permutations:
                textperm += [''.join(element)]
            print('Possible {} length words generated: {}'.format(l, len(textperm)))
            return textperm
        else:
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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nobody-gonna-guess-it'
#bootstrap = Bootstrap(app)


class ConfigForm(FlaskForm):
    #language = StringField('Language', validators=[DataRequired()])
    language = RadioField('Language', choices=[('EN', 'English')], validators=[DataRequired()])
    max_word_length = RadioField('Max Word Length', choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], coerce=int, validators=[DataRequired()])
    only_max = BooleanField('Only Max Length?')
    submit = SubmitField('Send')


@app.route('/index')
def index():
    user = {'username': 'Peter'}
    return render_template('index.html', title='Home', user=user, scores=score)


@app.route('/config', methods=['GET', 'POST'])
def config():
    form = ConfigForm()
    if form.validate_on_submit():
        flash('Configuration: Language {}, Max Word Length {}, Calculate for Maximum Length Only={}'.format(
            form.language.data, form.max_word_length.data, form.only_max.data))
        if request.method == 'POST':
            language = request.form['language']
            max_word_length = int(request.form['max_word_length'])
            tiles = build_tileset(language)
            tile_draw = draw(tiles, 7)
            # tile_draw = ['a', 'p', 'p', 'l', 'e', 'y', 's']
            word_candidates = word_gen(tile_draw, max_word_length, form.only_max.data)

            # intersection test
            start_time = timeit.default_timer()
            valid_words = find_inter(words, word_candidates)
            print(timeit.default_timer() - start_time)
            global score
            score = score_calc(valid_words, language)
        return redirect(url_for('index'))
    return render_template('config.html', title='Configuration', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
