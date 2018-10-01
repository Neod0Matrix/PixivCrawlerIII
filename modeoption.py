#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# provide modes setting target object

import re
from prettytable import PrettyTable
import dataload, privmatrix

# iterable call class
_pvmx = privmatrix.Matrix()

class RankingTop(object):
    """Ranking top crawl mode

    Pixiv website has a rank top, ordinary and R18, daily, weekly, monthly
    This class include fuction will gather all of those ranks
    """
    def __init__(self, workdir, log_path, html_path):
        """
        :param workdir:     work directory
        :param log_path:     log save path
        :param html_path:    html save path
        """
        self.workdir = workdir
        self.logpath = log_path
        self.htmlpath = html_path

    @staticmethod
    def gather_essential_info(ormode, whole_nbr):
        """Get input image count

        :param ormode:      select ranktop ordinary or r18 mode
        :param whole_nbr:   whole ranking crawl count
        :return:            crawl images count
        """
        # transfer ascii string to number
        img_cnt = 0
        # choose ordinary artwork images
        if ormode == 'o' or ormode == '1':
            # input a string for request image number
            img_cnt = int(dataload.logtime_input(
                'Gather whole ordinary vaild target %d, enter you want: '
                % whole_nbr))
            while img_cnt > whole_nbr:
                dataload.logtime_print(
                    'Input error, rank top at most %d' % whole_nbr)
                img_cnt = int(dataload.logtime_input(
                    'Enter again(max is %d): ' % whole_nbr))
        # choose R18 artwork images
        elif ormode == 'r' or ormode == '2':
            # input a string for request image number
            img_cnt = int(dataload.logtime_input(
                'Gather whole R18 vaild target %d, enter you want: '
                % whole_nbr))
            while img_cnt > whole_nbr:
                dataload.logtime_print(
                    'Input error, rank R18 top at most %d' % whole_nbr)
                img_cnt = int(dataload.logtime_input(
                    'Enter again(max is %d): ' % whole_nbr))
        else:
            pass

        return img_cnt

    @staticmethod
    def target_confirm(log_path):
        """Input option and confirm target

        :param log_path:    log save path
        :return:            request mainpage url, mode
        """

        rank_word, req_url = None, None
        log_context = 'Gather ranking list======>'
        _pvmx.logprowork(log_path, log_context)

        ormode = dataload.logtime_input(
            'Select ranking type, ordinary(o|1) or r18(r|2): ')
        if ormode == 'o' or ormode == '1':
            dwm = dataload.logtime_input(
                'Select daily(1)|weekly(2)|monthly(3) ordinary ranking type: ')
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
            dwm = dataload.logtime_input(
                'Select daily(1)/weekly(2) R18 ranking type: ')
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
            dataload.logtime_print(
                "Argument(s) error\n")
            log_context = None
        _pvmx.logprowork(log_path, log_context)

        return req_url, ormode

    def gather_rankingdata(self, option, log_path):
        """Crawl dailyRank list

        :param self:        self class
        :param option:      user choose option
        :param log_path:    log save path
        :return:            original images urls list
        """

        page_url, ormode = option[0], option[1]
        try:
            response = _pvmx.opener.open(
                fullurl=page_url,
                data=_pvmx.login_bias[2],
                timeout=30)
        except Exception as e:
            log_context = "Error Type: " + str(e)
            _pvmx.logprowork(log_path, log_context)
            response = None
        
        # if rank page can't get, crawler must exit
        if response is not None:
            if response.getcode() == dataload.HTTP_OK_CODE_200:
                log_context = 'Rankpage response successed'
            else:
                log_context = 'Rankpage response not ok, return code %d' \
                            % response.getcode()
            _pvmx.logprowork(log_path, log_context)
        else:
            log_context = 'Rankpage response failed'
            _pvmx.logprowork(log_path, log_context)
            exit()

        # size info in webpage source
        web_src = response.read().decode("UTF-8", "ignore")
        imgitem_pattern = re.compile(dataload.RANKING_SECTION_REGEX, re.S)
        info_pattern = re.compile(dataload.RANKING_INFO_REGEX, re.S)
        sizer_result = _pvmx.commit_spansizer(imgitem_pattern, info_pattern, web_src)
        # whole data cache pool
        whole_urls, img_infos = sizer_result[0], sizer_result[1]

        # cut need image count to be target list
        alive_targets = len(whole_urls)
        img_nbr = self.gather_essential_info(ormode, alive_targets)
        target_urls = whole_urls[:img_nbr]
        log_context = 'Gather rankingtop ' + str(img_nbr) + '======>'
        _pvmx.logprowork(log_path, log_context)

        # use prettytable package info list
        basepages = []
        image_info_table = PrettyTable(["ImageNumber", "ImageID", "ImageTitle", 
            "ImageID+PageNumber", "AuthorID", "AuthorName"])
        for k, i in enumerate(img_infos[:img_nbr]):
            # basepage will be a headers referer
            basepages.append(dataload.BASEPAGE_URL + i[3])
            image_info_table.add_row([(k + 1), i[3], i[1], 
                target_urls[k][57:-4], i[4], i[2]])

        # save table without time word
        _pvmx.logprowork(log_path, str(image_info_table), 'N')
            
        return target_urls, basepages

    def start(self):
        """Call method start()

        First create a task, for example its name is build_task
        Then run build_task.start() to boot this mode
        :return:    none
        """
        _pvmx.mkworkdir(self.logpath, self.workdir)
        _pvmx.camouflage_login(self.logpath)

        option = self.target_confirm(self.logpath)
        web_bias = self.gather_rankingdata(option, self.logpath)

        _pvmx.download_alltarget(self.logpath, web_bias[0], web_bias[1],
                                 self.workdir)
        _pvmx.htmlpreview_build(self.workdir, self.htmlpath, self.logpath)
        _pvmx.work_finished(self.logpath)

