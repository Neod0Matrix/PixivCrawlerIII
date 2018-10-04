#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# callable package class

import dataload                                     # call data collections
from privmatrix import Matrix                       # call private lib function
from modeoption import RankingTop as rtn            # call ranking top mode
from modeoption import RepertoAll as ira            # call illustrator repo mode

def main():
    """main() function

    :return:    none
    """
    print(Matrix.__doc__)
    # program work continue ask
    ask_res = dataload.logtime_input('%s lanuch, continue? (Y/N): ' % dataload.PROJECT_NAME)
    if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
        dataload.logtime_print("User exit program\n")
        exit(0)
    ask_res = dataload.logtime_input(
        'Crawler will use your Pixiv-ID and password to login to the website, agree? (Y/N): ')
    if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
        dataload.logtime_print("No ID and password crawler cannot work, exit")
        exit(0)
    
    myPrivMatrix = Matrix()         # instance class to a object
    myPrivMatrix.camouflage_login() # user agree input id and password, crawler simulated login
    # multiple task cycles
    while True:
        mode = dataload.logtime_input('Login finished, select mode: ')
        # ranking top N mode
        if mode == 'rtn' or mode == '1':
            rtn_instance = rtn(dataload.RANK_DIR, dataload.LOG_PATH, 
                dataload.HTML_PATH, myPrivMatrix)
            rtn_instance.start()
        # illustrator repositories all mode
        elif mode == 'ira' or mode == '2':
            ira_instance = ira(dataload.REPO_DIR, dataload.LOG_NAME, 
                dataload.HTML_NAME, myPrivMatrix)
            ira_instance.start()
        # help page
        elif mode == 'help' or mode == '3':
            print(Matrix.__doc__)
        # user normal exit program
        elif mode == 'exit' or mode == '4':
            dataload.logtime_print("User exit program\n")
            exit(0)
        # input parameter error
        else:
            dataload.logtime_print("Argument(s) error\n")

if __name__ == '__main__':
    main()

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
