#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# callable package class

import dataload                                     # call data collections
from privmatrix import PixivAPILib                  # call API library class
from modeoption import RankingTop as rtn            # call ranking top mode
from modeoption import RepertoAll as ira            # call illustrator repo mode

def main():
    """main() function

    Get user input arguments and launch mode function
    :return:    none
    """
    print(PixivAPILib.__doc__)
    # program work continue ask
    ask_res = dataload.logtime_input('%s lanuch, continue? (Y/N): ' % dataload.PROJECT_NAME)
    if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
        dataload.logtime_print("User exit program\n")
        exit(0)
    # website id and password require
    ask_res = dataload.logtime_input(
        'Crawler will use your Pixiv-ID and password to login to the website, agree? (Y/N): ')
    if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
        dataload.logtime_print("No ID and password crawler cannot work, exit")
        exit(0)
    
    api_instance = PixivAPILib()        # instance class to a object
    api_instance.camouflage_login()     # crawler simulated login
    # multiple task cycles
    while True:
        mode = dataload.logtime_input('Login finished, select mode: ')
        # ranking top N mode
        if mode == 'rtn' or mode == '1':
            dataload.logtime_print('Mode: [Ranking Top N]')
            rtn_instance = rtn(dataload.RANK_DIR, dataload.LOG_PATH, 
                dataload.HTML_PATH, api_instance)
            rtn_instance.start()
        # illustrator repositories all mode
        elif mode == 'ira' or mode == '2':
            dataload.logtime_print('Mode: [Illustrator Repository All]')
            ira_instance = ira(dataload.REPO_DIR, dataload.LOG_NAME, 
                dataload.HTML_NAME, api_instance)
            ira_instance.start()
        # help page
        elif mode == 'help' or mode == '3':
            print(PixivAPILib.__doc__)
        # user normal exit program
        elif mode == 'exit' or mode == '4':
            dataload.logtime_print("User exit program")
            dataload.crawler_logo()         # exit print logo
            exit(0)
        # input parameter error, into next circle
        else:
            dataload.logtime_print("Argument(s) error")

if __name__ == '__main__':
    main()

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
