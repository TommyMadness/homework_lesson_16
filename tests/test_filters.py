import allure
from allure_commons.types import Severity
from pages.main_page import MainPage
from pages.filters_page import FiltersPage
from pages.search_results_page import SearchResultsPage


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "atansan")
@allure.feature("Фильтрация объявлений")
@allure.suite("UI-Тесты")
class TestFilters:

    @allure.story("Фильтрация квартир по параметрам")
    @allure.title("Фильтр по количеству комнат и цене")
    def test_search_apartment_by_parameters(self, setup_browser):
        main_page = MainPage(setup_browser)
        filters_page = FiltersPage(setup_browser)
        search_results_page = SearchResultsPage(setup_browser)

        main_page.open()
        main_page.close_popup()

        filters_page.select_rooms(2)
        filters_page.set_price_range("5_000_000", "10_000_000")
        filters_page.apply_filters()

        search_results_page.verify_results_loaded()

    @allure.story("Фильтрация объявлений по наличию видео")
    @allure.title("Проверяем, что все объявления содержат иконку видео")
    def test_filter_by_video(self, setup_browser):
        main_page = MainPage(setup_browser)
        search_results_page = SearchResultsPage(setup_browser)

        main_page.open()
        main_page.close_popup()

        search_results_page.go_to_search_results()
        search_results_page.filter_by_video()
        search_results_page.wait_for_results_to_update()
        search_results_page.verify_all_listings_have_video_icon()
