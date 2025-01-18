import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


class UiPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.set_zoom_level(0.6)

    def set_zoom_level(self, zoom_level):
        self.driver.execute_script(f"document.body.style.zoom='{zoom_level * 100}%'")

    def _wait_for_elements(self, by, value, multiple=False, timeout=10):
        if multiple:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located((by, value)))
        else:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))

    def _wait_for_text_in_element(self, by, value, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((by, value), text)
        )

    def _get_element_texts(self, css_selector):
        elements = self._wait_for_elements(By.CSS_SELECTOR, css_selector, multiple=True)
        return [element.text for element in elements]

    @allure.step("Проверяем заголовок страницы")
    def check_page_title(self, expected_title):
        WebDriverWait(self.driver, 10).until(lambda driver: driver.title != "")
        return self.driver.title == expected_title

    @allure.step("Поиск книги по фразе: {phrase}")
    def search_by_phrase(self, phrase):
        search_input = self._wait_for_elements(By.CSS_SELECTOR, ".header-search__input")
        search_input.send_keys(phrase)
        self.driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    @allure.step("Получаем названия книг")
    def find_book_titles(self):
        return self._get_element_texts(".product-title__head")

    @allure.step("Получаем авторов книг")
    def find_book_authors(self):
        return self._get_element_texts(".product-title__author")

    @allure.step("Получаем сообщение об отсутствии результатов")
    def check_empty_result(self):
        element = self._wait_for_elements(By.CSS_SELECTOR, ".catalog-empty-result__header")
        return element.text.replace('&nbsp;', ' ')

    @allure.step("Добавление первой книги в корзину")
    def click_first_action_button(self):
        buttons = self._wait_for_elements(By.CSS_SELECTOR, ".action-button__text", multiple=True)
        if buttons:
            buttons[0].click()
            allure.step("Кликнули на первый элемент с классом action-button__text")
        else:
            raise Exception("Элементы с классом action-button__text не найдены.")

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        cart_link = self._wait_for_elements(By.CSS_SELECTOR, 'a[href="/cart"]')
        cart_link.click()
        allure.step("Перешли в корзину")

    @allure.step("Получаем количество товара в корзине")
    def get_cart_item_count(self):
        element = self._wait_for_elements(By.CSS_SELECTOR, ".app-title__append")
        text = element.text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group(0))
        return 0

    @allure.step("Удаление книги из корзины")
    def delete_from_cart(self,):
        delete_buttons = self._wait_for_elements(
            By.CSS_SELECTOR,'.cart-item__actions-button--delete', multiple=True)
        if delete_buttons:
            delete_buttons[0].click()
            allure.step("Удалили первую книгу")
        else:
            raise Exception("Книг в корзине нет")
