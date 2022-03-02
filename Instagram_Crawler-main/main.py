# -*- coding:utf-8 -*-

import argparse
from instagram_crawler.metadata import EXTRACT_NUM, LOGIN_OPTION, SAVE_FILE_NAME, SAVE_FILE_NAME_TAG, DRIVER_PATH, INSTAGRAM_ID_FORM_NAME, INSTAGRAM_PW_FORM_NAME, HASH_TAG, ID, password
from instagram_crawler.extract_data import crawling_instagram


parser = argparse.ArgumentParser(description='Crawling Instagram Post - Comment',
                                 formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("--driver_path",
                        default=DRIVER_PATH,
                        help="./chromedriver.exe",
                         type=str)

    parser.add_argument("--id", 
                        help="uuu.wqr",
                        default=ID,
                        type=str)

    parser.add_argument("--password", 
                        help="h9e8e1s2o3o1",
                        default=password,
                        type=str)

    parser.add_argument("--hash_tag", 
                        help="데일리룩",
                        default=HASH_TAG,
                        type=str)

    parser.add_argument("--display",
                        help="1",
                        default= 1,
                        type=int)


    parser.add_argument("--extract_num", 
                        help="3",
                        default=EXTRACT_NUM, type=int)

    parser.add_argument("--login_option", 
                        help="instagram",
                        default=LOGIN_OPTION, type=str)

    parser.add_argument("--extract_file",
                        help="i",
                        default=SAVE_FILE_NAME, type=str)

    parser.add_argument("--extract_tag_file",
                        help="o",
                        default=SAVE_FILE_NAME_TAG, type=str)

    _args = parser.parse_args()

    return _args


def instagram_main():
    args = get_arguments()
    is_file_save, is_tag_file_save = crawling_instagram(args=args)

    if is_file_save:
        print("file save success - {}".format(args.extract_file))

    if is_tag_file_save:
        print("file save success - {}".format(args.extract_tag_file))


if __name__ == "__main__":
    instagram_main()
