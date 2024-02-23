    #Imports
#pip install selenium==3.141
from selenium import webdriver 
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests #pip install requests
import random
import os
from datetime import datetime
import pytz #pip install pytz
import string

# Making folder for results and domain dropping times

VALID_PATH = "Available Domains"
if not os.path.exists(VALID_PATH):
	os.makedirs(VALID_PATH)

VALID_PATH2 = "Domain Dropping Times"
if not os.path.exists(VALID_PATH2):
	os.makedirs(VALID_PATH2)


# Options for chrome driver

options = Options()
#options.add_argument('--headless')
options.add_argument("--silent")
options.add_experimental_option('excludeSwitches', ['enable-logging']) # ----- TURNS OFF THE STARTUP ERROR
options.add_argument('--disable-gpu')
options.add_argument('--allow-insecure-localhost')
options.add_argument('--log-level=3')
options.add_extension('C:\Program Files (x86)\MetaMask_10.6.1.0.crx')


# Path for location of chrome driver

path = 'C:\Program Files (x86)\chromedriver.exe'


# opening chrome driver

driver = webdriver.Chrome(path, options=options)
driver.implicitly_wait(900)


# Single check

def single():
    os.system('cls')
    check = input('Enter the name you want to check: ')

    url = f'https://app.ens.domains/search/{check}'

    driver.get(url)

    ae = driver.find_element_by_xpath('//*[@id="root"]/div/main/a/div[1]/div')   # Trying to find a xpath on screen and if it finds it then it prints out taken or available names

    if 'Unavailable' in ae.text:
        print('')
        print(f'{check} is taken')
        print('')
        driver.quit()
        input('Press ENTER to go back to modules: ')
        start()

    if 'Available' in ae.text:
        print('')
        print(f'{check} is available')
        print('')
        driver.quit()
        input('Press ENTER to go back to modules: ')
        start()


# Multi check

def multi2(u):
    url = f'https://app.ens.domains/search/{u}'

    driver.get(url)

    ae = driver.find_element_by_xpath('//*[@id="root"]/div/main/a/div[1]/div')   # Trying to find a xpath on screen and if it finds it then it prints out taken or available names

    if 'Unavailable' in ae.text:

        print(f'{u} is taken')
        a9 = driver.find_element_by_xpath('//*[@id="root"]/div/main/a/p')   # looking for times of dropping names and divides them into their own seperate .txt files

        css = driver.find_element_by_xpath('//*[@id="root"]/div/main/a/p') #checks the color of the expiring text
        color = css.value_of_css_property('Color')

        #checks text return for a phrase that alters the index position of the date and time string
        if "Grace period" in a9.text:    #if expired
            year = a9.text[18:22]
            month = a9.text[23:25]
            day = a9.text[26:28]
            hour = a9.text[32:34]
            minutes = a9.text[35:37]
            prefix = a9.text[0:17]
        else:                            #if not expired
            year = a9.text[8:12]
            month = a9.text[13:15]
            day = a9.text[16:18]
            hour = a9.text[22:24]
            minutes = a9.text[25:27]
            prefix = a9.text[0:7]

        #converts the information pulled from the text to an int so it can be passed thru the conversion function
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minutes = int(minutes)
        est = pytz.timezone('US/Eastern')
        utc = pytz.utc
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'

        #converts date and time from UTC to EST and EDT depending on wether it is during daylights savings time
        winter = datetime(year, month, day, hour, minutes, 0, tzinfo=utc)
        summer = datetime(year, month, day, hour, minutes, 0, tzinfo=utc)
        newTime = winter.astimezone(est).strftime(fmt)
        newTime = newTime[0:len(newTime)-5]

        if color == "rgb(255, 0, 0)":
             with open(os.path.join(VALID_PATH2, 'Expiring Soon') + '.txt', 'a') as f:
                f.write(f'{u}.eth | ' + prefix + " " + newTime + '\n')       #appends the prefix to the date and time


        elif color != "rgb(255, 0, 0)":
            if '2021' in a9.text:
                with open(os.path.join(VALID_PATH2, '2021') + '.txt', 'a') as f:
                    f.write(f'{u}.eth | ' + prefix + " " + newTime + '\n')       

            if '2022' in a9.text:
                with open(os.path.join(VALID_PATH2, '2022') + '.txt', 'a') as f:
                    f.write(f'{u}.eth | ' + prefix + " " + newTime + '\n')

            if '2023' in a9.text:
                with open(os.path.join(VALID_PATH2, '2023') + '.txt', 'a') as f:
                    f.write(f'{u}.eth | ' + prefix + " " + newTime + '\n')

            if '2024' in a9.text:
                with open(os.path.join(VALID_PATH2, '2024') + '.txt', 'a') as f:
                    f.write(f'{u}.eth | ' + prefix + " " + newTime + '\n')

            if '2025' in a9.text:
                with open(os.path.join(VALID_PATH2, '2025') + '.txt', 'a') as f:
                    f.write(f'{u}.eth | ' + prefix + " " + newTime + '\n')
                    
    if 'Available' in ae.text:
        ao = driver.find_element_by_xpath('//*[@id="root"]/div/main/a').click()   # Clicking name to see the price
            
        st = driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/div[2]/div[3]/div/div[1]/span').text   # If this is found the MAX price will be printed out into a .txt file
            
        with open(os.path.join(VALID_PATH, 'Available') + '.txt', 'a') as f:
            f.write(u + '.eth' + f' | {st}' + '\n')
        print(f'{u} is available')



