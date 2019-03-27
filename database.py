import sqlite3


def get_words():

    conn = sqlite3.connect('/home/Cynonym/mysite/syndict.db')
    c = conn.cursor()

    command = 'SELECT word FROM words'

    result = [item for sublist in c.execute(command).fetchall() for item in sublist]

    conn.close()

    return result

word_list = get_words()


def find_word(query):

    conn = sqlite3.connect('/home/Cynonym/mysite/syndict.db')
    c = conn.cursor()

    command = 'SELECT * FROM words WHERE word=?'

    result = [item for sublist in c.execute(command, (query,)).fetchall() for item in sublist]

    conn.close()

    if len(result) == 3:
        return {'word': result[0],
                'word_id': result[1],
                'sl_id': result[2]}

    else:
        return None


def find_line(query):

    word = find_word(query)

    if word:

        conn = sqlite3.connect('/home/Cynonym/mysite/syndict.db')
        c = conn.cursor()

        command = 'SELECT * FROM sequences WHERE seq_id=?'

        result = [item for sublist in c.execute(command, (word['sl_id'],)).fetchall() for item in sublist]

        conn.close()

        if len(result) == 10:
            return {'syn_w_marks': result[1],
                    'definition': result[2],
                    'examples': result[3],
                    'exact_defs': result[4],
                    'synt_use': result[5],
                    'sem_use': result[6],
                    'paraphrase': result[7],
                    'antonyms': result[8],
                    'analogues': result[9],
                    'id': result[0]}

        else:
            return None

    else:
        return None
