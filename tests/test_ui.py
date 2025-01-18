import allure
import pytest
from selenium import webdriver
from pages.ui_page import UiPage
from settings import ui_url


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    ui_page = UiPage(driver, ui_url)
    yield ui_page
    driver.quit()


@allure.feature("Тестирование интернет-магазина")
@allure.story("Smoke тесты.UI")
@allure.severity("blocker")
@allure.title("Проверка заголовка главной страницы")
def test_check_main_page_title(browser):
    with allure.step("Заголовок главной страницы"):
        assert browser.check_page_title(
            "«Читай-город» – интернет-магазин книг")


@allure.feature("Тестирование интернет-магазина")
@allure.story("Позитивные тесты.UI")
@allure.severity("blocker")
@allure.title("Найти книгу по заголовку")
@pytest.mark.parametrize("book_name", ["1984", "Python с нуля", "Манга"])
def test_search_by_phrase(browser, book_name):
    with allure.step(f"Поиск книг с названием"
                     f" {book_name}"):
        browser.search_by_phrase(book_name)

    with allure.step(f"Книга с названием {book_name} найдена"):
        assert book_name in browser.find_book_titles()


@allure.feature("Тестирование интернет-магазина")
@allure.story("Позитивные тесты.UI")
@allure.severity("blocker")
@allure.title("Найти книгу по автору")
@pytest.mark.parametrize("author_name", ["Михаил Лермонтов",
                                         "Agatha Christie"])
def test_search_by_author(browser, author_name):
    with allure.step(f"Поиск книг автора: "
                     f" {author_name}"):
        browser.search_by_phrase(author_name)

    with allure.step(f"Книга с названием {author_name} есть в ответе"):
        assert author_name in browser.find_book_authors()


@allure.feature("Тестирование интернет-магазина")
@allure.title("Позитивные тесты.UI")
@allure.severity("blocker")
@allure.title("Добавление книги в корзину")
@pytest.mark.parametrize("book_name", [
    "Дневник книготорговца",
#    "трое в лодке не считая собаки",
#    "1984",
#    "Sailor moon",
    "Соня"
])
def test_add_to_cart(browser, book_name):
    with allure.step("Поиск книг для добавления"):
        browser.search_by_phrase(book_name)

    with allure.step("Добавить книгу в корзину"):
        browser.click_first_action_button()

    with allure.step("Переход в корзину"):
        browser.go_to_cart()

    with allure.step("Проверить, что корзина не пуста"):
        assert browser.get_cart_item_count() > 0


@allure.feature("Тестирование интернет-магазина")
@allure.title("Негативные тесты.UI")
@allure.severity("major")
@allure.step("Добавить книгу в корзину с невалидным названием")
@pytest.mark.parametrize("book_name", ["$^&*", ";)"])
def test_add_to_cart_negative(browser, book_name):
    with allure.step("Попробовать добавить книгу с невалидным названием"):
        browser.search_by_phrase(book_name)

    with allure.step("Проверить, что ничего не найдено"):
        assert browser.check_empty_result() == "Похоже, у нас такого нет"


@allure.feature("Тестирование интернет-магазина")
@allure.title("Позитивные тесты.UI")
@allure.step("Удаление товара из корзины")
@allure.severity("blocker")
@pytest.mark.parametrize("book_name", ["Умная собачка Соня"])
def test_delete_from_cart(browser, book_name):
    with allure.step("Добавить книгу в корзину"):
        browser.search_by_phrase(book_name)
        browser.click_first_action_button()

    with allure.step("Перейти в корзину и удалить книгу"):
        browser.go_to_cart()
        items_before = browser.get_cart_item_count()
        browser.delete_from_cart()
        items_after = browser.get_cart_item_count()

    with allure.step("Проверить, что товар больше не существует в списке"):
        assert items_before < items_after