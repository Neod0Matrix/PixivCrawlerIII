#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright(C) 2017-2020 T.WKVER | </MATRIX>. All rights reserved.
# code by </MATRIX>@Neod Anderjon(LeaderN)
#
# modeoption.py
# Original Author: Neod Anderjon(1054465075@qq.com/EnatsuManabu@gmail.com), 2018-3-10
#
# PixivCrawlerIII component
# T.WKVER crawler functional modules for PixivCrawlerIII project
# Provide modes setting target object

import re
from prettytable import PrettyTable     # info list package table module
import dataload as dl

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
    def __init__(self, workdir, log_path, html_path, wkv_cw_api, ir_mode, rtn_r18_arg='', rtn_rank_type='', rtn_sex_opt='0'):
        """
        :param workdir:         work directory
        :param log_path:        log save path
        :param html_path:       html save path
        :param wkv_cw_api:      API library class instance
        :param ir_mode:         interactive mode or server mode
        :param rtn_r18_arg:     RTN mode set R18 or not
        :param rtn_rank_type:   RTN mode set ranking type
        :param rtn_sex_opt:     RTN male or female favor setting
        """
        self.workdir            = workdir
        self.logpath            = log_path
        self.htmlpath           = html_path
        self.wkv_cw_api         = wkv_cw_api
        self.ir_mode            = ir_mode
        # class inside global variable
        self.rtn_r18_arg        = rtn_r18_arg
        self.rtn_rank_type      = rtn_rank_type
        self.rtn_sex_opt        = rtn_sex_opt
        self.rtn_target_urls    = []
        self.rtn_basepages      = []

    @staticmethod
    def rtn_gather_essential_info(page_opt, whole_nbr):
        """Get input image count

        If user input number more than whole number, set target count is whole number
        Only intercative mode call this function
        :param page_opt:      select ranktop ordinary or r18 mode
        :param whole_nbr:   whole ranking crawl count
        :return:            crawl images count
        """
        img_cnt = 0
        # choose ordinary artwork images
        if page_opt == dl.PAGE_ORDINARY:
            # input a string for request image number
            img_str = dl.LT_INPUT(dl.HL_CY('crawl ordinary valid target %d, enter you want: ' % whole_nbr))
        # choose R18 artwork images
        elif page_opt == dl.PAGE_R18:
            # input a string for request image number
            img_str = dl.LT_INPUT(dl.HL_CY('crawl R18 vaild target %d, enter you want: ' % whole_nbr))
        else:
            dl.nolog_raise_arguerr()
            return dl.PUB_E_PARAM_FAIL

        while not img_str.isdigit():
            img_str = dl.LT_INPUT(dl.HL_CY('input error, enter again(max is %d): ' % whole_nbr))
        img_cnt = int(img_str)
        if img_cnt <= 0:
            dl.LT_PRINT(dl.BR_CB('what the f**k is wrong with you?'))
            return dl.PUB_E_PARAM_FAIL

        if img_cnt > whole_nbr:
            img_cnt = whole_nbr

        return img_cnt

    def rtn_target_confirm(self):
        """Input option and confirm target

        :return:        status code
        """
        req_url     = None      # request target ranking url
        rank_word   = None      # ranking word
        dwm_opt     = None      # daily/weekly/monthly

        if self.ir_mode == dl.MODE_INTERACTIVE:
            page_opt = dl.LT_INPUT(dl.HL_CY('select ranking type, ordinary(1) or r18(2): '))
            sex_opt = dl.LT_INPUT(dl.HL_CY('select sex favor, normal(0) or male(1) or female(2): '))
        elif self.ir_mode == dl.MODE_SERVER:
            page_opt = self.rtn_r18_arg
            sex_opt = self.rtn_sex_opt
        else:
            dl.nolog_raise_arguerr()
            return dl.PUB_E_PARAM_FAIL

        if page_opt == dl.PAGE_ORDINARY:
            if self.ir_mode == dl.MODE_INTERACTIVE:
                dwm_opt = dl.LT_INPUT(dl.HL_CY('select daily(1) | weekly(2) | monthly(3) ordinary ranking type: '))
            elif self.ir_mode == dl.MODE_SERVER:
                dwm_opt = self.rtn_rank_type
            else:
                dl.nolog_raise_arguerr()
                return dl.PUB_E_PARAM_FAIL

            if dwm_opt == dl.RANK_DAILY:
                if sex_opt == dl.SEX_NORMAL:
                    req_url = dl.DAILY_RANKING_URL
                    rank_word = dl.DAILY_WORD
                elif sex_opt == dl.SEX_MALE:
                    req_url = dl.DAILY_MALE_RANKING_URL
                    rank_word = dl.MALE_WORD
                elif sex_opt == dl.SEX_FEMALE:
                    req_url = dl.DAILY_FEMALE_RANKING_URL
                    rank_word = dl.FEMALE_WORD
                else:
                    dl.nolog_raise_arguerr()
                    return dl.PUB_E_PARAM_FAIL

            elif dwm_opt == dl.RANK_WEEKLY:
                req_url = dl.WEEKLY_RANKING_URL
                rank_word = dl.WEEKLY_WORD
            elif dwm_opt == dl.RANK_MONTHLY:
                req_url = dl.MONTHLY_RANKING_URL
                rank_word = dl.MONTHLY_WORD
            else:
                dl.nolog_raise_arguerr()
                return dl.PUB_E_PARAM_FAIL
            log_content = 'crawler set target to %s rank top' % rank_word

        elif page_opt == dl.PAGE_R18:
            if self.ir_mode == dl.MODE_INTERACTIVE:
                dwm_opt = dl.LT_INPUT(dl.HL_CY('select daily(1)/weekly(2) R18 ranking type: '))
            elif self.ir_mode == dl.MODE_SERVER:
                dwm_opt = self.rtn_rank_type
            else:
                dl.nolog_raise_arguerr()
                return dl.PUB_E_PARAM_FAIL

            if dwm_opt == dl.RANK_DAILY:
                if sex_opt == dl.SEX_NORMAL:
                    req_url = dl.DAILY_RANKING_R18_URL
                    rank_word = dl.DAILY_WORD
                elif sex_opt == dl.SEX_MALE:
                    req_url = dl.DAILY_MALE_RANKING_R18_URL
                    rank_word = dl.MALE_WORD
                elif sex_opt == dl.SEX_FEMALE:
                    req_url = dl.DAILY_FEMALE_RANKING_R18_URL
                    rank_word = dl.FEMALE_WORD
                else:
                    dl.nolog_raise_arguerr()
                    return dl.PUB_E_PARAM_FAIL

            elif dwm_opt == dl.RANK_WEEKLY:
                req_url = dl.WEEKLY_RANKING_R18_URL
                rank_word = dl.WEEKLY_WORD
            else:
                dl.nolog_raise_arguerr()
                return dl.PUB_E_PARAM_FAIL
            log_content = dl.BY_CB('crawler set target to %s r18 rank top' % rank_word)

        else:
            dl.nolog_raise_arguerr()
            return dl.PUB_E_PARAM_FAIL

        self.wkv_cw_api.wca_logprowork(self.logpath, log_content)
        self.rtn_req_url    = req_url
        self.page_opt        = page_opt

        return dl.PUB_E_OK

    def rtn_gather_rankingdata(self):
        """Crawl dailyRank list

        :return:        status code
        """
        response = self.wkv_cw_api.wca_url_request_handler(target_url=self.rtn_req_url,
                                                        post_data=self.wkv_cw_api.getway_data, 
                                                        timeout=30, 
                                                        target_page_word='Rankpage',
                                                        log_path=self.logpath)

        # size info in webpage source
        web_src = response.read().decode("UTF-8", "ignore")
        imgitem_pattern = re.compile(dl.RANKING_SECTION_REGEX, re.S)
        info_pattern = re.compile(dl.RANKING_INFO_REGEX, re.S)
        sizer_result = self.wkv_cw_api.wca_commit_spansizer(imgitem_pattern, info_pattern, web_src)
        if sizer_result is dl.PUB_E_FAIL:
            return dl.PUB_E_FAIL
        url_lst         = sizer_result['url lst']
        img_info_lst    = sizer_result['info lst']

        # cut need image count to be target list
        alive_targets = len(url_lst)
        if self.ir_mode == dl.MODE_INTERACTIVE:
            img_nbr = self.rtn_gather_essential_info(self.page_opt, alive_targets)
            if img_nbr == dl.PUB_E_PARAM_FAIL:
                return dl.PUB_E_FAIL

        # server mode directly get all of alive targets
        elif self.ir_mode == dl.MODE_SERVER:
            img_nbr = alive_targets
            dl.LT_PRINT(dl.BY_CB('server mode auto crawl all of alive targets'))
        self.rtn_target_urls = url_lst[:img_nbr]

        # use prettytable package info list  
        log_content = dl.BY_CB(
            'crawl rankingtop ' + str(img_nbr) + ', target table:')
        self.wkv_cw_api.wca_logprowork(self.logpath, log_content)      
        image_info_table = PrettyTable(["ImageNumber", "ImageID", "ImageTitle", 
            "ImageID+PageNumber", "AuthorID", "AuthorName"])
        for k, i in enumerate(img_info_lst[:img_nbr]):
            # basepage will be a headers referer
            self.rtn_basepages.append(dl.BASEPAGE_URL + i[3])
            image_info_table.add_row([(k + 1), i[3], i[1], 
                self.rtn_target_urls[k][57:-4], i[4], i[2]])
        # save table without time header word
        self.wkv_cw_api.wca_logprowork(self.logpath, str(image_info_table), 'N')

        return dl.PUB_E_OK

    def start(self):
        """Call method start()

        First create a task, for example its name is build_task
        Then run build_task.start() to boot this mode
        :return:    none
        """
        self.wkv_cw_api.wca_mkworkdir(self.logpath, self.workdir)

        # get target infomation may fail
        if self.rtn_target_confirm() != dl.PUB_E_OK:
            return dl.PUB_E_FAIL

        # gather ranking data may fail(especially R18 page)
        if self.rtn_gather_rankingdata() != dl.PUB_E_OK:
            return dl.PUB_E_FAIL

        self.wkv_cw_api.wca_download_alltarget(self.logpath, self.rtn_target_urls, 
                                                self.rtn_basepages, self.workdir)
        self.wkv_cw_api.wca_htmlpreview_build(self.workdir, self.htmlpath, self.logpath)

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

    def __init__(self, workdir, log_name, html_name, wkv_cw_api, ir_mode, ext_id=''):
        """
        :param workdir:     work directory
        :param log_name:    log name
        :param html_name:   html name
        :param wkv_cw_api:  API library class instance
        :param ir_mode:     interactive mode or server mode
        :param ext_id:      external illustrator id
        """
        if ir_mode == dl.MODE_INTERACTIVE:
            target_id = dl.LT_INPUT(dl.HL_CY('target crawl illustrator pixiv-id: '))
        elif ir_mode == dl.MODE_SERVER:
            target_id = ext_id
        self.user_input_id      = target_id
        self.workdir            = workdir + 'illustrepo_' + self.user_input_id
        self.logpath            = self.workdir + log_name
        self.htmlpath           = self.workdir + html_name
        self.wkv_cw_api         = wkv_cw_api
        self.ir_mode            = ir_mode
        # class inside call global variable
        self.ira_author_name    = None
        self.ira_max_cnt        = 0
        self.ira_pure_idlist    = []
        self.ira_target_capture = []
        self.ira_basepages      = []

    def ira_gather_preloadinfo(self):
        """Crawler need to know how many images do you want

        This function will get author name base on author id
        :return:            status code
        """
        # request all of one illustrator's artworks
        response = self.wkv_cw_api.wca_url_request_handler(target_url=dl.AJAX_ALL_URL(self.user_input_id),
                                                        post_data=self.wkv_cw_api.getway_data, 
                                                        timeout=30, 
                                                        target_page_word='Ajaxpage',
                                                        log_path=self.logpath)

        # mate illustrator name
        web_src = response.read().decode("UTF-8", "ignore")
        ajax_idlist_pattern = re.compile(dl.AJAX_ALL_IDLIST_REGEX, re.S)
        ajax_idlist = re.findall(ajax_idlist_pattern, web_src)
        # ajax id list may be empty
        if not ajax_idlist:
            log_content = dl.BR_CB('regex get ajax id list fail, return')
            self.wkv_cw_api.wca_logprowork(self.logpath, log_content)
            return dl.PUB_E_REGEX_FAIL

        # id list result may include some garbages, use number regex get pure result
        number_pattern = re.compile(dl.NUMBER_REGEX, re.S)
        for index in ajax_idlist:
            one_pure_id = re.findall(number_pattern, index)
            # list empty process
            if one_pure_id:
                self.ira_pure_idlist.append(one_pure_id[0])
            else:
                log_content = dl.BR_CB('get ajax page valid info failed, return')
                self.wkv_cw_api.wca_logprowork(self.logpath, log_content)
                return dl.PUB_E_RESPONSE_FAIL

        # use quick-sort algorithm to handle id number, descending order sort
        pure_idlist_nbr = []
        for index in self.ira_pure_idlist:
            pure_idlist_nbr.append(int(index))      # string to integer number
        self.wkv_cw_api.wca_quick_sort(pure_idlist_nbr, 0, len(pure_idlist_nbr) - 1)
        pure_idlist_nbr.reverse()                   # reverse order
        self.ira_pure_idlist.clear()                # clear origin list
        for index in pure_idlist_nbr:
            self.ira_pure_idlist.append(str(index))
        del pure_idlist_nbr
        self.ira_max_cnt = len(self.ira_pure_idlist)
        
        # get author name from member-main-page
        response = self.wkv_cw_api.wca_url_request_handler(target_url=dl.USERS_ARTWORKS_URL(self.user_input_id),
                                                        post_data=self.wkv_cw_api.getway_data, 
                                                        timeout=30, 
                                                        target_page_word='Mainpage',
                                                        log_path=self.logpath)

        # match illustrator name
        web_src = response.read().decode("UTF-8", "ignore")
        illust_name_pattern = re.compile(dl.ILLUST_NAME_REGEX(self.user_input_id), re.S)
        author_info = re.findall(illust_name_pattern, web_src)
        # if login failed, catch illust man page failed
        if not author_info:
            dl.LT_PRINT(dl.BR_CB("Regex parsing result error, no author info, return"))
            return dl.PUB_E_REGEX_FAIL
        else:
            self.ira_author_name = author_info[0]
        log_content = dl.HL_CY('check illustrator: [%s]' % self.ira_author_name)
        self.wkv_cw_api.wca_logprowork(self.logpath, log_content)

        return dl.PUB_E_OK

    def ira_crawl_onepage_data(self, index, index_url):
        """Crawl all target url about images

        :param index:       request page index
        :param index_url:   index group url
        :return:            one page get info list(2-d)
        """
        response = self.wkv_cw_api.wca_url_request_handler(target_url=index_url,
                                                        post_data=self.wkv_cw_api.getway_data, 
                                                        timeout=30, 
                                                        target_page_word='Data group %d' % index,
                                                        log_path=self.logpath)

        # catch need info from web source
        web_src = response.read().decode("UTF-8", "ignore")
        error_status_pattern = re.compile(dl.PAGE_REQUEST_SYM_REGEX, re.S)
        error_status_list = re.findall(error_status_pattern, web_src)
        # check error status list is empty or not
        if not error_status_list:
            log_content = dl.BR_CB('regex get error status failed, return')
            self.wkv_cw_api.wca_logprowork(self.logpath, log_content)
            return dl.PUB_E_REGEX_FAIL

        error_status = error_status_list[0]
        # page display error is "true" status
        if error_status == 'true':
            log_content = dl.BR_CB('data group %d response failed, return' % index)
            self.wkv_cw_api.wca_logprowork(self.logpath, log_content)
            return dl.PUB_E_RESPONSE_FAIL

        # crawl one page items info
        page_target_pattern = re.compile(dl.PAGE_TARGET_INFO_REGEX, re.S)
        page_tgt_info_lst = re.findall(page_target_pattern, web_src)
        # check tuple result is empty or not
        if not page_tgt_info_lst:
            log_content = dl.BR_CB('regex get target page info failed, return')
            return dl.PUB_E_REGEX_FAIL

        # tuple transform to list
        tmp_target_info_list = []
        for i in range(len(page_tgt_info_lst)):
            tmp_target_info_list.append([])
            for j in range(len(page_tgt_info_lst[i])):
                tmp_target_info_list[i] = list(page_tgt_info_lst[i])
        del page_tgt_info_lst
        # judge illust type, if it's gif(type symbol: 2), delete this item
        page_tgt_info_lst = []
        illust_type_pattern = re.compile(dl.ILLUST_TYPE_REGEX, re.S)
        for k in range(len(tmp_target_info_list)):
            illust_type_sym = re.findall(illust_type_pattern, tmp_target_info_list[k][2])
            # regex process result error
            if len(illust_type_sym) == 0:
                log_content = dl.BR_CB('illust type process error, return')
                self.wkv_cw_api.wca_logprowork(self.logpath, log_content)
                return dl.PUB_E_FAIL

            # jump gif out
            if illust_type_sym[0] == '2':
                continue
            del tmp_target_info_list[k][2]
            del tmp_target_info_list[k][-2]
            page_tgt_info_lst.append(tmp_target_info_list[k])
        del tmp_target_info_list

        return page_tgt_info_lst

    def ira_crawl_allpage_target(self):
        """Package all gather urls

        :return:            status code
        """
        # calcus nbr need request count
        # each page at most ONE_AUTHOR_MAINPAGE_IMGCOUNT(20181003:48) images
        require_page_cnt = 0
        if self.ira_max_cnt <= dl.ONE_PAGE_COMMIT:
            require_page_cnt = 1
        else:
            require_page_cnt = int(self.ira_max_cnt / dl.ONE_PAGE_COMMIT)
            # remainder decision
            if self.ira_max_cnt % dl.ONE_PAGE_COMMIT != 0:
                require_page_cnt += 1

        # build request url of one page 
        iid_string_tail = ''
        page_url_array = []
        for ix in range(require_page_cnt):
            # tail number limit
            tmp_tail_nbr = dl.ONE_PAGE_COMMIT * (ix + 1)
            if tmp_tail_nbr > self.ira_max_cnt:
                tmp_tail_nbr = self.ira_max_cnt
            for index in self.ira_pure_idlist[(dl.ONE_PAGE_COMMIT * ix):tmp_tail_nbr]:
                iid_string_tail += dl.IDS_UNIT(index)
            if ix == 0:
                one_page_request_url = dl.ALLREPOINFO_URL(self.user_input_id, iid_string_tail, 1)
            else:
                one_page_request_url = dl.ALLREPOINFO_URL(self.user_input_id, iid_string_tail, 0)
            iid_string_tail = ''                            # clear last cache
            page_url_array.append(one_page_request_url)

        # gather all data from response xhr page into a temp list
        tmp_receive_list    = []
        tmp_ret             = []
        for i in range(require_page_cnt):
            tmp_ret = self.ira_crawl_onepage_data(i + 1, page_url_array[i]) # here return any status code is fail
            if not isinstance(tmp_ret, list):
                return dl.PUB_E_FAIL
            tmp_receive_list += tmp_ret

        repo_target_all_list = []
        for i in range(len(tmp_receive_list)):
            tmp_receive_list[i][1] = dl.UNICODE_ESCAPE(tmp_receive_list[i][1])  # tasnform title '\\uxxx' to unicode
            tmp_receive_list[i][1] = dl.REPL_EMOJI(tmp_receive_list[i][1])      # replace damn emoji
            # build original url without image format
            tmp = tmp_receive_list[i][2]
            tmp = tmp.replace('\\', '')                                         # delete character '\'
            tmp_receive_list[i][2] = dl.ORIGINAL_IMAGE_HEAD + tmp[50:] + '.png'
            repo_target_all_list.append(tmp_receive_list[i])                    # move original item to target list
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
                log_content = dl.BR_CB('page count process error!')
                self.wkv_cw_api.wca_logprowork(self.logpath, log_content)
                return dl.PUB_E_FAIL

        del tmp_receive_list
        # collection target count
        alive_targetcnt = len(repo_target_all_list)
        require_img_nbr = 0
        if self.ir_mode == dl.MODE_INTERACTIVE:
            require_img_str = dl.LT_INPUT(dl.HL_CY('crawl all repo %d, whole target(s): %d, enter you want count: '
                % (self.ira_max_cnt, alive_targetcnt)))
            # if user input isn't number
            while not require_img_str.isdigit():
                dl.LT_PRINT(dl.BR_CB('input error, your input content was not a decimal number'))
                require_img_str = dl.LT_INPUT(dl.HL_CY('enter again(max is %d): ' % alive_targetcnt))
            require_img_nbr = int(require_img_str)
            # if user input number more than limit max, set it to max
            if require_img_nbr > alive_targetcnt:
                require_img_nbr = alive_targetcnt
            elif require_img_nbr <= 0:
                dl.LT_PRINT(dl.BR_CB('what the f**k is wrong with you?'))
                return dl.PUB_E_PARAM_FAIL

        elif self.ir_mode == dl.MODE_SERVER:
            require_img_nbr = alive_targetcnt
            dl.LT_PRINT(dl.BY_CB('server mode auto crawl all of alive targets'))

        for k, i in enumerate(repo_target_all_list[:require_img_nbr]):
            self.ira_target_capture.append(i[2])                # put url into target capture list
            self.ira_basepages.append(dl.BASEPAGE_URL + i[0])   # build basepage url

        log_content = ('illustrator: ' + self.ira_author_name + ' id: '
            + self.user_input_id + ' require image(s): ' 
            + str(require_img_nbr) + ', target table:')
        self.wkv_cw_api.wca_logprowork(self.logpath, log_content)

        image_info_table = PrettyTable(["ImageNumber", "ImageID", "ImageTitle", "ImagePageName"])
        for k, i in enumerate(repo_target_all_list[:require_img_nbr]):
            image_info_table.add_row([(k + 1), i[0], i[1], i[2][57:-4]])

        # damn emoji, maybe dump failed
        try:
            self.wkv_cw_api.wca_logprowork(self.logpath, str(image_info_table), False)
        except Exception as e:
            dl.LT_PRINT(dl.BR_CB('error: %s, dump prettytable interrupt' % str(e)))
        del repo_target_all_list

        return dl.PUB_E_OK

    def start(self):
        """Call method start()

        First create a task, for example its name is build_task
        Then run build_task.start() to boot this mode
        :return:    none
        """
        self.wkv_cw_api.wca_mkworkdir(self.logpath, self.workdir)

        # gather pre-load infomation may fail
        if self.ira_gather_preloadinfo() != dl.PUB_E_OK:
            return dl.PUB_E_FAIL

        # crawl all of pages may fail
        if self.ira_crawl_allpage_target() != dl.PUB_E_OK:
            return dl.PUB_E_FAIL

        self.wkv_cw_api.wca_download_alltarget(self.logpath, self.ira_target_capture, 
                                                self.ira_basepages, self.workdir)
        self.wkv_cw_api.wca_htmlpreview_build(self.workdir, self.htmlpath, self.logpath)
