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

    mode = dataload.logtime_input('Select mode: ')
    if mode == 'rtn' or mode == '1':
        build_task = rtn(
            dataload.RANK_DIR, 
            dataload.LOG_PATH, 
            dataload.HTML_PATH)
        build_task.start()
    elif mode == 'ira' or mode == '2':
        build_task = ira(
            dataload.REPO_DIR, 
            dataload.LOG_NAME, 
            dataload.HTML_NAME)
        build_task.start()
    elif mode == 'help' or mode == '3':
        print(Matrix.__doc__)
    elif mode == 'exit' or mode == '4':
        exit(0)
    else:
        dataload.logtime_print("Argument(s) error\n")

if __name__ == '__main__':
    main()

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
