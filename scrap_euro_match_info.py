from selenium import webdriver
import time



class EuroMatchInfoScraper:

    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.max_waiting_time = 5
        self.season = 1960
        self.base_url = "https://fr.uefa.com/uefaeuro/"

    def wait_for_element(self, xpath, component_to_search=None):
        data = self.driver.find_elements_by_xpath(xpath)
        start = time.time()
        while not data:
            if component_to_search:
                data = component_to_search.find_elements_by_xpath(xpath)
            else:
                data = self.driver.find_elements_by_xpath(xpath)
            print("waiting")
            time.sleep(0.01)
            if time.time() - start > self.max_waiting_time:
                return None
        return data

    def extract_season_data(self):
        url = self.base_url + "season={}/matches/all/index.html".format(self.season)
        self.driver.get(url)

        count_table = 1
        while True:
            # div 3 here because chrome asking for cookies adds div
            x_path_date = "/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div/div[2]/table[{}]".format(count_table)
            print(x_path_date)
            data_date = self.wait_for_element(x_path_date)
            if data_date:
                self.extract_date_data(data_date[0])
            else:
                break
            count_table += 1
        print(self.season, count_table)



        # first match
        "/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div/div[2]/table[1]"
        "/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div/div[2]/table[60]"


    def extract_date_data(self, data_date):
        match_count = 1
        while True:
            add_xpath = ".//body[{}]".format(match_count)
            data_match = self.wait_for_element(add_xpath, data_date)
            if data_match:
                self.extract_match_data(data_match)
            else:
                break
            match_count += 1


    def extract_match_data(self, data_match):
        pass



    def main(self):
        last_season = 2016
        while self.season <= last_season:
            print("season", self.season)
            self.extract_season_data()
            self.season += 4
            time.sleep(2)

        self.driver.close()


if __name__ == '__main__':
    scraper = EuroMatchInfoScraper()
    scraper.main()
