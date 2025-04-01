import allure
from allure_commons.types import AttachmentType


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(
        body=png,
        name="screenshot",
        attachment_type=AttachmentType.PNG,
        extension=".png",
    )


def add_logs(browser):
    logs = browser.driver.get_log(log_type="browser")
    formatted_logs = "\n".join(f"{entry}" for entry in logs)
    allure.attach(formatted_logs, "browser_logs", AttachmentType.TEXT, ".log")


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, "page_source", AttachmentType.HTML, ".html")


def add_video(browser):
    video_url = (
        f"https://selenoid.autotests.cloud/video/{browser.driver.session_id}.mp4"
    )
    html = (
        "<html><body><video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'></video></body></html>"
    )
    allure.attach(
        html, f"video_{browser.driver.session_id}", AttachmentType.HTML, ".html"
    )
