from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver import ChromeOptions
import pyautogui
#from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
import subprocess

USERNAME = "defaultUser"
PASSWORD = "defaultPass"
SEED_PHRASE = ['enter you seed phrase as an array here']
FILE_EXTENSION = r'C:\Users\yutab\AppData\Local\Google\Chrome\User Data\Default\Extensions\lpfcbjknijpeeillifnkikgncikgfhdo\3.5.0_0.crx'
try:
    opt = webdriver.ChromeOptions()
    opt.add_extension(FILE_EXTENSION)
except:
    pass
DRIVER = webdriver.Chrome(options=opt)
KEYBOARD = Controller()
accountBalance = 0 #this is set in startup()
minApr = 10 #percent, set this to your liking
acceptedLoanTickers = ['ADA']
acceptedCollateralTickers = ['LENFI', 'MIN', 'WMT', 'LQ', 'iUSD']
maxLoanSize = 999999
minLoanSize = 1000
maxDuration = 365

def main():

    try:
        startup()
    except:
        print('Failed on startup')
        return

    while accountBalance > -2:

        #every minute refresh and go to the liquidity requests tab
        sleep(10)
        clickXpath('/html/body/div/section/section[2]/main/section/section[1]/section[1]/section[2]/button')
        sleep(3)
        loanElement = DRIVER.find_element(by = By.XPATH, value = '/html/body/div/section/section[2]/main/section/section[2]/section/section/section/section[2]/div/section[1]/section').text.split(' ')
        loanAmount = float(loanElement[0].replace(',',''))
        loanTicker = loanElement[1].split('\n')[0]

        apr = DRIVER.find_element(by = By.XPATH, value = '/html/body/div/section/section[2]/main/section/section[2]/section/section/section/section[2]/div/section[3]/section/span[1]/section/div[2]').text
        apr = float(apr.strip()[:-1])
        
        durationElement = DRIVER.find_element(by = By.XPATH, value = '/html/body/div/section/section[2]/main/section/section[2]/section/section/section/section[2]/div/section[4]/section').text
        duration = durationElement.split(' ')[0]
        
        collateralElement = DRIVER.find_element(by = By.XPATH, value = '/html/body/div/section/section[2]/main/section/section[2]/section/section/section/section[2]/div/section[2]/section').text
        collateralTicker = collateralElement.split(' ')[1].split('\n')[0]
        
        healthFactor = DRIVER.find_element(by = By.XPATH, value = '/html/body/div/section/section[2]/main/section/section[2]/section/section/section/section[2]/div/section[5]/section/span').text
        healthFactor = healthFactor.split('\n')[1]

        #if the loan qualifies, take it:
        if (collateralTicker in acceptedCollateralTickers) and \
            (loanTicker in acceptedLoanTickers) and \
            (loanAmount < (accountBalance+5)) and \
            (loanAmount <= maxLoanSize) and \
            (loanAmount >= minLoanSize) and \
            (duration <= maxDuration):
            #deposit
            clickXpath('/html/body/div/section/section[2]/main/section/section[2]/section/section/section/section[2]/div/section[6]/section/button')
            sleep(10)
            #confirm
            clickXpath('/html/body/div[3]/div/div/div/section/section[2]/section[2]/section/button[2]')
            sleep(15)
            typeText(PASSWORD)
            pressEnter()
            sleep(15)
            pressTab()
            pressEnter()

        sleep(20)
        refreshPage()



#____________________________________________________________
#Helper functions
def clickLocationOfImage(imagePath, conf=0.8):
    sleep()
    extension = pyautogui.locateOnScreen(imagePath, confidence=conf)
    extensionPoint = pyautogui.center(extension)
    x, y = extensionPoint
    pyautogui.click(x,y)

def clickXpath(xpath):
    sleep()
    DRIVER.find_element(by = By.XPATH, value = xpath).click()

def pressDown():
    sleep()
    KEYBOARD.press(Key.down) 
    KEYBOARD.release(Key.down)

def pressEnter():
    sleep()
    KEYBOARD.press(Key.enter)
    KEYBOARD.release(Key.enter)

def pressTab():
    sleep()
    KEYBOARD.press(Key.tab)
    KEYBOARD.release(Key.tab)

def pressSpace():
    sleep()
    KEYBOARD.press(Key.space)
    KEYBOARD.release(Key.space)


def sleep(t=0.5):
    time.sleep(t)

def importWallet():
    sleep(2)
    pressTab()
    pressTab()
    pressSpace() #import    
    pressTab()
    pressSpace()
    pressDown()
    if len(SEED_PHRASE) == 24:
        pressDown()
    pressEnter() #accept phrase length
    pressTab()
    pressSpace() #accept terms of use
    pressTab()
    pressTab()
    pressSpace() #get to the seed phrase entry
    sleep(2)
    pressTab()
    sleep(2)

def enterSeedPhrase(sp = SEED_PHRASE):
    for word in sp:
        typeText(word)
        pressTab()
    pressSpace()

def createAccountCredentials(username = USERNAME, password = PASSWORD):
    pressTab()
    typeText(username)
    pressTab()
    typeText(password)
    pressTab()
    pressTab()
    typeText(password)
    pressTab()
    pressTab()
    pressSpace()
    sleep(2)
    pressTab()
    pressSpace()             

def typeText(txt):
    copy(txt)
    paste()

def copy(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def paste():
    pyautogui.hotkey('ctrl', 'v')

def refreshPage():
    KEYBOARD.press(Key.ctrl)
    KEYBOARD.press(Key.f5)
    KEYBOARD.release(Key.ctrl)
    KEYBOARD.release(Key.f5)

def startup():
    DRIVER.get('https://app.aada.finance/')
    sleep(1)

    #exit out of popups
    try:
        clickXpath('/html/body/div[3]/div/div/div/section/section/section[1]/a')
    except:
        pass

    #click extensions
    clickLocationOfImage("images/extensionImg.PNG")

    #click nami extensions
    pressDown()
    pressDown()
    pressEnter()

    importWallet()
    enterSeedPhrase()
    createAccountCredentials()

    #click connect wallet
    sleep(2)
    clickXpath('/html/body/div/section/section[1]/div/header/div[2]/div[2]/button')

    #click nami and allow access
    sleep(2)
    clickXpath('/html/body/div[3]/div/div/div/section/section[2]/section[1]/a')
    sleep(2) 
    pressSpace()
    pressTab()
    pressTab()
    pressSpace()

    #get the account balance
    sleep(6)
    clickXpath('/html/body/div/section/section[1]/div/header/div[2]/div[2]/div/div/span')
    sleep()
    accountBalance=float(DRIVER.find_element(by = By.XPATH, value = '/html/body/div/section/section[1]/div/header/div[2]/div[2]/section/div[2]/div/span[2]').text)

    #click market tab
    sleep(2)
    clickXpath('/html/body/div/section/section[1]/div/header/div[2]/ul/li[3]/a')

    #click liquitiy requests tab
    sleep(2)
    clickXpath('/html/body/div/section/section[2]/main/section/section[1]/section[1]/section[2]/button')

#____________________________________________________________
if __name__ == "__main__":
    main()