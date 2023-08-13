from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from inputimeout import inputimeout, TimeoutOccurred
import random

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir= PATH TO YOUR GOOGLE PROFILES HERE")
options.add_argument(r"--profile-directory=Default")
options.add_experimental_option("excludeSwitches",['enable-automation'])

browser = webdriver.Chrome(options) #change to whichever driver you have

#login = 'https://farmrpg.com/index.php#!/login.php'  # url for login page
#explore = 'https://farmrpg.com/index.php#!/explore.php'  # url for explore page
#user = 'FILL HERE'  # put your username here, the script will enter it automatically
#pw = 'FILL HERE'  # put your password here, the script will enter it automatically


# used for timestamping
def logTime():
    return datetime.now().strftime('%H:%M:%S')


#Login to the game
#browser.get(login)
#time.sleep(1)
#browser.find_element(By.NAME, "username").send_keys(user)  # enter username
#browser.find_element(By.NAME, "password").send_keys(pw)  # enter password
#browser.find_element(By.CSS_SELECTOR, 'input#login_sub.button.btngreen').click()

home = 'https://farmrpg.com/index.php#!/index.php'  # url for home page
browser.get(home)

# updated farming bot - needs work
# process:
# 1. go to farm page
# 2. press harvest all button + confirm
# 3. plant new crops if possible + confirm
# 4. if no seeds, go buy more (runs buy seeds script)

def farming():
    print(logTime() + ': Accessing farm.')
    playerId = "FILL WITH YOUR PLAYER ID HERE"
    farm = 'https://farmrpg.com/index.php#!/xfarm.php?id=' + playerId
    browser.get(farm)
    time.sleep(3)
    browser.get(farm)
    time.sleep(3)
    try:
        # Harvest ready crops + sanity check for farm loaded.
        print(logTime() + ': Harvesting all ready crops.')
        browser.find_element(By.CLASS_NAME, "harvestallbtn").click()
        time.sleep(1)
        try:
            # If we have seeds, plant new crops
            seedsAmt = int(0)
            for x in browser.find_element(By.CLASS_NAME, 'seedid').find_elements(By.TAG_NAME, 'option'):
                if x.get_attribute('data-name') == "Hops Seeds": #change to whichever seed needs planting
                    seedsAmt = int(x.get_attribute('data-amt'))
                    print(logTime() + ': ' +str(seedsAmt) + ' seeds available.')
                    
                    #(if there's no more space in inventory)
                    # if it's actually sacrifice-able, be sure to change the sacrifice func
                    #if "*" in x.text: 
                        #sacrifice()
                    break
                
            cropRows = 9  #change to how many crop rows you have    
            if seedsAmt >= 4 * cropRows: 
                while True:
                    # Plant new crops
                    if seedsAmt > 0:
                        print(logTime() + ': Planting new crops')
                        browser.find_element(By.CLASS_NAME, "plantallbtn").click()
                        time.sleep(3)
                        print(logTime() + ': ' + str(seedsAmt-36) + ' seeds available.')
                        print(logTime() + ': Waiting for crops to grow.')
                        time.sleep(242) #change to growth of whichever crop you're growing (check for the seeds in inventory)
                        print(logTime() + ': Restarting.')
                        farming()
            else:
                print(logTime() + ': Not enough seeds remaining.')
                buyseeds()
        except:
            # If we don't have new seeds, go buy more.
            print(logTime() + ': No more seeds remaining.')
            buyseeds()
    except:
        print(logTime() + ': Accessing farm failed. Trying again in 2 seconds.')
        time.sleep(2)
        farming()


def sacrifice():
    temple = 'https://farmrpg.com/index.php#!/templeitem.php?id=13' #change to temple you're actually sacrificing to
    browser.get(temple)
    time.sleep(2)
    browser.get(temple)
    time.sleep(2)
    try:
        print(logTime() + ": Beginning sacrifice.")
        browser.find_element(By.CLASS_NAME, 'sacrificebtn').click()
        time.sleep(1)
        browser.find_elements(By.CLASS_NAME, 'actions-modal-button')[0].click()
        time.sleep(1)
        browser.find_element(By.CLASS_NAME, 'modal-button-bold').click()
        time.sleep(1)
        print(logTime() + ": Sacrifice successful")
    except:
        print(logTime() + ": Failed to sacrifice. Trying again in 2 sec.")
        time.sleep(2)
        sacrifice()
    print(logTime() + ": Returning to farm.")
    farming()

# buy seeds if farming bot runs out. customize to your pleasure

