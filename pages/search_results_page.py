import allure
from selene import be, have, query
import re


class SearchResultsPage:
    def __init__(self, browser):
        self.browser = browser

    @allure.step("Проверяем, что результаты поиска отображаются")
    def verify_results_loaded(self):
        self.browser.element('[data-name="SummaryHeader"]').wait_until(be.visible)
        self.browser.all('[data-name="SummaryHeader"]').element_by(have.text("Найдено"))

    @allure.step("Включаем фильтр 'Только с видео'")
    def filter_by_video(self):
        self.browser.element('[data-name="AdvancedFiltersContainer"]').click()
        self.browser.all("span").element_by(have.text("Видео")).click()
        self.browser.all("span").element_by(have.text("Показать")).click()

    @allure.step("Проверяем, что у каждого объявления есть иконка видео")
    def verify_all_listings_have_video_icon(self):
        self.browser.element('[data-name="FeatureLabels"] svg').wait_until(be.visible)
        listings = self.browser.all('[data-testid="offer-card"]')

        for listing in listings:
            listing.element('[data-name="FeatureLabels"] svg').should(be.visible)

    @allure.step("Переход на страницу поиска квартир")
    def go_to_search_results(self):
        self.browser.element('a[href*="kupit"]').click()
        self.browser.element('[data-mark="FiltersSearchButton"]').click()

    @allure.step("Выбираем сортировку по возрастанию цены")
    def sort_by_price_ascending(self):
        self.browser.element('[data-mark="SortDropdownButton"]').click()
        self.browser.all('[data-name="SelectPopupOption"]').element_by(
            have.text("По цене (сначала дешевле)")
        ).click()

    @allure.step("Ожидаем обновления списка объявлений")
    def wait_for_results_to_update(self):
        self.browser.wait_until(
            lambda: len(
                self.browser.all(
                    '[data-name="GeneralInfoSectionRowComponent"] [data-mark="MainPrice"]'
                )
            )
            > 5
        )

    @allure.step("Проверяем, что объявления отсортированы по возрастанию цены")
    def verify_sorted_by_price(self):
        price_elements = self.browser.all(
            '[data-name="GeneralInfoSectionRowComponent"] [data-mark="MainPrice"]'
        )

        prices = [price.get(query.text) for price in price_elements]

        price_values = [
            int(re.search(r"\d[\d\s]*", price).group().replace(" ", ""))
            for price in prices
            if re.search(r"\d[\d\s]*", price)
        ]

        price_values = list(dict.fromkeys(price_values))

        assert price_values == sorted(
            price_values
        ), f"Цены не отсортированы по возрастанию: {price_values}"

    @allure.step("Переключаемся на отображение карты")
    def toggle_map_view_from_search_results(self):
        self.browser.all('[data-name="SummaryButtonWrapper"]').element_by(
            have.text("На карте")
        ).click()

    @allure.step("Проверяем, что карта отображается")
    def verify_map_is_displayed(self):
        self.browser.element(
            '[data-name="Map"][data-results-status="succeed"]'
        ).wait_until(be.visible)
