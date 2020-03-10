from selenium import webdriver
import time


csv_header = "team_name;rank;global_rating;avg_rating;total_nb_match;home_nb_match;away_nb_match;neutral_nb_match;win_nb_match;loss_nb_match;draw_nb_match;goal_for_total;goal_against_total;year\n"

def get_xpath_row(number):
    return "/html/body/div[1]/div[2]/div[1]/div[6]/div/div[{}]".format(number)

class EloRatingScraper:

    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.base_url = "https://www.eloratings.net/"
        self.year = 2020
        self.year_fin = 2020
        self.lines_to_write = []
        self.lines_to_write.append(csv_header)

    def get_data(self):
        self.driver.get(self.base_url + "/" + str(self.year))
        equipe_number = 1
        base_xpath = "/html/body/div[1]/div[2]/div[1]/div[6]/div/div[1]"

        data_team = None
        while not data_team:
            data_team = self.driver.find_elements_by_xpath(base_xpath)
            time.sleep(0.5)

        while True:
            x_path_row = get_xpath_row(equipe_number)
            data_team = self.driver.find_elements_by_xpath(x_path_row)
            if not data_team:
                break
            self.extract_data(data_team[0])
            equipe_number += 1


    def extract_data(self, data_team):
        rank = data_team.find_element_by_xpath(".//div[1]").text
        team_name = data_team.find_element_by_xpath(".//div[2]/a").get_attribute("href").split(r"//")[-1]
        print("\tgetting data for team", team_name)
        global_rating = data_team.find_element_by_xpath(".//div[3]").text
        if self.year == 2020:
            average_rating = data_team.find_element_by_xpath(".//div[7]").text
            total_match = data_team.find_element_by_xpath(".//div[10]").text
            home_match = data_team.find_element_by_xpath(".//div[11]").text
            away_match = data_team.find_element_by_xpath(".//div[12]").text
            neutral_match = data_team.find_element_by_xpath(".//div[13]").text

            win_match = data_team.find_element_by_xpath(".//div[14]").text
            loss_match = data_team.find_element_by_xpath(".//div[15]").text
            draw_match = data_team.find_element_by_xpath(".//div[16]").text
            goal_for = data_team.find_element_by_xpath(".//div[17]").text
            goal_against = data_team.find_element_by_xpath(".//div[18]").text
        else:
            average_rating = data_team.find_element_by_xpath(".//div[5]").text
            total_match = data_team.find_element_by_xpath(".//div[8]").text
            home_match = data_team.find_element_by_xpath(".//div[9]").text
            away_match = data_team.find_element_by_xpath(".//div[10]").text
            neutral_match = data_team.find_element_by_xpath(".//div[11]").text

            win_match = data_team.find_element_by_xpath(".//div[12]").text
            loss_match = data_team.find_element_by_xpath(".//div[13]").text
            draw_match = data_team.find_element_by_xpath(".//div[14]").text

            goal_for = data_team.find_element_by_xpath(".//div[15]").text
            goal_against = data_team.find_element_by_xpath(".//div[16]").text

        toadd = team_name
        toadd += ";" + rank
        toadd += ";" + global_rating
        toadd += ";" + average_rating
        toadd += ";" + total_match
        toadd += ";" + home_match
        toadd += ";" + away_match
        toadd += ";" + neutral_match
        toadd += ";" + win_match
        toadd += ";" + loss_match
        toadd += ";" + draw_match
        toadd += ";" + goal_for
        toadd += ";" + goal_against
        toadd += ";" + str(self.year) + "\n"
        self.lines_to_write.append(toadd)

    def main(self):
        start_time_all = time.time()
        start_time = time.time()
        while self.year <= self.year_fin:
            print("starting year", self.year)
            self.get_data()
            print("year", self.year, "acquired in", time.time() - start_time, "seconds")
            try:
                with open("eloratings.csv", 'w') as file:
                    file.writelines(self.lines_to_write)
                    self.lines_to_write = []
            except UnicodeEncodeError:
                for line in self.lines_to_write:
                    print(line)
            start_time = time.time()
            self.year += 1
            time.sleep(1)

        self.driver.close()

        print("SCRAPING DONE IN", time.time() - start_time_all, "seconds")


if __name__ == '__main__':
    scraper = EloRatingScraper()
    scraper.main()
