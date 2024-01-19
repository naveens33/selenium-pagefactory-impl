import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium_pagefactory_impl.page_factory import PageFactory


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


class PageClass:
    locators = {
        'button': (By.TAG_NAME, "button"),
        'username': (By.NAME, "username"),
        'image': (By.XPATH, "//img[3]"),
        'text_': (By.TAG_NAME, "h3"),
        'login_button': (By.CSS_SELECTOR, "button.radius"),
        'checked_checkbox': (By.XPATH,"//form/input[2]"),
        'unchecked_checkbox': (By.XPATH, "//form/input[1]"),
        'text_box_en_dis': (By.XPATH,"//input[@type='text']"),
        'button_en_dis': (By.XPATH,"//button[not(text()='Remove')]")
    }

    def __init__(self, driver):
        self.driver = driver
        PageFactory.initialize_elements(self, driver)


class TestWebElementMethod:

    def test_tag_name(self, driver):
        driver.get("https://the-internet.herokuapp.com/abtest")
        assert PageClass(driver).text_.tag_name == 'h3'

    def test_text_property(self, driver):
        driver.get("https://the-internet.herokuapp.com/abtest")
        assert PageClass(driver).text_.text is not None

    def test_click(self, driver):
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
        PageClass(driver).button.click()

    def test_submit(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        PageClass(driver).username.send_keys("Username")
        PageClass(driver).username.submit()

    def test_clear(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        PageClass(driver).username.send_keys("Username")
        PageClass(driver).username.clear()

    def test_get_property(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        PageClass(driver).username.send_keys("Username")
        assert PageClass(driver).username.get_property("value") == "Username"

    def test_get_dom_attribute(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        assert PageClass(driver).username.get_dom_attribute("type") == "text"

    def test_get_attribute(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        assert PageClass(driver).username.get_attribute("type") == "text"

    def test_is_selected(self, driver):
        driver.get("https://the-internet.herokuapp.com/checkboxes")
        assert not PageClass(driver).unchecked_checkbox.is_selected()
        assert PageClass(driver).checked_checkbox.is_selected()

    def test_is_enabled(self, driver):
        driver.get("https://the-internet.herokuapp.com/dynamic_controls")
        assert not PageClass(driver).text_box_en_dis.is_enabled()
        PageClass(driver).button_en_dis.click()
        time.sleep(10)
        assert PageClass(driver).text_box_en_dis.is_enabled()

    def test_send_keys(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        PageClass(driver).username.send_keys("Username")

    def test_get_attribute(self, driver):
        driver.get("https://the-internet.herokuapp.com/broken_images")
        assert PageClass(driver).image.get_attribute('src') is not None


