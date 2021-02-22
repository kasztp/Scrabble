import random
import timeit
import pandas as pd

# Load Word dictionaries from text files.
EN_FILENAME = './app/static/Scrabble.txt'  # Scrabble EN word list
HU_FILENAME = './app/static/szavak.txt'  # https://sourceforge.net/projects/wordlist-hu/ hu_HU list
with open(HU_FILENAME, encoding='utf-8') as hu_file, open(EN_FILENAME, encoding='utf-8') as en_file:
    EN_WORDS = set(en_file.read().splitlines())
    HU_WORDS = set(hu_file.read().splitlines())


class Hand:
    def __init__(self, tileset, tilecount):
        self.tileset = tileset
        self.tilecount = tilecount
        self.held_tiles = self.draw_tiles(tilecount)
        self.hasblank = self.held_tiles.count('BLANK')
        if self.hasblank >= 1:
            print('Removing BLANK tiles...')
            self.held_tiles = [tile for tile in self.held_tiles if tile != 'BLANK']

    # Draw n number of random tiles from the tile set
    def draw_tiles(self, tilecount: int) -> list:
        if tilecount >= 2:
            owntiles = random.sample(self.tileset, k=tilecount)
            print(f'Tiles drawn: {owntiles}')
            return owntiles
        else:
            print('ERROR: Tile number less than 2!')
            return []

    def update_hand(self, tiles, blanks):
        self.held_tiles = tiles
        self.hasblank = blanks


