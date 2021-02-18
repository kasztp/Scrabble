def finder_HU(perm):
    temp = ''.join(perm)
    if temp in HU_words:
        return temp
    else:
        return ()


def finder_EN(perm):
    temp = ''.join(perm)
    if temp in EN_words:
        return temp
    else:
        return ()

# Generate possible words (tile permutations)
def word_gen_mt(owntiles, l, s, lang):
    if l >= 2:
        workers = multiprocessing.cpu_count()
        if s:
            if __name__ == "__main__":
                start_time = timeit.default_timer()
                print("Estimating batch length...")
                pool = multiprocessing.Pool(processes=workers)
                length = factorial(len(owntiles)) // factorial(len(owntiles) - l)
                print(length)
                if l <= 4:
                    chunksize = 1000
                elif l == 5:
                    chunksize = 10000
                else:
                    chunksize = 20000
                values = itertools.permutations(owntiles, r=l)
                print(timeit.default_timer() - start_time)
                if lang == 'EN':
                    results = set(tqdm.tqdm(pool.imap_unordered(finder_EN, values, chunksize=chunksize), total=length))
                if lang == 'HU':
                    results = set(tqdm.tqdm(pool.imap_unordered(finder_HU, values, chunksize=chunksize), total=length))
                pool.close()
                pool.join()
            print('Unique {} length words generated: {}'.format(l, len(results)))
            return results
        else:
            textperm = set()
            for i in range(2, (l+1)):
                if __name__ == "__main__":
                    start_time = timeit.default_timer()
                    print("Estimating batch length...")
                    pool = multiprocessing.Pool(processes=workers)
                    length = factorial(len(owntiles)) // factorial(len(owntiles)-i)
                    print(length)
                    if i <= 4:
                        chunksize = 1000
                    elif i == 5:
                        chunksize = 10000
                    else:
                        chunksize = 20000
                    values = itertools.permutations(owntiles, r=i)
                    print(timeit.default_timer() - start_time)
                    if lang == 'EN':
                        results = set(tqdm.tqdm(pool.imap_unordered(finder_EN, values, chunksize=chunksize), total=length))
                    if lang == 'HU':
                        results = set(tqdm.tqdm(pool.imap_unordered(finder_HU, values, chunksize=chunksize), total=length))
                    pool.close()
                    pool.join()
                print('Unique {} length words generated: {}'.format(i, len(results)))
                textperm |= results
                print('Unique words generated so far: {}'.format(len(textperm)))
            return textperm
    else:
        print('ERROR: Word length parameter less than 2!')

def word_check(owntiles, l, s, lang):
    if l >= 2:
        workers = multiprocessing.cpu_count()
        if s:
            if __name__ == "__main__":
                print("Estimating batch length...")
                length = len(EN_words)
                print(length)
                if lang == 'EN':
                    results = set(checker(owntiles, EN_words, l))
                if lang == 'HU':
                    results = 'lol'
            print('Unique {} length words generated: {}'.format(l, len(results)))
            return results
        else:
            textperm = set()
            for i in range(2, (l+1)):
                if __name__ == "__main__":
                    start_time = timeit.default_timer()
                    print("Estimating batch length...")
                    #pool = multiprocessing.Pool(processes=workers)
                    #length = factorial(len(owntiles)) // factorial(len(owntiles)-i)
                    #print(length)
                    #if i <= 4:
                    #    chunksize = 1000
                    #elif i == 5:
                    #    chunksize = 10000
                    #else:
                    #    chunksize = 20000
                    #values = itertools.permutations(owntiles, r=i)
                    #print(timeit.default_timer() - start_time)
                    if lang == 'EN':
                        #results = set(tqdm.tqdm(pool.imap_unordered(finder_EN, values, chunksize=chunksize), total=length))
                        results = set(checker(owntiles, EN_words, i))
                        print(timeit.default_timer() - start_time)
                    if lang == 'HU':
                        results = set(tqdm.tqdm(pool.imap_unordered(finder_HU, values, chunksize=chunksize), total=length))
                    #pool.close()
                    #pool.join()
                print('Unique {} length words generated: {}'.format(i, len(results)))
                textperm |= results
                print('Unique words generated so far: {}'.format(len(textperm)))
            return textperm
    else:
        print('ERROR: Word length parameter less than 2!')


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


if __name__ == '__main__':
    #console_mode = input("Run without web GUI? (Y/N) ")
    #print(console_mode)
    #if console_mode != ('Y' or 'y'):
    app.run(host='0.0.0.0', debug=True)
    # else:
    #     language = input("Language? (EN/HU) ")
    #     max_word_length = input("Maximum word length? (2+) ")
    #     only_max = input("Calculate only for maximum length? (Y/N) ")
    #     if only_max == ('Y' or 'y'):
    #         only_max = bool(True)
    #     else:
    #         only_max = bool(False)
    #     own_tileset = input("Own tiles? (NO or lowercase alphabets and BLANK for a maximum of 2 blank tiles)")
    #     tiles = build_tileset(language)
    #     tile_draw = []
    #     if own_tileset != 'NO':
    #         hasblank = own_tileset.count('BLANK')
    #         if hasblank >= 1:
    #             own_tileset = own_tileset.replace('BLANK', '')
    #         for i in range(hasblank):
    #             for element in set(tiles[0:-2]):
    #                 own_tileset += str(element)
    #         print(own_tileset)
    #         if language == 'HU':
    #             global hasdigraph
    #             hasdigraph = 0
    #             digraph_count = 0
    #             digraphs = []
    #             for digraph in ('cs', 'gy', 'sz', 'zs', 'ty', 'ly', 'ny'):
    #                 if digraph in own_tileset:
    #                     digraph_count += own_tileset.count(digraph)
    #                     for i in range(digraph_count):
    #                         hasdigraph += 1
    #                         digraphs += digraph
    #                     own_tileset.replace(digraph, '')
    #             for character in own_tileset:
    #                 tile_draw += [character]
    #             tile_draw += digraphs
    #         else:
    #             for character in own_tileset:
    #                 tile_draw += [character]
    #     else:
    #         tile_draw = draw(tiles, 7)
    #     print('Tiles drawn: {}'.format(tile_draw))
    #     valid_words = word_gen_mt(tile_draw, int(max_word_length), only_max, language)
    #     grouped = {}
    #     if valid_words != 'NONE':
    #         scores = score_calc(valid_words, language)
    #         grouped = group_by_score(scores)
    #     else:
    #         grouped = {0: 'Number of valid words found'}
    #     #print(grouped)


    <div class="row">
        {% for col in column_names %}
        <div class="col" style = "text-align: center; font-family: scrabblefont; font-size: 30px; color: rgb(0, 102, 204)">{{col}}</div>
        {% endfor %}
    </div>