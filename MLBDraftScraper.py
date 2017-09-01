from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url_template = "http://www.baseball-reference.com/draft/index.cgi?year_ID={year}&draft_round={round}&draft_type=junreg&query_type=year_round"

draft_df = pd.DataFrame()

column_headers = ['Year', 'Rnd', 'DT', 'OvPck', 'FrRnd', 'RdPck', 'Tm',
                  'Signed', 'Name', 'Pos', 'WAR', 'G', 'AB', 'HR', 'BA',
                  'OPS', 'G', 'W', 'L', 'ERA', 'WHIP', 'SV', 'Type', 'Drafted Out of']

for year in range(1965, 2018):
    for round in range(1,51):
        url = url_template.format(year=year, round=round)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        data_rows = soup.findAll('tr')[6:] # [6:] to remove extraneous rows
        player_data = [[td.getText() for td in data_rows[i].findAll(['td','th'])]
                        for i in range(len(data_rows))]
        year_df = pd.DataFrame(player_data, columns=column_headers)
        draft_df = draft_df.append(year_df, ignore_index=True)
        draft_df.to_csv("DraftData.csv")