import sqlite3
import string

db = sqlite3.connect('dict.db')
# NUM_POS_WORDS = db.execute(
#     'SELECT COUNT(*) FROM words WHERE Positive != "0"').fetchone()[0]
# NUM_NEG_WORDS = db.execute(
#     'SELECT COUNT(*) FROM words WHERE Negative != "0"').fetchone()[0]
# TOTAL_WORDS = db.execute('SELECT COUNT(*) FROM words').fetchone()[0]

# p_POS = NUM_POS_WORDS / TOTAL_WORDS
# p_NEG = NUM_NEG_WORDS / TOTAL_WORDS

f_POS = 0.0
for row in db.execute('SELECT "Word Count" FROM words WHERE Positive != "0"'):
    f_POS += float(row[0])

f_NEG = 0.0
for row in db.execute('SELECT "Word Count" FROM words WHERE Negative != "0"'):
    f_NEG += float(row[0])

f_TOT = 0.0
for row in db.execute('SELECT "Word Count" FROM words'):
    f_TOT += float(row[0])

print(f_POS, f_NEG, f_TOT)
# print(db.execute(
#     'SELECT "Word Count" FROM words WHERE Word == "ABANDON"').fetchone()[0])


def analyze(msg):
    tokens = msg.split(' ')
    tokens = [tk.translate(string.maketrans(
        "", ""), string.punctuation).upper() for tk in tokens]

    p_msg_pos = 0.0
    p_msg_neg = 0.0
    p_msg_neut = 0.0
    for word in tokens:
        if db.execute('SELECT "Word Count" FROM words WHERE Word == "' + word + '"').fetchone() is not None:
            if db.execute('SELECT Positive FROM words WHERE Word == "' + word + '"').fetchone()[0] != "0":
                print(word + ': pos')
                p_msg_pos += float(db.execute(
                    'SELECT "Word Count" FROM words WHERE Word == "' + word + '"').fetchone()[0]) / f_POS
            elif db.execute('SELECT Negative FROM words WHERE Word == "' + word + '"').fetchone()[0] != "0":
                print(word + ': neg')
                p_msg_neg += float(db.execute(
                    'SELECT "Word Count" FROM words WHERE Word == "' + word + '"').fetchone()[0]) / f_NEG
            else:
                print(word + ': neut')
                p_msg_neut += float(db.execute('SELECT "Word Count" FROM words WHERE Word == "' + word + '"').fetchone()[
                    0]) / (f_TOT - f_NEG - f_POS)
            print(p_msg_neg, p_msg_neut, p_msg_pos)
