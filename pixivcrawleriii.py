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
    select_option       = dl.SELECT_RTN
    rtn_page_opt        = dl.PAGE_ORDINARY
    rtn_rank_opt        = dl.RANK_DAILY
    rtn_sex_opt         = dl.SEX_NORMAL
    ira_illust_id_list  = []

    print(dl.HL_CR(WkvCwApi.__doc__))
    mode_interactive_server = dl.MODE_INTERACTIVE if len(sys.argv) == 1 else dl.MODE_SERVER
    api_instance = WkvCwApi(mode_interactive_server)
    api_instance.wca_camouflage_login()

    while True:
        if mode_interactive_server == dl.MODE_INTERACTIVE:
            select_option = dl.LT_INPUT(dl.HL_CY('login completed, select mode: '))
        else:
            opts, args = getopt.getopt(sys.argv[1:], "hm:r:l:s:i:", ["help", "mode", "R18", "list", "sex", "id"])
            for opt, value in opts:
                if opt in ("-m", "--mode"):
                    select_option       = value
                elif opt in ("-r", "--R18"):
                    rtn_page_opt        = value
                elif opt in ("-l", "--list"):
                    rtn_rank_opt        = value
                elif opt in ("-s", "--sex"):
                    rtn_sex_opt         = value
                elif opt in ("-i", "--id"):
                    ira_illust_id_list  = value.split(',')  # server mode support multi-input id and split with ','
                elif opt in ("-h", "--help"):
                    print(dl.HL_CR(WkvCwApi.__doc__))
                    exit(dl.PUB_E_OK)

        if select_option == dl.SELECT_RTN:
            dl.LT_PRINT(dl.BY_CB('mode: [Ranking Top N]'))
            rtn_instance = rtn(dl.RANK_DIR, dl.LOG_PATH, 
                dl.HTML_PATH, api_instance, mode_interactive_server, 
                rtn_page_opt, rtn_rank_opt, rtn_sex_opt)
            rtn_instance.start()

        elif select_option == dl.SELECT_IRA:
            dl.LT_PRINT(dl.BY_CB('mode: [Illustrator Repository All]'))
            if mode_interactive_server == dl.MODE_SERVER:
                for ira_illust_id in ira_illust_id_list:
                    ira_instance = ira(dl.g_dl_work_dir, dl.LOG_NAME, 
                        dl.HTML_NAME, api_instance, mode_interactive_server, ira_illust_id)
                    ira_instance.start()
            else:
                ira_instance = ira(dl.g_dl_work_dir, dl.LOG_NAME, 
                    dl.HTML_NAME, api_instance, mode_interactive_server, '')
                ira_instance.start()

        elif select_option == dl.SELECT_HELP:
            print(dl.HL_CR(WkvCwApi.__doc__))

        elif select_option == dl.SELECT_EXIT:
            dl.LT_PRINT(dl.BY_CB("user exit program"))
            dl.crawler_logo()         # exit print logo
            exit(dl.PUB_E_OK)

        else:
            dl.nolog_raise_arguerr()

        if mode_interactive_server == dl.MODE_SERVER:
            exit(dl.PUB_E_OK)

if __name__ == '__main__':
    main()
