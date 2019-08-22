#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright(C) 2018-2019 T.WKVER | </MATRIX>. All rights reserved.
# code by </MATRIX>@Neod Anderjon(LeaderN)
#
# pixivcrawleriii.py
# Original Author: Neod Anderjon(1054465075@qq.com/EnatsuManabu@gmail.com), 2018-3-10
#
# PixivCrawlerIII part
# T.WKVER crawler main callable file for PixivCrawlerIII project
# Callable package class
#
# History
#
# 2.9.9 LTE     Neod Anderjon, 2019-08-15
#               Refactor names all of this project
#               Complete comment stadard

import sys, getopt
import dataload                                     # call data collections
from wkvcwapi import WkvCwApi                       # call API library class
from modeoption import RankingTop as rtn            # call ranking top mode
from modeoption import RepertoAll as ira            # call illustrator repo mode

def main():
    """main() function

    Get user input arguments and launch mode function
    :return:    none
    """

    print(dataload.set_pcode_red(
        WkvCwApi.__doc__))
    mode_interactive_server = 1                     # intercative mode or server mode, default interavtive mode(1)
    # judge the count of command line argument
    # if no external arguments, into interactive mode
    if len(sys.argv) == 1:
        mode_interactive_server = 1
        # program work continue ask
        ask_res = dataload.logtime_input(dataload.set_pcode_yellow(
            '%s lanuch, continue? (Y/N): ' % dataload.PROJECT_NAME))
        if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
            dataload.logtime_print(dataload.set_pcode_blue_pback_yellow(
                "User exit program\n"))
            exit(0)

        # website id and password require
        ask_res = dataload.logtime_input(dataload.set_pcode_yellow(
            'Crawler will use your Pixiv-ID and password to login to the website, agree? (Y/N): '))
        if ask_res == 'N' or ask_res == 'No' or ask_res == 'n':
            dataload.logtime_print(dataload.set_pback_red(
                "No ID and password crawler cannot work, exit"))
            exit(-1)
        
        api_instance = WkvCwApi(mode_interactive_server) # instance class to a object
        api_instance.wca_camouflage_login()                     # crawler simulated login
        # multiple task cycles
        while True:
            mode = dataload.logtime_input(dataload.set_pcode_yellow(
                'Login finished, select mode: '))
            # ranking top N mode
            if mode == 'rtn' or mode == '1':
                dataload.logtime_print(dataload.set_pcode_blue_pback_yellow(
                    'Mode: [Ranking Top N]'))
                rtn_instance = rtn(dataload.RANK_DIR, dataload.LOG_PATH, 
                    dataload.HTML_PATH, api_instance, mode_interactive_server)
                rtn_instance.start()
            # illustrator repositories all mode
            elif mode == 'ira' or mode == '2':
                dataload.logtime_print(dataload.set_pcode_blue_pback_yellow(
                    'Mode: [Illustrator Repository All]'))
                ira_instance = ira(dataload.REPO_DIR, dataload.LOG_NAME, 
                    dataload.HTML_NAME, api_instance, mode_interactive_server)
                ira_instance.start()
            # help page
            elif mode == 'help' or mode == '3':
                print(dataload.set_pcode_red(
                    WkvCwApi.__doc__))
            # user normal exit program
            elif mode == 'exit' or mode == '4':
                dataload.logtime_print(dataload.set_pcode_blue_pback_yellow(
                    "User exit program"))
                dataload.crawler_logo()         # exit print logo
                exit(0)
            # input parameter error, into next circle
            else:
                dataload.nolog_raise_arguerr()
    else:
        mode_interactive_server = 2
        # argument pass to variable
        opts, args = getopt.getopt(sys.argv[1:], \
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
                print(dataload.set_pcode_red(
                    WkvCwApi.__doc__))
                exit(0)
    
        api_instance = WkvCwApi(mode_interactive_server) # instance class to a object
        api_instance.wca_camouflage_login()                     # crawler simulated login

        if catch_mode == '1':
            dataload.logtime_print(dataload.set_pcode_blue_pback_yellow(
                'Mode: [Ranking Top N]'))
            rtn_instance = rtn(dataload.RANK_DIR, dataload.LOG_PATH, 
                dataload.HTML_PATH, api_instance, mode_interactive_server, 
                rtn_r18_opt, rtn_list_type, rtn_mf_word)
            rtn_instance.start()
        # illustrator repositories all mode
        elif catch_mode == '2':
            dataload.logtime_print(dataload.set_pcode_blue_pback_yellow(
                'Mode: [Illustrator Repository All]'))
            ira_instance = ira(dataload.REPO_DIR, dataload.LOG_NAME, 
                dataload.HTML_NAME, api_instance, mode_interactive_server, ira_illust_id)
            ira_instance.start()
        # help page
        elif catch_mode == 'help' or catch_mode == '3':
            print(dataload.set_pcode_red(
                WkvCwApi.__doc__))

if __name__ == '__main__':
    main()
