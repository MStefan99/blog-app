import sqlite3
from pathlib import Path


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


path = Path(__file__).parent.parent.joinpath('database', 'db.sqlite')
DATABASE = sqlite3.connect(str(path), check_same_thread=False)  # TODO: check if thread-safe
DATABASE.row_factory = dict_factory
DATABASE.cursor().execute('pragma foreign_keys = on')

COOKIE_NAME = 'MSTID'
