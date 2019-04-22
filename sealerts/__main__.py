import sys
from __init__ import main

if __name__ == '__main__':
    file_name_with_path = (sys.path[0]+'\\last_saved_se_data.txt').replace('\\', '/')
    rss_link = 'https://bitcoin.stackexchange.com/feeds'
    main(rss_link, file_name_with_path)
