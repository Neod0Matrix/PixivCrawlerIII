#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# callable package class

import sys, getopt
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
    mode_interactive_server = 1                     # intercative mode or server mode, default interavtive mode(1)
    # judge the count of command line argument
    # if no external arguments, into interactive mode
    if len(sys.argv) == 1:
        mode_interactive_server = 1
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
        
        api_instance = PixivAPILib(mode_interactive_server) # instance class to a object
        api_instance.camouflage_login()                     # crawler simulated login
        # multiple task cycles
        while True:
            mode = dataload.logtime_input('Login finished, select mode: ')
            # ranking top N mode
            if mode == 'rtn' or mode == '1':
                dataload.logtime_print('Mode: [Ranking Top N]')
                rtn_instance = rtn(dataload.RANK_DIR, dataload.LOG_PATH, 
                    dataload.HTML_PATH, api_instance, mode_interactive_server)
                rtn_instance.start()
            # illustrator repositories all mode
            elif mode == 'ira' or mode == '2':
                dataload.logtime_print('Mode: [Illustrator Repository All]')
                ira_instance = ira(dataload.REPO_DIR, dataload.LOG_NAME, 
                    dataload.HTML_NAME, api_instance, mode_interactive_server)
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
    else:
        mode_interactive_server = 2
        # argument pass to variable
        opts, args = getopt.getopt(sys.argv[1:], "hm:r:l:i:", ["help", "mode", "R18", "list", "id"])
        catch_mode = '1'
        rtn_r18_opt = '1'
        rtn_list_type = '1'
        ira_illust_id = ''
        for opt, value in opts:
            if opt in ("-m", "--mode"):
                catch_mode = value
            elif opt in ("-r", "--R18"):
                rtn_r18_opt = value
            elif opt in ("-l", "--list"):
                rtn_list_type = value
            elif opt in ("-i", "--id"):
                ira_illust_id = value
            elif opt in ("-h", "--help"):
                print(PixivAPILib.__doc__)
                exit(0)
    
        api_instance = PixivAPILib(mode_interactive_server) # instance class to a object
        api_instance.camouflage_login()                     # crawler simulated login

        if catch_mode == '1':
            dataload.logtime_print('Mode: [Ranking Top N]')
            rtn_instance = rtn(dataload.RANK_DIR, dataload.LOG_PATH, 
                dataload.HTML_PATH, api_instance, mode_interactive_server, 
                rtn_r18_opt, rtn_list_type)
            rtn_instance.start()
        # illustrator repositories all mode
        elif catch_mode == '2':
            dataload.logtime_print('Mode: [Illustrator Repository All]')
            ira_instance = ira(dataload.REPO_DIR, dataload.LOG_NAME, 
                dataload.HTML_NAME, api_instance, mode_interactive_server, ira_illust_id)
            ira_instance.start()
        # help page
        elif mode == 'help' or mode == '3':
            print(PixivAPILib.__doc__)

if __name__ == '__main__':
    main()

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
