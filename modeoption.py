#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# provide modes setting target object

import re
from prettytable import PrettyTable     # info list package table module
import dataload

class RankingTop(object):
    """Ranking top crawl mode

    Pixiv website has a rank top, ordinary and R18, daily, weekly, monthly
    This class include fuction will gather all of those ranks
    Parameter require: 
        work directory
        log save path
        result html page file save path
        API lib class instance
    """

    def __init__(self, workdir, log_path, html_path, pvmx, ir_mode, rtn_r18_arg='', rtn_rank_type=''):
        """
        :param workdir:         work directory
        :param log_path:        log save path
        :param html_path:       html save path
        :param pvmx:            API library class instance    
        :param ir_mode:         interactive mode or server mode
        :param rtn_r18_arg:     RTN mode set R18 or not
        :param rtn_rank_type:   RTN mode set ranking type
        """
        self.workdir = workdir
        self.logpath = log_path
        self.htmlpath = html_path
        self.pvmx = pvmx
        self.ir_mode = ir_mode
        # class inside global variable
        self.rtn_r18_arg = rtn_r18_arg
        self.rtn_rank_type = rtn_rank_type
        self.target_urls = []
        self.basepages = []  
        
    @staticmethod
    def gather_essential_info(ormode, whole_nbr):
        """Get input image count

        If user input number more than whole number, set target count is whole number
        Only intercative mode call this function
        :param ormode:      select ranktop ordinary or r18 mode
        :param whole_nbr:   whole ranking crawl count
        :return:            crawl images count
        """
        # transfer ascii string to number
        img_cnt = 0
        # choose ordinary artwork images
        if ormode == 'o' or ormode == '1':
            # input a string for request image number
            img_str = dataload.logtime_input(
                'Gather whole ordinary valid target %d, enter you want: '
                % whole_nbr)
        # choose R18 artwork images
        elif ormode == 'r' or ormode == '2':
            # input a string for request image number
            img_str = dataload.logtime_input(
                'Gather whole R18 vaild target %d, enter you want: '
                % whole_nbr)
        # error input
        else:
            dataload.logtime_print("Argument(s) error\n")
            exit(-1)

        # if user input isn't number
        while not img_str.isdigit():
            dataload.logtime_print(
                'Input error, your input content was not a decimal number')
            img_str = dataload.logtime_input(
                'Enter again(max is %d): ' % whole_nbr)
        # check input content is a number
        # if user input number more than limit max, set it to max
        img_cnt = int(img_str)
        if img_cnt > whole_nbr:
            img_cnt = whole_nbr
        elif img_cnt <= 0:
            dataload.logtime_print('What the f**k is wrong with you?')
            exit(-1)

        return img_cnt

    def target_confirm(self):
        """Input option and confirm target

        :return:            request mainpage url, mode
        """

        rank_word, req_url = None, None

        if self.ir_mode == 1:
            log_context = 'Gather ranking list======>'
            self.pvmx.logprowork(self.logpath, log_context)

            ormode = dataload.logtime_input(
                'Select ranking type, ordinary(o|1) or r18(r|2): ')
        elif self.ir_mode == 2:
            ormode = self.rtn_r18_arg

        if ormode == 'o' or ormode == '1':
            if self.ir_mode == 1:
                dwm = dataload.logtime_input(
                    'Select daily(1) | weekly(2) | monthly(3) ordinary ranking type: ')
            elif self.ir_mode == 2:
                dwm = self.rtn_rank_type

            if dwm == '1':
                req_url = dataload.DAILY_RANKING_URL
                rank_word = dataload.DAILY_WORD
            elif dwm == '2':
                req_url = dataload.WEEKLY_RANKING_URL
                rank_word = dataload.WEEKLY_WORD
            elif dwm == '3':
                req_url = dataload.MONTHLY_RANKING_URL
                rank_word = dataload.MONTHLY_WORD
            else:
                dataload.logtime_print("Argument(s) error\n")
            log_context = 'Crawler set target to %s rank top' % rank_word
        elif ormode == 'r' or ormode == '2':
            if self.ir_mode == 1:
                dwm = dataload.logtime_input(
                    'Select daily(1)/weekly(2) R18 ranking type: ')
            elif self.ir_mode == 2:
                dwm = self.rtn_rank_type

            if dwm == '1':
                req_url = dataload.DAILY_RANKING_R18_URL
                rank_word = dataload.DAILY_WORD
            elif dwm == '2':
                req_url = dataload.WEEKLY_RANKING_R18_URL
                rank_word = dataload.WEEKLY_WORD
            else:
                dataload.logtime_print(
                    "Argument(s) error\n")
            log_context = 'Crawler set target to %s r18 rank top' % rank_word
        else:
            dataload.logtime_print("Argument(s) error\n")
            log_context = None
        self.pvmx.logprowork(self.logpath, log_context)

        return req_url, ormode

    def gather_rankingdata(self, option):
        """Crawl dailyRank list

        :param option:      user choose option
        :return:            none
        """
        response = self.pvmx.url_request_handler(
            target_url=option[0],
            post_data=self.pvmx.login_bias[2], 
            timeout=30, 
            target_page_word='Rankpage',
            need_log=True,
            log_path=self.logpath)
        # size info in webpage source
        web_src = response.read().decode("UTF-8", "ignore")
        imgitem_pattern = re.compile(dataload.RANKING_SECTION_REGEX, re.S)
        info_pattern = re.compile(dataload.RANKING_INFO_REGEX, re.S)
        sizer_result = self.pvmx.commit_spansizer(imgitem_pattern, info_pattern, web_src)
        # whole data cache pool
        whole_urls, img_infos = sizer_result[0], sizer_result[1]

        # cut need image count to be target list
        alive_targets = len(whole_urls)
        if self.ir_mode == 1:
            img_nbr = self.gather_essential_info(option[1], alive_targets)
        # server mode directly get all of alive targets
        elif self.ir_mode == 2:
            img_nbr = alive_targets
            dataload.logtime_print('Server mode auto crawl all of alive targets')            
        self.target_urls = whole_urls[:img_nbr]
        log_context = 'Gather rankingtop ' + str(img_nbr) + ', target table:'
        self.pvmx.logprowork(self.logpath, log_context)
        # use prettytable package info list        
        image_info_table = PrettyTable(["ImageNumber", "ImageID", "ImageTitle", 
            "ImageID+PageNumber", "AuthorID", "AuthorName"])
        for k, i in enumerate(img_infos[:img_nbr]):
            # basepage will be a headers referer
            self.basepages.append(dataload.BASEPAGE_URL + i[3])
            image_info_table.add_row([(k + 1), i[3], i[1], 
                self.target_urls[k][57:-4], i[4], i[2]])
        # save table without time header word
        self.pvmx.logprowork(self.logpath, str(image_info_table), 'N')

    def start(self):
        """Call method start()

        First create a task, for example its name is build_task
        Then run build_task.start() to boot this mode
        :return:    none
        """
        self.pvmx.mkworkdir(self.logpath, self.workdir)

        option = self.target_confirm()
        self.gather_rankingdata(option)

        self.pvmx.download_alltarget(self.logpath, self.target_urls, 
            self.basepages, self.workdir)
        self.pvmx.htmlpreview_build(self.workdir, self.htmlpath, self.logpath)

