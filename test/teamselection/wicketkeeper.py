
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def return_wicketkeeper():
    return "Kamran Akmal","Sarfaraz Ahmed"

'''
df = pd.read_excel("Wicket Keeper Dataset.xlsx")


Player_Name = ['Kamran Akmal', 'Sarfaraz Ahmed', 'Umar Akmal', 'Muhammad Rizwan', 'Muhammad Salman', 'Yonus Khan', 'Adnan Akmal', 'Zulqarnain Haider']
ypos = np.arange(len(Player_Name))
Total_Matches = df['TotalMatches']
Total_Stampings = df['TotalStamping']
Total_Catches = df['TotalCatches']
Total_Run_Outs = df['TotalRunOut']


fig = plt.figure(figsize=(12,12))
plt.ylabel("Total = (Matches, Stampings, Catches, Run Outs)", fontsize=20)
plt.xlabel("Players Names", fontsize=20)
plt.title("Wicket Keeper Bar Chart", fontsize=20)
plt.xticks(ypos, Player_Name, fontsize=7)
plt.bar(ypos-.4, Total_Matches, width=.2, label="Total Matches")
plt.bar(ypos-.2, Total_Stampings, width=.2, label="Total Stampings")
plt.bar(ypos, Total_Catches, width=.2, label="TotalCatches")
plt.bar(ypos+.2, Total_Run_Outs, width=.2, label="TotalRunOut")
plt.legend()

print("Kamran Akmal")
print("Sarfaraz Ahmed")
'''
