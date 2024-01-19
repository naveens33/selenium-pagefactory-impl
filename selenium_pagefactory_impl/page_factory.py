from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class LocatingElementHandler:
    def __init__(self, driver, locator):
        self.locator = locator
        self.driver = driver
        self.cached_element = None
        self.save_cache_element()

    def is_callable(self, method):
        return callable(getattr(WebElement, method))

    def __call__(self, instance, method, *args, **kwargs):
        if method == "find_elements":
            return self.find_elements()

        if self.check_staleness():
            self.cached_element = self.find_element()

        try:
            action_method = getattr(self.cached_element, method)
            if action_method is not None and callable(action_method):
                return action_method(*args, **kwargs)
            else:
                return action_method
        except AttributeError:
            raise AttributeError(f"{type(self.cached_element).__name__} object has no attribute '{method}'")
        except Exception as e:
            raise e

    def find_element(self):
        return self.driver.find_element(*self.locator)

    def find_elements(self):
        return self.driver.find_elements(*self.locator)

    def save_cache_element(self):
        try:
            self.cached_element = self.find_element()
        except Exception as e:
            pass

    def check_staleness(self):
        try:
            # Calling any method forces a staleness check
            self.cached_element.is_enabled()
            return False
        except StaleElementReferenceException:
            return True


class ElementProxy:
    def __init__(self, handler):
        self.handler = handler

    def __getattr__(self, item):
        if self.handler.is_callable(item):
            def method_missing(*args, **kwargs):
                return self.handler(None, item, *args, **kwargs)

            return method_missing
        else:
            # If the attribute is not callable (an attribute), return the result
            return self.handler(None, item)


class PageFactory:
    @staticmethod
    def create_element_proxy(handler):
        return ElementProxy(handler)

    @classmethod
    def initialize_elements(cls, obj, driver):
        for element_name, locator in obj.locators.items():
            if isinstance(locator, tuple) and cls.is_valid_locator_strategy(locator[0]):
                element_proxy = cls.create_element_proxy(LocatingElementHandler(driver, locator))
                setattr(obj, element_name, element_proxy)

    @staticmethod
    def is_valid_locator_strategy(strategy):
        return any(strategy == getattr(By, attr) for attr in dir(By) if
                   not callable(getattr(By, attr)) and not attr.startswith("__"))