# reads .txt file for domains and passes them 1 by 1 to the multi checker

def multi():
    os.system('cls')
    with open(input('Enter your domain list file: ')) as l:   # Enter the .txt file you want to use to check domains
        print(" ")
        print('Checking Domains Now...')
        print(" ")
        for u in l:
            u = u.strip()
            multi2(u)
    print(" ")
    input('All done! Press enter to go back to modules. ')
    start()


#checks namelist file for any names under 2 characters that will interfere with the multi function.
def domainListCheck():
    os.system('cls')
    fileName = input('Enter your domain list file: ')
    print(" ")
    print("Cleaning Up Your Domain List...")
    #reads file and counts number of lines.
    with open(fileName,'r') as file:
        lines = file.readlines()
    #writes file and checks for lines that are less than than three characters long.
    with open(fileName,'w') as file:
        for line in lines:            #for loop to read each line
            
            #2 letter names are three characters long in the text file, calculate string lenght by doing characters+1. also removes special characters that interrupt the code.
            if (len(line) <= 3):
                pass                  #skips line that we dont want to rewrite to the file.
            elif(line[0:-1].isalnum()==False):
                pass
            else:                     #if the index is longer than 3 characters it writes it back to the original file.
                file.write(line)      #writes accepted index to the file.
    time.sleep(3)
    print(" ")
    input("All done! Press enter to go back to the modules: ")
    start()

def sniper():
    os.system('cls')
    check = input('Enter the domain name you want to snipe: ')

    secret = input('Enter your secret Recovery Phrase (metamask): ')

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(14))

    registrationPeriod = input('How many years do you want to register the domain for: ')

    url = f'https://app.ens.domains/search/{check}'

    driver.get(url)

    driver.find_element_by_xpath('//*[@id="root"]/div/main/a').click() #clicks connect on APP.ENS
    driver.find_element_by_xpath('//*[@id="root"]/div/nav/div/div/div[3]/div').click() #clicks connect matamask on APP.ENS

    driver.switch_to.window(driver.window_handles[0]) #switches to metamask extension

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div/button').click() #get started

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button').click() #import wallet

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]').click() #I agree

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/form/div[4]/div[1]/div/input').send_keys(secret) #types metamask passphrase

    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password) #types password in metamask 

    driver.find_element_by_xpath('//*[@id="confirm-password"]').send_keys(password) #confirms password

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/form/div[7]/div').click() # - TOS

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/form/button').click() # - CONFIRM

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/button').click() #all done

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[4]/div[2]/button[2]').click() #next

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click() #connect

    driver.switch_to.window(driver.window_handles[1]) #switches back to APP.ENS

    driver.find_element_by_xpath('//*[@id="WEB3_CONNECT_MODAL_ID"]/div/div/div[2]/div[1]/div').click() #clicks connect again(maybe)

    #put registration period selector here

    driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/div[2]/div[5]/button').click() #request to register

    time.sleep(.5) #time for metamask to load 

    driver.switch_to.window(driver.window_handles[2]) #switches to metamask popup

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/div[3]/footer/button[1]').click() #CLICKS REJECT. SWITCH TO ACCEPT!

    driver.switch_to.window(driver.window_handles[1]) #switches back to APP.ENS

    time.sleep(60) #waits for 60 second timer to finish 

    driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/div[2]/div[3]/button').click() #clicks new register button

    time.sleep(.5) #waits for metmask extension to load

    driver.switch_to.window(driver.window_handles[2]) #switches to metamask popup

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/div[3]/footer/button[2]') #final purchase confirmation for metamask

    driver.switch_to.window(driver.window_handles[1]) #switches back to APP.ENS

    if driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/div[2]/div[3]/a'):
        print(check + " succesfully purchased!")   #checks to see if the page says "manage" to confirm the snipe was successful
    else:
        print("Snipe failed.")  

    input('Press enter to quit: ')


# GUI

def start():
    os.system('cls')
    print('')
    print("""
███████╗███╗  ██╗ ██████╗  ████████╗ █████╗  █████╗ ██╗      ██████╗
██╔════╝████╗ ██║██╔════╝  ╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝
█████╗  ██╔██╗██║╚█████╗      ██║   ██║  ██║██║  ██║██║     ╚█████╗ 
██╔══╝  ██║╚████║ ╚═══██╗     ██║   ██║  ██║██║  ██║██║      ╚═══██╗
███████╗██║ ╚███║██████╔╝     ██║   ╚█████╔╝╚█████╔╝███████╗██████╔╝
╚══════╝╚═╝  ╚══╝╚═════╝      ╚═╝    ╚════╝  ╚════╝ ╚══════╝╚═════╝ 
    """)
    print('Created by Ambush and Dylon')
    print('')
    print('Modules: ')
    print('[1] Single Domain Check')
    print('[2] Domain sorter')
    print('[3] Multi Domain Check')
    print('[4] Domain Sniper')
    print('')
    op = input('Choose a module: ')
    if op == '1':
        single()
    if op == '2':
        domainListCheck()
    if op == '3':
        multi()
    if op == '4':
        sniper()




start()
driver.quit()