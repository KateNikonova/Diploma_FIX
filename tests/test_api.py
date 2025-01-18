import pytest
import allure
from pages.api_page import ApiPage
from settings import api_url, my_headers


api = ApiPage(api_url, my_headers)

@allure.feature("Тестирование API интернет-магазина")
@allure.title("Позитивные тесты")
@allure.step("Поиск книги по названию. API")
@pytest.mark.parametrize("title, customer_city", [
    ("Дневник книготорговца", 213),
    ("мастер и маргарита", 98),
    ("python", 45),
    ("1984", 65),
    ("Sailor Moon", 16)
    ])
def test_search_by_title(title, customer_city):
    resp_search = api.search_book(title, customer_city)
    assert resp_search.status_code == 200
    assert title in resp_search.text

@allure.feature("Тестирование API интернет-магазина")
@allure.title("Позитивные тесты")
@allure.step("Поиск книги по фамилии автора. API")
@pytest.mark.parametrize("author_name, customer_city", [
    ("Байтелл", 213),
    ("Достоевский", 98),
    ("Kant", 45),
    ("Салтыков-Щедрин", 172),
    ("Garcia Lorca", 65)
    ])
def test_search_by_author(author_name, customer_city):
    resp_search = api.search_book(author_name, customer_city)
    assert resp_search.status_code == 200
    assert author_name in resp_search.text

@allure.feature("Тестирование API интернет-магазина")
@allure.title("Позитивные тесты")
@allure.step("Добавление книги в корзину. API")
@pytest.mark.parametrize("book_id", [2648551, 3022703, 2893579, 2614111])
def test_add_book(book_id):
    books_before = api.check_cart()
    resp_add = api.add_book(book_id)
    assert resp_add.status_code == 200
    books_after = api.check_cart()
    assert books_before == (books_after-1)
    api.clean_cart()

@allure.feature("Тестирование API интернет-магазина")
@allure.title("Позитивные тесты")
@allure.step("Удаление книги из корзины.API")
@pytest.mark.parametrize("book_id", [2648551, 3022703, 2893579, 2614111])
def test_delete_from_cart(book_id):
    api.clean_cart()
    books_before = api.check_cart()
    api.add_book(book_id)
    book_cart_id = api.check_cart_ids(books_before)
    resp_delete = api.delete_from_cart(book_cart_id)
    assert resp_delete.status_code == 204
    books_after = api.check_cart()
    assert books_before == books_after

@allure.feature("Тестирование API интернет-магазина")
@allure.title("Негативные тесты")
@allure.step("Пустой поиск. API")
@pytest.mark.parametrize("title, customer_city", [
    ("", 213),
    (" ", 213),
    ("тест", 0),
    ("______", 65)
])
def test_search_negative(title, customer_city):
    resp_search = api.search_book(title, customer_city)
    assert resp_search.status_code in (400, 422)