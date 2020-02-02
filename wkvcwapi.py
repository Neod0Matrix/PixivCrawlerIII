#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright(C) 2017-2020 T.WKVER | </MATRIX>. All rights reserved.
# code by </MATRIX>@Neod Anderjon(LeaderN)
#
# wkvcwapi.py
# Original Author: Neod Anderjon(1054465075@qq.com/EnatsuManabu@gmail.com), 2018-3-10
#
# PixivCrawlerIII component
# T.WKVER crawler API library for PixivCrawlerIII project
# Write all universal function into a class and package them

from __future__ import print_function
import urllib.request, urllib.parse, urllib.error, http.cookiejar
import json
from retrying import retry          # timeout auto retry decorator
import threading                    # multi-thread
from Crypto.Cipher import AES       # user info local crypto storage
from Crypto import Random           
from PIL import Image               # image process module
from collections import OrderedDict # order dictory
import time, random, re, os, getpass
from functools import wraps         # decorator wrapper
import dataload as dl
from selenium import webdriver
from requests.cookies import RequestsCookieJar

class WkvCwApi(object):
    """
    =================================================================================================================
    |       ██████╗ ██╗██╗  ██╗██╗██╗   ██╗ ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ ██╗██╗██╗      |
    |       ██╔══██╗██║╚██╗██╔╝██║██║   ██║██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗██║██║██║      |
    |       ██████╔╝██║ ╚███╔╝ ██║██║   ██║██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝██║██║██║      |
    |       ██╔═══╝ ██║ ██╔██╗ ██║╚██╗ ██╔╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗██║██║██║      |
    |       ██║     ██║██╔╝ ██╗██║ ╚████╔╝ ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║██║██║██║      |
    |       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝╚═╝      |
    |                                                                                                               |
    |       Copyright (c) 2017-2020 T.WKVER | </MATRIX>. All rights reserved.                                       |
    |       Version: 3.3.2 LTE                                                                                      |
    |       Code by </MATRIX>@Neod Anderjon(LeaderN)                                                                |
    |       PixivCrawlerIII Help Page                                                                               |
    |       1.rtn  ---     RankingTopN, crawl Pixiv daily/weekly/month ranking top artworks                         |
    |       2.ira  ---     IllustRepoAll, crawl Pixiv any illustrator all repertory artworks                        |
    |       3.help ---     Print this help page                                                                     |
    |       4.exit ---     Exit crawler program                                                                     |
    |                                                                                                               |
    |       Server Mode Help Content                                                                                |
    |       -h/--help      @Print usage page                                                                        |
    |       -m/--mode      @Set mode, RTN(1) | IRA(2)                                                               |
    |       -r/--R18       @Ordinary(1) | R18(2) | R18G(3), only support Mode RTN                                   |
    |       -l/--list      @Daily(1) | Weekly(2) | Monthly(3), only support Mode RTN                                |
    |       -s/--sex       @Nomal(0) | Male(1) | Female(2) favor, only support Mode RTN                             |
    |       -i/--id        @Illustrator ID, only support Mode IRA                                                   |
    |                                                                                                               |
    |       Example:                                                                                                |
    |       python3 pixivcrawleriii.py -m 1 -r 1 -l 1 -s 0                                                          |
    |       python3 pixivcrawleriii.py -m 2 -i 0000001,0000002,0000003                                              |
    =================================================================================================================
    """

    _datastream_pool    = 0         # statistics data stream, must set as global variable
    _login_once_flag    = False     # login once global flag

    def __init__(self, ir_mode):
        """Create a class public call webpage opener with cookie

        From first login save cookie and continue call
        Call this global opener must write parameter name
        Cookie, cookiehandler, opener all can inherit and call
        :param ir_mode:     interactive mode or server mode
        """
        self.cookie                 = http.cookiejar.LWPCookieJar()
        self.cookieHandler          = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener                 = urllib.request.build_opener(self.cookieHandler)
        urllib.request.install_opener(self.opener)

        # class inside global variable
        self.alivethread_counter    = 0
        self.ir_mode                = ir_mode

    def _generate_aes_info(self, aes_file_path, username, passwd):
        """Generate aes info and save to file

        :param aes_file_path:       .aes_crypto_login.ini file path
        :param username:            username
        :param passwd:              password
        :return:                    none
        """
        generate_aes_iv_param = Random.new().read(AES.block_size)   # generate random aes iv param

        username_cipher = AES.new(dl.AES_SECRET_KEY, AES.MODE_CFB, generate_aes_iv_param)
        username_encrypto = generate_aes_iv_param + username_cipher.encrypt(username.encode('utf-8'))

        passwd_cipher = AES.new(dl.AES_SECRET_KEY, AES.MODE_CFB, generate_aes_iv_param)
        passwd_encrypto = generate_aes_iv_param + passwd_cipher.encrypt(passwd.encode('utf-8'))

        aes_fd = open(aes_file_path, 'wb')
        # write bin value to file with b'\n' to wrap
        aes_fd.write(generate_aes_iv_param + b'\n')     # row 1 is iv param
        aes_fd.write(username_encrypto + b'\n')         # row 2 is username
        aes_fd.write(passwd_encrypto + b'\n')           # row 3 is password
        aes_fd.close()

    def _login_preload(self, aes_file_path):
        """Get user input login info and storage into aes file

        If project directory has no file, you need hand-input login info,
        then program will create new file to storage AES encrypt info to it
        This method use pycrypto, need import external call
        :param aes_file_path:       .aes_crypto_login.ini file path
        :return:                    none
        """
        if os.path.exists(aes_file_path):
            # stable read rows get username and password
            read_aes_file = open(aes_file_path, 'rb+')
            readline_cache = read_aes_file.readlines()                      # all line list
            read_aes_file.close()

            # get aes file storage info and split tail '\n'
            aes_info = {'iv_param':     readline_cache[0][:-1], 
                        'user_mail':    readline_cache[1][:-1],
                        'passwd':       readline_cache[2][:-1]}

            # analysis hash value to string
            username_aes_decrypt_cipher = AES.new(dl.AES_SECRET_KEY, AES.MODE_CFB, aes_info['iv_param'])
            username = str(username_aes_decrypt_cipher.decrypt(aes_info['user_mail'][AES.block_size:]), 'UTF-8')
            password_aes_decrypt_cipher = AES.new(dl.AES_SECRET_KEY, AES.MODE_CFB, aes_info['iv_param'])
            passwd = str(password_aes_decrypt_cipher.decrypt(aes_info['passwd'][AES.block_size:]), 'UTF-8')

            if self.ir_mode == dl.MODE_INTERACTIVE:
                check = dl.LT_INPUT(dl.HL_CY("get user account info ok, check: \n"
                    "[*username] %s\n[*password] %s\n"
                    "Is that correct? (Y/N): " % (username, passwd)))

                # if user judge info are error, delete old AES file and record new info
                if check == 'N' or check == 'n':
                    os.remove(aes_file_path)        # delete old AES file
                    # temporarily enter login information
                    dl.LT_PRINT(dl.BY_CB("Well, you need hand-input your login data: "))
                    username = dl.LT_INPUT(dl.HL_CY('enter your pixiv id(mailbox), must be a R18: '))
                    passwd = getpass.getpass(dl.realtime_logword(dl.base_time)
                        + dl.HL_CY('enter your account password: '))
                    self._generate_aes_info(aes_file_path, username, passwd)
                else:
                    pass
            elif self.ir_mode == dl.MODE_SERVER:
                dl.LT_PRINT(dl.BY_CB("check server mode, jump user info confirm out"))
            else:
                pass

        # if no AES file, then create new and write md5 value into it
        else:
            dl.LT_PRINT(dl.HL_CY("Create new AES encrypt file to storage your username and password: "))
            username = dl.LT_INPUT(dl.HL_CY('enter your pixiv id(mailbox), must be a R18: '))
            passwd = getpass.getpass(dl.realtime_logword(dl.base_time)
                + dl.HL_CY('enter your account password: '))
            self._generate_aes_info(aes_file_path, username, passwd)

        # build data string
        getway_register = [('user', username), ('pass', passwd)]
        getway_data = urllib.parse.urlencode(getway_register).encode(encoding='UTF8')

        self.username       = username
        self.passwd         = passwd
        self.getway_data    = getway_data

    @staticmethod
    def wca_remove_color_chars(string):
        """Remove color effect style characters

        @@API that allows external calls
        After print to console, log may has color effect char '\033'('\x1b')
        It needs to remove these characters before writing to the file
        :param string:      wait for check has color chars or not string
        :return:            string when process over
        """
        # '\033' -> '\x1b'
        if string[0] == '\x1b':
            m_word_index = string.index('m')        # get 'm' index number
            string = string[(m_word_index + 1):]    # remove header
            string = string[:-4]                    # remove tail
        else:
            pass

        return string

    def wca_logprowork(self, log_path, log_content, withtime=True):
        """Universal work log save

        @@API that allows external calls
        Notice: If here print series fucntion raise UnicodeEncodeError, it must web page 
        include emoji symbol encode title when use prettytable to package title info
        :param log_path:    log save path
        :param log_content: log save content
        :param withtime:    default parameter, print and save with real time or not
        :return:            none
        """
        # if log path is none, just print message and return, no log action
        if log_path == None:
            dl.LT_PRINT(log_content)
            return

        # add context to the file use option 'a+'
        # write content may have some not utf8 code, example Japanese
        log_fd = open(log_path, 'a+', encoding='utf-8')

        if withtime == True:
            dl.LT_PRINT(log_content)

            log_content = self.wca_remove_color_chars(log_content)  # remove log color chars
            # remove timestamp log color chars
            timestamp = dl.realtime_logword(dl.base_time)
            timestamp = self.wca_remove_color_chars(timestamp)
            timestamp = timestamp[:-1] + ' '                        # timestamp has a space in tail

            log_fd.write(timestamp + log_content + '\n')

        else:
            print(log_content)
            log_content = self.wca_remove_color_chars(log_content)
            log_fd.write(log_content + '\n')
        log_fd.close()

    def wca_mkworkdir(self, log_path, folder):
        """Create a crawler work directory

        @@API that allows external calls
        :param log_path:    log save path
        :param folder:      folder create path
        :return:            folder create path
        """
        # create a folder to save picture
        dl.LT_PRINT('crawler work directory setting: ' + folder)
        is_folder_existed = os.path.exists(folder)
        if not is_folder_existed:
            os.makedirs(folder)
            log_content = 'create a new work folder'
        else:
            log_content = 'target folder has already existed'

        # log file first line here
        if os.path.exists(log_path):
            os.remove(log_path)
        self.wca_logprowork(log_path, log_content)

    @staticmethod
    def _partition(array, l, r):
        """Partition of quick sort algorithm

        code by CSDN@lookupheaven
        :param array:       wait for sort array
        :param l:           edge left
        :param r:           edge right
        :return:            part index
        """
        x = array[r]
        i = l - 1
        for j in range(l, r):
            if array[j] <= x:
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[r] = array[r], array[i+1]

        return i + 1

    def wca_quick_sort(self, array, l, r):
        """Quick sort algorithm

        @@API that allows external calls
        code by CSDN@lookupheaven
        Private quick sort algorithm achieve
        Of course You can use the sorting method provided by the list directly
        :param array:       wait for sort array
        :param l:           edge left
        :param r:           edge right
        :return:            none
        """
        if l < r:
            q = self._partition(array, l, r)
            self.wca_quick_sort(array, l, q - 1)
            self.wca_quick_sort(array, q + 1, r)

    def wca_url_request_handler(self, target_url, post_data, timeout, 
                                target_page_word, log_path):
        """Universal URL request format handler

        @@API that allows external calls
        If no need log, set log path to None
        :param target_url:          target request url
        :param post_data:           post way data
        :param timeout:             request timeout, suggest 30s
        :param target_page_word:    target page symbol word
        :param log_path:            log save path
        :return:                    request result response(raw)
        """
        try:
            response = self.opener.open(fullurl=target_url,
                                        data=post_data,
                                        timeout=timeout)
        except Exception as e:
            log_content = dl.BR_CB('%s response failed, error: %s' % (target_page_word, str(e)))
            self.wca_logprowork(log_path, log_content)
            return dl.PUB_E_RESPONSE_FAIL

        if response.getcode() == dl.HTTP_REP_OK_CODE:
            log_content = target_page_word + ' response ok'
        else:
            log_content = dl.BR_CB(target_page_word + ' return code %d' % response.getcode())
        self.wca_logprowork(log_path, log_content)

        return response

    def _gatherpostkey(self):
        """POST way login need post-key

        Pixiv website POST login address: (see dl.LOGIN_POSTKEY_URL)
        This operation will get cookie and post-key
        :return:            status code
        """

        self._login_preload(dl.LOGIN_AES_INI_PATH)

        response = self.wca_url_request_handler(target_url=dl.LOGIN_POSTKEY_URL, 
                                                post_data=None, # cannot set data when get post key
                                                timeout=30, 
                                                target_page_word='post-key',
                                                log_path=None)

        web_src = response.read().decode("UTF-8", "ignore")
        # debug recaptcha v3 token use
        ## self.wca_save_test_html('post-key', 'E:\\OperationCache', web_src)

        post_pattern    = re.compile(dl.POSTKEY_REGEX, re.S)
        postkey         = re.findall(post_pattern, web_src)
        if not postkey:
            dl.LT_PRINT('regex parse post key failed')
            return dl.PUB_E_REGEX_FAIL

        # build post-way data with order dictory structure
        post_orderdict = OrderedDict()
        post_orderdict['captcha']               = ""
        post_orderdict['g_recaptcha_response']  = ""
        post_orderdict['password']              = self.passwd
        post_orderdict['pixiv_id']              = self.username
        post_orderdict['post_key']              = postkey[0]
        post_orderdict['source']                = "accounts"
        post_orderdict['ref']                   = ""
        post_orderdict['return_to']             = dl.HTTPS_HOST_URL
        post_orderdict['recaptcha_v3_token']    = ""    # google recaptcha v3 token
        self.postway_data = urllib.parse.urlencode(post_orderdict).encode("UTF-8")

        return dl.PUB_E_OK

    @staticmethod
    def _get_chrome_cookie(cache_path, url):
        '''Get chrome cookies with selenium

        @@API that allows external calls
        Due to the recaptcha mechanism set by the website, 
        it is impossible to obtain the token using the normal method, 
        and it is forced to adopt the webdriver of selenium.
        :param cache_path:  local cookie cache text path
        :param url:         selenium webdriver request url
        :return:            cookie jar
        '''
        cookie_jar = RequestsCookieJar()
        # first judge local cookie text file exist
        # if exists, just read it and return
        if os.path.exists(cache_path):
            dl.LT_PRINT('check local cookie file')
            with open(cache_path, "r") as fp:
                cookies = json.load(fp)
            # package to jar type
            for cookie in cookies:
                cookie_jar.set(cookie['name'], cookie['value'])

            return cookie_jar

        dl.LT_PRINT('start selenium webdriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')               # hide window
        chrome_options.add_argument('--disable-extensions')     # disable chrome externsions
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--incognito')              # seamless mode
        chrome_options.add_argument('--blink-settings=imagesEnabled=false') # do not load image
        ## chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('user-data-dir=' + os.path.abspath(dl.chrome_user_data_dir))
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # request website and get cookie
        driver.get(url)
        cookies = driver.get_cookies()
        driver.close()
        dl.LT_PRINT('stop selenium webdriver')

        ## dl.LT_PRINT('get cookies:\n%s' % json.dumps(cookies, sort_keys=True, indent=4))
        # save cookies to file
        with open(cache_path, "w") as fp:
            json.dump(cookies, fp)
        # package to jar type
        for cookie in cookies:
            cookie_jar.set(cookie['name'], cookie['value'])

        return cookie_jar

    def wca_camouflage_login(self):
        """Camouflage browser to login

        If login failed, program will exit here
        @@API that allows external calls
        :return:        status code
        """
        if WkvCwApi._login_once_flag:
            return dl.PUB_E_OK
        else:
            WkvCwApi._login_once_flag = True

        if self._gatherpostkey() != dl.PUB_E_OK:
            exit(dl.PUB_E_RESPONSE_FAIL)

        cookie_jar          = self._get_chrome_cookie(dl.local_cache_cookie_path, dl.HTTPS_HOST_URL)
        self.cookieHandler  = urllib.request.HTTPCookieProcessor(cookie_jar)
        self.opener         = urllib.request.build_opener(self.cookieHandler)
        urllib.request.install_opener(self.opener)

        response = self.wca_url_request_handler(target_url=dl.LOGIN_REQUEST_API_URL,
                                                post_data=self.postway_data,
                                                timeout=30, 
                                                target_page_word='login',
                                                log_path=None)
        if response == dl.PUB_E_RESPONSE_FAIL:
            dl.LT_PRINT(dl.BR_CB('login response return a boolean FALSE, exit'))
            exit(dl.PUB_E_RESPONSE_FAIL)

        web_src = response.read().decode("UTF-8", "ignore")
        dl.LT_PRINT(dl.BY_CB('response source: %s' % web_src.encode("UTF-8").decode("unicode_escape")))

        login_info_pattern = re.compile(dl.LOGIN_INFO_REGEX, re.S)
        response_info = re.findall(login_info_pattern, web_src)
        if response_info:
            if response_info[0] != 'false':
                # error false means no error
                dl.LT_PRINT(dl.BR_CB('login confirm raise a error, exit'))
                exit(dl.PUB_E_RESPONSE_FAIL)
            else:
                dl.LT_PRINT('login check response right')
        else:
            dl.LT_PRINT('login confirm response no error status')
            exit(dl.PUB_E_RESPONSE_FAIL)

    def wca_save_test_html(self, filename, workdir, content):
        """Save request web source page in a html file, test use

        @@API that allows external calls
        :param filename:    save html file name
        :param workdir:     work directory
        :param content:     save content(web source code)
        :return:            none
        """
        htmlfile = open(workdir + '/' + filename + '.html', "w", encoding='utf-8')
        htmlfile.write(content)
        htmlfile.close()
        dl.LT_PRINT(dl.BY_CB('save test request html page ok'))

    @staticmethod
    def wca_commit_spansizer(whole_pattern, info_pattern, web_src):
        """A sizer for all of images in once commit item

        @@API that allows external calls
        After Pixiv 20181002 update, this method only support mode rtn
        :param whole_pattern:   whole info data regex compile pattern
        :param info_pattern:    image info regex compile pattern
        :param web_src:         webpage source
        :return:                original target url list & image info list dict
        """
        img_info_lst = []
        tgt_url_lst  = []

        datasrc_pattern = re.compile(dl.DATASRC_REGEX, re.S)
        span_pattern    = re.compile(dl.SPAN_REGEX, re.S)
        img_whole_info  = re.findall(whole_pattern, web_src)

        # image have 3 format: jpg/png/gif
        # this crawler will give gif format up and crawl png or jpg
        # pixiv one repertory maybe have multi-images
        for item in img_whole_info:
            tmp_thumbnail = re.findall(datasrc_pattern, item)
            if not tmp_thumbnail:
                dl.LT_PRINT(dl.BR_CB('span sizer regex cannot get valid info'))
                return dl.PUB_E_FAIL

            thumbnail = tmp_thumbnail[0]
            judge_word = thumbnail[-18:]
            # check jpg/png or gif
            if judge_word == dl.JUDGE_NOGIF_WORD:
                span_word = re.findall(span_pattern, item)
                vaild_word = thumbnail[44:-18]

                # try to check multi-span images
                if len(span_word) != 0:
                    for _px in range(int(span_word[0])):
                        info = re.findall(info_pattern, item)[0]
                        img_info_lst.append(info)
                        # more pages point, range 0~span-1
                        target_url = dl.ORIGINAL_IMAGE_HEAD + vaild_word + dl.ORIGINAL_IMAGE_TAIL(_px)
                        tgt_url_lst.append(target_url)
                # just only one picture in a commit
                else:
                    info = re.findall(info_pattern, item)[0]
                    img_info_lst.append(info)
                    # only _p0 page
                    target_url = dl.ORIGINAL_IMAGE_HEAD + vaild_word + dl.ORIGINAL_IMAGE_TAIL(0)
                    tgt_url_lst.append(target_url)
            # give up gif format, or list is empty
            else:
                pass

        return {'url lst': tgt_url_lst, 'info lst': img_info_lst}

    @retry
    def _save_oneimage(self, index, url, basepages, img_savepath, log_path):
        """Download one target image, then multi-thread will call here

        Add retry decorator, if first try failed, it will auto-retry
        :param index:           image index
        :param url:             one image url
        :param basepages:       referer basic pages list
        :param img_savepath:    image save path
        :param log_path:        log save path
        :return:                none
        """
        img_datatype    = 'png'
        image_name      = dl.FROM_URL_GET_IMG_NAME(url)
        img_save_path   = img_savepath + '/' + image_name + '.' + img_datatype

        # use opener method
        headers                 = dl.build_original_headers(basepages[index])
        proxy_handler           = None
        response                = None
        timeout                 = 30
        list_headers            = dl.dict2list(headers)
        self.opener.addheaders  = list_headers
        urllib.request.install_opener(self.opener)      # update install opener

        # first try default png format, if failed change to jpg
        try:
            response = self.opener.open(fullurl=url, timeout=timeout)
        except urllib.error.HTTPError as e:
            # http error 404, change image type
            if e.code == dl.HTTP_REP_404_CODE:
                img_datatype = 'jpg'
                jpg_img_url = url[:-3] + img_datatype
                try:
                    response = self.opener.open(fullurl=jpg_img_url, timeout=timeout)
                except urllib.error.HTTPError:
                    pass
            else:
                pass

        if response.getcode() == dl.HTTP_REP_OK_CODE:
            img_bindata = response.read()
            source_size = round(float(len(img_bindata) / 1024), 2)
            WkvCwApi._datastream_pool += source_size        # multi-thread, no resource lock, it must use class name to call
            with open(img_save_path, 'wb') as img:
                img.write(img_bindata)
        else:
            pass

    class _MultiThreading(threading.Thread):
        """Overrides its run method by inheriting the Thread class

        This class can be placed outside the main class, you can also put inside
        Threads are the smallest unit of program execution flow
        That is less burdensome than process creation
        Only internal call
        """
        queue_t    = []
        event_t    = threading.Event()    # use event let excess threads wait
        lock_t     = threading.Lock()     # thread lock

        def __init__(self, index, url, basepages, workdir, log_path):
            """Provide class arguments

            :param index, url, basepages, workdir:  function _save_oneimage param
            :param log_path:                        log save path
            """
            threading.Thread.__init__(self)         # callable class init
            self.index      = index
            self.url        = url
            self.basepages  = basepages
            self.workdir    = workdir
            self.logpath    = log_path

        def run(self):
            """Overwrite threading.thread run() method

            :return:    none
            """
            try:
                # package download one image thread
                # default set server mode here(actually it doesn’t matter)
                WkvCwApi(2)._save_oneimage(self.index, self.url, 
                    self.basepages, self.workdir, self.logpath)
            except Exception as e:
                log_content = dl.BR_CB("Error type: " + str(e))
                WkvCwApi.wca_logprowork(log_content, self.logpath)

            self.lock_t.acquire()           # thread queue adjust, lock it
            self.queue_t.remove(self)       # remove end thread from list
            if len(self.queue_t) == dl.SYSTEM_MAX_THREADS - 1:
                self.event_t.set()
                self.event_t.clear()
            self.lock_t.release()

        def create(self):
            """Create a new thread

            Use built-in queue to manage threads list
            :return:    status flag
            """
            self.lock_t.acquire()
            self.queue_t.append(self)
            self.lock_t.release()
            # if the system has insufficient memory
            # it will not be able to create more threads
            # this step will fail
            try:
                self.start()
            except Exception as e:
                log_content = dl.BR_CB("Error type: " + str(e))
                WkvCwApi.wca_logprowork(log_content, self.logpath)
                return dl.PUB_E_FAIL
            return dl.PUB_E_OK

    def wca_timer_decorator(origin_func):
        """Timer decorator

        @@API that allows external calls
        Using python decorator feature to design program runtime timer
        In this project this function only have used in internal call
        But it also can be used in external call in only one place
        :param origin_func: decorated function
        :return:            wrapper function
        """

        @wraps(origin_func)     # reserve property of original function 
        def _wrapper(self, log_path, *args, **kwargs):
            """Timer wrapper

            Mainly for the function download_alltarget() to achieve timing expansion
            :param log_path:    log save path
            :param *args:       pythonic variable argument
            :param **kwargs:    pythonic variable argument
            :return:            none
            """
            log_content = "launch timer decorator, start download threads timer"
            self.wca_logprowork(log_path, log_content)
            starttime = time.time()

            origin_func(self, log_path, *args, **kwargs)    # packaged original function 

            endtime = time.time()
            elapesd_time = endtime - starttime
            average_download_speed = float(WkvCwApi._datastream_pool / elapesd_time)
            log_content = (dl.BY_CB(
                "all of threads reclaim, total download data-stream size: %0.2fMB, "
                "average download speed: %0.2fkB/s"
                % (float(WkvCwApi._datastream_pool / 1024), average_download_speed)))
            self.wca_logprowork(log_path, log_content)
            WkvCwApi._datastream_pool = 0    # clear global data stream list

        return _wrapper

    @wca_timer_decorator
    def wca_download_alltarget(self, log_path, urls, basepages, workdir):
        """Multi-process download all image

        @@API that allows external calls
        :param urls:        all original images urls
        :param basepages:   all referer basic pages
        :param workdir:     work directory
        :param log_path:    log save path
        :return:            none
        """
        thread_block_flag = False               # thread blocking flag
        alive_thread_cnt = queueLength = len(urls)
        log_content = dl.BY_CB('hit %d target(s), start download task(s)' % queueLength)
        self.wca_logprowork(log_path, log_content)

        # capture timeout and the user interrupt fault and exit the failed thread
        try:
            for i, one_url in enumerate(urls):
                self._MultiThreading.lock_t.acquire()
                if len(self._MultiThreading.queue_t) > dl.SYSTEM_MAX_THREADS:
                    thread_block_flag = True
                    self._MultiThreading.lock_t.release()
                    # if the number of created threads reach max limit
                    # program will stop here, wait all of threads have been created over
                    # when one thread executed over, create next one
                    self._MultiThreading.event_t.wait()
                else:
                    self._MultiThreading.lock_t.release()

                # build overwrite threading.Thread object
                sub_thread = self._MultiThreading(i, one_url, basepages, workdir, log_path)
                # set every download sub-process daemon property
                # set false, then if you exit one thread, others threads will not end
                # set true, quit one is quit all
                sub_thread.setDaemon(True)
                # if create this sub-thread failed from function
                if sub_thread.create() == dl.PUB_E_FAIL:
                    log_content = dl.BR_CB('create a new sub-thread failed')
                    print(log_content)
                    return dl.PUB_E_FAIL

                if thread_block_flag == False:
                    log_content = dl.BY_CB('created {:d} download target object(s)')
                else:
                    log_content = dl.BY_CB('created {:d} download target object(s), thread creation is blocked, please wait')
                dl.LT_FLUSH(log_content, i + 1)
            print(dl.BY_CB(', all threads have been loaded OK'))
            thread_block_flag = False

            # parent thread wait all sub-thread end
            # the count of all threads is 1 parent thread and n sub-thread(s)
            # when all pictures have been downloaded over, thread count is 1
            while alive_thread_cnt > 1:
                # global variable update
                self.alivethread_counter = threading.active_count()
                # when alive thread count change, print its value
                if alive_thread_cnt != self.alivethread_counter:
                    alive_thread_cnt = self.alivethread_counter # update alive thread count
                    # display alive sub-thread count
                    # its number wouldn't more than thread max count
                    log_content = dl.BY_CB('currently remaining sub-thread(s):({:4d}/{:4d}), completed:({:4.1%})|({:5.2f}MB)')
                    dl.LT_FLUSH(log_content, alive_thread_cnt - 1, queueLength, 
                        ((queueLength - (alive_thread_cnt - 1)) / queueLength), 
                        (float(WkvCwApi._datastream_pool / 1024)))
            print(dl.BY_CB(', sub-threads execute finished'))
        except KeyboardInterrupt:
            print(dl.BY_CB(', user interrupt a thread, exit all threads'))

    def wca_htmlpreview_build(self, workdir, html_path, log_path):
        """Build a html file to browse image

        @@API that allows external calls
        This function is not written by me, but I don't remember where it was copied
        If the original author sees this code, please be sure to submit an issue 
            to contact me to add your copyright logo
        If you run this crawler in server, you can use python simple http server
        and the html file built by this function to browse result
        :param self:        class self
        :param workdir:     work directory
        :param html_path:   html file save path
        :param log_path:    log save path
        :return:            none
        """
        html_file = open(html_path, "w")
        html_file.writelines(
            "<!Doctype html>\r\n"
            "<html>\r\n"
            "<head>\r\n"
            "<title>%s ResultPage</title>\r\n"          # HTML page title
            "</head>\r\n"
            "<body>\r\n" % dl.PROJECT_NAME)
        # put all crawl images into html source code
        html_file.writelines(
            # here call javascript method to collect all of images
            "<script>window.onload = function(){"
                "var imgs = document.getElementsByTagName('img');"
                "for (var i = 0; i < imgs.length; i++) {"
                    # function: click once any image, it will restore the original size
                    "imgs[i].onclick = function(){"
                        "if (this.width == this.attributes['oriWidth'].value "
                            "&& this.height == this.attributes['oriHeight'].value) {"
                            "this.width = this.attributes['oriWidth'].value * 1.0 "
                            "/ this.attributes['oriHeight'].value * 200;"
                            "this.height = 200;"
                        "} else {this.width = this.attributes['oriWidth'].value ;"
                        "this.height = this.attributes['oriHeight'].value;}}}};"
            "</script>")
        for i in os.listdir(workdir):
            # match image formats
            if i[-4:len(i)] in [".png", ".jpg", ".bmp"]:
                width, height = Image.open(
                    workdir + '/' + i).size
                i = i.replace("#", "%23")
                ## html_file.writelines("<a href = \"%s\">"%("./" + filename))
                html_file.writelines(
                    "<img src = \"%s\" width = \"%dpx\" height = \"%dpx\" "
                    "oriWidth = %d oriHeight = %d />\r\n"
                    % ("./" + i, width * 1.0 / height * 200, 200, width, height))
                ## html_file.writelines("</a>\r\n")
        html_file.writelines(
            "</body>\r\n"
            "</html>")
        html_file.close()
        log_content = 'image browse html file generate ok'
        self.wca_logprowork(log_path, log_content)
