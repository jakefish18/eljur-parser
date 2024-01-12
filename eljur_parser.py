import logging
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from settings import settings

logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w")


class EljurParser:
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(settings.user_agent)
        self.options.add_experimental_option(
            "prefs", {"download.default_directory": settings.STUDENT_DATA_STORE_PATH}
        )
        self.driver = webdriver.Chrome(options=self.options)
        self.enter_auth_data()
        self.headers = {}

    def get_lyceum_class_page(self, lyceum_class: str, year_part: int, lessond_id=98):
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

        self.driver.get(
            settings.ELJUR_URL
            + f"/journal-app/page.journal/class.{lyceum_class}/lesson_id.{lessond_id}/sp.{year_part}"
        )
        # Waiting while page is loading.
        WebDriverWait(self.driver, 10)

        student_ids = self.parse_lyceum_class_page(
            self.driver.page_source, lyceum_class
        )

        # with open(f"{lyceum_class}.txt", "w") as file:
        #     for student, student_id in student_ids.items():
        #         file.write(student + " " + student_id + "\n")

    def get_student_marks(
        self, save_folder_path: str, student_name: str, uid: int
    ) -> None:
        """
        Getting student marks by eljur uid.

        Eljur has unique uid for every student.
        So student page can be accessed by the uid of the student.

        Parameters:
            save_folder_path: str - path to save student marks
            student_name: str - name of the student behind the uid
            uid: int - uid of the student
        """
        url_student_marks_in_xlsx = (
            f"https://rbli.eljur.ru/journal-index-my-action/u.{uid}?mode=excel"
        )
        file_response = 200
        self.driver.get(url_student_marks_in_xlsx)
        logging.info(
            f"Parsing {uid} {student_name} {url_student_marks_in_xlsx} {file_response}"
        )

        # with open(save_folder_path + f"/{student_name}.xslx", "wb") as student_marks_file:
        #     shutil.copyfileobj(file_response.raw, student_marks_file)

    def parse_lyceum_class_page(self, page_html: str, lyceum_class: str):
        """
        Parsing every student from lyceum class page.

        page_html - string of page html.
        """

        lyceum_class_folder_path = settings.STUDENT_DATA_STORE_PATH + f"/{lyceum_class}"

        try:
            os.mkdir(lyceum_class_folder_path)
        except:
            logging.warning(f"{lyceum_class} folder is already exist")

        soup = BeautifulSoup(page_html, features="html.parser")
        student_ids = {}

        student_div_class = "cell notcat nobr noselect pointer cell-color-odd"
        for student in soup.find_all("div", class_=student_div_class):
            student_name = student.get("title")
            student_uid = student.get("uid")
            student_ids[student_name] = student_uid
            self.get_student_marks(lyceum_class_folder_path, student_name, student_uid)

        return student_ids

    def enter_auth_data(self) -> None:
        """
        Passing password and username to input form and clicking auth button.
        """
        self.driver.get(url=settings.ELJUR_URL)

        try:
            # Entering user_name.
            user_name_input = self.driver.find_element(
                By.XPATH,
                "/html/body/div/div/main/div/div/div/div/form/div[1]/div[1]/div/input",
            )
            user_name_input.send_keys(settings.user_name)

            # Entering password.
            password_input = self.driver.find_element(
                By.XPATH,
                "/html/body/div/div/main/div/div/div/div/form/div[1]/div[2]/div/input",
            )
            password_input.send_keys(settings.user_password)

            # Clicking auth button.
            auth_button = self.driver.find_element(
                By.XPATH, '//*[@id="loginviewport"]/div/div/form/div[2]/button'
            )
            auth_button.click()

        except:
            logging.error("AUTH WENT WRONG")

    def parse_all_students(self):
        """
        Parsing all students from all lyceum classes.

        It's needed to lyceum_classes in settings to parse them.
        Parser can parse lyceum class info only if teacher account have access to this class.

        HTML files will be generated for each class.
        """
        for lyceum_class in settings.lyceum_classes:
            self.get_lyceum_class_page(lyceum_class, year_part=1)


if __name__ == "__main__":
    eljur_parser = EljurParser()
    eljur_parser.parse_all_students()
