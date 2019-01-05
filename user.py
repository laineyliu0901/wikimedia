import pandas as pd
import numpy as np
import cmd
from os import path


class User(cmd.Cmd):

    def __init__(self, InputData):

        cmd.Cmd.__init__(self)
        self.InputData = InputData

    intro = 'Welcome to the interface! Type help or ?.\n'
    prompt = '(wiki media)'
    file = None

    def do_ingest(self, arg):
        self.InputData.ingest_input_file()

    def do_get_full_analysis(self, arg):
        print(self.InputData.tops_by_language)
        return

    def do_get_specific_analysis(self, arg):
        print(self.InputData.get_analysis(*parse_str(arg))) 
        return

    def do_exit(self, arg):
        return True


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

def parse_str(arg):
    return list(map(str, arg.split()))
