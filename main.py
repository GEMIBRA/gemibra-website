"""
Basic example of a Mkdocs-macros module
"""

import math
import yaml
import os
import csv
import pandas as pd
import json

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    @env.macro
    def get_table_headers():
        print(env.project_dir)
        d = env.project_dir+"/docs/GEMIBRA_2300_V2_19_Sep_2024.csv"
        # d = env.project_dir+"/docs/test.csv"
        reader = csv.DictReader(open(d))
        headers = reader.fieldnames
        print(headers)
        return headers

    @env.macro
    def get_table_rows():
        d = env.project_dir+"/docs/GEMIBRA_2300_V2_19_Sep_2024.csv"
        print(d)
        # d = env.project_dir+"/docs/test.csv"
        data = []
        for i,row in enumerate(csv.reader(open(d))):
            if i==0:
                continue
            data.append(row)

        
        return json.dumps(data)

    
