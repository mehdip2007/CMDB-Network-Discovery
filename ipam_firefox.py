# this is for creating FireFox object using selenium to automate the login, upload, re calculate VRFs 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import logging

# Creating and Configuring Logger
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename="logfile.log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()


class IpamFirefox:

    def __init__(self, username, password, ip):
        options = Options()
        options.headless = True
        self.username = username
        self.password = password
        binary = FirefoxBinary('/root/firefox/firefox')
        self.driver = webdriver.Firefox(executable_path='/root/geckodriver', firefox_binary=binary, options=options)

        # self.driver = webdriver.Firefox(executable_path='/root/geckodriver', options=options)
        # self.driver = webdriver.Firefox(executable_path='/root/geckodriver')
        time.sleep(3)
        self.driver.get(ip)

    def login(self, username, password):
        try:
            time.sleep(5)
            # get username and password element
            user = self.driver.find_element(By.ID, 'username')
            passwd = self.driver.find_element(By.ID, 'password')

            # fill username and password
            user.send_keys(username)
            passwd.send_keys(password)
             
            # click the login button
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="login"]/div/div[6]/input').click()

            return True
        except Exception as err:
            logging.error(err)
            logging.error("Please Make Sure You Have Entered the Correct Username and Password.")

    def subnets_import(self, file):
        time.sleep(5)
        logging.error("Logged in Successfully.")
        if self.login(self.username, self.password):
            time.sleep(5)

            # click Administration to select import/export
            logging.error("Click Administration")
            self.driver.find_element(By.XPATH, '//*[@id="admin"]').click()

            logging.error("Click Import/Export")
            import_export_xpath = '//*[@id="menu-collapse"]/ul[3]/li/ul/li[27]/a'
            # import_export_xpath = '/html/body/div[1]/div[6]/div/div/nav/div[2]/ul[3]/li/ul/li[27]/a'
            import_export = self.driver.find_element(By.XPATH, import_export_xpath)
            self.driver.execute_script("arguments[0].click();", import_export)

            # select subnet
            logging.error("Select Subnet Data Type")
            self.driver.implicitly_wait(5)
            select = Select(self.driver.find_element(By.ID, 'dataType'))
            select.select_by_value('subnets')

            logging.error("Import subnet File ---> ")
            # click import
            import_button_xpath = '//*[@id="dataImportExport"]/tbody/tr[3]/td[2]/div/button[1]'
            self.driver.find_element(By.XPATH, import_button_xpath).click()

            # click drag & drop for uploading the file
            logging.error("Uploading the File...")
            self.driver.execute_script("document.getElementById('csvfile').style.display='none';")

            up_file = self.driver.find_element(By.XPATH, '//*[@id="csvfile"]')
            time.sleep(5)

            # call the validator for uploaded file
            self.driver.find_element(By.XPATH, '//*[@id="drop"]/input[2]')
            up_file.send_keys(file)

            logging.error("File is Imported Successfully.")
            time.sleep(5)

            logging.error("Clicking the Green Preview Button after File is Uploaded")
            import_button_xpath = '//*[@id="dataImportPreview"]'
            self.driver.find_element(By.XPATH, import_button_xpath).click()
            time.sleep(5)

            logging.error("Checking if Import After Preview Button is Available or not")
            preview_import_button_xpath = '//*[@id="dataImportSubmit"]'
            import_button = self.driver.find_element(By.XPATH, preview_import_button_xpath).is_enabled()

            if import_button:
                logging.error('Clicking to Import...')
                time.sleep(5)
                self.driver.find_element(By.XPATH, preview_import_button_xpath).click()

                time.sleep(5)
                logging.error("Data Imported Successfully.")
                close_button_xpath = '//*[@id="popup"]/div[3]/button'
                self.driver.find_element(By.XPATH, close_button_xpath).click()

                self.recompute()
            else:
                logging.error('File is Already Uploaded.')
                # Click Cancel Button
                time.sleep(5)
                cancel_button_xpath = '//*[@id="popup"]/div[3]/div/button[1]'
                self.driver.find_element(By.XPATH, cancel_button_xpath).click()

                self.recompute()

        return True

    def recompute(self):
        # Click ReCompute Button
        logging.error('Click ReCompute..')
        time.sleep(5)
        recompute_butoon_xpath = '//*[@id="dataRecompute"]'
        self.driver.find_element(By.XPATH, recompute_butoon_xpath).click()

        time.sleep(5)
        recompute_preview_button_xpath = '//*[@id="dataImportPreview"]'
        self.driver.find_element(By.XPATH, recompute_preview_button_xpath).click()

        # When new file is imported after click recompute there will be a save modal
        time.sleep(5)
        save_button_xpath = '//*[@id="dataImportSubmit"]'
        save_button = self.driver.find_element(By.XPATH, save_button_xpath).is_enabled()

        if save_button:
            logging.error("Saving...")
            self.driver.find_element(By.XPATH, save_button_xpath).click()

            time.sleep(5)
            logging.error("Data Recomputed Successfully.")
            close_button_xpath = '//*[@id="popup"]/div[3]/button'
            self.driver.find_element(By.XPATH, close_button_xpath).click()

            self.propagate()

        else:
            logging.error("There is Nothing to ReCompute")
            cancel_button_xpath = '//*[@id="popup"]/div[3]/div/button[1]'
            self.driver.find_element(By.XPATH, cancel_button_xpath).click()

            self.propagate()

    def propagate(self):
        time.sleep(5)

        logging.error("Propagating Starts...")

        logging.error("Click Subnets at Top Left and choose IP")
        self.driver.find_element(By.XPATH, '//*[@id="menu-collapse"]/ul[1]/li[3]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="menu-collapse"]/ul[1]/li[3]/ul/li[3]/a').click()

        # should get the specific vrf for progations click pencil
        time.sleep(5)

        # change progations to Yes
        element_xpath = '/html/body/div[1]/div[7]/div/table/tbody/tr/td[2]/div/div[22]/div[2]/div[2]/table/tbody/tr/td[10]/div/button[1]/i'
        element = self.driver.find_element(By.XPATH, element_xpath)
        self.driver.execute_script("arguments[0].click();", element)
        logging.error("Changing Propagation to Yes!")
        time.sleep(2)

        logging.error("---------------------------")
        propagate_change_xpath = '//*[@id="editSubnetDetails"]/table/tbody/tr[29]/td[2]/div/div/input'
        propagate_change = self.driver.find_element(By.XPATH, propagate_change_xpath)

        logging.error("Changing Done.")
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", propagate_change)

        self.driver.find_element(By.XPATH, '//*[@id="popup"]/div[3]/div[1]/button[2]').click()
        time.sleep(2)

        logging.error("Propagation for New File is Finished.")
        self.driver.close()
