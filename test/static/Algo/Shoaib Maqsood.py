import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [7.0, 7.0]


df = pd.read_excel("Dataset for Linear Regression.xlsx")
print(df)

#collecting X and Y

X = df['Shoaib Maqsood_BF']
Y = df['Shoaib Maqsood_R']

#Mean of X and Y

mean_x = np.mean(X)
mean_y = np.mean(Y)

#Total number of values

m = len(X)
#using the formula to calculate b1 and b2

numer = 0
denom = 0
for i in range(m):
    numer += (X[i] - mean_x) * (Y[i] - mean_y)
    denom += (X[i] - mean_x) ** 2
b1 = numer / denom
b0 = mean_y - (b1 * mean_x)

#print coefficient
print("Coefficients :")
print(b1, b0)    

#plotting values and regression line :

max_x = np.max(X) +100
min_x = np.min(X) -100

#calculating line values X and Y
x = np.linspace(min_x, max_x)
y = b0 + b1 * x

#plotting line
plt.plot(x, y, color = '#58b970', label = 'Regression line')
#plotting scatter points
plt.scatter(X, Y, c='#ef5423', label = 'Scatter plot')


plt.xlabel('Shoaib Maqsood_BF')
plt.ylabel('Shoaib Maqsood_R') 
plt.legend()
plt.show()


#finding values:
m = len(X)
ss_t = 0
ss_r = 0
for i in range(m):
    y_pred = b0 + b1 * X[i]
    ss_t += (Y[i] - mean_y) ** 2 
    ss_r += (Y[i] - y_pred) ** 2
    
r2 = (1 - (ss_r/ss_t))  
print("How good :", r2)

# predicting runs:

from sklearn import linear_model


df = pd.read_excel("Dataset for Linear Regression.xlsx")
#print(df)

reg = linear_model.LinearRegression()
reg.fit(df[['Shoaib Maqsood_BF','Shoaib Maqsood_4','Shoaib Maqsood_6']],df['Shoaib Maqsood_R'])
c=reg.coef_
print("coefficient =", c)
intercept=reg.intercept_
print("intercept =", intercept)
output=reg.predict([[100,5,5]])
print(output)   

weight =r2 * output
print("weight :", weight)
           
           
