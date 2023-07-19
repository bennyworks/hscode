# -*- coding: utf-8 -*-
"""
    Write rows to files
"""
import time
import os
import json


def read(root_dir, chapter):
    """
        Write to the file
    """
    latest_name = 'hscode_' + chapter + '.txt'
    file_path = os.path.join(root_dir, 'latest', latest_name)

    hscodes = []
    with open(file_path, 'r') as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break

            json_obj = json.loads(line)
            hscode = json_obj.get('code')
            hscodes.append(hscode)

    return hscodes
