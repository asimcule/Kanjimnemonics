import csv
import re


# ,literal,grade,stroke_counts,freq,jlpt,ja_ons,ja_kuns,meanings,example,example_translation
main = open('kanji_data.csv', 'r')
kanji = open('kanji.csv', 'w')
onyomi = open('onyomi.csv', 'w')
kunyoumi = open('kunyoumi.csv', 'w')
words = open('words.csv', 'w')
kanji_data = []
onyomi_data = []
kunyoumi_data = []
words_data = []

kanji_writer = csv.writer(kanji)
onyomi_writer = csv.writer(onyomi)
kunyoumi_writer = csv.writer(kunyoumi)
words_writer = csv.writer(words)

csv_reader = csv.reader(main)
for item in csv_reader:
    kanji_data = [int(item[0]), item[1], int(float(item[2])), int(item[3]), int(item[4]), int(float(item[5]))] 
    kanji_writer.writerow(kanji_data)
    # cleaning up onyoumi
    on = re.sub('["\[\]]', '', item[6])
    on = on.split(", ")
    for char in on:
        # if char == "":
        #     onyomi_writer.writerow([int(item[0]), 0])
        #     continue
        onyomi_writer.writerow([int(item[0]), char.replace("'", "")])
    # cleaning kunyoumi
    kun = re.sub('["\[\]]', '', item[7])
    kun = kun.split(", ")
    for char in kun:
        # if char == "":
        #     kunyoumi_writer.writerow([int(item[0]), 0])
        #     continue
        kunyoumi_writer.writerow([ int(item[0]), char.replace("'", "")])
    # cleaning words
    meaning = re.sub('["\[\]]', '', item[8])
    meaning = meaning.split(", ")
    for char in meaning:
        words_writer.writerow([int(item[0]), char.replace("'", "")])
