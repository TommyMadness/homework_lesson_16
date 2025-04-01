import allure
from allure_commons.types import Severity

from pages.filters_page import FiltersPage
from pages.main_page import MainPage
from pages.search_results_page import SearchResultsPage


@allure.tag("web")
@allure.severity(Severity.MINOR)
@allure.label("owner", "atansan")
@allure.feature("Главная страница")
@allure.suite("UI-Тесты")
class TestMainPage:

    @allure.story("Проверка кликабельности кнопки 'Найти'")
    @allure.title("Кнопка 'Найти' доступна и кликабельна")
    def test_open_main_page(self, setup_browser):
        main_page = MainPage(setup_browser)

        main_page.open()
        main_page.close_popup()
        main_page.click_search_button()

    @allure.story("Смена вида отображения результатов")
    @allure.title(
        "Переключение со списка на карту после открытия страницы с результатами"
    )
    def test_toggle_map_view(self, setup_browser):
        filters_page = FiltersPage(setup_browser)
        main_page = MainPage(setup_browser)
        search_page = SearchResultsPage(setup_browser)

        main_page.open()
        main_page.close_popup()
        filters_page.select_rooms(2)
        filters_page.set_price_range("10_000_000", "15_000_000")
        filters_page.apply_filters()

        search_page.toggle_map_view_from_search_results()
        search_page.verify_map_is_displayed()
