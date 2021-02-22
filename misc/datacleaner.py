FILENAME = 'words.txt'  # SCOWL-wl en_US word list
with open(FILENAME, encoding='utf-8') as db:
    EN_words = set(db.read().splitlines())

shortened_wordlist = set()

for word in EN_words:
    if len(word) > 1:
        if "'" not in word:
            shortened_wordlist.add(word.lower())

outfile = list(shortened_wordlist)

with open("Scrabble.txt", "w") as output_file:
    output_file.writelines(line + '\n' for line in sorted(outfile))
