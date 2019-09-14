
[![Python 3.6](https://img.shields.io/badge/Python-3.6-yellow.svg)](http://www.python.org/download/)

# PixivCrawlerIII - A \</MATRIX> Pixiv website crawler with python3
    
    ██████╗ ██╗██╗  ██╗██╗██╗   ██╗ ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ ██╗██╗██╗
    ██╔══██╗██║╚██╗██╔╝██║██║   ██║██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗██║██║██║
    ██████╔╝██║ ╚███╔╝ ██║██║   ██║██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝██║██║██║
    ██╔═══╝ ██║ ██╔██╗ ██║╚██╗ ██╔╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗██║██║██║
    ██║     ██║██╔╝ ██╗██║ ╚████╔╝ ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║██║██║██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝╚═╝
                                                                                                  
    ASCII artword from http://patorjk.com/software/taag/ font: ANSI Shadow

# LICENSE

    Copyright(C) 2018-2019 T.WKVER | </MATRIX>. All rights reserved.
    Code by </MATRIX>@Neod Anderjon(LeaderN)
    MIT license read in LICENSE
    Thanks to watch my project
    If you want to help me improve this project, please submit an issue or fork

# UPDATE LOG

    Version: 3.0.0
    Last Update Time: 20191117pm1831

# ANNOUNCEMENT(YOU WILL WANT TO READ)

    2019/11/17
    Today, two months later, I was in a whim, using selenium according to the recommendations on the Internet.
    To simulate landing, bypass the recaptcha problem.
    R18 ranking page crawling has been restored.
    The IRA mode can't find the author information when parsing the page,
    it is estimated that the page layout of the website has been modified, That problem has not been solved yet.
    Notice:
    You need to configure your chrome user-data path yourself(dataload.py L130).
    The first use will open webdriver to save the cookie to the local, 
    and then read it as long as the .pixiv_cookies.txt file exists.

    2019/09/14
    After testing the pixiv website does use the recaptcha method to block the crawler, 
    the logic is as follows: When you request the login page, the server will call 
    recaptcha-javascript to dynamically generate a recpatcha code, you receive the code 
    and then encapsulate it into the request header and pass it back to the server. 
    If they are consistent, the login is successful.
    Otherwise, you must perform recpatcha image verification.

    2019/08/24
    Confirmed that the Pixiv website uses the reCAPTCHA method to intercept the crawler robot.

    2019/08/22
    Today after several tests, the root cause of the failure of 
    the crawler RTN-R18 mode and IRA mode was found: the simulated login failed.
    The login page responds successfully, but returning the accounts page waiting for the ID and password.
    I will take the time to try to fix the problem this weekend.

    2019/08/14
    Today refactor comment format and API lib class and function name standard.

    2019/08/02
    After many tests, the crawler seems to have returned to the state at the end of June, 
    that is, unable to crawl the R18 page and the artist's personal work page.
    Based on the status quo and the past events (0717 incident), 
    I decided not to modify the crawler core business logic for the time being, 
    and wait for 5~6 days before testing.

    2019/07/17
    I am sorry to inform you that the announcement on June 30th 
    stated that the Pixiv website has adopted a new anti-crawl mechanism to counter this project. 
    THIS INFORMATION IS FAKE. 
    The Pixiv website should be purely internal maintenance. 
    After today's test, THE PROJECT STILL WORKING FINE.

# PLATFORM

    Linux x86_64 and Windows NT(tested in Ubuntu 16.04 x64 and Windows 10 x64 1803)
    Python: 3.x(not support 2.x) suggest 3.5+(3.6 and 3.7 tested over)

# REQUIREMENTS

* [selenium](https://github.com/SeleniumHQ/selenium)
* [retrying](https://github.com/rholder/retrying)
* [Pillow](https://github.com/python-pillow/Pillow)
* [prettytable](https://pypi.org/project/PrettyTable/)
* [pycryptodome](https://github.com/Legrandin/pycryptodome)

# RUN

  last python2 version: (very old version, maintenance has been discontinued)

- ## [pixiv-crawler](https://github.com/Neod0Matrix/pixiv-crawler)

    >git clone https://github.com/Neod0Matrix/pixiv-crawler.git
    
    this python3 version:

- ## [PixivCrawlerIII](https://github.com/Neod0Matrix/PixivCrawlerIII)

    >git clone https://github.com/Neod0Matrix/PixivCrawlerIII.git \
    >cd PixivCrawlerIII

    First config your local folder in dataload.py, then run this:
    >python3 pixivcrawleriii.py

    If your crawler is deployed on a remote server, 
    you can use "python3 -m http.server \<port number>" provided by python3 
    to view the crawl results. 
    Click the generated html file on the server page to render 
    the crawl directly picture results in the browser. 

- ### New server mode

    Version V2.9.6 adds a server mode based on usage feedback provided by enthusiastic users.
    The server mode is different from the interactive mode, 
    that is, the user does not need to perform arguments determination 
    according to the data obtained by the crawler according to the step, 
    and the arguments is passed to the crawler by using the command line.

    In this way, the user can deploy the crawler on the VPS 
    and configure it with the Linux crontab or Windows task scheduler for timed crawling.
    Or just don't have to look at the characters have been refreshed on the command line, 
    it should be very convenient.

 - ### Providing system arguments means using server mode

    If the crawler detects that the command line argument is empty, incomplete, or incorrect, 
    the crawler will exit or enter interactive mode.
    For security reasons, the user's Pixiv-ID and password cannot be passed 
    in the form of command line arguments. 
    You must enter the local key file in interactive mode before you can use the server mode.

    > Arguments:\
    > -h/--help       @Print usage page\
    > -m/--mode       @Set mode, RTN(1) | IRA(2)\
    > -r/--R18        @Ordinary(1) | R18(2), only support Mode RTN\
    > -l/--list       @Daily(1) | Weekly(2) | Monthly(3), only support Mode RTN\
    > -s/--sex        @Nomal(0) | Male(1) | Female(2) favor, only support Mode RTN\
    > -i/--id         @Illustrator ID, only support Mode IRA\
    >\
    > Example:\
    > python3 pixivcrawleriii.py -m 1 -r 1 -l 1 -s 0\
    > python3 pixivcrawleriii.py -m 2 -i 0000000

    Notice:
    If the sex option selects male or female, then the list option only can be daily.
    If you set the list type option to weekly or monthly and the sex option to either male or female,
    then the list option overrides the sex option.(List type option has a higher priority)

 - ### Color effect style
    
    Add color character display effects from version V2.9.8, 
    and use colors to distinguish the attributes of the displayed information.

    | Code | Background | Use |
    | :----: | :----: | :----: |
    | red | black | logo |
    | black | red | error or failed |
    | yellow | blue | timestamp |
    | blue | yellow | important info |
    | yellow | black | request user input argument |
    | white | black | normal info |

# PROBLEMS THAT MAY ARISE

    May the good network status with you

    To ensure that the display output is normal, 
    please set the console code to UTF-8, 
    the windows system to use the command "chcp 65001".

    If you use the crawler too often to request data from the server, 
    the server may return an 10060 error for you, 
    just need to wait for a while and then try again, or use a proxy server
    
    If your test network environment has been dns-polluted, I suggest you 
    fix your PC dns-server to a pure server or get a proxy server
    
    IRA mode you need input that illuster id, not image id
    crawler log image will rename to array number + image id, 
    you can use this id to find original image with URL:
    https://www.pixiv.net/member_illust.php?mode=medium&illust_id=<your known id>

    Version 2.7.8 is the last batch download solution 
    that loads the main-page for the Pixiv website's old static HTML page.
    From October 2, 2018, 
    Pixiv began to use js-dynamically load the artist's home page information.
    On October 4, 2018, in response to the countermeasures made 
    on the website 1002 big change event, version V2.8.2 was fully optimized 
    and upgraded, the original two download modes were restored. 
    At the same time, one request for downloading was suspended after one login.

    If you want to optimze CPU and memory usage, you can use cProfile tool to 
    analysis object usage and use module gc to collecte garbage.

    If the system memory is very low, 
    even the [SYSTEM_MAX_THREADS(setting in dataload.py L42)] threads of the basic settings 
    can not be created, then the program will be stuck for a period of time 
    and finally report an error.
    In order to ensure the successful operation of the program, 
    please be sure to leave more than 2G free memory.
