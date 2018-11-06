
[![Python 3.6](https://img.shields.io/badge/Python-3.6-yellow.svg)](http://www.python.org/download/)

# PixivCrawlerIII - A \</MATRIX> Pixiv website crawler with python3
    
    ██████╗ ██╗██╗  ██╗██╗██╗   ██╗ ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ ██╗██╗██╗
    ██╔══██╗██║╚██╗██╔╝██║██║   ██║██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗██║██║██║
    ██████╔╝██║ ╚███╔╝ ██║██║   ██║██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝██║██║██║
    ██╔═══╝ ██║ ██╔██╗ ██║╚██╗ ██╔╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗██║██║██║
    ██║     ██║██╔╝ ██╗██║ ╚████╔╝ ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║██║██║██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝╚═╝
                                                                                                  
    ASCII artword from http://patorjk.com/software/taag/ font: ANSI Shadow

License
======
    
    Copyright (c) 2018 @T.WKVER </MATRIX>
    Code by </MATRIX>@Neod Anderjon(LeaderN)
    MIT license read in LICENSE
    Thanks to watch my project
    If you want to help me improve this project, please submit an issue or fork

Update
======

    Version: 2.9.1
    Last Update Time: 20181106pm1430
    
    This python crawler is built to crawl pixiv images
    It have two mode: RankTopN and illustRepoAll 
    Call threading to add multi-thread download images

Platform
======

    Linux x86_64 and Windows NT(tested in Ubuntu 16.04 x64 and Windows 10 x64 1803)
    Python: 3.x(not support 2.x) suggest 3.4+

## Requirements

* [retrying](https://github.com/rholder/retrying)
* [Pillow](https://github.com/python-pillow/Pillow)
* [prettytable](https://pypi.org/project/PrettyTable/)
* [pycryptodome](https://github.com/Legrandin/pycryptodome)

Run
======

  last python2 version: (very old version, maintenance has been discontinued)
    
- [pixiv-crawler](https://github.com/Neod0Matrix/pixiv-crawler)
    
    git clone https://github.com/Neod0Matrix/pixiv-crawler.git
    
  this python3 version:

- [PixivCrawlerIII](https://github.com/Neod0Matrix/PixivCrawlerIII)

    git clone https://github.com/Neod0Matrix/PixivCrawlerIII.git
    
    cd PixivCrawlerIII
    
    First config your local folder in dataload.py, then run this:
    
    python3 pixivcrawleriii.py

    If your crawler is deployed on a remote server, 
    you can use "python3 -m http.server <port number>" provided by python3 
    to view the crawl results. 
    Click the generated html file on the server page to render 
    the crawl directly picture results in the browser. 

Problems that may arise
======

    May the good network status with you

    To ensure that the display output is normal, 
    please set the console code to UTF-8, 
    the windows system to use the command "chcp 65001".

    If you use the crawler too often to request data from the server, 
    the server may return an 10060 error for you, 
    just need to wait for a while and then try again, or use a proxy server
    
    If your test network environment has been dns-polluted, I suggest you 
    fix your PC dns-server to a pure server
    like Google Pure DNS: 8.8.8.8:53, or build a dnsmasq server, etc
    
    IRA mode you need input that illuster id, not image id
    crawler log image will rename to array number + image id, 
    you can use this id to find original image with URL:
    https://www.pixiv.net/member_illust.php?mode=medium&illust_id=<your known id>
    
    Pixiv website will often change the image URL frame, 
    please use the lastest results from browser javascript console
    
    Remember delete login.cr info before push or commit issue
    
    Login successed, Pixiv sees the post-data rather than the headers,
    as long as the opener is guaranteed to be used correctly, 
    no headers can be successfully logged in
    Now you can use this crawler to crawl all targets in Pixiv

    Version 2.6.2+ use pycrypto to encrypt username and password, of course
    we cancel login.cr rule. 
    In Linux system, you may just run "pip3 install pycrypto" install pycypto module.
    But if you run our program in Windows system, install pycrypto may a little hard. 
    We suggest first install VS2015, just select python and VC option.
    When VS2015 install finished, add "VCINSTALLDIR" env-variable to system,
    its target directory is {VS2015_INSTALL_DIR/VC}.
    Then download pycrypto source code and run "python3 setup.py install" to install
    pycrypto module. After it compile finish, change {PYTHON3_DIR/Lib/site-packages/crypto}
    to {PYTHON3_DIR/Lib/site-packages/Crypto}, in Crypto directory, has a Crypto\Random\OSRNG
    directory, change here nt.py "import winrandom" to "from . import winrandom",
    now you may finish install pycrypto in Windows system.
    Good luck, it's so hard not my fault.

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

    Since the pycrypto module is no longer maintained, 
    the project decided to use the cryptographic module pycryptodome, 
    which is still being updated, from the V2.8.5 version instead of pycrypto.
    You need to delete the original .aes_crypto_login.ini file, 
    uninstall the pycrypto module from the python environment, 
    and install the pycryptodome module.