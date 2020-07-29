
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Converted into a function
def return_captain():
    return "Misbah-ul-Haq"

'''
df = pd.read_excel("Captains Dataset.xlsx")

Player_Name = ['Shoaib Malik', 'Misbah-ul-Haq', 'Shahid Afridi', 'Azhar Ali', 'Sarfaraz Ahmed', 'Muhammad Hafeez', 'Imad Wasim']
ypos = np.arange(len(Player_Name))
WinM = df['WinMatch']
LostM = df['LostMatch']
Total_50 = df['T(50)']
Total_100 = df['T(100)']


fig = plt.figure(figsize=(12,12))
plt.ylabel("Total = (Win Matches, Lost Matches, Total 50's, Total 100's)", fontsize=20)
plt.xlabel("Players Names", fontsize=20)
plt.title("Captains Bar Chart", fontsize=40)
plt.xticks(ypos, Player_Name, fontsize=9)
plt.bar(ypos-.4, WinM, width=.2, label="WinMatch")
plt.bar(ypos-.2, LostM, width=.2, label="LostMatch")
plt.bar(ypos, Total_50, width=.2, label="T(50)")
plt.bar(ypos+.2, Total_100, width=.2, label="T(100)")
plt.legend()

print("Misbah-ul-Haq")
'''
