"""
    https://www.hsbianma.com/ 用于爬取海关编码及其详情
    https://www.365area.com/ 用于爬取海关编码的申报实例 

    海关编码爬虫程序
    参数列表：
        --help或-h：查看帮助信息
        --search或-s [chapter]：爬取具体章节(商品编码前两位)的内容，默认01
        --hscode-case [hscode]: 爬取具体章节的商品编码的申报实例,如果[hscode]有值，则从该商品编码开始爬取，配合 -s 使用
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
from hscode import argument
from hscode.spider import search_chapter, search_cases
from hscode.writter import write, write_cases, write_cases_ok
from hscode.reader import read


def search_and_save(chapter, args):
    """
        Search and save
    """
    include_outdated = args.outdated
    quiet = args.quiet_mode
    proxy = args.url_proxy
    hscodes = search_chapter(chapter, include_outdated, quiet, proxy)
    write(args.file_root, chapter, hscodes, not args.no_latest)


def search_case_and_save(chapter, args):
    """
        搜索商品编码申报实例并保存
    """
    # 读取最新的章节商品编码
    hscodes = read(args.file_root, chapter)
    for hscode in hscodes:
        if type(args.hscode_case) is not bool and hscode < args.hscode_case:
            continue
        cases = search_cases(hscode)
        write_cases(args.file_root, chapter, cases)

    write_cases_ok(args.file_root, chapter)


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
