#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright(C) 2017-2020 T.WKVER | </MATRIX>. All rights reserved.
# code by </MATRIX>@Neod Anderjon(LeaderN)
#
# pixivcrawleriii.py
# Original Author: Neod Anderjon(1054465075@qq.com/EnatsuManabu@gmail.com), 2018-3-10
#
# PixivCrawlerIII component
# T.WKVER crawler main callable file for PixivCrawlerIII project
# Callable package class

import sys, getopt
import dataload as dl                               # call data collections
from wkvcwapi import WkvCwApi                       # call API library class
from modeoption import RankingTop as rtn            # call ranking top mode
from modeoption import RepertoAll as ira            # call illustrator repo mode

def main():
    """main logic

    Get user input arguments and launch mode function
    :return:    none
    """

    print(dl.HL_CR(WkvCwApi.__doc__))
    mode_interactive_server = 1                     # intercative mode or server mode, default interavtive mode(1)
    # judge the count of command line argument
    # if no external arguments, into interactive mode
    if len(sys.argv) == 1:
        mode_interactive_server = 1
        # program work continue ask
        ask_res = dl.LT_INPUT(dl.HL_CY('%s lanuch, continue? (Y/N): ' % dl.PROJECT_NAME))
        if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
            dl.LT_PRINT(dl.BY_CB("User exit program\n"))
            exit(0)

        # website id and password require
        ask_res = dl.LT_INPUT(dl.HL_CY('Crawler will use your Pixiv-ID and password to login to the website, agree? (Y/N): '))
        if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
            dl.LT_PRINT(dl.BR_CB("No ID and password crawler cannot work, exit"))
            exit(-1)

        api_instance = WkvCwApi(mode_interactive_server)    # instance class to a object
        api_instance.wca_camouflage_login()                 # crawler simulated login
        # multiple task cycles
        while True:
            mode = dl.LT_INPUT(dl.HL_CY('Login finished, select mode: '))
            # ranking top N mode
            if mode == 'rtn' or mode == '1':
                dl.LT_PRINT(dl.BY_CB('Mode: [Ranking Top N]'))
                rtn_instance = rtn(dl.RANK_DIR, dl.LOG_PATH, 
                    dl.HTML_PATH, api_instance, mode_interactive_server)
                rtn_instance.start()
            # illustrator repositories all mode
            elif mode == 'ira' or mode == '2':
                dl.LT_PRINT(dl.BY_CB('Mode: [Illustrator Repository All]'))
                ira_instance = ira(dl.REPO_DIR, dl.LOG_NAME, 
                    dl.HTML_NAME, api_instance, mode_interactive_server)
                ira_instance.start()
            # help page
            elif mode == 'help' or mode == '3':
                print(dl.HL_CR(WkvCwApi.__doc__))
            # user normal exit program
            elif mode == 'exit' or mode == '4':
                dl.LT_PRINT(dl.BY_CB("User exit program"))
                dl.crawler_logo()         # exit print logo
                exit(0)
            # input parameter error, into next circle
            else:
                dl.nolog_raise_arguerr()
    else:
        mode_interactive_server = 2
        # argument pass to variable
        opts, args = getopt.getopt(sys.argv[1:], 
                                "hm:r:l:s:i:", ["help", "mode", "R18", "list", "sex", "id"])
        catch_mode = '1'
        rtn_r18_opt = '1'
        rtn_list_type = '1'
        rtn_mf_word = ''
        ira_illust_id = ''
        for opt, value in opts:
            if opt in ("-m", "--mode"):
                catch_mode = value
            elif opt in ("-r", "--R18"):
                rtn_r18_opt = value
            elif opt in ("-l", "--list"):
                rtn_list_type = value
            elif opt in ("-s", "--sex"):
                rtn_mf_word = value
            elif opt in ("-i", "--id"):
                ira_illust_id = value
            elif opt in ("-h", "--help"):
                print(dl.HL_CR(WkvCwApi.__doc__))
                exit(0)

        api_instance = WkvCwApi(mode_interactive_server)    # instance class to a object
        api_instance.wca_camouflage_login()                 # crawler simulated login

        if catch_mode == '1':
            dl.LT_PRINT(dl.BY_CB('Mode: [Ranking Top N]'))
            rtn_instance = rtn(dl.RANK_DIR, dl.LOG_PATH, 
                dl.HTML_PATH, api_instance, mode_interactive_server, 
                rtn_r18_opt, rtn_list_type, rtn_mf_word)
            rtn_instance.start()
        # illustrator repositories all mode
        elif catch_mode == '2':
            dl.LT_PRINT(dl.BY_CB('Mode: [Illustrator Repository All]'))
            ira_instance = ira(dl.REPO_DIR, dl.LOG_NAME, 
                dl.HTML_NAME, api_instance, mode_interactive_server, ira_illust_id)
            ira_instance.start()
        # help page
        elif catch_mode == 'help' or catch_mode == '3':
            print(dl.HL_CR(WkvCwApi.__doc__))

if __name__ == '__main__':
    main()
