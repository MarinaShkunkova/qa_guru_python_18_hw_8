class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        Метод сравнения имеющегося количества продукта с запрашиваемым
        """
        return self.quantity >= quantity

    def buy(self, quantity):
        """
        Метод покупки
        """
        if self.check_quantity(quantity):
            self.quantity -= quantity
        else:
            raise ValueError(f'Отсутствует нужное количество товара с наименованием {self.name}')

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        """
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        """
        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count

    def clear(self):
        """
        Метод обнуления корзины.
        """
        self.products.clear()

    def get_total_price(self) -> float:
        """
        Метод расчета стоимости суммарной стоимости продуктов в корзине.
        """
        total_prise = 0.0
        for product, quantity in self.products.items():
            total_prise += product.price * quantity
        return total_prise

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        if not self.products:
            raise ValueError("Корзина пуста. Пожалуйста, положите в неё товары")

        for product, quantity in self.products.items():
            if product.quantity < quantity:
                raise ValueError(f'Отсутствует нужное количество товара с наименованием {product.name}')

        for product, quantity in self.products.items():
            product.buy(quantity)

        self.clear()
