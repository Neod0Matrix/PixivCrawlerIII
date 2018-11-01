#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# write all universal function into a class and package them

from __future__ import print_function
import urllib.request, urllib.parse, urllib.error, http.cookiejar   # crawler main modules
from retrying import retry          # timeout auto retry decorator
import threading                    # multi-thread
from Crypto.Cipher import AES       # user info local crypto storage
from Crypto import Random           
from PIL import Image               # image process module
from collections import OrderedDict # order dictory
import time, random, re, os, getpass
from functools import wraps         # decorator wrapper
import dataload

class PixivAPILib:
    """
    =================================================================================================================
    |       ██████╗ ██╗██╗  ██╗██╗██╗   ██╗ ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ ██╗██╗██╗      |
    |       ██╔══██╗██║╚██╗██╔╝██║██║   ██║██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗██║██║██║      |
    |       ██████╔╝██║ ╚███╔╝ ██║██║   ██║██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝██║██║██║      |
    |       ██╔═══╝ ██║ ██╔██╗ ██║╚██╗ ██╔╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗██║██║██║      |
    |       ██║     ██║██╔╝ ██╗██║ ╚████╔╝ ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║██║██║██║      |
    |       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝╚═╝      |
    |                                                                                                               |
    |       Copyright (c)2018 T.WKVER </MATRIX> Neod Anderjon(LeaderN)                                              |
    |       Version: 2.8.6 LTE                                                                                      |
    |       Code by </MATRIX>@Neod Anderjon(LeaderN)                                                                |
    |       PixivCrawlerIII Help Page                                                                               |
    |       1.rtn  ---     RankingTopN, crawl Pixiv daily/weekly/month ranking top artworks                         |
    |       2.ira  ---     IllustRepoAll, crawl Pixiv any illustrator all repertory artworks                        |
    |       3.help ---     Print this help page                                                                     |
    |       4.exit ---     Exit crawler program                                                                     |
    =================================================================================================================
    """

    # this download data stream counter involves the simultaneous access of multi-threaded resources
    # which must be declared as class attribute # variables for access
    _datastream_pool = 0    

    def __init__(self):
        """Create a class public call webpage opener with cookie

        From first login save cookie and continue call
        Call this global opener must write parameter name
        Cookie, cookiehandler, opener all can inherit and call
        """
        self.cookie = http.cookiejar.LWPCookieJar()
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.cookieHandler)
        urllib.request.install_opener(self.opener)
        # class inside global variable
        self.login_bias = []
        self.proxy_hasrun_flag = False
        self.alivethread_counter = 0

    @staticmethod
    def _login_preload(aes_file_path):
        """Get user input login info and storage into aes file

        If project directory has no file, you need hand-input login info,
        then program will create new file to storage AES encrypt info to it
        This method use pycrypto, need import external call
        :param aes_file_path:       .aes_crypto_login.ini file path
        :return:                    username, password, get data
        """
        is_aes_file_existed = os.path.exists(aes_file_path)
        if is_aes_file_existed:
            # stable read rows get username and password
            # read bin file content to a list
            read_aes_file = open(aes_file_path, 'rb+')
            readline_cache = read_aes_file.readlines()                      # all line list
            read_aes_file.close()           

            read_aes_iv_param_raw = readline_cache[0]                       # row 1 is AES IV PARAM
            read_user_mailbox_raw = readline_cache[1]                       # row 2 is username
            read_user_passwd_raw = readline_cache[2]                        # row 3 is password   
            # cut last char (b'\n')
            read_aes_iv_param_raw = read_aes_iv_param_raw[:-1]
            read_user_mailbox_raw = read_user_mailbox_raw[:-1]
            read_user_passwd_raw = read_user_passwd_raw[:-1]

            # analysis hash value to string
            username_aes_decrypt_cipher = AES.new(dataload.AES_SECRET_KEY, AES.MODE_CFB, read_aes_iv_param_raw)
            username = str(username_aes_decrypt_cipher.decrypt(read_user_mailbox_raw[AES.block_size:]), 'UTF-8')
            password_aes_decrypt_cipher = AES.new(dataload.AES_SECRET_KEY, AES.MODE_CFB, read_aes_iv_param_raw)
            passwd = str(password_aes_decrypt_cipher.decrypt(read_user_passwd_raw[AES.block_size:]), 'UTF-8')

            # check username and password
            check = dataload.logtime_input(
                "Read user login information configuration ok, check this: \n"
                "[-> Username] %s\n[-> Password] %s\n"
                "Is that correct? (Y/N): " % (username, passwd))

            # if user judge info are error, delete old AES file and record new info
            if check == 'N' or check == 'n':
                os.remove(aes_file_path)        # delete old AES file
                # temporarily enter login information
                dataload.logtime_print(
                    "Well, you need hand-input your login data: ")
                username = dataload.logtime_input(
                    'Enter your pixiv id(mailbox), must be a R18: ').encode('utf-8')
                passwd = getpass.getpass(
                    dataload.realtime_logword(dataload.base_time)
                    + 'Enter your account password: ').encode('utf-8')

                generate_aes_iv_param = Random.new().read(AES.block_size)   # generate random aes iv param
                username_cipher = AES.new(dataload.AES_SECRET_KEY, AES.MODE_CFB, generate_aes_iv_param)
                username_encrypto = generate_aes_iv_param + username_cipher.encrypt(username)
                passwd_cipher = AES.new(dataload.AES_SECRET_KEY, AES.MODE_CFB, generate_aes_iv_param)
                passwd_encrypto = generate_aes_iv_param + passwd_cipher.encrypt(passwd)
                
                # create new aes file rewrite it
                write_aes_file = open(aes_file_path, 'wb')
                # write bin value to file with b'\n' to wrap
                write_aes_file.write(generate_aes_iv_param + b'\n')     # row 1 is iv param
                write_aes_file.write(username_encrypto + b'\n')         # row 2 is username
                write_aes_file.write(passwd_encrypto + b'\n')           # row 3 is password
                write_aes_file.close()
            # read info correct, jump out here
            else:
                pass

        # if no AES file, then create new and write md5 value into it
        else:
            dataload.logtime_print(
                "Create new AES encrypt file to storage your username and password: ")
            username = dataload.logtime_input(
                'Enter your pixiv id(mailbox), must be a R18: ').encode('utf-8')
            passwd = getpass.getpass(
                dataload.realtime_logword(dataload.base_time)
                + 'Enter your account password: ').encode('utf-8')

            generate_aes_iv_param = Random.new().read(AES.block_size)   # generate random aes iv param
            username_cipher = AES.new(dataload.AES_SECRET_KEY, AES.MODE_CFB, generate_aes_iv_param)
            username_encrypto = generate_aes_iv_param + username_cipher.encrypt(username)
            passwd_cipher = AES.new(dataload.AES_SECRET_KEY, AES.MODE_CFB, generate_aes_iv_param)
            passwd_encrypto = generate_aes_iv_param + passwd_cipher.encrypt(passwd)
            
            # create new AES file, set write bin bytes mode
            write_aes_file = open(aes_file_path, 'wb')
            # write bin value to file with b'\n' to wrap
            write_aes_file.write(generate_aes_iv_param + b'\n')     # row 1 is iv param
            write_aes_file.write(username_encrypto + b'\n')         # row 2 is username
            write_aes_file.write(passwd_encrypto + b'\n')           # row 3 is password
            write_aes_file.close()

        # build data string
        getway_register = [('user', username), ('pass', passwd)]
        getway_data = urllib.parse.urlencode(getway_register).encode(encoding='UTF8')

        return username, passwd, getway_data                        # return login use 3 elements

    @staticmethod
    def replace_emoji(judge_str):
        """Replace emoji symbol to a replaced string

        @@API that allows external calls
        Remove trouble emoji code, if string not emoji, return origin string
        Judge method: regex match
        code by CSDN@orangleliu
        :param judge_str:   wait for judge string
        :return:            origin string or replaced string
        """
        emoji_pattern = re.compile(dataload.EMOJI_REGEX, re.S)  # re.UNICODE

        # match emoji string and replace it
        return emoji_pattern.sub(r'[EMOJI]', judge_str)

    @staticmethod
    def logprowork(log_path, log_content, withtime='y'):
        """Universal work log save

        @@API that allows external calls
        Notice: If here print series fucntion raise UnicodeEncodeError, it must web page 
        include emoji symbol encode title when use prettytable to package title info
        :param log_path:    log save path
        :param log_content: log save content
        :param withtime:    default parameter, print and save with real time or not
        :return:            none
        """
        # add context to the file use option 'a+'
        # write content may have some not utf8 code, example Japanese
        log_file_ptr = open(log_path, 'a+', encoding='utf-8')

        # select add real time word or not
        if withtime == 'y':
            dataload.logtime_print(log_content)
            # use variable-length argument write word to the log file
            log_file_ptr.write(dataload.realtime_logword(dataload.base_time)
                + log_content + '\n')
        else:
            print(log_content)
            log_file_ptr.write(log_content + '\n')
        log_file_ptr.close()

    def mkworkdir(self, log_path, folder):
        """Create a crawler work directory

        @@API that allows external calls
        :param log_path:    log save path
        :param folder:      folder create path
        :return:            folder create path
        """
        # create a folder to save picture
        dataload.logtime_print(
            'Crawler work directory setting: ' + folder)
        is_folder_existed = os.path.exists(folder)
        if not is_folder_existed:
            os.makedirs(folder)
            log_context = 'Create a new work folder'
        else:
            log_context = 'Target folder has already existed'
        # remove old log file
        if os.path.exists(log_path):
            os.remove(log_path)
        # this step will create a new log file and write the first line
        self.logprowork(log_path, log_context)

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

    def quick_sort(self, array, l, r):
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
            self.quick_sort(array, l, q - 1)
            self.quick_sort(array, q + 1, r)

    def _getproxyserver(self, log_path):
        """Catch a proxy server

        When crwaler crawl many times website forbidden host ip
        If you use VPS as a proxy server, you can set the cost proxy port directly
        Example: 127.0.0.1:1080
        :param log_path: log save path
        :return:        proxy server, add to opener
        """
        req_ps_url = dataload.PROXYSERVER_URL
        ps_headers = dataload.uc_user_agent()
        request = urllib.request.Request(
            url=req_ps_url,
            headers=ps_headers)
        try:
            response = urllib.request.urlopen(
                request,
                timeout=30)
        except Exception as e:
            log_context = "Error Type: " + str(e)
            self.logprowork(log_path, log_context)
            response = None
            # here don't exit, log error
        except KeyboardInterrupt:
            log_context = 'User interrupt, exit'
            self.logprowork(log_path, log_context)
            response = None

        # proxy error but don't exit, ignore this
        if response is not None:
            if response.getcode() == dataload.HTTP_OK_CODE_200:
                log_context = 'Crawl proxy successed'
            else:
                log_context = 'Crawl proxy not ok, return code: %d' \
                            % response.getcode()
        else:
            log_context = 'Get proxy response failed, check network'
        self.logprowork(log_path, log_context)

        web_src = response.read().decode("UTF-8", "ignore")
        proxy_pattern = re.compile(dataload.PROXYIP_REGEX, re.S)
        proxy_rawwords = re.findall(proxy_pattern, web_src)

        # catch key words in web source
        proxy_iplist = []
        for i in range(len(proxy_rawwords)):
            # base on list content set this judge way
            if i % 5 == 0 and proxy_rawwords[i].isdigit():
                # build proxy ip string
                proxy_ip = dataload.PROXYIP_STR_BUILD(i, proxy_rawwords)
                proxy_iplist.append(proxy_ip)
            else:
                pass
        # random choose a proxy ip with its port and build the dict format data
        proxy_choose = random.choice(proxy_iplist)
        proxyserver_d = {'http': proxy_choose}
        log_context = 'Choose proxy server: ' + proxy_choose
        self.logprowork(log_path, log_context)

        return proxyserver_d

    def url_request_handler(self, target_url, post_data, timeout, 
        target_page_word, need_log, log_path):
        """Universal URL request format handler

        @@API that allows external calls
        :param target_url:          target request url
        :param post_data:           post way data
        :param timeout:             request timeout, suggest 30s
        :param target_page_word:    target page symbol word
        :param need_log:            need log? True is need, then log_path is must
        :param log_path:            log save path
        :return:                    request result response(raw)
        """
        response = None
        try:
            response = self.opener.open(
                fullurl=target_url,
                data=post_data,
                timeout=timeout)
        except Exception as e:
            log_context = "Error Type: " + str(e)
            if need_log == True:
                self.logprowork(log_path, log_context)
            else:
                dataload.logtime_print(log_context)
        except KeyboardInterrupt:
            log_context = 'User interrupt request, exit program'
            if need_log == True:
                self.logprowork(log_path, log_context)
            exit()

        # if response failed, crawler will exit with error code -1
        if response is not None:
            if response.getcode() == dataload.HTTP_OK_CODE_200:
                log_context = target_page_word + ' response successed'
            else:
                log_context = (target_page_word + 
                    ' response not ok, return code %d' % response.getcode())
            if need_log == True:
                self.logprowork(log_path, log_context)
            else:
                dataload.logtime_print(log_context)
        else:
            log_context = target_page_word + ' response failed'
            if need_log == True:
                self.logprowork(log_path, log_context)
            else:
                dataload.logtime_print(log_context)
            exit(-1)

        return response

    def _gatherpostkey(self):
        """POST way login need post-key

        :return:            post way request data
        """

        # call gather login data function
        self.login_bias = self._login_preload(dataload.LOGIN_AES_INI_PATH)
        response = self.url_request_handler(
            target_url=dataload.LOGIN_POSTKEY_URL, 
            post_data=None,                 # cannot set data when get post key
            timeout=30, 
            target_page_word='POST-key',
            need_log=False,
            log_path='')
        # cookie check
        for item in self.cookie:
            log_context = 'Cookie: [name:' + item.name + '-value:' + item.value + ']'
            dataload.logtime_print(log_context)

        # mate post key
        web_src = response.read().decode("UTF-8", "ignore")
        post_pattern = re.compile(dataload.POSTKEY_REGEX, re.S)
        postkey = re.findall(post_pattern, web_src)[0]
        log_context = 'Get post-key: ' + postkey
        dataload.logtime_print(log_context)

        # build post-way data with order dictory structure
        post_orderdict = OrderedDict()
        post_orderdict['pixiv_id'] = self.login_bias[0]
        post_orderdict['password'] = self.login_bias[1]
        post_orderdict['captcha'] = ""
        post_orderdict['g_recaptcha_response'] = ""
        post_orderdict['post_key'] = postkey
        post_orderdict['source'] = "pc"
        post_orderdict['ref'] = dataload.LOGIN_POSTDATA_REF
        post_orderdict['return_to'] = dataload.HTTPS_HOST_URL
        # transfer to json data format, the same way as GET way data
        postway_data = urllib.parse.urlencode(post_orderdict).encode("UTF-8")

        return postway_data

    def camouflage_login(self):
        """Camouflage browser to login

        @@API that allows external calls
        :return:        none
        """
        # login init need to commit post data to Pixiv
        postway_data = self._gatherpostkey()
        response = self.url_request_handler(
            target_url=dataload.LOGIN_REQUEST_URL,
            post_data=postway_data, 
            timeout=30, 
            target_page_word='Login',
            need_log=False,
            log_path='')

    def save_test_html(self, workdir, content, log_path):
        """Save request web source page in a html file, test use

        @@API that allows external calls
        :param workdir:     work directory
        :param content:     save content(web source code)
        :param log_path:    log save path
        :return:            none
        """
        htmlfile = open(workdir + dataload.fs_operation[1] + 'test.html', "w", 
            encoding='utf-8')
        htmlfile.write(content)
        htmlfile.close()
        log_context = 'Save test request html page ok'
        self.logprowork(log_path, log_context)

    @staticmethod
    def unicode_escape(raw_str):
        """Transform '\\uxxx' code to unicode

        @@API that allows external calls
        Notice: code '\(uxxx)' can auto transform
        But emoji unicode can't decode
        Normally this method only use in javascript page
        :param raw_str:     wait to decode raw string
        :return:            unicode escape code
        """

        return raw_str.encode('utf-8').decode('unicode_escape')

    @staticmethod
    def commit_spansizer(whole_pattern, info_pattern, web_src):
        """A sizer for all of images in once commit item

        @@API that allows external calls
        After Pixiv 20181002 update, this method only support mode rtn
        :param whole_pattern:   whole info data regex compile pattern
        :param info_pattern:    image info regex compile pattern
        :param web_src:         webpage source
        :return:                original target urls, image infos
        """
        gather_info, gather_url = [], []
        datasrc_pattern = re.compile(dataload.DATASRC_REGEX, re.S)
        span_pattern = re.compile(dataload.SPAN_REGEX, re.S)
        img_whole_info = re.findall(whole_pattern, web_src)
        # image have 3 format: jpg/png/gif
        # this crawler will give gif format up and crawl png or jpg
        # pixiv one repertory maybe have multi-images
        for item in img_whole_info:
            # get judge key word
            thumbnail = re.findall(datasrc_pattern, item)[0]
            judge_word = thumbnail[-18:]

            # check jpg/png or gif
            if judge_word == dataload.JUDGE_NOGIF_WORD:
                span_word = re.findall(span_pattern, item)
                # get vaild word
                vaild_word = thumbnail[44:-18]

                # try to check multi-span images
                if len(span_word) != 0:
                    # one commit artwork has more pages, iter it
                    for _px in range(int(span_word[0])):
                        # set same info
                        info = re.findall(info_pattern, item)[0]
                        gather_info.append(info)
                        # more pages point, range 0~span-1
                        target_url = dataload.ORIGINAL_IMAGE_HEAD + vaild_word \
                                     + dataload.ORIGINAL_IMAGE_TAIL(_px)
                        gather_url.append(target_url)
                # just only one picture in a commit
                else:
                    info = re.findall(info_pattern, item)[0]
                    gather_info.append(info)
                    # only _p0 page
                    target_url = dataload.ORIGINAL_IMAGE_HEAD + vaild_word \
                                 + dataload.ORIGINAL_IMAGE_TAIL(0)
                    gather_url.append(target_url)  
            # give up gif format
            else:
                pass

        return gather_url, gather_info

    @retry              # retrying decorator call
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
        # setting image save info
        img_datatype = 'png'
        image_name = url[57:-4]             # name artwork_id + _px
        img_save_path = (img_savepath + dataload.fs_operation[1]
                         + image_name + '.' + img_datatype)

        # use opener method
        headers = dataload.build_original_headers(basepages[index])
        proxy_handler = None
        response = None
        timeout = 30
        list_headers = dataload.dict_transto_list(headers)
        self.opener.addheaders = list_headers
        urllib.request.install_opener(self.opener)  # update install opener

        # this request image step will delay much time
        try:
            response = self.opener.open(fullurl=url, timeout=timeout)
        # first request fatal
        except urllib.error.HTTPError as e:
            ## log_context = "Error type: " + str(e)
            ## self.logprowork(logpath, log_context)
            # http error 404, change image type
            if e.code == dataload.HTTP_NOTFOUND_CODE_404:
                img_datatype = 'jpg'                    # change data type
                jpg_img_url = url[0:-3] + img_datatype  # replace url content
                # after change image type word try again
                try:
                    response = self.opener.open(fullurl=jpg_img_url, timeout=timeout)
                except urllib.error.HTTPError as e:
                    ## log_context = "Error type: " + str(e)
                    ## self.logprowork(logpath, log_context)
                    # not 404 change proxy, cause request server forbidden
                    if e.code != dataload.HTTP_NOTFOUND_CODE_404:
                        log_context = "Add proxy server in request"
                        self.logprowork(log_path, log_context)
                        # preload a proxy handler, just run once
                        if self.proxy_hasrun_flag == False:
                            self.proxy_hasrun_flag = True
                            proxy = self._getproxyserver(log_path)
                            proxy_handler = urllib.request.ProxyHandler(proxy)
                        # with proxy request again
                        self.opener = urllib.request.build_opener(proxy_handler)
                        response = self.opener.open(fullurl=jpg_img_url, timeout=timeout)
                    else:
                        pass
            # if timeout, use proxy reset request
            else:
                log_context = "Add proxy server in request"
                self.logprowork(log_path, log_context)
                # with proxy request again
                self.opener = urllib.request.build_opener(proxy_handler)
                response = self.opener.open(fullurl=url, timeout=timeout)

        # save image bin data to files
        if response.getcode() == dataload.HTTP_OK_CODE_200:
            img_bindata = response.read()
            # calcus target source total size
            source_size = float(len(img_bindata) / 1024)
            # multi-thread, no resource lock, it must use class name to call
            PixivAPILib._datastream_pool += source_size   
            # save image bin data
            with open(img_save_path, 'wb') as img:
                img.write(img_bindata)
            log_context = 'No.%d target[%s] download finished, image size [%dkB]' \
                % (index + 1, image_name, source_size)
            self.logprowork(log_path, log_context)

    class _MultiThreading(threading.Thread):
        """Overrides its run method by inheriting the Thread class

        This class can be placed outside the main class, you can also put inside
        Threads are the smallest unit of program execution flow
        That is less burdensome than process creation
        Only internal call
        """

        # handle thread max limit
        queue_t = []
        event_t = threading.Event()     # use event let excess threads wait

        def __init__(self, lock, thmax, index, url, basepages, workdir, log_path):
            """Provide class arguments

            :param lock:                            object lock
            :param thmax:                           thread queue max count
            :param index, url, basepages, workdir:  function _save_oneimage param
            :param log_path:                        log save path
            """
            threading.Thread.__init__(self)     # callable class init
            self.lock = lock
            self.thmax = thmax
            self.index = index
            self.url = url
            self.basepages = basepages
            self.workdir = workdir
            self.logpath = log_path

        def run(self):
            """Overwrite threading.thread run() method

            :return:    none
            """
            try:
                # try to create a new thread
                PixivAPILib()._save_oneimage(self.index, self.url, 
                    self.basepages, self.workdir, self.logpath)
            except Exception as e:
                log_context = "Error Type: " + str(e)
                PixivAPILib.logprowork(log_context, self.logpath)

            self.lock.acquire()
            if len(self.queue_t) == self.thmax - 1:
                self.event_t.set()
                self.event_t.clear()
            self.queue_t.remove(self)       # remove end thread from list       
            self.lock.release()

        def create(self):
            """Create a new thread

            It can handle more over threads create
            :return:    none
            """
            self.lock.acquire()
            self.queue_t.append(self)
            self.lock.release()
            self.start()        # finally call start() method 

    def timer_decorator(origin_func):
        """Timer decorator

        @@API that allows external calls
        Using python decorator feature to design program runtime timer
        In this project this function only have used in internal call
        But it also can be used in external call
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

            log_context = "Launch timer decorator, start program runtime timer..."
            self.logprowork(log_path, log_context)
            starttime = time.time()    

            # packaged original function 
            origin_func(self, log_path, *args, **kwargs)       

            endtime = time.time()
            elapesd_time = endtime - starttime
            average_download_speed = float(PixivAPILib._datastream_pool / elapesd_time)
            log_context = (
                "All of threads reclaim, total download data-stream size: %0.2fMB, "
                "average download speed: %0.2fkB/s"
                % (float(PixivAPILib._datastream_pool / 1024), average_download_speed))
            self.logprowork(log_path, log_context)
            PixivAPILib._datastream_pool = 0   # once task finished, clear pool cache

        return _wrapper

    @timer_decorator            # add timig decorator
    def download_alltarget(self, log_path, urls, basepages, workdir):
        """Multi-process download all image

        @@API that allows external calls
        :param urls:        all original images urls
        :param basepages:   all referer basic pages
        :param workdir:     work directory
        :param log_path:    log save path
        :return:            none
        """
        # here init var alive thread count
        alive_thread_cnt = queueLength = len(urls)
        # first push N tasks to stack 
        thread_max_count = queueLength if queueLength \
            <= dataload.SYSTEM_MAX_THREADS \
            else queueLength - dataload.SYSTEM_MAX_THREADS 
        log_context = 'Start to download %d target(s)======>' % queueLength
        self.logprowork(log_path, log_context)

        try:
            # create overwrite threading.Thread object
            lock = threading.Lock()
            for i, one_url in enumerate(urls):
                lock.acquire()          # handle thread create max limit
                # if now all of threads count less than limit, ok
                if len(self._MultiThreading.queue_t) > thread_max_count:
                    lock.release()
                    self._MultiThreading.event_t.wait() # wait last threads work end
                else:
                    lock.release()
                # continue to create new one
                sub_thread = self._MultiThreading(lock, thread_max_count, i, 
                    one_url, basepages, workdir, log_path)
                # set every download sub-process daemon property
                # set false, then if you exit one thread, others threads will not end
                # set true, quit one is quit all
                sub_thread.setDaemon(True)            
                sub_thread.create()

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
                    log_context = ('Currently remaining sub-thread(s): %d/%d'
                        % (alive_thread_cnt - 1, queueLength))
                    self.logprowork(log_path, log_context)
        # user press ctrl+c interrupt thread
        except KeyboardInterrupt:
            log_context = 'User interrupt thread, exit'
            self.logprowork(log_path, log_context)

    def htmlpreview_build(self, workdir, html_path, log_path):
        """Build a html file to browse image

        @@API that allows external calls
        This function is not written by me, but I don't remember where it was copied
        :param self:        class self
        :param workdir:     work directory
        :param html_path:   html file save path
        :param log_path:    log save path
        :return:            none
        """

        html_file = open(html_path, "w")
        # build html background page text
        # write a title
        html_file.writelines(
            "<html>\r\n"
            "<head>\r\n"
            "<title>%s ResultPage</title>\r\n"
            "</head>\r\n"
            "<body>\r\n" % dataload.PROJECT_NAME)
        # put all crawl images into html source code
        html_file.writelines(
            "<script>window.onload = function(){"
                "var imgs = document.getElementsByTagName('img');"
                "for(var i = 0; i < imgs.length; i++){"
                    "imgs[i].onclick = function(){"
                        "if(this.width == this.attributes['oriWidth'].value "
                            "&& this.height == this.attributes['oriHeight'].value){"
                            "this.width = this.attributes['oriWidth'].value * 1.0 "
                            "/ this.attributes['oriHeight'].value * 200;"
                            "this.height = 200;"
                        "}else{this.width = this.attributes['oriWidth'].value ;"
                        "this.height = this.attributes['oriHeight'].value;}}}};"
            "</script>")
        for i in os.listdir(workdir):
            if i[-4:len(i)] in [".png", ".jpg", ".bmp"]:
                width, height = Image.open(
                    workdir + dataload.fs_operation[1] + i).size
                i = i.replace("#", "%23")
                ## html_file.writelines("<a href = \"%s\">"%("./" + filename))
                # set image size
                html_file.writelines(
                    "<img src = \"%s\" width = \"%dpx\" height = \"%dpx\" "
                    "oriWidth = %d oriHeight = %d />\r\n"
                    % ("./" + i, width * 1.0 / height * 200, 200, width, height))
                ## html_file.writelines("</a>\r\n")

        # end of htmlfile
        html_file.writelines(
            "</body>\r\n"
            "</html>")
        html_file.close()

        log_context = 'Image browse html generate finished'
        self.logprowork(log_path, log_context)

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
