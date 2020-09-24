# I USE THIS FILE KINDA AS A BASH SCRIPT

import time
from korp import open_browser, download_korp_files

download_folder = ''
file_format = 'CSV'
annot_format = 'Sentence per row, match and contexts separated'
link = ''

# run driver
driver = open_browser(link, download_folder)
# a minute to log-in or navigate where you want to be
time.sleep(60)

download_korp_files(driver, file_format, annot_format, download_folder)
