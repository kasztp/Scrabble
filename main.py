import random
import timeit
import pandas as pd
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


# Load Word dictionary from files.
filename = 'Scrabble.txt'  # Scrabble EN word list
db = open(filename, encoding='utf-8')
EN_words = set(db.read().splitlines())
db.close()

filename = 'szavak.txt'  # https://sourceforge.net/projects/wordlist-hu/ hu_HU word list
db = open(filename, encoding='utf-8')
HU_words = set(db.read().splitlines())
db.close()

scores = {}
grouped = {}


# Build Scrabble table representation as Pandas dataframe
def build_table():
    table = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']]
    for i in range(15):
        table += [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        df = pd.DataFrame(table)
    return df


# Build language specific tile set
def build_tileset(lang):
    if lang == 'EN':
        tile_set = ['a'] * 9 + ['b'] * 2 + ['c'] * 2 + ['d'] * 4 + ['e'] * 12 + ['f'] * 2 + ['g'] * 3 + ['h'] * 2 + [
            'i'] * 9 + ['j'] + \
                   ['k'] + ['l'] * 4 + ['m'] * 2 + ['n'] * 6 + ['o'] * 8 + ['p'] * 2 + ['q'] + ['r'] * 6 + ['s'] * 4 + [
                       't'] * 6 + \
                   ['u'] * 4 + ['v'] * 2 + ['w'] * 2 + ['x'] + ['y'] * 2 + ['z'] + ['BLANK'] * 2
        if len(tile_set) == 100:
            print('Tile set generated OK!')
            return tile_set
        else:
            print('ERROR: Tile set generation error with length: {}'.format(len(tile_set)))
            return len(tile_set)
    elif lang == 'HU':
        tile_set = ['a'] * 6 + ['b'] * 3 + ['c'] + ['d'] * 3 + ['e'] * 6 + ['f'] * 2 + ['g'] * 3 + ['h'] * 2 + \
                   ['i'] * 3 + ['j'] * 2 + ['k'] * 6 + ['l'] * 4 + ['m'] * 3 + ['n'] * 4 + ['o'] * 3 + ['p'] * 2 + \
                   ['á'] * 4 + ['r'] * 4 + ['s'] * 3 + ['t'] * 5 + ['u'] * 2 + ['v'] * 2 + ['é'] * 3 + ['í'] + \
                   ['ó'] * 3 + ['z'] * 2 + ['ö'] * 2 + ['ő'] + ['ú'] + ['ü'] * 2 + ['ű'] + ['sz'] * 2 + ['gy'] * 2 + \
                   ['ny'] + ['cs'] + ['ly'] + ['zs'] + ['ty'] + ['BLANK'] * 2
        if len(tile_set) == 100:
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
    if n >= 2:
        own_tiles = random.sample(tileset, k=n)
        print('Tiles drawn: {}'.format(own_tiles))
        return own_tiles
    else:
        print('ERROR: Tile number less than 2!')


# Check if word is in the dictionary (HU version to be polished):
def checker(owntiles, dictionary, l):
    print(owntiles)
    valid_words = set()
    if hasblank >= 1:
        print(owntiles)
        for word in dictionary:
            if len(word) == l:
                word = word.lower()
                characters = list(word)
                owntiles_tmp = owntiles.copy()
                matches = 0
                for character in characters:
                    if character in owntiles_tmp:
                        matches += 1
                        owntiles_tmp.remove(character)
                    else:
                        pass
                if matches == l or matches == (l - hasblank):
                    valid_words.add(word)
                    print(word)
    else:
        for word in dictionary:
            if len(word) == l:
                word = word.lower()
                characters = list(word)
                owntiles_tmp = owntiles.copy()
                matches = 0
                for character in characters:
                    if character in owntiles_tmp:
                        matches += 1
                        owntiles_tmp.remove(character)
                    else:
                        pass
                if matches == l:
                    valid_words.add(word)
    print(valid_words)
    return valid_words


def word_check(owntiles, l, s, lang):
    if l >= 2:
        results = set()
        if s:
            if lang == 'EN':
                results = set(checker(owntiles, EN_words, l))
            if lang == 'HU':
                results = set(checker(owntiles, HU_words, l))
            print('Unique {} length words generated: {}'.format(l, len(results)))
            return results
        else:
            textperm = set()
            for i in range(2, (l + 1)):
                # if __name__ == "__main__":
                start_time = timeit.default_timer()
                if lang == 'EN':
                    results = set(checker(owntiles, EN_words, i))
                    print(timeit.default_timer() - start_time)
                if lang == 'HU':
                    results = set(checker(owntiles, HU_words, i))
                    print(timeit.default_timer() - start_time)
                print('Unique {} length words generated: {}'.format(i, len(results)))
                textperm |= results
                print('Unique words generated so far: {}'.format(len(textperm)))
            return textperm
    else:
        print('ERROR: Word length parameter less than 2!')


# Calculate word point values
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
            characters_en.update(dict.fromkeys(["BLANK"], 0))
            # print(characters_en)
            scores = {}
            for word in words:
                if word != ():
                    value = 0
                    for character in word:
                        value += characters_en.get(character, 0)
                    scores[word] = value
            print(scores)
            return scores
        elif lang == 'HU':
            characters_en = dict.fromkeys(["i", "m", "o", "s", "á", "l", "n", "r", "t", "a", "e", "k"], 1)
            characters_en.update(dict.fromkeys(["b", "d", "g", "ó"], 2))
            characters_en.update(dict.fromkeys(["h", "v", "é", "sz"], 3))
            characters_en.update(dict.fromkeys(["f", "j", "ö", "p", "u", "ü", "z", "gy"], 4))
            characters_en.update(dict.fromkeys(["c", "í", "ny"], 5))
            characters_en.update(dict.fromkeys(["ő", "ú", "ű", "cs"], 7))
            characters_en.update(dict.fromkeys(["ly", "zs"], 8))
            characters_en.update(dict.fromkeys(["ty"], 10))
            characters_en.update(dict.fromkeys(["BLANK"], 0))
            # print(characters_en)
            scores = {}
            for word in words:
                if word != ():
                    value = 0
                    for character in word:
                        value += characters_en.get(character, 0)
                    scores[word] = value
            print(scores)
            return scores
        else:
            print('ERROR: Unsupported Language: {}'.format(lang))
            return 'NONE'
    else:
        print('ERROR: NO valid words given!')
        return 'NONE'


def group_by_score(scores):
    score_groups = sorted(set(val for val in scores.values()), reverse=True)
    # print(score_groups)
    grouped_words = {}
    for number in score_groups:
        wordgroup = []
        for i in scores.items():
            # print(i)
            if i[1] == number:
                wordgroup.extend(i[0:1])
        # print(wordgroup)
        grouped_words[number] = sorted(wordgroup)
    return grouped_words


def calc_best_hand(tiles):
    start_time = timeit.default_timer()
    print(timeit.default_timer() - start_time)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nobody-gonna-guess-it'
bootstrap = Bootstrap(app)


class ConfigForm(FlaskForm):
    language = RadioField('Language', choices=[('EN', 'English'), ('HU', 'Hungarian')], validators=[DataRequired()])
    max_word_length = RadioField('Max Word Length',
                                 choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                          (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13')], coerce=int,
                                 validators=[DataRequired()])
    own_tileset = StringField('Enter your own tiles here (without any breaks):')
    only_max = BooleanField('Only Max Length?')
    submit = SubmitField('Send')


@app.route('/')
def root():
    user = {'username': 'Peter'}
    return render_template('index.html', title='Home', user=user, scores=grouped, tiles='none', blanks='none')


@app.route('/index')
def index():
    user = {'username': 'Peter'}
    return render_template('index.html', title='Home', user=user, scores=grouped, tiles=tile_draw, blanks=hasblank)


@app.route('/table')
def table():
    user = {'username': 'Peter'}
    mytable = build_table()
    print(mytable)
    return render_template("table.html", title='Table', user=user, column_names=mytable.columns.values,
                           row_data=list(mytable.values.tolist()),
                           link_column="A", zip=zip)


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
            global tile_draw
            tile_draw = []
            global hasblank
            if form.own_tileset.data:
                # own_tileset = []
                hasblank = form.own_tileset.data.count('BLANK')
                if hasblank >= 1:
                    print("Removing BLANK tiles...")
                    form.own_tileset.data = form.own_tileset.data.replace('BLANK', '')
                print(form.own_tileset.data)
                if language == 'HU':
                    global hasdigraph
                    hasdigraph = 0
                    digraph_count = 0
                    digraphs = []
                    for digraph in ('cs', 'gy', 'sz', 'zs', 'ty', 'ly', 'ny'):
                        if digraph in form.own_tileset.data:
                            digraph_count += form.own_tileset.data.count(digraph)
                            for i in range(digraph_count):
                                hasdigraph += 1
                                digraphs += digraph
                            form.own_tileset.data.replace(digraph, '')
                    for character in form.own_tileset.data:
                        tile_draw += [character]
                    tile_draw += digraphs
                else:
                    for character in form.own_tileset.data:
                        tile_draw += [character]
            else:
                tile_draw = draw(tiles, 7)
                hasblank = tile_draw.count('BLANK')
                if hasblank >= 1:
                    form.own_tileset.data = tile_draw.replace('BLANK', '')
            print('Tiles drawn: {}'.format(tile_draw))
            flash('Tiles: {}'.format(tile_draw))
            valid_words = word_check(tile_draw, max_word_length, form.only_max.data, language)
            global grouped
            grouped = {}
            if valid_words != 'NONE':
                scores = score_calc(valid_words, language)
                grouped = group_by_score(scores)
            else:
                grouped = {0: 'Number of valid words found'}
            df = pd.DataFrame.from_dict(grouped, orient='index')
            print(df.transpose())
        return redirect(url_for('index'))
    return render_template('config.html', title='Configuration', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
