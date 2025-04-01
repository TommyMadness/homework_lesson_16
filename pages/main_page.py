import allure
from selene import be, have


class MainPage:
    def __init__(self, browser):
        self.browser = browser

    @allure.step("Открываем главную страницу Cian")
    def open(self):
        self.browser.open("/")

    @allure.step("Закрываем всплывающее окно, если оно появилось")
    def close_popup(self):
        popup_close_button = self.browser.element("button[title='Закрыть']")
        if popup_close_button.matching(be.visible):
            popup_close_button.click()

    @allure.step("Нажимаем кнопку 'Найти'")
    def click_search_button(self):
        self.browser.all('[data-mark="FiltersSearchButton"]').element_by(
            have.text("Найти")
        ).click()