#SEED IDS
#[0]:Pepper #[1]:Carrot #[2]:Pea #[3]:Cucumber #[4]Eggplant: #[5]:Radish #[6]:Onion #[7]:Hops #[8]:Potato
#[9]:Tomato #[10]:Leek #[11]:Watermelon #[12]:Corn #[13]:Cabbage #[14]:Pine #[15]:Pumpkin #[16]:Wheat
#[17]:Mushroom #[18]:Broccoli #[19]:Cotton #[20]:Sunflower #[21]:Beet #[22]:Rice
def buyseeds():
    print(logTime() + ': Going to the market to buy more seeds.')
    market = 'https://farmrpg.com/index.php#!/store.php'
    try:
        browser.get(market)
        time.sleep(2)
        browser.get(market)
        time.sleep(2)
        print(logTime() + ': Selecting MAX for seeds.')
        m = browser.find_elements(By.CLASS_NAME, 'maxqty')[7] #change to number of whichever seed you're planting
        browser.execute_script("arguments[0].click();", m)
        time.sleep(1)
        print(logTime() + ': Buying seeds.')
        b = browser.find_elements(By.CLASS_NAME, 'buybtn')[7] #change to number of whichever seed you're planting
        browser.execute_script("arguments[0].click();", b)
        time.sleep(1)
        print(logTime() + ': Confirm.')
        browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
        time.sleep(1)
        print(logTime() + ': OK.')
        browser.find_elements(By.CLASS_NAME, "modal-button")[2].click()
        time.sleep(1)
    except:
        print(logTime() + ': Market failed to load. Trying again in 2 seconds.')
        time.sleep(2)
        buyseeds()
    print(logTime() + ': Restart.')
    farming()



# fishing bot
def fishing():
    pondMenu = 'https://farmrpg.com/index.php#!/fish.php'
    browser.get(pondMenu)
    time.sleep(1)
    browser.get(pondMenu)
    time.sleep(1)
    pondSelect = input(
        "---Possible Fishing Places---\n1: Small Pond\n2: Farm Pond\n3: Forest Pond\n4: Lake Tempest\n5: Small "
        "Island\n6: Crystal River\n7: Emerald Beach\n8: Vast Ocean\n9: Lake Minerva\n10: Large Island\n\nInput a number: ")  # replace 1 and 8 to select
    # your range of ponds. change to your needs
    fishingloop(pondSelect)


def fishingloop(pondSelect):
    pond = 'https://farmrpg.com/index.php#!/fishing.php?id=' + pondSelect
    print(logTime() + ': Entering pond ' + pondSelect + '.')
    browser.get(pond)
    time.sleep(2)
    browser.get(pond)
    time.sleep(2)
    try:
        worms = int(browser.find_element(By.CLASS_NAME, "col-45").find_element(By.TAG_NAME, 'strong').text)
        counter = 0
    except:
        fishing()
    else:
        rand = random.randint(30, 100)
        while worms > 0:
            print(logTime() + ': Fishing in pond ' + pondSelect + ' (' + str(counter) + '/'+str(rand)+')')
            catch()
            counter += 1
            total = int(browser.find_element(By.CLASS_NAME, 'sellallfishbtnnc').find_element(By.TAG_NAME, 'span').text)
            if total > 420:
                browser.find_element(By.CLASS_NAME, 'sellallfishbtnnc').click() #sell all caught fish for profit
            worms = int(browser.find_element(By.CLASS_NAME, "col-45").find_element(By.TAG_NAME, 'strong').text)
            if counter > rand:  # pond page will refersh to avoid detection after a random number of catches.
                print(logTime() + ': Stopping fishing, limit reached.')
                try:
                    response = inputimeout(prompt='Return(1), Stay(0). Defaults to Stay: ', timeout=5)
                except TimeoutOccurred:
                    response = "0"
                if response == "1":
                    fishing()
                if response == "0":
                    counter = 0
                    fishingloop(pondSelect)
        if worms == 0:
            buyworms(pondSelect)


# used in fishing bot. buys worms if all worms are gone
def buyworms(pondSelect):
    print(logTime() + ': Buying more worms.')
    market = 'https://farmrpg.com/index.php#!/store.php'
    browser.get(market)
    time.sleep(1)
    try:
        browser.find_elements(By.CLASS_NAME, "maxqty")[-1].click()
    except:
        browser.get(market)
    time.sleep(.5)
    s = browser.find_elements(By.CLASS_NAME, 'buybtn')[-1]
    browser.execute_script("arguments[0].scrollIntoView(true);", s)
    time.sleep(.5)
    s.click()
    time.sleep(.5)
    browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
    time.sleep(.5)
    browser.find_elements(By.CLASS_NAME, "modal-button")[2].click()
    time.sleep(.5)
    fishingloop(pondSelect)

# important script needed for fishing bot. used for actually catching the fish.
def catch():
    fish = browser.find_elements(By.CLASS_NAME, "fishcell")
    catcher = browser.find_element(By.CLASS_NAME, "fishcaught")
    for i in fish:
        try:
            i.click()
        except:
            pass
    try:
        time.sleep(random.uniform(0.5,0.8))
        catcher.click()
        time.sleep(random.uniform(1.0,1.2))
    except:
        pass

def explore():
    #zone = str(random.randint(1,9))
    zone = str(8)
    currExplore = 'https://farmrpg.com/index.php#!/area.php?id=' + zone
    print(logTime() + ': Entering zone ' + zone + '.')
    browser.get(currExplore)
    time.sleep(2)
    browser.get(currExplore)
    time.sleep(2)
    counter = 0
    rand = random.randint(30,50)
    while True:
        try:
            print(logTime() + ': Explore in zone ' + zone + ' (' + str(counter) + '/' + str(rand) + ')')
            browser.find_element(By.ID, "exploreconsole").click()
            counter += 1
            time.sleep(.5)
            if counter > rand:
                print(logTime() + ': Leaving zone ' + zone + '.')
                explore()
        except:
            explore()