class RepertoAll(object):
    """Crawl any illustrator repertory all artworks

    Every illustrator in Pixiv has own mainpage
    This class include fuction will crawl all of those page all images
    Parameter require: 
        work directory
        log file name
        result html page file name
        API lib class instance
    """

    def __init__(self, workdir, log_name, html_name, pvmx, ir_mode, ext_id=''):
        """
        :param workdir:     work directory
        :param log_name:    log name
        :param html_name:   html name
        :param pvmx:        API library class instance
        :param ir_mode:     interactive mode or server mode
        :param ext_id:      external illustrator id
        """
        if ir_mode == 1:
            target_id = dataload.logtime_input(
                        'Target crawl illustrator pixiv-id: ')
        elif ir_mode == 2:
            target_id = ext_id
        self.user_input_id = target_id
        self.workdir = workdir + 'illustrepo_' + self.user_input_id
        self.logpath = self.workdir + log_name
        self.htmlpath = self.workdir + html_name
        self.pvmx = pvmx
        self.ir_mode = ir_mode
        # class inside call global variable
        self.author_name = None
        self.max_cnt = 0
        self.pure_idlist = []
        self.target_capture = []
        self.basepages = []

    def gather_preloadinfo(self):
        """Crawler need to know how many images do you want

        This function will get author name base on author id
        :return:            none
        """
        # request all of one illustrator's artworks
        response = self.pvmx.url_request_handler(
            target_url=dataload.AJAX_ALL_URL(self.user_input_id),
            post_data=self.pvmx.login_bias[2], 
            timeout=30, 
            target_page_word='Ajaxpage',
            need_log=True,
            log_path=self.logpath)
        # mate illustrator name
        web_src = response.read().decode("UTF-8", "ignore")
        ajax_idlist_pattern = re.compile(dataload.AJAX_ALL_IDLIST_REGEX, re.S)
        ajax_idlist = re.findall(ajax_idlist_pattern, web_src)
        # id list result may include some garbages, use number regex get pure result
        number_pattern = re.compile(dataload.NUMBER_REGEX, re.S)
        for index in ajax_idlist:
            one_pure_id = re.findall(number_pattern, index)
            if one_pure_id:
                self.pure_idlist.append(one_pure_id[0])
            else:
                # very rare error, only happening in this address:
                # https://www.pixiv.net/member_illust.php?id=15115322
                log_context = 'Get ajax page valid info failed, exit'
                self.pvmx.logprowork(self.logpath, log_context)
                exit(-1)

        # use quick-sort algorithm to handle id number
        # descending order sort
        pure_idlist_nbr = []
        for index in self.pure_idlist:
            pure_idlist_nbr.append(int(index))      # string to integer number
        self.pvmx.quick_sort(pure_idlist_nbr, 0, len(pure_idlist_nbr) - 1)
        pure_idlist_nbr.reverse()                   # reverse order
        self.pure_idlist.clear()                         # clear origin list
        for index in pure_idlist_nbr:
            self.pure_idlist.append(str(index))
        del pure_idlist_nbr                         # clear number cache
        self.max_cnt = len(self.pure_idlist)
        
        # get author name from member-main-page
        response = self.pvmx.url_request_handler(
            target_url=dataload.MEMBER_ILLUST_URL + self.user_input_id,
            post_data=self.pvmx.login_bias[2], 
            timeout=30, 
            target_page_word='Mainpage',
            need_log=True,
            log_path=self.logpath)
        # mate illustrator name
        web_src = response.read().decode("UTF-8", "ignore")
        illust_name_pattern = re.compile(dataload.ILLUST_NAME_REGEX, re.S)
        author_info = re.findall(illust_name_pattern, web_src)
        # if login failed, regex parsing result will be a empty list
        if len(author_info) == 0:
            dataload.logtime_print("Regex parsing result error, no author info, exit")
            exit()
        else:
            self.author_name = author_info[0]
        
    def crawl_onepage_data(self, index, index_url):
        """Crawl all target url about images

        :param index:       request page index
        :param index_url:   index group url
        :return:            one page get info list(2-d)
        """
        response = self.pvmx.url_request_handler(
            target_url=index_url,
            post_data=self.pvmx.login_bias[2], 
            timeout=30, 
            target_page_word='Data group %d' % index,
            need_log=True,
            log_path=self.logpath)
        # catch need info from web source
        web_src = response.read().decode("UTF-8", "ignore")
        error_status_pattern = re.compile(dataload.PAGE_REQUEST_SYM_REGEX, re.S)
        error_status = re.findall(error_status_pattern, web_src)[0]
        # page display error is "true" status
        if error_status == 'true':
            log_context = 'Data group %d response failed' % index
            self.pvmx.logprowork(self.logpath, log_context)
            exit(-1)
        # crawl one page items info
        page_target_pattern = re.compile(dataload.PAGE_TARGET_INFO_REGEX, re.S)
        page_target_info_tuple = re.findall(page_target_pattern, web_src)
        # tuple transform to list
        tmp_target_info_list = []
        for i in range(len(page_target_info_tuple)):
            tmp_target_info_list.append([])
            for j in range(len(page_target_info_tuple[i])):
                tmp_target_info_list[i] = list(page_target_info_tuple[i])
        # delete no use info items
        del page_target_info_tuple
        # judge illust type, if it's gif(type symbol: 2), delete this item
        page_target_info_list = []
        illust_type_pattern = re.compile(dataload.ILLUST_TYPE_REGEX, re.S)
        for k in range(len(tmp_target_info_list)):
            illust_type_sym = re.findall(illust_type_pattern, tmp_target_info_list[k][2])
            # regex process result error
            if len(illust_type_sym) == 0:
                log_context = 'Illust type process error, exit!'
                self.pvmx.logprowork(self.logpath, log_context)
                exit(-1)
            # jump gif out
            if illust_type_sym[0] == '2':
                continue
            del tmp_target_info_list[k][2]
            del tmp_target_info_list[k][-2]
            page_target_info_list.append(tmp_target_info_list[k])
        del tmp_target_info_list

        return page_target_info_list 

    def crawl_allpage_target(self):
        """Package all gather urls

        :return:            none
        """
        # calcus nbr need request count
        # each page at most ONE_AUTHOR_MAINPAGE_IMGCOUNT(20181003:48) images
        require_page_cnt = 0
        if self.max_cnt <= dataload.ONE_PAGE_COMMIT:
            require_page_cnt = 1
        else:
            require_page_cnt = int(self.max_cnt / dataload.ONE_PAGE_COMMIT)
            # remainder decision
            if self.max_cnt % dataload.ONE_PAGE_COMMIT != 0:
                require_page_cnt += 1

        # build request url of one page 
        iid_string_tail = ''
        page_url_array = []
        for ix in range(require_page_cnt):
            # tail number limit
            tmp_tail_nbr = dataload.ONE_PAGE_COMMIT * (ix + 1)
            if tmp_tail_nbr > self.max_cnt:
                tmp_tail_nbr = self.max_cnt
            for index in self.pure_idlist[(dataload.ONE_PAGE_COMMIT * ix):tmp_tail_nbr]:
                iid_string_tail += dataload.IDS_UNIT(index)
            one_page_request_url = dataload.ALLREPOINFO_URL(self.user_input_id, iid_string_tail)
            iid_string_tail = ''                                # clear last cache
            page_url_array.append(one_page_request_url)
        
        # gather all data from response xhr page into a temp list
        tmp_receive_list = []
        for i in range(require_page_cnt):
            tmp_receive_list += self.crawl_onepage_data(i + 1, page_url_array[i])
        # handle url string
        repo_target_all_list = []
        for i in range(len(tmp_receive_list)):
            # tasnform title '\\uxxx' to unicode
            tmp_receive_list[i][1] = self.pvmx.unicode_escape(tmp_receive_list[i][1])
            # replace emoji string
            tmp_receive_list[i][1] = self.pvmx.replace_emoji(tmp_receive_list[i][1])
            # build original url without image format
            tmp = tmp_receive_list[i][2]
            tmp = tmp.replace('\\', '')                         # delete character '\' 
            tmp_receive_list[i][2] = dataload.ORIGINAL_IMAGE_HEAD + tmp[50:] + '.png'
            repo_target_all_list.append(tmp_receive_list[i])    # move original item to target list
            # use page count number build total url
            tmp_page_count_str = tmp_receive_list[i][3]
            if tmp_page_count_str.isdigit():
                index_page_count = int(tmp_page_count_str)
                if index_page_count != 1:
                    # add others items into list
                    for px in range(index_page_count - 1):
                        insert_item = [tmp_receive_list[i][0], 
                            tmp_receive_list[i][1], 
                            tmp_receive_list[i][2][:-5] + str(px + 1) + '.png', 
                            tmp_receive_list[i][3]]
                        repo_target_all_list.append(insert_item)
            else:
                log_context = 'Page count process error!'
                self.pvmx.logprowork(self.logpath, log_context)
                exit(-1)
        del tmp_receive_list                                    # clear cache

        # collection target count
        alive_targetcnt = len(repo_target_all_list)
        require_img_nbr = 0
        if self.ir_mode == 1:
            require_img_str = dataload.logtime_input(
                'Gather all repo %d, whole target(s): %d, enter you want count: '
                        % (self.max_cnt, alive_targetcnt))
            # if user input isn't number
            while not require_img_str.isdigit():
                dataload.logtime_print(
                    'Input error, your input content was not a decimal number')
                require_img_str = dataload.logtime_input(
                    'Enter again(max is %d): ' % alive_targetcnt)
            require_img_nbr = int(require_img_str)
            # if user input number more than limit max, set it to max
            if require_img_nbr > alive_targetcnt:
                require_img_nbr = alive_targetcnt
            elif require_img_nbr <= 0:
                dataload.logtime_print('What the f**k is wrong with you?')
                exit(-1)
        # server mode directly catch all of alive targets
        elif self.ir_mode == 2:
            require_img_nbr = alive_targetcnt
            dataload.logtime_print('Server mode auto crawl all of alive targets')
        
        # download image number limit
        for k, i in enumerate(repo_target_all_list[:require_img_nbr]):
            self.target_capture.append(i[2])    # put url into target capture list
            self.basepages.append(dataload.BASEPAGE_URL + i[0]) # build basepage url
            
        # display author info
        log_context = ('Illustrator: ' + self.author_name + ' id: '
            + self.user_input_id + ' require image(s): ' 
            + str(require_img_nbr) + ', target table:')
        self.pvmx.logprowork(self.logpath, log_context)
        # use prettytable build a table save and print info list
        image_info_table = PrettyTable(
            ["ImageNumber", "ImageID", "ImageTitle", "ImagePageName"])
        for k, i in enumerate(repo_target_all_list[:require_img_nbr]):
            image_info_table.add_row([(k + 1), i[0], i[1], i[2][57:-4]]) 
        # save with str format and no time word
        self.pvmx.logprowork(self.logpath, str(image_info_table), 'N')
        del repo_target_all_list            # clear cache 

    def start(self):
        """Call method start()

        First create a task, for example its name is build_task
        Then run build_task.start() to boot this mode
        :return:    none
        """
        self.pvmx.mkworkdir(self.logpath, self.workdir)

        self.gather_preloadinfo()
        self.crawl_allpage_target()

        self.pvmx.download_alltarget(self.logpath, self.target_capture, 
            self.basepages, self.workdir)
        self.pvmx.htmlpreview_build(self.workdir, self.htmlpath, self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
