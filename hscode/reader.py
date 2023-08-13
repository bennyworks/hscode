# -*- coding: utf-8 -*-
"""
    Write rows to files
"""
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


def read_exception_hscode(root_dir, chapter):
    """
        保存运行中断时正在爬取的hscode，用于处理中断重爬
    """
    hscode = False
    file_name = 'hscode_exception_' + chapter + '.txt'
    file_path = os.path.join(root_dir, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            hscode = file.readline()
            if len(hscode) == 0:
                return False

    return hscode


def read_exception_hscode_case(root_dir, chapter):
    """
        保存运行中断时正在爬取的hscode，用于处理中断重爬
    """
    hscode = False
    file_name = 'hscode_case_exception_' + chapter + '.txt'
    file_path = os.path.join(root_dir, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            hscode = file.readline()
            if len(hscode) == 0:
                return False

    return hscode