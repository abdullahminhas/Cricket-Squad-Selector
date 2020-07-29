import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from math import sqrt
import os
from test import app

def returnAustraliaBowlers():
    #reading the csv file :
    df = pd.read_csv(os.path.join(app.root_path, 'static',"Bowlers Dataset (Australia).csv"))


    #creating a new dataframe :
    X = pd.DataFrame({
    #
              'Wickets' : df['Wickets'],
              'Serial' : df['TRuns']
    })

    #Applying KMeans :
    Kmeans = KMeans(n_clusters = 4,  random_state=0)
    Kmeans.fit(X)

    labels = Kmeans.predict(X)
    centroids = Kmeans.cluster_centers_


    #Plotting :
    #fig = plt.figure(figsize=(10,10))
    #colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'y'}
    #colors = map(lambda x: colmap[x+ 1], labels)
    #colors1 = list(colors)

    #plt.scatter(X['Wickets'],X['Serial'], color=colors1, alpha=0.5, edgecolor = 'k')
    #for idx, centroid in enumerate(centroids):
    #    plt.scatter(*centroid, color=colmap[idx+1])
    #plt.xlim(-250,700)
    #plt.ylim(0,700)
    #plt.show()


    #concatination of labels and result :
    labelling = labels.tolist()
    #print("")
    #print("")
    #print("")
    #print("")
    #print(labelling)
    X['labelled'] = labelling
    #print("")
    #print("")
    #print("")
    #print("")
    #print(X)


    #Creating new dataframe containg 3 parameters :
    Y = pd.DataFrame({
            'Total Runs' : df['TRuns'],
            'Total Ball Faced' : df['TBF'],
            'labelled' : labels
    })

    #print("")
    #print("")


    t = 0
    c = 0
    array = []
    result = []
    for t in range(0,len(Y)):
       if Y.iloc[t, 2] == 0:
            c = c + 1
            dist = sqrt((0-Y.iloc[t, 0])**2 + (0-Y.iloc[t, 1])**2)
            array.append(dist)
            #print(df.iloc[t, 0],"    (Bowler) ",  )
            result.append(df.iloc[t, 0])
            if len(result) == 6:
                break
    #print("Total Players : ", c)
    return result












































































































































































































    #
    #
    #
    #
    #
    #s = int(array[0])
    #t = 0
    #for e in array:
    #    now = int(array[t])
    #    if s >= now:
    #        s = now
    #    t = t+1
    #print("Smallest distance : ", s)
    #
    #b = int(array[0])
    #t = 0
    #for e in array:
    #    now = int(array[t])
    #    if b <= now:
    #        b = now
    #    t = t+1
    #print("Biggest distance : ", b)
    #
    #distance_measure = (s + b)/ c
    #print("Average distance : ", distance_measure)
    #
    #
