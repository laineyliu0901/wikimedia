import argparse
import sys
import cmd
import os
import pandas as pd
import datetime
import gzip
import sqlite3
import urllib.request

from user import User
from logger import logger
from inputdata import InputData
from const import BASEURL
from utils import get_file_from_pattern, check_pattern, move_file


def main():
    parser = argparse.ArgumentParser(
        description='A tool to merge two data',
        usage='''merge two data sets

        Please input the following in order:
        year
        month
        day
        hour

        ''')
    # 4 INPUTS TO REQUEST DATA
    parser.add_argument(
        'year', type=int,
        help='the year of the data you want to retrieve',
        choices=list(range(2007, 2017)))

    parser.add_argument(
        'month', type=int,
        help='the month of the data you want to retrieve')

    parser.add_argument(
        'day', type=int,
        help='the day of the data you want to retrievee')

    # improvement: to make it, so we can have an inteval of hours
    parser.add_argument(
        'hour', type=int,
        help='the nth hour of the data you want to retrieve')

    arg = parser.parse_args()
    # check if the date you provide is valid
    try:
        newDate = datetime.datetime(
            arg.year,
            arg.month,
            arg.day,
            arg.hour-1)

    except ValueError:
        logger.error('Invalid date/time input!!!')
        parser.print_help()
        exit(1)

    # GETTING THE FILE NAME FROM THE INPUT
    monthURL = BASEURL + newDate.strftime("%Y/%Y-%m/")
    file_pattern = newDate.strftime("pagecounts-%Y%m%d-%H")

    # check in the file is already in the database

    # check if the file is already downloaded but not in the database
    if check_pattern("./history", file_pattern) > 0:
        logger.info('the file is already downloaded and ingested')
        file_name = get_file_from_pattern("./history", file_pattern)

    elif check_pattern("./waiting", file_pattern) > 0:
        logger.info('the file is already downloaded and not yet ingested')
        file_name = get_file_from_pattern("./waiting", file_pattern)

    else:

        logger.info('the file is not downloaded')
        # some file is ending with 0001
        fileURL = file_pattern + "0000.gz"
        outFilePath = fileURL[:-3]
        download_wikimedia(monthURL + fileURL, outFilePath)
        move_downloaded_file(outFilePath)
        file_name = outFilePath+'.txt'

    input_data = InputData(newDate, file_name, top=10)

    User(input_data).cmdloop()
    return


def download_wikimedia(totalURL, outFilePath):
    response = urllib.request.urlopen(totalURL)
    logger.info('downloading the file.......')
    with open(outFilePath, 'wb') as outfile:
        outfile.write(gzip.decompress(response.read()))
    logger.info('file downloaded!!!!')
    return


def move_downloaded_file(outFilePath):
    src = outFilePath
    dst = './waiting/'+outFilePath+'.txt'
    move_file(src, dst)
    return

if __name__ == "__main__":
    main()
