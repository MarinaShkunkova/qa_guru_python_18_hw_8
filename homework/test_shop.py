import pytest

from homework.models import Product, Cart


@pytest.fixture
def product_book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_pen():
    return Product("pen", 90, "This is a pen", 500)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product_book):
        assert product_book.check_quantity(999) is True
        assert product_book.check_quantity(1000) is True
        assert product_book.check_quantity(1001) is False

    def test_product_buy(self, product_book):
        product_book.buy(999)
        assert product_book.quantity == 1

    def test_product_buy_all(self, product_book):
        product_book.buy(1000)
        assert product_book.quantity == 0

    def test_product_buy_more_than_available(self, product_book):
        with pytest.raises(ValueError, match="Отсутствует нужное количество товара с наименованием book"):
            product_book.buy(1001)
        assert product_book.quantity == 1000


class TestCart:

    def test_cart_add_product_in_cart(self, cart, product_book):
        cart.add_product(product_book, 2)
        assert product_book in cart.products

    def test_cart_add_product_first_addendum(self, cart, product_book):
        cart.add_product(product_book, 2)
        assert cart.products[product_book] == 2

    def test_cart_add_product_second_addendum(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.add_product(product_book, 1)
        assert cart.products[product_book] == 3

    def test_cart_add_two_products(self, cart, product_book, product_pen):
        cart.add_product(product_book, 2)
        cart.add_product(product_pen, 1)
        assert cart.products[product_book] == 2
        assert cart.products[product_pen] == 1

    def test_cart_remove_product_partly(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.remove_product(product_book, 1)
        assert cart.products[product_book] == 1

    def test_cart_remove_product_all(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.remove_product(product_book, 2)
        assert product_book not in cart.products

    def test_cart_remove_one_of_the_products(self, cart, product_book, product_pen):
        cart.add_product(product_book, 2)
        cart.add_product(product_pen, 1)
        cart.remove_product(product_book, 2)
        assert product_book not in cart.products
        assert product_pen in cart.products

    # удалить товаров больше, чем есть в корзине
    def test_cart_remove_more_products_then_exist(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.remove_product(product_book, 3)
        assert product_book not in cart.products

    # удалить товар, без указания количества для удаления
    def test_cart_remove_products_without_remove_count(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.remove_product(product_book)
        assert product_book not in cart.products

    # удалить товар, которого нет в корзине
    def test_cart_remove_products_in_empty_cart(self, cart, product_book, product_pen):
        cart.add_product(product_book, 2)
        with pytest.raises(ValueError, match="Товар с наименованием pen отсутствует в корзине"):
            cart.remove_product(product_pen)

    # удалить товар когда корзина пуста
    def test_cart_remove_products_in_empty_cart(self, cart, product_book):
        with pytest.raises(ValueError, match="В корзине отсутствуют товары"):
            cart.remove_product(product_book)

    def test_cart_clear(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.clear()
        assert cart.products == {}

    def test_cart_get_total_price(self, cart, product_book, product_pen):
        cart.add_product(product_book, 2)
        cart.add_product(product_pen, 1)
        assert cart.get_total_price() == ((product_book.price * 2) + (product_pen.price * 1))

    def test_cart_buy_success(self, cart, product_book):
        product_book_quantity_before_buy = product_book.quantity
        cart.add_product(product_book, 2)
        cart.buy()
        assert product_book.quantity == product_book_quantity_before_buy - 2
        assert cart.products == {}

    def test_cart_buy_empty_cart(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.remove_product(product_book, 2)
        with pytest.raises(ValueError, match="Корзина пуста. Пожалуйста, положите в неё товары"):
            cart.buy()

    def test_cart_buy_not_enough_product(self, cart, product_book):
        cart.add_product(product_book, 1001)
        with pytest.raises(ValueError, match="Отсутствует нужное количество товара с наименованием book"):
            cart.buy()
