# selenium-pagefactory-impl

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

A Selenium Page Factory implementation for Python, providing enhanced functionality for web automation.

## Features

- Simplified and intelligent page factory for Selenium projects.
- Convenient methods for interacting with web elements.
- Improved handling of StaleElementReferenceException.

## Installation

Use [Poetry](https://python-poetry.org/) to install the package and its dependencies:

```bash
poetry install
```
## How to implement in the test

```python
# Import the PageFactory class
from selenium_pagefactory.page_factory_impl import PageFactory

# Your page class using PageFactory
class YourPageClass:
    # Define locators
    locators = {
        'element_name': (By.XPATH, "//your/xpath"),
        # Add more locators as needed
    }

    # Initialize elements using PageFactory
    def __init__(self, driver):
        self.driver = driver
        PageFactory.initialize_elements(self, driver)

# Example usage
driver = webdriver.Chrome()
page_instance = YourPageClass(driver)
page_instance.element_name.click()
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Special thanks to the Selenium and pytest communities.
