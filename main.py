"""
    https://www.hsbianma.com/ 用于爬取海关编码及其详情
    https://www.365area.com/ 用于爬取海关编码的申报实例

    海关编码爬虫程序
    参数列表：
        --help或-h：查看帮助信息
        --search或-s [chapter]：爬取具体章节(商品编码前两位)的内容，默认01
        --hscode-case: 爬取具体章节的商品编码的申报实例，配合 -s 使用
        --all或-a：爬取所有章节的内容。该开关开启时，-s 无效
        --file-root [dir]: 设置保存文件的根路径，默认值[HOME]/hascode_file。\
          文件命名hscode_[chapter]_YYYYMMDD_HH:mm.txt，以及hscode_[chapter]_latest.txt
        --no-latest：不生成(或覆盖原有的)latest文件
        --quiet或-q：静默模式，不打印海关编码信息
        --proxy或-p [proxy-url]: 使用请求代理
    @author zhy
    @version 1.2
"""
import sys
import json
from hscode import argument
from hscode.spider import search_chapter_hscodes, search_cases, parse_details
from hscode.writter import (write, write_ok,
                            write_cases, write_cases_ok,
                            write_exception_hscode, remove_exception_hscode,
                            write_exception_hscode_case, remove_exception_hscode_case)
from hscode.reader import read, read_exception_hscode, read_exception_hscode_case


def search_and_save(chapter, args):
    """
        Search and save
    """
    include_outdated = args.outdated
    quiet = args.quiet_mode
    proxy = args.url_proxy
    # 爬取所有海关编码的详情
    search_chapter(chapter, args, include_outdated, quiet, proxy)


def search_case_and_save(chapter, args):
    """
        搜索商品编码申报实例并保存
    """

    # 检查是否有运行中断文件，有则充运行中断文件中读取中断hscode，重新进行爬取
    exception_hscode = read_exception_hscode_case(args.file_root, chapter)
    # 读取最新的章节商品编码
    hscodes = read(args.file_root, chapter)
    # 将hscode列表按照数值从小到大进行排序
    hscodes.sort()
    for hscode in hscodes:
        # 运行中断位置前的hscode详情不需要重复爬取，直接跳过
        if exception_hscode and exception_hscode > hscode:
            continue

        try:
            cases = search_cases(hscode)
        except Exception:
            # 保存运行中断时的hscode
            write_exception_hscode_case(args.file_root, chapter, hscode)
            raise Exception

        write_cases(args.file_root, chapter, cases)

    write_cases_ok(args.file_root, chapter)
    remove_exception_hscode_case(args.file_root, chapter)


def search_chapter(chapter, args, include_outdated, quiet, proxy=None):
    """
        爬取海关编码详情
    """
    # 检查是否有运行中断文件，有则充运行中断文件中读取中断hscode，重新进行爬取
    exception_hscode = read_exception_hscode(args.file_root, chapter)
    # 找出章节的所有海关编码
    all_code = search_chapter_hscodes(chapter, include_outdated, quiet, proxy)
    for code in all_code:
        # 运行中断位置前的hscode详情不需要重复爬取，直接跳过
        if exception_hscode and exception_hscode > code:
            continue

        try:
            # 解析海关编码
            hscode_detail = parse_details(code, proxy)
        except Exception:
            # 保存运行中断时的hscode
            write_exception_hscode(args.file_root, chapter, code)
            raise Exception

        # 检验是否合法json
        hscode_str = str(hscode_detail)
        json.loads(hscode_str)

        write(args.file_root, chapter, hscode_detail, not args.no_latest)

        if not quiet:
            print('searching "' + chapter + '"'
                  + ' hscode: ' + code)

    write_ok(args.file_root, chapter)
    remove_exception_hscode(args.file_root, chapter)


def main():
    """
        Entrance
    """
    args = argument.parse_argv(sys.argv)

    if args.print_help:
        argument.print_help()
        return
    # 搜索条件
    chapter = args.chapter
    # 是否爬取所有页面
    all_search = args.all_chapters
    # 是否爬取对应章的hscode的申报实例

    if all_search:
        # 01-09
        for i in range(1, 10):
            chapter = '0' + str(i)
            search_and_save(chapter, args)
        # 10-99
        for i in range(10, 100):
            search_and_save(str(i), args)
    elif args.hscode_case:
        search_case_and_save(str(chapter), args)
    else:
        search_and_save(str(chapter), args)


main()
