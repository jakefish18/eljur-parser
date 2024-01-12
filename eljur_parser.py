from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from settings import settings


def get_lyceum_class_page(
    driver: webdriver.Chrome, lyceum_class: str, year_part: int, lessond_id=98
):
    """
    Gettings lyceum class page.

    Parameters:
        driver - selenium driver
        lyceum_class - lyceum class
        year_part - the part of the year to get marks. Can be equal 1 or 2
        lesson_id - the id of teacher lesson
    """
    match year_part:
        case 1:
            year_part = "I"
        case 2:
            year_part = "II"
        case _:
            raise IndexError

    driver.get(
        settings.ELJUR_URL
        + f"/journal-app/page.journal/class.{lyceum_class}/lesson_id.{lessond_id}/sp.{year_part}"
    )
    # Waiting while page is loading.
    WebDriverWait(driver, 10)

    with open(f"{lyceum_class}.html", "w") as file:
        file.write(driver.page_source)


def enter_auth_data(driver: webdriver.Chrome) -> None:
    """
    Passing password and username to input form and clicking auth button.
    """
    driver.get(url=settings.ELJUR_URL)
    try:
        email_input = driver.find_element(
            By.XPATH,
            "/html/body/div/div/main/div/div/div/div/form/div[1]/div[1]/div/input",
        )
        email_input.send_keys(settings.user_name)
        password_input = driver.find_element(
            By.XPATH,
            "/html/body/div/div/main/div/div/div/div/form/div[1]/div[2]/div/input",
        )
        password_input.send_keys(settings.user_password)
        auth_button = driver.find_element(
            By.XPATH, '//*[@id="loginviewport"]/div/div/form/div[2]/button'
        )
        auth_button.click()

    except:
        print("AUTH WENT WRONG")


def parse_all_students():
    """
    Parsing all students from all lyceum classes.

    It's needed to lyceum_classes in settings to parse them.
    Parser can parse lyceum class info only if teacher account have access to this class.

    HTML files will be generated for each class.
    """
    driver = webdriver.Chrome()
    options = Options()
    options.add_argument(settings.user_agent)
    enter_auth_data(driver)

    for lyceum_class in settings.lyceum_classes:
        get_lyceum_class_page(driver, lyceum_class, year_part=1)


if __name__ == "__main__":
    parse_all_students()
