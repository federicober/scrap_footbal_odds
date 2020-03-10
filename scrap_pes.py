from selenium import webdriver
import time

csv_header = "team_name;overall_score;def_score;mid_score;att_score;speed_score;strength_score;year\n"


class PESRankingScraper:

    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.urls = [
            "https://www.pesmaster.com/national-teams-europe/pes-2020/league/33/",
            "https://www.pesmaster.com/national-teams-europe/pes-2019/league/33/",
            "https://www.pesmaster.com/national-teams-europe/pes-2018/league/90/",
            "https://www.pesmaster.com/national-teams-europe/pes-2017/league/90/",
            "https://www.pesmaster.com/national-teams-europe/pes-2016/league/90/",
            "https://www.pesmaster.com/national-teams-europe/pes-2015/league/90/",
            # Missing 2014
            "https://www.pesmaster.com/classic-teams/pes-2013/league/50/",
            "https://www.pesmaster.com/classic-teams/pes-2012/league/50/",
            "https://www.pesmaster.com/classic-teams/pes-2011/league/50/"
        ]
        self.url_test = "https://www.pesmaster.com/national-teams-europe/pes-2014/league/7/"
        self.lines_to_add = []
        self.lines_to_add.append(csv_header)

    def get_data_2020(self):
        self.driver.get(self.urls[0])
        for i in range(1, 56):
            x_path_team = "/html/body/div/div[2]/div[3]/div/div[{}]".format(i)
            data_team = self.driver.find_element_by_xpath(x_path_team)

            team_name = data_team.get_attribute("data-name")
            overall_score = data_team.get_attribute("data-overall")
            def_score = data_team.get_attribute("data-defence")
            mid_score = data_team.get_attribute("data-midfield")
            att_score = data_team.get_attribute("data-attack")
            speed_score = data_team.get_attribute("data-speed")
            strength_score = data_team.get_attribute("data-strength")

            toadd = team_name
            toadd += ";" + overall_score
            toadd += ";" + def_score
            toadd += ";" + mid_score
            toadd += ";" + att_score
            toadd += ";" + speed_score
            toadd += ";" + strength_score
            toadd += ";" + "2020\n"
            self.lines_to_add.append(toadd)

    def get_2011_2019_data(self):
        for i in range(1, len(self.urls)):
            self.driver.get(self.urls[i])
            indice_team = 1
            while True:
                xpath_team = "/html/body/div/div[1]/div/div[3]/table/tbody/tr[{}]".format(indice_team)
                data_team = self.driver.find_elements_by_xpath(xpath_team)
                indice_team += 1
                if not data_team:
                    break
                team_name = data_team[0].find_element_by_xpath(".//td[1]/a").text
                overall_score = data_team[0].find_element_by_xpath(".//td[2]/span").text
                def_score = data_team[0].find_element_by_xpath(".//td[3]/span").text
                mid_score = data_team[0].find_element_by_xpath(".//td[4]/span").text
                att_score = data_team[0].find_element_by_xpath(".//td[5]/span").text
                speed_score = data_team[0].find_element_by_xpath(".//td[6]/span").text
                strength_score = data_team[0].find_element_by_xpath(".//td[7]/span").text
                if i <= 5:
                    year = str(2020 - i)
                else:
                    year = str(2020 - i - 1)
                print("team", team_name, "year", year)
                toadd = team_name
                toadd += ";" + overall_score
                toadd += ";" + def_score
                toadd += ";" + mid_score
                toadd += ";" + att_score
                toadd += ";" + speed_score
                toadd += ";" + strength_score
                toadd += ";" + year + "\n"
                self.lines_to_add.append(toadd)
            time.sleep(2)

    def main(self):
        print("data 2020")
        self.get_data_2020()
        with open("output/pes.csv", 'w') as file:
            file.writelines(self.lines_to_add)
        self.lines_to_add = []
        time.sleep(2)
        self.get_2011_2019_data()
        with open("output/pes.csv", 'a') as file:
            file.writelines(self.lines_to_add)
        self.driver.close()


if __name__ == "__main__":
    scraper = PESRankingScraper()
    scraper.main()
