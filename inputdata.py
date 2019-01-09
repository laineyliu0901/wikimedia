import pandas as pd
import sqlite3
import cmd
import os
from const import DB_PATH, DB_NAME
from logger import logger
from utils import move_file


class InputData(object):
    def __init__(self, newDate, file_name, top):
        self.file_name = file_name
        self.df = clean_before_ingest(
            read_file(file_name), newDate)
        self.top = top
        self.tops_by_language = self._get_language_analysis()

    def ingest_input_file(self):
        if './history' in self.file_name:
            logger.warning(
                'the data should be ingested already! check database!')
        else:
            # make sure the directory exist
            os.makedirs(DB_PATH, exist_ok=True)
            # connect to the database
            db = sqlite3.connect(DB_PATH + DB_NAME + '.sqlite3')
            # if the table does not exist, create one
            db.execute('CREATE TABLE IF NOT EXISTS wikimedia (id integer primary key autoincrement not null, language STRING, page_name STRING, non_unique_views INTEGER, timestamp TEXT, last_update datetime default current_timestamp )')

            # insert the new data
            logger.info('ingesting the new data.....')
            db.executemany(
                "insert into wikimedia(language, page_name, non_unique_views, timestamp) values (?, ?, ?, ?)",
                [tuple(x) for x in self.tops_by_language .values])
            db.commit()
            db.close()
            logger.info('finished ingesting the new data!')

            # move the file from waiting to history
            src = self.file_name
            dst = './history/'+self.file_name.split('/')[-1]
            logger.info('moved the new data to history file!')
            move_file(src, dst)
        return

    def _get_language_analysis(self):
        tops_by_language = self.df.sort_values(
            ['language', 'non_unique_views'],
            ascending=[True, False]
            ).groupby(
            'language').head(self.top).reset_index(drop=True)
        return tops_by_language

    def get_analysis(self, language_):
        return self.tops_by_language[self.tops_by_language['language'] == language_]


def read_file(file_name):
    logger.info('reading the file..........')

    df = pd.read_csv(
        file_name,
        sep=' ',
        encoding='latin-1',
        header=None)

    df.columns = [
        'language', 'page_name',
        'non_unique_views', 'bytes_transferred']
    return df


def clean_before_ingest(df, newDate):
    df = df[~df['page_name'].str.contains(
        ":", na=False
        )].dropna(
        subset=['language']
        ).reset_index(drop=True)
    """
    in case you need to consider the type of the page
    df['type'] = [i.split('.')[1] if len(
        i.split('.')) == 2 else np.nan for i in df['language']]
        """
    df['language'] = [i.split('.')[0] for i in df['language']]
    df['timestamp'] = newDate.strftime("%Y/%m/%d %H")

    return df.drop(['bytes_transferred'], axis=1)
