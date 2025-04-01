import allure
from allure_commons.types import Severity
from pages.main_page import MainPage
from pages.search_results_page import SearchResultsPage


@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "atansan")
@allure.feature("Сортировка объявлений")
@allure.suite("UI-Тесты")
class TestSorting:

    @allure.story("Сортировка объявлений по цене")
    @allure.title("Проверка сортировки по возрастанию цены")
    def test_sort_by_price(self, setup_browser):
        main_page = MainPage(setup_browser)
        search_results = SearchResultsPage(setup_browser)

        main_page.open()
        main_page.close_popup()

        search_results.go_to_search_results()
        search_results.sort_by_price_ascending()
        search_results.wait_for_results_to_update()
        search_results.verify_sorted_by_price()
