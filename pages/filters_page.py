import allure


class FiltersPage:
    def __init__(self, browser):
        self.browser = browser

    @allure.step("Выбираем количество комнат: {rooms}")
    def select_rooms(self, rooms: int):
        self.browser.element('[data-mark="FilterRoomsCount"]').click()
        selected_rooms = self.browser.all(
            '//div[@class="_025a50318d--dropdown--aOO1u"]//button[contains(@class, "active")]'
        )
        for room in selected_rooms:
            room.click()
        self.browser.element(
            f'//div[@class="_025a50318d--dropdown--aOO1u"]//*[contains(text(),"{rooms}")]'
        ).click()

    @allure.step("Указываем диапазон цен от {min_price} до {max_price} рублей")
    def set_price_range(self, min_price: str, max_price: str):
        self.browser.element('[data-mark="FilterPrice"]').click()
        self.browser.element('[placeholder="от"]').type(min_price)
        self.browser.element('[placeholder="до"]').type(max_price)

    @allure.step("Применяем фильтры")
    def apply_filters(self):
        self.browser.element('[data-mark="FiltersSearchButton"]').click()
