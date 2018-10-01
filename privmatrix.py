#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# write all universal function into a class and package them

from __future__ import print_function
import urllib.request, urllib.parse, urllib.error, http.cookiejar
from retrying import retry
import threading
from Crypto.Cipher import AES
from Crypto import Random
from PIL import Image
from collections import OrderedDict
import time, random, re, os, getpass
from functools import wraps
import dataload

class Matrix:
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
    |       Version: 2.6.5 LTE                                                                                      |
    |       Code by </MATRIX>@Neod Anderjon(LeaderN)                                                                |
    |       PixivCrawlerIII Help Page                                                                               |
    |       1.rtn  ---     RankingTopN, crawl Pixiv daily/weekly/month ranking top artworks                         |
    |       2.ira  ---     IllustRepoAll, crawl Pixiv any illustrator all repertory artworks                        |
    |       3.help ---     Print this help page                                                                     |
    =================================================================================================================
    """

    login_bias = []
    _proxy_hasrun_flag, _datastream_pool, _alivethread_counter = False, 0, 0

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
                "[!Username] %s\n[!Password] %s\n"
                "Is that correct?(y/N): " % (username, passwd))

            # if user judge info are error, delete old AES file and record new info
            if check != 'y' and check != 'Y':
                # delete old AES file
                os.remove(aes_file_path)

                # temp input content
                dataload.logtime_print(
                    "Well, you need hand-input your login data: ")
                username = dataload.logtime_input(
                    'Enter your pixiv id(mailbox), must be a R18: ')
                passwd = getpass.getpass(
                    dataload.realtime_logword(dataload.base_time)
                    + 'Enter your account password: ')

                # generate random aes iv param
                generate_aes_iv_param = Random.new().read(AES.block_size)
                # encrypt login info
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
                # close file
                write_aes_file.close()
            # read info correct, jump out here
            else:
                pass

        # if no AES file, then create new and write md5 value into it
        else:
            dataload.logtime_print(
                "Create new AES encrypt file to storage your username and password: ")
            username = dataload.logtime_input(
                'Enter your pixiv id(mailbox), must be a R18: ')
            passwd = getpass.getpass(
                dataload.realtime_logword(dataload.base_time)
                + 'Enter your account password: ')

            # generate random aes iv param
            generate_aes_iv_param = Random.new().read(AES.block_size)
            # encrypt login info
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
            # close file
            write_aes_file.close()

        # build data string
        getway_register = [('user', username), ('pass', passwd)]
        getway_data = urllib.parse.urlencode(getway_register).encode(encoding='UTF8')

        return username, passwd, getway_data                        # return login use 3 elements

    @staticmethod
    def logprowork(log_path, log_content, withtime='y'):
        """Universal work log save

        :param log_path:    log save path
        :param log_content: log save content
        :param withtime:    default parameter, print and save with real time or not
        :return:            none
        """
        # add context to the file use option 'a+'
        # write content may have some not utf8 code, example Japanese
        log_file_ptr = open(log_path, 'a+', encoding='utf-8')

        # select add real time word
        if withtime == 'y':
            dataload.logtime_print(log_content)
            # use variable-length argument write word to the log file
            print(dataload.realtime_logword(dataload.base_time)
                                + log_content, file=log_file_ptr)
        else:
            print(log_content)
            print(log_content, file=log_file_ptr)

    def mkworkdir(self, log_path, folder):
        """Create a crawler work directory

        :param self:        self class
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

    def _getproxyserver(self, log_path):
        """Catch a proxy server

        When crwaler crawl many times website forbidden host ip
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

    def _gatherpostkey(self, log_path):
        """POST way login need post-key

        :param log_path:    log save path
        :return:            post way request data
        """

        # call gather login data function
        self.login_bias = self._login_preload(dataload.LOGIN_AES_INI_PATH)

        # request a post key
        try:
            response = self.opener.open(
                dataload.LOGIN_POSTKEY_URL,
                timeout=30)
        except Exception as e:
            log_context = "Error type: " + str(e)
            self.logprowork(log_path, log_context)
            response = None

        # if response failed, crawler must exit
        if response is not None:
            if response.getcode() == dataload.HTTP_OK_CODE_200:
                log_context = 'POST-key response successed'
            else:
                log_context = 'POST-key response not ok, return code: %d' \
                            % response.getcode()
            self.logprowork(log_path, log_context)
        else:
            log_context = 'Get post-key request failed, check network and proxy setting, crawler exit'
            self.logprowork(log_path, log_context)
            exit()

        # cookie check
        for item in self.cookie:
            log_context = 'Cookie: [name:' + item.name + '-value:' + item.value + ']'
            self.logprowork(log_path, log_context)

        # mate post key
        web_src = response.read().decode("UTF-8", "ignore")
        post_pattern = re.compile(dataload.POSTKEY_REGEX, re.S)
        postkey = re.findall(post_pattern, web_src)[0]
        log_context = 'Get post-key: ' + postkey
        self.logprowork(log_path, log_context)

        # build post-way data order dict
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

        # clear username and password cache
        ## del self.login_bias

        return postway_data

    def camouflage_login(self, log_path):
        """Camouflage browser to login

        :param log_path: log save path
        :return:        none
        """
        # login init need to commit post data to Pixiv
        postway_data = self._gatherpostkey(log_path)

        # the most important step
        # if this step failed, then crawler will exit 
        try:
            response = self.opener.open(
                fullurl=dataload.LOGIN_REQUEST_URL,
                data=postway_data,
                timeout=30)
        except Exception as e:
            log_context = "Error Type: " + str(e)
            self.logprowork(log_path, log_context)
            response = None

        # if login failed, crawler must exit
        if response is not None:
            if response.getcode() == dataload.HTTP_OK_CODE_200:
                log_context = 'Login response successed'
            else:
                log_context = 'Login response not ok, return code %d' \
                            % response.getcode()
            self.logprowork(log_path, log_context)
        else:
            log_context = 'Get login request failed, check network and proxy, crawler exit'
            self.logprowork(log_path, log_context)
            exit()

    def save_test_html(self, workdir, content, log_path):
        """Save request web source page in a html file, test use

        :param workdir:     work directory
        :param content:     save content
        :param log_path:    log save path
        :return:            none
        """
        htmlfile = open(workdir + dataload.fs_operation[1] + 'test.html', "w")
        htmlfile.write(content)
        htmlfile.close()
        log_context = 'Save test request html page ok'
        self.logprowork(log_path, log_context)

    @staticmethod
    def commit_spansizer(whole_pattern, info_pattern, web_src):
        """A sizer for all of images in once commit item

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
        """Download one target image, then multi-process will call here

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

        # use urlretrieve() method:
        # def __progress(count, block_size, total_size):
        #     """Use in urllib.request.urlretrieve() function display progress
        #
        #     :param count:       finished part size
        #     :param block_size:  data block size
        #     :param total_size:  remote file size
        #     :return:            none
        #     """
        #     finish_percent = float(100.0 * count * block_size / total_size)
        #     if finish_percent > 100:
        #         finish_percent = 100
        #     # flush finished percent
        #     # if use in multi-threads crawler, target number will flush with percent
        #     sys.stdout.write('\r' + dataload.realtime_logword(dataload.base_time)
        #         + 'Target no.%d finished percent: %.1f%%'
        #             % ((index + 1), finish_percent))
        #     sys.stdout.flush()
        # urllib.request.urlretrieve(url=url,
        #                            filename=img_save_path,
        #                            reporthook=__progress)

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
            ## log_context = "Error Type: " + str(e)
            ## self.logprowork(logpath, log_context)
            # http error 404, change image type
            if e.code == dataload.HTTP_NOTFOUND_CODE_404:
                img_datatype = 'jpg'                    # change data type
                jpg_img_url = url[0:-3] + img_datatype  # replace url content
                # after change image type word try again
                try:
                    response = self.opener.open(fullurl=jpg_img_url, timeout=timeout)
                except urllib.error.HTTPError as e:
                    ## log_context = "Error Type: " + str(e)
                    ## self.logprowork(logpath, log_context)
                    # not 404 change proxy, cause request server forbidden
                    if e.code != dataload.HTTP_NOTFOUND_CODE_404:
                        log_context = "Add proxy server in request"
                        self.logprowork(log_path, log_context)
                        # preload a proxy handler, just run once
                        if self._proxy_hasrun_flag is False:
                            self._proxy_hasrun_flag = True
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
            self._datastream_pool += source_size
            # save image bin data
            with open(img_save_path, 'wb') as img:
                img.write(img_bindata)
            log_context = 'Target no.%d(%s) image download finished, image size: %dkB' \
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

        def __init__(self, lock, i, img_url, basepages, img_savepath, log_path, thmax):
            """Provide class arguments

            :param lock:            object lock
            :param i:               image index
            :param img_url:         image url
            :param basepages:       referer basic page
            :param img_savepath:    image save path
            :param log_path:        log save path
            :param thmax:           thread queue max count
            """

            threading.Thread.__init__(self)     # callable class init
            self.lock = lock
            self.i = i
            self.img_url = img_url
            self.base_pages = basepages
            self.img_path = img_savepath
            self.logpath = log_path
            self.thmax = thmax

        def run(self):
            """Overwrite threading.thread run() method

            :return:    none
            """
            try:
                # try to create a new thread
                Matrix()._save_oneimage(self.i, self.img_url, self.base_pages,
                                        self.img_path, self.logpath)
            except Exception as e:
                log_context = "Error Type: " + str(e)
                Matrix.logprowork(log_context, self.logpath)

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

        Using python decorator feature to design program runtime timer
        In this project this function only have used in internal call
        But it also can be used in external call
        :param origin_func: decorated function
        :return:            wrapper function
        """

        @wraps(origin_func)     # reserve property of original function 
        def wrapper(self, log_path, *args, **kwargs):
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
            average_download_speed = float(self._datastream_pool / elapesd_time)
            log_context = (
                "All of threads reclaim, total download data-stream size: %0.2fMB, "
                "average download speed: %0.2fkB/s"
                % (float(self._datastream_pool / 1024), average_download_speed))
            self.logprowork(log_path, log_context)

        return wrapper

    @timer_decorator            # add timig decorator
    def download_alltarget(self, log_path, urls, basepages, workdir):
        """Multi-process download all image

        :param urls:        all original images urls
        :param basepages:   all referer basic pages
        :param workdir:     work directory
        :param log_path:    log save path
        :return:            none
        """

        # here init var alive thread count
        aliveThreadCnt = queueLength = len(urls)
        # first push N tasks to stack 
        thread_max_count = queueLength if queueLength \
            <= dataload.SYSTEM_MAX_THREADS \
            else queueLength - dataload.SYSTEM_MAX_THREADS 
        log_context = 'Start to download %d target(s)======>' % queueLength
        self.logprowork(log_path, log_context)

        # create overwrite threading.Thread object
        lock = threading.Lock()
        for i, one_url in enumerate(urls):
            # handle thread create max limit
            lock.acquire()
            # if now all of threads count less than limit, ok
            if len(self._MultiThreading.queue_t) \
                    > thread_max_count:
                lock.release()
                # wait last threads work end
                self._MultiThreading.event_t.wait()
            else:
                lock.release()
            # continue to create new one
            sub_thread = self._MultiThreading(lock, i, one_url,
                        basepages, workdir, log_path, thread_max_count)
            # set every download sub-process daemon property
            # set false, then if you exit one thread, others threads will not end
            # set true, quit one is quit all
            sub_thread.setDaemon(True)            
            sub_thread.create()

        # parent thread wait all sub-thread end
        while aliveThreadCnt > 1:
            # global variable update
            self._alivethread_counter = threading.active_count()
            # when alive thread count change, print its value
            if aliveThreadCnt != self._alivethread_counter:
                # update alive thread count
                aliveThreadCnt = self._alivethread_counter
                log_context = ('Currently remaining sub-thread(s): %d/%d'
                              % (aliveThreadCnt - 1, queueLength))
                self.logprowork(log_path, log_context)

    def htmlpreview_build(self, workdir, html_path, log_path):
        """Build a html file to browse image

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
            "<title>PixivCrawlerIII ResultPage</title>\r\n"
            "</head>\r\n"
            "<body>\r\n")
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

    def work_finished(self, log_path):
        """Work finished log

        :param log_path:    log save path
        :return:            none
        """

        # logo display
        log_context = (
            dataload.LABORATORY + ' ' + dataload.ORGANIZATION + ' technology support |'                       
            ' Code by ' + dataload.ORGANIZATION + '@' + dataload.DEVELOPER)
        self.logprowork(log_path, log_context)
        # open work directory, check result
        ## os.system(dataload.fs_operation[2] + ' ' + dataload.fs_operation[0])

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
