#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# list all constant data

import time, os

# project info
PROJECT_NAME        = 'PixivCrawlerIII'
DEVELOPER           = 'Neod Anderjon(LeaderN)'
LABORATORY          = 'T.WKVER'
ORGANIZATION        = '</MATRIX>'
VERSION             = '2.8.6'

# logfile log real-time operation
base_time = time.time()
realtime_logword = lambda bt: "[%02d:%02d:%02d] " \
                              % (int((time.time() - bt) / 3600),
                                int((time.time() - bt) / 60),
                                (time.time() - bt) % 60)

SHELL_BASHHEAD = PROJECT_NAME + '@' + ORGANIZATION + ':~$ '
logtime_input = lambda str_: input(realtime_logword(base_time) + str_)
logtime_print = lambda str_: print(realtime_logword(base_time) + str_)

SYSTEM_MAX_THREADS = 500                # setting system can contain max tasks
DEFAULT_PURE_PROXYDNS = '8.8.8.8:53'    # default pure dns by Google

def platform_setting():
    """Set os platform to set folder format

    Folder must with directory symbol '/' or '\\'
    :return:    platform work directory
    """
    
    work_dir, symbol, file_manager = None, None, None
    home_dir = os.environ['HOME']   # get system default setting home folder, for windows
    get_login_user = os.getlogin()  # get login user name to build user home directory, for linux
    # linux
    if os.name == 'posix':
        work_dir, symbol = '/home/' + get_login_user + '/Pictures/Crawler/', '/'
        file_manager = 'nautilus'
    # windows
    elif os.name == 'nt':
        work_dir, symbol = home_dir + '\\PictureDatabase\\Crawler\\', '\\'
        file_manager = 'explorer'
    else:
        pass

    return work_dir, symbol, file_manager
# for filesystem operation entity
fs_operation = platform_setting()

# real time clock
_rtc = time.localtime()
_ymd = '%d-%d-%d' % (_rtc[0], _rtc[1], _rtc[2])

# AES encrypto use secret key
AES_SECRET_KEY = 'secretkeyfrommat'.encode('utf-8')     # 16 bytes secret key

# universal path
LOGIN_AES_INI_PATH = os.getcwd() + fs_operation[1] + '.aes_crypto_login.ini' # storage login info AES crypto file, default hide
LOG_NAME = fs_operation[1] + 'CrawlerWork[%s].log' % _ymd
HTML_NAME = fs_operation[1] + 'CrawlerWork[%s].html' % _ymd
RANK_DIR = fs_operation[0] + 'rankingtop_%s%s' % (_ymd, fs_operation[1])
# rankingtop use path
LOG_PATH = RANK_DIR + LOG_NAME
HTML_PATH = RANK_DIR + HTML_NAME
# illustrepo use path
REPO_DIR = fs_operation[0]

# login and request image https proxy
# website may update or change some url address
WWW_HOST_URL = "www.pixiv.net"
HTTPS_HOST_URL = 'https://www.pixiv.net/'
ACCOUNTS_URL = "accounts.pixiv.net"
LOGIN_POSTKEY_URL = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
LOGIN_POSTDATA_REF = 'wwwtop_accounts_index'
LOGIN_REQUEST_URL = "https://accounts.pixiv.net/api/login?lang=en"
_LOGIN_REQUEST_URL = "https://accounts.pixiv.net"
# request universal original image constant words
ORIGINAL_IMAGE_HEAD = 'https://i.pximg.net/img-original/img'
####NEW_WEBSITE_FORMAT
ORIGINAL_IMAGE_PAGE = lambda iid, px: 'https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=%s&page=%d' % (iid, px)
ORIGINAL_IMAGE_TAIL = lambda px: '_p%d.png' % px
# page request http proxy
PROXYSERVER_URL = 'http://www.xicidaili.com/nn/'
# ranking top url and word
RANKING_URL = 'http://www.pixiv.net/ranking.php?mode='
R18_WORD = '_r18'
DAILY_WORD = 'daily'
WEEKLY_WORD = 'weekly'
MONTHLY_WORD = 'monthly'
DAILY_RANKING_URL = RANKING_URL + DAILY_WORD
WEEKLY_RANKING_URL = RANKING_URL + WEEKLY_WORD
MONTHLY_RANKING_URL = RANKING_URL + MONTHLY_WORD
DAILY_RANKING_R18_URL = DAILY_RANKING_URL + R18_WORD
WEEKLY_RANKING_R18_URL = WEEKLY_RANKING_URL + R18_WORD
BASEPAGE_URL = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id='
MEMBER_URL = 'http://www.pixiv.net/member.php?id='
MEMBER_ILLUST_URL = 'http://www.pixiv.net/member_illust.php?id='
AJAX_ALL_URL = lambda aid: 'http://www.pixiv.net/ajax/user/%s/profile/all' % aid
IDS_UNIT = lambda iid: 'ids%%5B%%5D=%s&' % iid      # ids[]=
ALLREPOINFO_URL = lambda aid, ids_sym: \
    'http://www.pixiv.net/ajax/user/%s/profile/illusts?%sis_manga_top=0' % (aid, ids_sym)
ONE_PAGE_COMMIT = 48
JUDGE_NOGIF_WORD = '_p0_master1200.jpg'             # don't download gif format
PROXYIP_STR_BUILD = lambda ix, list_: 'http://' + list_[ix - 1] + ':' + list_[ix]

