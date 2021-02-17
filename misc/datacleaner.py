filename = 'words.txt'  # SCOWL-wl en_US word list
db = open(filename, encoding='utf-8')
EN_words = set(db.read().splitlines())
db.close()

print(len(EN_words))

newdictionary = set()

for word in EN_words:
    if len(word) > 1:
        if not ("'" in word):
            newdictionary.add(word.lower())

print(len(newdictionary))
outfile = list(newdictionary)
outF = open("myOutFile.txt", "w")
outF.writelines(line + '\n' for line in sorted(outfile))
outF.close()