class Scrabble:
    def __init__(self, language):
        self.language = language
        if self.language == 'HU':
            self.wordlist = HU_WORDS
        else:
            self.wordlist = EN_WORDS
        self.board = self.build_table()
        self.tileset = self.build_tileset(self.language)
        self.hand = Hand(self.tileset, 7)

    # Build Scrabble table representation as Pandas dataframe
    @staticmethod
    def build_table():
        table = []
        for _ in range(15):
            table += [[chr(160), chr(160), chr(160), chr(160), chr(160),
                       'p', 'r', 'o', 'b', 'a',
                       chr(160), chr(160), chr(160), chr(160), chr(160)]]
        df = pd.DataFrame(table)
        return df

    # Build language specific tile set
    @staticmethod
    def build_tileset(lang: str) -> list:
        if lang == 'EN':
            tile_set = ['a'] * 9 + ['b'] * 2 + ['c'] * 2 + ['d'] * 4 + ['e'] * 12 +\
                       ['f'] * 2 + ['g'] * 3 + ['h'] * 2 + ['i'] * 9 + ['j'] + ['k'] +\
                       ['l'] * 4 + ['m'] * 2 + ['n'] * 6 + ['o'] * 8 + ['p'] * 2 +\
                       ['q'] + ['r'] * 6 + ['s'] * 4 + ['t'] * 6 + ['u'] * 4 +\
                       ['v'] * 2 + ['w'] * 2 + ['x'] + ['y'] * 2 + ['z'] + \
                       ['BLANK'] * 2
            if len(tile_set) == 100:
                print('Tile set generated OK!')
                return tile_set
            else:
                print(f'ERROR: Tile set generation error with length: {len(tile_set)}')
                return len(tile_set)
        elif lang == 'HU':
            tile_set = ['a'] * 6 + ['b'] * 3 + ['c'] + ['d'] * 3 + ['e'] * 6 + ['f'] * 2 +\
                       ['g'] * 3 + ['h'] * 2 + ['i'] * 3 + ['j'] * 2 + ['k'] * 6 + ['l'] * 4 +\
                       ['m'] * 3 + ['n'] * 4 + ['o'] * 3 + ['p'] * 2 + ['á'] * 4 + ['r'] * 4 +\
                       ['s'] * 3 + ['t'] * 5 + ['u'] * 2 + ['v'] * 2 + ['é'] * 3 + ['í'] +\
                       ['ó'] * 3 + ['z'] * 2 + ['ö'] * 2 + ['ő'] + ['ú'] + ['ü'] * 2 + ['ű'] +\
                       ['sz'] * 2 + ['gy'] * 2 + ['ny'] + ['cs'] + ['ly'] + ['zs'] + ['ty'] + \
                       ['BLANK'] * 2
            if len(tile_set) == 100:
                print('Tile set generated OK!')
                return tile_set
            else:
                print(f'ERROR: Tile set generation error with length: {len(tile_set)}')
                return len(tile_set)
        else:
            print(f'ERROR: Unsupported Language: {lang}')
            return 1

    # Check which words of the dictionary can be built from held tiles (HU version to be polished):
    def checker(self, owntiles, length):
        valid_words = set()
        if self.hand.hasblank >= 1:
            for word in self.wordlist:
                if len(word) == length:
                    word = word.lower()
                    characters = list(word)
                    owntiles_tmp = owntiles.copy()
                    matches = 0
                    for character in characters:
                        if character in owntiles_tmp:
                            matches += 1
                            owntiles_tmp.remove(character)
                    if matches in (length, length - self.hand.hasblank):
                        valid_words.add(word)
        else:
            for word in self.wordlist:
                if len(word) == length:
                    word = word.lower()
                    characters = list(word)
                    owntiles_tmp = owntiles.copy()
                    matches = 0
                    for character in characters:
                        if character in owntiles_tmp:
                            matches += 1
                            owntiles_tmp.remove(character)
                    if matches == length:
                        valid_words.add(word)
        return valid_words

    def word_check(self, owntiles, length, max_only):
        if length >= 2:
            if max_only:
                results = set(self.checker(owntiles, length))
                print(f'Unique {length} length words generated: {len(results)}')
                return results
            else:
                textperm = set()
                for wordlength in range(2, (length + 1)):
                    start_time = timeit.default_timer()
                    results = set(self.checker(owntiles, wordlength))
                    print(timeit.default_timer() - start_time)
                    print(f'Unique {wordlength} length words generated: {len(results)}')
                    textperm |= results
                    print(f'Unique words generated so far: {len(textperm)}')
                return textperm
        else:
            print('ERROR: Word length parameter less than 2!')

    # Calculate word point values - HU version to be
    def score_calc(self, words: list) -> dict:
        if words != 1:
            scores = {}
            if self.language == 'EN':
                characters_en = dict.fromkeys(['a', 'e', 'i', 'o', 'n', 'r', 't', 'l', 's', 'u'], 1)
                characters_en.update(dict.fromkeys(['d', 'g'], 2))
                characters_en.update(dict.fromkeys(['b', 'c', 'm', 'p'], 3))
                characters_en.update(dict.fromkeys(['f', 'h', 'v', 'w', 'y'], 4))
                characters_en.update(dict.fromkeys(['k'], 5))
                characters_en.update(dict.fromkeys(['j', 'x'], 8))
                characters_en.update(dict.fromkeys(['q', 'z'], 10))
                characters_en.update(dict.fromkeys(['BLANK'], 0))
                for word in words:
                    if word != ():
                        value = 0
                        for character in word:
                            value += characters_en.get(character, 0)
                        scores[word] = value
                return scores
            elif self.language == 'HU':
                characters_hu = dict.fromkeys(['i', 'm', 'o', 's', 'á', 'l', 'n', 'r', 't', 'a', 'e', 'k'], 1)
                characters_hu.update(dict.fromkeys(['b', 'd', 'g', 'ó'], 2))
                characters_hu.update(dict.fromkeys(['h', 'v', 'é', 'sz'], 3))
                characters_hu.update(dict.fromkeys(['f', 'j', 'ö', 'p', 'u', 'ü', 'z', 'gy'], 4))
                characters_hu.update(dict.fromkeys(['c', 'í', 'ny'], 5))
                characters_hu.update(dict.fromkeys(['ő', 'ú', 'ű', 'cs'], 7))
                characters_hu.update(dict.fromkeys(['ly', 'zs'], 8))
                characters_hu.update(dict.fromkeys(['ty'], 10))
                characters_hu.update(dict.fromkeys(['BLANK'], 0))
                for word in words:
                    if word != ():
                        value = 0
                        for character in word:
                            value += characters_hu.get(character, 0)
                        scores[word] = value
                return scores
            else:
                print(f'ERROR: Unsupported Language: {self.language}')
                return 'NONE'
        else:
            print('ERROR: NO valid words given!')
            return 'NONE'

    def group_by_score(self, scores: dict) -> dict:
        score_groups = sorted(set(val for val in scores.values()), reverse=True)
        grouped_words = {}
        for number in score_groups:
            wordgroup = []
            for i in scores.items():
                if i[1] == number:
                    wordgroup.extend(i[0:1])
            grouped_words[number] = sorted(wordgroup)
        return grouped_words
