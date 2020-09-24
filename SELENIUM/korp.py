import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import glob
import io
import os


def open_browser(link, download_folder):
    """
    Opens a chrome browser at a specific korp page set by 'link'.
    Sets the folder where the chrome will save the files to. 
    if the folder doesn't exist, it creates it.
    
    INPUT:
    link - url to open the browser
    download_folder - tells chrome where to store the files
    
    OUTPUT:
    driver - a browser with its settings
    """
    # create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        print('creating '+ download_folder)
        os.mkdir(download_folder)
        
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : download_folder}
    path_to_driver = './chromedriver'
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options, executable_path=path_to_driver)
    driver.get(link)
    
    return driver

def is_downloaded(download_folder, i):
    """
    Checks if there is any in-progress download in a download foler.
    
    INPUT:
    download_folder - tells chrome where to store the files
    i - the number of files that should be downloaded at this point
    """
    file_names = glob.glob(download_folder+'/*')
    # if there is unfinished download OR the download hasn't started yet
    if any(".crdownload" in name for name in file_names) | (len(file_names) != i):
        time.sleep(0.5)
        is_downloaded(download_folder, i)
    else:
        print('Download is done')

def download_korp_files(driver, file_format, annot_format, download_folder):
    """
    Selects the data and file formats you need, 
    goes page by page and downloads those files.
    
    note: the number of hits per page is set to 1000
    
    INPUT:
    driver - a browser with its settings
    file_format - the file extension for the download files
    annot_format - type of data to download
    download_folder - tells chrome where to store the files
    """
    
    kwic_tab = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div/div[1]/div/ul/li[5]/a/uib-tab-heading') 
    
    # select data and file formats to download
    select_annot_format = Select(kwic_tab.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div/div[1]/div/div/div[5]/div/div[5]/select[1]'))
    select_annot_format.select_by_visible_text(annot_format)
    
    select_file_format = Select(kwic_tab.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div/div[1]/div/div/div[5]/div/div[5]/select[2]'))
    select_file_format.select_by_visible_text(file_format)
    
    # getting the number of cvs files to download
    results_string = kwic_tab.find_element_by_xpath('//*[@id="left-column"]/div/div/div[5]/div/div[1]')
    number_of_words = int(results_string.text.replace('Results: ', '').replace(',',''))
    print(number_of_words)
    if number_of_words%1000 != 0:
        number_of_pages = (number_of_words//1000)+1
    else:
        number_of_pages = number_of_words/1000
    print("There are", number_of_pages, "files to download")
    # finding a button that switches to the next page
    pagination = kwic_tab.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div/div[1]/div/div/div[5]/div/div[2]')
    next_page = pagination.find_element_by_css_selector("a[ng-click='selectPage(page + 1, $event)']")
    
    for i in range(1, number_of_pages+1):
        print('Downloading part number:', i)
        download_button = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div[3]/div/div[1]/div/div/div[5]/div/div[5]/button')))
        download_button.click()
        # check if the download is done
        is_downloaded(download_folder, i)
        # go to the next page
        next_page.click()