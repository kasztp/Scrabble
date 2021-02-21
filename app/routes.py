from flask import render_template, flash, redirect, request, url_for
from app import app
from .forms import ConfigForm
from .scrabble_logic import Scrabble

tile_draw = []
grouped = {}
hasblank = 0


@app.route('/')
def root():
    return render_template('index.html', title='Home', scores=grouped,
                           tiles='tiles', blanks='blanks')


@app.route('/index')
def index():
    return render_template('index.html', title='Home', scores=grouped,
                           tiles=tile_draw, blanks=hasblank*(chr(160) + ' '))


@app.route('/table')
def table():
    mytable = Scrabble.build_table()
    return render_template('table.html', title='Table', column_names=mytable.columns.values,
                           row_data=list(mytable.values.tolist()),
                           link_column='A', zip=zip)


@app.route('/config', methods=['GET', 'POST'])
def config():
    form = ConfigForm()
    if form.validate_on_submit():
        flash(f'Configuration: Language {form.language.data}, Max Word Length {form.max_word_length.data},'
              f'Calculate for Maximum Length Only={form.max_word_length.data}')

        if request.method == 'POST':
            language = request.form['language']
            max_word_length = int(request.form['max_word_length'])
            game = Scrabble(language)
            global tile_draw
            tile_draw = []
            if form.own_tileset.data:
                global hasblank
                hasblank = form.own_tileset.data.count('BLANK')
                if hasblank >= 1:
                    print('Removing BLANK tiles...')
                    form.own_tileset.data = form.own_tileset.data.replace('BLANK', '')
                if language == 'HU':
                    hasdigraph = 0
                    digraph_count = 0
                    digraphs = []
                    for digraph in ('cs', 'gy', 'sz', 'zs', 'ty', 'ly', 'ny'):
                        if digraph in form.own_tileset.data:
                            digraph_count += form.own_tileset.data.count(digraph)
                            for _ in range(digraph_count):
                                hasdigraph += 1
                                digraphs += digraph
                            form.own_tileset.data.replace(digraph, '')
                    for character in form.own_tileset.data:
                        tile_draw += [character]
                    tile_draw += digraphs
                else:
                    for character in form.own_tileset.data:
                        tile_draw += [character]
                game.hand.update_hand(tile_draw, hasblank)
            else:
                tile_draw = game.hand.held_tiles
            print('Tiles drawn: {}'.format(tile_draw))
            flash('Tiles: {}'.format(tile_draw))
            valid_words = game.word_check(tile_draw, max_word_length, form.only_max.data)
            global grouped
            grouped = {}
            if valid_words != 'NONE':
                scores = game.score_calc(valid_words)
                grouped = game.group_by_score(scores)
            else:
                grouped = {0: 'Number of valid words found'}
        return redirect(url_for('index'))
    return render_template('config.html', title='Configuration', form=form)