# http status code
HTTP_OK_CODE_200 = 200
HTTP_REQUESTFAILED_CODE_403 = 403
HTTP_NOTFOUND_CODE_404 = 404
# login headers info dict
_USERAGENT_LINUX = ("Mozilla/5.0 (X11; Linux x86_64) " 
                   "AppleWebKit/537.36 (KHTML, like Gecko) " 
                   "Chrome/56.0.2924.87 Safari/537.36")
_USERAGENT_WIN = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) " 
                    "Chrome/60.0.3112.90 Safari/537.36")
_HEADERS_ACCEPT = "application/json, text/javascript, */*; q=0.01"
_HEADERS_ACCEPT2 = ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/webp,image/apng,*/*;q=0.8")
_HEADERS_ACCEPT_ENCODING = "gzip, deflate, br"
_HEADERS_ACCEPT_ENCODING2 = "br"   # request speed slowly, but no error
_HEADERS_ACCEPT_LANGUAGE = "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2"
_HEADERS_CACHE_CONTROL = "no-cache"
_HEADERS_CONNECTION = "keep-alive"
_HEADERS_CONTENT_TYPE = "application/x-www-form-urlencoded; charset=UTF-8"
_HEADERS_XMLHTTPREQUEST = "XMLHttpRequest"

# some regex words depend on website url or webpage source
# if website update or change them, regex need to be updated 
POSTKEY_REGEX = 'key".*?"(.*?)"'
# group match info
RANKING_INFO_REGEX = (
    'data-rank-text="(.*?)" data-title="(.*?)" data-user-name="(.*?)"'
    '.*?data-id="(.*?)".*?data-user-id="(.*?)"')
NUMBER_REGEX = '\d+\.?\d*'              # universal number match
IMAGEITEM_REGEX = '<li class="image-item">(.*?)</li>'
DATASRC_REGEX = 'data-src="(.*?)"'
ILLUST_NAME_REGEX = '<title>「(.*?)」'
AJAX_ALL_IDLIST_REGEX = '"(.*?)":null'
AJAX_INFO_REGEX = 'ter(.*?)_p0_square1200'
PAGE_REQUEST_SYM_REGEX = '"error":(.*?),'
PAGE_TARGET_INFO_REGEX = \
    '"id":"(.*?)","title":"(.*?)"(.*?)"url":"(.*?)_square1200.jpg"(.*?)"pageCount":(.*?),'
ILLUST_TYPE_REGEX = '"illustType":(.*?),'
SPAN_REGEX = '<span>(.*?)</span>'
RANKING_SECTION_REGEX = '<section id=(.*?)</section>'
PROXYIP_REGEX = '<td>(.*?)</td>'
#### code by CSDN@orangleliu
EMOJI_REGEX = (u"(\ud83d[\ude00-\ude4f])|"      # emoticons
    u"(\ud83c[\udf00-\uffff])|"                 # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"                 # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"                 # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"                  # flags (iOS)
    "+")

def dict_transto_list (input_dict):
    """Change dict data-type to list

    :param input_dict:      dict
    :return:                list
    """
    result_list = []
    for key, value in list(input_dict.items()):
        item = (key, value)
        result_list.append(item)

    return result_list

def uc_user_agent():
    """Choose platform user-agent headers

    :return:    headers
    """
    # build dict word
    ua_headers_linux = {'User-Agent': _USERAGENT_LINUX}
    ua_headers_windows = {'User-Agent': _USERAGENT_WIN}
    # platform choose
    headers = None
    if os.name == 'posix':
        headers = ua_headers_linux
    elif os.name == 'nt':
        headers = ua_headers_windows
    else:
        pass

    return headers

def build_login_headers(cookie):
    """Build the first request login headers

    :param cookie:  cookie
    :return:        login headers
    """
    # this build headers key-word is referer and user-agent
    base_headers = {
        'Accept': _HEADERS_ACCEPT,
        'Accept-Encoding': _HEADERS_ACCEPT_ENCODING,
        'Accept-Language': _HEADERS_ACCEPT_LANGUAGE,
        'Cache-Control': _HEADERS_CACHE_CONTROL,
        'Connection': _HEADERS_CONNECTION,
        'Content-Length': "207",
        'Content-Type': _HEADERS_CONTENT_TYPE,
        'Cookie': cookie,
        'DNT': "1",
        'Host': ACCOUNTS_URL,
        'Origin': _LOGIN_REQUEST_URL,
        'Referer': LOGIN_POSTKEY_URL,
        'X-Requested-With': _HEADERS_XMLHTTPREQUEST,
    }
    # dict merge, longth-change argument
    build_headers = dict(base_headers, **uc_user_agent())

    return build_headers

def build_original_headers(referer):
    """Original image request headers

    :param referer: headers need a last page referer
    :return:        build headers
    """
    base_headers = {
        'Accept': "image/webp,image/*,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': _HEADERS_ACCEPT_LANGUAGE,
        'Connection': _HEADERS_CONNECTION,
        # must add referer, or server will return a damn http error 403, 404
        # copy from javascript console network request headers of image
        'Referer': referer,  # request basic page
    }
    build_headers = dict(base_headers, **uc_user_agent())

    return build_headers

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