class RepertoAll(object):
    """Crawl any illustrator repertory all artworks

    Every illustrator in Pixiv has own mainpage
    This class include fuction will crawl all of those page all images
    """
    def __init__(self, workdir, log_name, html_name):
        """
        :param workdir:     work directory
        :param log_name:    log name
        :param html_name:   html name
        """
        target_id = dataload.logtime_input(
                    'Target crawl illustrator pixiv-id: ')
        self.user_input_id = target_id
        self.workdir = workdir + 'illustrepo_' + self.user_input_id
        self.logpath = self.workdir + log_name
        self.htmlpath = self.workdir + html_name

    @staticmethod
    def gather_preloadinfo(illust_id):
        """Crawler need to know how many images do you want

        :param illust_id:   illustrator id
        :return:            request images count
        """
        # get illust artwork whole count mainpage url
        cnt_url = dataload.MEMBER_ILLUST_URL + illust_id
        try:
            response = _pvmx.opener.open(
                fullurl=cnt_url,
                data=_pvmx.login_bias[2],
                timeout=30)
        except Exception as e:
            # here has no log file, just print error
            dataload.logtime_print("Error Type: " + str(e))
            response = None

        # if preload page can't get, crawler must exit
        if response is not None:
            if response.getcode() == dataload.HTTP_OK_CODE_200:
                log_context = 'Preload response successed'
            else:
                log_context = 'Preload response not ok, return code %d' \
                            % response.getcode()
        else:
            log_context = 'Preload response failed'
            exit()
    
        # mate illustrator name
        web_src = response.read().decode("UTF-8", "ignore")
        illust_name_pattern = re.compile(dataload.ILLUST_NAME_REGEX, re.S)
        arthor_names = re.findall(illust_name_pattern, web_src)
        # if login failed, this step will raise an error
        arthor_name = None
        if len(arthor_names) == 0:
            dataload.logtime_print("Login failed, please check method call")
            exit()
        else:
            arthor_name = arthor_names[0]

        # mate max count
        pattern = re.compile(dataload.REPO_WHOLE_NUMBER_REGEX, re.S)
        max_cntword = re.findall(pattern, web_src)[1][:-1]
        max_cnt = int(max_cntword)

        return max_cnt, arthor_name

    @staticmethod
    def crawl_onepage_data(illust_id, index, log_path):
        """Crawl all target url about images

        Page request regular:
        No.1 referer: &type=all     request url: &type=all&p=2
        No.2 referer: &type=all&p=2 request url: &type=all&p=3
        No.3 referer: &type=all&p=3 request url: &type=all&p=4
        :param illust_id:   illustrator id
        :param index:       count cut to every 20 images from each page
        :param log_path:    log save path
        :return:            use regex to mate web src thumbnail images url
        """
        step1url = (dataload.MEMBER_ILLUST_URL + illust_id
                   + dataload.TYPE_ALL_WORD)
        if index == 1:
            urlTarget = step1url
        elif index == 2:
            urlTarget = step1url + dataload.PAGE_NUM_WORD + str(index)
        else:
            urlTarget = step1url + dataload.PAGE_NUM_WORD + str(index)
        try:
            response = _pvmx.opener.open(
                fullurl=urlTarget,
                 data=_pvmx.login_bias[2],
                 timeout=30)
        except Exception as e:
            log_context = "Error occur: " + str(e) + " open no.%d page failed" % index
            _pvmx.logprowork(log_path, log_context)
            response = None
        
        # if can't get mainpage, crawler must exit
        if response is not None:
            if response.getcode() == dataload.HTTP_OK_CODE_200:
                log_context = "Mainpage %d response successed" % index
            else:
                log_context = "Mainpage %d response not ok" % index
            _pvmx.logprowork(log_path, log_context)
        else:
            log_context = 'Mainpage response failed'
            _pvmx.logprowork(log_path, log_context)
            exit()

        # catch need info from web source
        web_src = response.read().decode("UTF-8", "ignore")
        imgitem_pattern = re.compile(dataload.IMAGEITEM_REGEX, re.S)
        image_name_pattern = re.compile(dataload.IMAGE_NAME_REGEX, re.S)
        # sizer data
        sizer_result = \
            _pvmx.commit_spansizer(imgitem_pattern, image_name_pattern, web_src)

        return sizer_result

    def crawl_allpage_target(self, illust_id, nbr, arthor_name, log_path):
        """Package all gather url

        :param self:        self class
        :param illust_id:   illustrator id
        :param nbr:         package images count
        :param arthor_name: arthor name
        :param log_path:    log save path
        :return:            build original images urls list
        """
        # calcus nbr need request count
        # each page at most 20 images
        if nbr <= 20:
            need_pagecnt = 1
        else:
            need_pagecnt = int(nbr / 20) + 1

        # gather all data
        all_targeturls, all_artworknames = [], []
        for i in range(need_pagecnt):
            data_capture = self.crawl_onepage_data(illust_id, i + 1, log_path)
            # data write into list stack
            all_targeturls += data_capture[0]
            all_artworknames += data_capture[1]

        # collection target count
        alive_targetcnt = len(all_targeturls)
        log_context = ("Gather all repo %d, whole target(s): %d"
                       % (nbr, alive_targetcnt))
        _pvmx.logprowork(log_path, log_context)
        nbr_capture = int(dataload.logtime_input(
                'Enter you want count: '))
        while (nbr_capture > alive_targetcnt) or (nbr_capture <= 0):
            nbr_capture = int(dataload.logtime_input(
                'Error, input count must <= %d and not 0: ' % alive_targetcnt))
        log_context = ("Check crawl illustrator id:" + self.user_input_id +
                      " image(s):%d" % nbr_capture)
        _pvmx.logprowork(log_path, log_context)

        # cut need data
        artwork_ids, target_capture, basepages = [], [], []
        number_regex_comp = re.compile(dataload.NUMBER_REGEX, re.S)
        # download image number limit
        for k, i in enumerate(all_targeturls[:nbr_capture]):
            target_capture.append(i)                        # elements move
            # get image own id    
            img_id = re.findall(number_regex_comp, i[57:])[0]
            artwork_ids.append(img_id)
            basepage = dataload.BASEPAGE_URL + img_id       # build basepage url
            basepages.append(basepage)

        log_context = ('Illustrator: ' + arthor_name + ' id: '
                       + self.user_input_id + ' artworks info====>')
        _pvmx.logprowork(log_path, log_context)

        # use prettytable build a table save and print info list
        image_info_table = PrettyTable(["ImageNumber", "ImageID", "ImageTitle",
             "ImageID+PageNumber"])
        for k, i in enumerate(all_artworknames[:nbr_capture]):
            image_info_table.add_row([(k + 1), artwork_ids[k], 
                i, all_targeturls[k][57:-4]])
        # save with str format and no time word
        _pvmx.logprowork(log_path, str(image_info_table), 'N') 

        return target_capture, basepages

    def start(self):
        """Call method start()

        First create a task, for example its name is build_task
        Then run build_task.start() to boot this mode
        :return:    none
        """
        _pvmx.mkworkdir(self.logpath, self.workdir)
        _pvmx.camouflage_login(self.logpath)

        info = self.gather_preloadinfo(self.user_input_id)
        web_bias = self.crawl_allpage_target(self.user_input_id,
                                             info[0], info[1], self.logpath)

        _pvmx.download_alltarget(self.logpath, web_bias[0], web_bias[1],
                                 self.workdir)
        _pvmx.htmlpreview_build(self.workdir, self.htmlpath, self.logpath)
        _pvmx.work_finished(self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
