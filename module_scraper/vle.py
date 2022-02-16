from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

VLE_BASE = "https://vle.york.ac.uk"

# Login consts
LOGIN_BUTTON_NAME = "_eventId_proceed"
YORKSHARE_BUTTON_XPATH = "//div[@class='containerPortal clearfix']/div/div/div[2]/div/div/table/tbody/tr[2]/td[1]/div/p/a"


class VLEWrapper:

    def __init__(self, driver, timeout=2):
        self.driver = driver
        self.logged_in = False
        self.timeout = timeout
        self.module = None

    def __del__(self):
        self.driver.quit()

    def _get_element(self, *args):
        return WebDriverWait(
            self.driver, self.timeout).until(lambda d: d.find_element(*args))

    def _get_elements(self, *args):
        return WebDriverWait(
            self.driver, self.timeout).until(lambda d: d.find_elements(*args))

    def login(self, username, password):
        self.driver.get(VLE_BASE)

        # Yorkshare forwarding
        yorkshare_button = self._get_element(By.XPATH, YORKSHARE_BUTTON_XPATH)
        yorkshare_button.click()

        # York shib auth
        username_box = self._get_element(By.ID, "username")
        password_box = self.driver.find_element(By.ID, "password")
        username_box.send_keys(username)
        password_box.send_keys(password)
        login_button = self.driver.find_element(By.NAME, LOGIN_BUTTON_NAME)
        login_button.click()

        # Yorkshare forwarding again if we need it
        try:
            yorkshare_button = self._get_element(By.XPATH,
                                                 YORKSHARE_BUTTON_XPATH)
            yorkshare_button.click()
        except TimeoutException:
            pass

        self.logged_in = True

    def get_modules(self, search_string):
        assert self.logged_in
        self.driver.get(VLE_BASE)
        self.module = None
        return self._get_elements(By.PARTIAL_LINK_TEXT, search_string)

    def goto_module(self, module):
        assert self.logged_in
        self.driver.get(VLE_BASE)
        self.get_modules(module)[0].click()
        self.module = module.lower()
