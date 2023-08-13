from home.models import Kanji, Onyomi, Kunyoumi, Meanings, Post
import csv


def kanji_insert():
    with open('/home/asimsys/Desktop/Project/Kanjimnemonics/data/kanji.csv', 'r') as file:
        reader = csv.reader(file)
        # next(reader)  # Advance past the header

        Kanji.objects.all().delete()
        # Genre.objects.all().delete()

        for row in reader:
            print(row)
            film = Kanji(id=row[0], kanji=row[1], grade=row[2], stroke_count=row[3], frequency=row[4], jlpt=row[5])
            film.save()

def onyomi_insert():
    with open('/home/asimsys/Desktop/Project/Kanjimnemonics/data/onyomi.csv', 'r') as file:
        reader = csv.reader(file)
        Onyomi.objects.all().delete()

        for row in reader:
            print(row)
            film = Onyomi(kanji_key_id=row[0], character=row[1])
            film.save()


def kunyoumi_insert():
    with open('/home/asimsys/Desktop/Project/Kanjimnemonics/data/kunyoumi.csv', 'r') as file:
        reader = csv.reader(file)
        Kunyoumi.objects.all().delete()
        for row in reader:
            print(row)
            film = Kunyoumi(kanji_key_id=row[0], character=row[1])
            film.save()


def words_insert():
    with open('/home/asimsys/Desktop/Project/Kanjimnemonics/data/words.csv', 'r') as file:
        reader = csv.reader(file)
        Meanings.objects.all().delete()

        for row in reader:
            print(row)
            film = Meanings(kanji_key_id=row[0], character=row[1])
            film.save()

def clear_table():
    Post.objects.all().delete()


# kanji_insert()
# onyomi_insert()
# kunyoumi_insert()
# words_insert()
# clear_table()