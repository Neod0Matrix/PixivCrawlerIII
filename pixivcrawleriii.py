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
    mode_interactive_server = dl.MODE_INTERACTIVE   # default

    if len(sys.argv) == 1:
        mode_interactive_server = dl.MODE_INTERACTIVE
        # program work continue ask
        ask_res = dl.LT_INPUT(dl.HL_CY('%s lanuch, continue? (Y/N): ' % dl.PROJECT_NAME))
        if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
            dl.LT_PRINT(dl.BY_CB("User exit program\n"))
            exit(dl.PUB_E_OK)

        # website id and password require
        ask_res = dl.LT_INPUT(dl.HL_CY('crawler will use your Pixiv-ID and password to login to the website, agree? (Y/N): '))
        if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
            dl.LT_PRINT(dl.BR_CB("No ID and password crawler cannot work, exit"))
            exit(dl.PUB_E_PARAM_FAIL)

        api_instance = WkvCwApi(mode_interactive_server)    # instance class to a object
        api_instance.wca_camouflage_login()                 # crawler simulated login
        # multiple task cycles
        while True:
            mode = dl.LT_INPUT(dl.HL_CY('login completed, select mode: '))
            # ranking top N mode
            if mode == dl.SELECT_RTN:
                dl.LT_PRINT(dl.BY_CB('Mode: [Ranking Top N]'))
                rtn_instance = rtn(dl.RANK_DIR, dl.LOG_PATH, 
                    dl.HTML_PATH, api_instance, mode_interactive_server)
                rtn_instance.start()
            # illustrator repositories all mode
            elif mode == dl.SELECT_IRA:
                dl.LT_PRINT(dl.BY_CB('Mode: [Illustrator Repository All]'))
                ira_instance = ira(dl.g_dl_work_dir, dl.LOG_NAME, 
                    dl.HTML_NAME, api_instance, mode_interactive_server)
                ira_instance.start()
            # help page
            elif mode == dl.SELECT_HELP:
                print(dl.HL_CR(WkvCwApi.__doc__))
            # user normal exit program
            elif mode == dl.SELECT_EXIT:
                dl.LT_PRINT(dl.BY_CB("User exit program"))
                dl.crawler_logo()         # exit print logo
                exit(dl.PUB_E_OK)
            # input parameter error, into next circle
            else:
                dl.nolog_raise_arguerr()
    else:
        mode_interactive_server = dl.MODE_SERVER
        # argument pass to variable
        opts, args = getopt.getopt(sys.argv[1:], "hm:r:l:s:i:", ["help", "mode", "R18", "list", "sex", "id"])
        # default value
        select_option   = dl.SELECT_RTN
        rtn_page_opt    = dl.PAGE_ORDINARY
        rtn_rank_opt    = dl.RANK_DAILY
        rtn_sex_opt     = dl.SEX_NORMAL
        ira_illust_id   = ''

        for opt, value in opts:
            if opt in ("-m", "--mode"):
                select_option = value
            elif opt in ("-r", "--R18"):
                rtn_page_opt = value
            elif opt in ("-l", "--list"):
                rtn_rank_opt = value
            elif opt in ("-s", "--sex"):
                rtn_sex_opt = value
            elif opt in ("-i", "--id"):
                ira_illust_id = value
            elif opt in ("-h", "--help"):
                print(dl.HL_CR(WkvCwApi.__doc__))
                exit(dl.PUB_E_OK)

        api_instance = WkvCwApi(mode_interactive_server)    # instance class to a object
        api_instance.wca_camouflage_login()                 # crawler simulated login

        if select_option == dl.SELECT_RTN:
            dl.LT_PRINT(dl.BY_CB('Mode: [Ranking Top N]'))
            rtn_instance = rtn(dl.RANK_DIR, dl.LOG_PATH, 
                dl.HTML_PATH, api_instance, mode_interactive_server, 
                rtn_page_opt, rtn_rank_opt, rtn_sex_opt)
            rtn_instance.start()
        # illustrator repositories all mode
        elif select_option == dl.SELECT_IRA:
            dl.LT_PRINT(dl.BY_CB('Mode: [Illustrator Repository All]'))
            ira_instance = ira(dl.g_dl_work_dir, dl.LOG_NAME, 
                dl.HTML_NAME, api_instance, mode_interactive_server, ira_illust_id)
            ira_instance.start()
        # help page
        elif select_option == dl.SELECT_HELP:
            print(dl.HL_CR(WkvCwApi.__doc__))

if __name__ == '__main__':
    main()
