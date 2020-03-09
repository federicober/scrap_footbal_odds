from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import datetime
import time
import os


def write_table(driver):
    """
    Writes the table into the data.txt file
    :param driver: selenium driver
    :return: None
    """
    table = driver.find_element_by_id("tournamentTable")
    with open('data.txt', 'a') as fp:
        fp.write('\n')
        fp.write(table.get_attribute('innerHTML'))


def get_year(year=2019, page=1):
    """
    Scraps year starting from page
    :param year: the year to scrap
    :param page: the page to start scrapping
    :return: None
    """
    driver = webdriver.Chrome(executable_path=os.path.join(os.environ['CHROMIUM_DIR'], 'chromedriver.exe'))

    # Current y
    if year == datetime.date.today().year:
        url = f"https://www.oddsportal.com/soccer/world/friendly-international/results/#/page/{page}/"
    else:
        url = f"https://www.oddsportal.com/soccer/world/friendly-international-{year}/results/#/page/{page}/"
    print(url)
    driver.get(url)
    time.sleep(0.5)
    write_table(driver)
    try:
        # If in the pagination object there is a link greater that the current page number
        # it means that we have not finished scappring the year
        pagination = driver.find_element_by_id('pagination')
        for i in pagination.find_elements_by_tag_name('a'):
            next_page = i.get_attribute('innerHTML').strip('</span>')
            try:
                int(next_page)
            except ValueError:
                # arrows in the pagination are to be ignored
                # they can be identified because we cannot convert them into inf
                # we use continue to skip this iteration
                continue
            if int(next_page) > page:
                driver.close()
                get_year(year=year, page=page + 1)
                # close the driver and stop iterating because we already know that there is a bigger page
                break

    # If there is no pagination, this means that there is only one table. We finish the year
    except NoSuchElementException:
        pass

    # close the driver if it isn't already
    try:
        driver.close()
    except:
        pass


def main():
    """
    Clears the file and starts scrapping from 2004
    :return:
    """
    # clears file
    with open('data.txt', 'w') as fp:
        pass

    for year_ in range(2004, datetime.date.today().year+1):
        get_year(year_)


if __name__ == '__main__':
    main()
