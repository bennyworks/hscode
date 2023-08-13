# -*- coding: utf-8 -*-
"""
    Write rows to files
"""
import os


def check_directory(root_dir, write_to_latest=False):
    """
        Check whether the directories exist
    """
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    if write_to_latest:
        latest_dir = os.path.join(root_dir, 'latest')
        if not os.path.exists(latest_dir):
            os.makedirs(latest_dir)


def write(root_dir, chapter, row, write_to_latest=False):
    """
        Write to the file
    """
    check_directory(root_dir, write_to_latest)
    file_name = 'hscode_' + chapter + '.txt'

    row_str = "{}".format(row)
    content = row_str + '\r\n'

    with open(os.path.join(root_dir, 'latest', file_name), 'a') as file:
        file.writelines(content)


def write_ok(root_dir, chapter):
    """
        创建章节海关编码详情爬取成功结束文件，即OK文件
    """
    file_name = 'hscode_' + chapter + '.ok'
    with open(os.path.join(root_dir, 'latest', file_name), 'w'):
        pass


def write_cases(root_dir, chapter, rows):
    """
        Write cases to the file
    """
    rows_str = ["{}".format(row) for row in rows]
    content = "\r\n".join(rows_str) + "\r\n"

    latest_name = 'hscode_case_' + chapter + '.txt'
    with open(os.path.join(root_dir, 'latest', latest_name), 'a') as file:
        file.writelines(content)


def write_cases_ok(root_dir, chapter):
    """
        创建申报实例抓取成功结束文件，即OK文件
    """
    latest_name = 'hscode_case_' + chapter + '.ok'
    with open(os.path.join(root_dir, 'latest', latest_name), 'w') as file:
        pass


def write_exception_hscode(root_dir, chapter, hscode):
    """
        保存运行中断时正在爬取的hscode，用于处理中断重爬
    """
    file_name = 'hscode_exception_' + chapter + '.txt'
    with open(os.path.join(root_dir, file_name), 'w') as file:
        file.writelines(hscode)


def remove_exception_hscode(root_dir, chapter):
    """
        保存运行中断时正在爬取的hscode，用于处理中断重爬
    """
    file_name = 'hscode_exception_' + chapter + '.txt'
    file_path = os.path.join(root_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def write_exception_hscode_case(root_dir, chapter, hscode):
    """
        保存运行中断时正在爬取申报实例的hscode，用于处理中断重爬
    """
    file_name = 'hscode_case_exception_' + chapter + '.txt'
    with open(os.path.join(root_dir, file_name), 'w') as file:
        file.writelines(hscode)


def remove_exception_hscode_case(root_dir, chapter):
    """
        保存运行中断时正在爬取申报实例的hscode，用于处理中断重爬
    """
    file_name = 'hscode_case_exception_' + chapter + '.txt'
    file_path = os.path.join(root_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
