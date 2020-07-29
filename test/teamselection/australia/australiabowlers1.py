from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

#your required site here.  Should be the link of 'Most Runs' page of any series or overall records.
url = 'http://stats.espncricinfo.com/ci/engine/records/batting/most_runs_career.html?id=12741;type=tournament'#IPL2019
response = get(url)
html_soup = BeautifulSoup(response.text,'html.parser')

right_table = html_soup.find_all('tr', class_ = 'data2')

player_name= []
played_matches = []
played_inns = []
not_outs = []
runs_scored = []
high_scores = []
average = []
balls_faced = []
strike_rate = []
hundreds = []
fifties = []
ducks = []
fours = []
sixes = []
i=0
infinite = 0
for row in right_table:
        cells = row.find_all("td")
        i+=1
        if len(cells)==1:
            break;
        if len(cells)>0:
            player_name.append(cells[0].find(text=True))
            # print(player_name)
            played_matches.append(cells[1].find(text=True))
            # print(i,played_matches)
            played_inns.append(int(cells[2].find(text=True)))
            # print(played_inns)
            not_outs.append(int(cells[3].find(text=True)))
            # print(not_outs)
            runs_scored.append(int(cells[4].find(text=True)))
            high_scores.append(cells[5].find(text=True))
            if (cells[6].find(text=True))=='-':
                average.append(infinite)
            else:
                average.append(float(cells[6].find(text=True)))
            balls_faced.append(int(cells[7].find(text=True)))
            strike_rate.append(float(cells[8].find(text=True)))
            hundreds.append(int(cells[9].find(text=True)))
            fifties.append(int(cells[10].find(text=True)))
            ducks.append(int(cells[11].find(text=True)))
            fours.append(int(cells[12].find(text=True)))
            sixes.append(int(cells[13].find(text=True)))

tables = pd.DataFrame({'Names': player_name,
                        'Matches': played_matches,
                        'Innings': played_inns,
                        'NO': not_outs,
                        'Runs': runs_scored,
                        'HS': high_scores,
                        'Average': average,
                        'BF': balls_faced,
                        'SR': strike_rate,
                        '100s': hundreds,
                        '50s': fifties,
                        '0s': ducks,
                        'Fours': fours,
                        'Sixes': sixes})

#saving the above pandas dataframe to a csv file
tables.to_csv("/Users/mac/PycharmProjects/series_batting_stats_IPL2019.csv", index=False, encoding='utf8')

#calculating who has maximum strike rate, highest score, most sixes and so on
max_SR=tables[tables['SR']== max(tables['SR'])]
most_runs = tables[tables['Runs']== max(tables['Runs'])]
highest_score = tables[tables['HS']== max(tables['HS'])]
best_average = tables[tables['Average'] == max(tables['Average'])]
max_balls_faced = tables[tables['BF']== max(tables['BF'])]
most_hundreds = tables[tables['100s']== max(tables['100s'])]
most_fours = tables[tables['Fours']== max(tables['Fours'])]
most_sixes = tables[tables['Sixes']== max(tables['Sixes'])]

sorted_rate = sorted(tables['SR'],reverse = True)
sorted_SR = []
for i in range(len(sorted_rate)):
    sorted_SR.append(tables[tables['SR'] == sorted_rate[i]])
for i in range(len(sorted_rate)):
    print(sorted_SR[i]['SR'],sorted_SR[i]['Names'])

print(most_runs['Names'],"has scored ",max(tables['Runs']), "as most runs")
print("The highest score of ",max(tables['HS'])," is scored by ",highest_score['Names'])
print(best_average['Names']," has the best average of ",max(tables['Average']))
print(max_balls_faced['Names'], " has faced ",max(tables['BF'])," as maximum number of balls")
print(max_SR['Names']," has the maxmimum strike rate of ",max(tables['SR']))
# print(most_hundreds['Names']," has ",max(tables['100s'])," hundreds as maximum hundreds.")
print(most_fours['Names'], " has hit ",max(tables['Fours'])," fours as maximum fours so far.")
print(most_sixes['Names'], " has hit ",max(tables['Sixes'])," sixes as maximum sixes so far.")