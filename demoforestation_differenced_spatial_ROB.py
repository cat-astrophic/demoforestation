# This script runs expanded econometric models using both old and new data - ROBUST

# Import required modules

import pandas as pd
import numpy as np
import statsmodels.api as stats
from ToTeX import restab

# Reading in the data

data = pd.read_csv('C:/Users/User/Documents/Data/demoforestation_differenced_spatial.csv', encoding = 'cp1252')
W = pd.read_csv('C:/Users/User/Documents/Data/demoforestation_W.csv', header = None)

# Add Urbanization squared to the data for the robustness checks

U = pd.Series(data.Urbanization*data.Urbanization, name = 'Urbanization_2')
data = pd.concat([data, U], axis = 1)

# Create spatially democracy term for neighbors

Dd = np.dot(W,data.Democracy)
D2d = np.dot(W,data.Democracy_2)

# Add these to the data sets

data = pd.concat([data, pd.DataFrame(Dd, columns = ['W*Demo']), pd.DataFrame(D2d, columns = ['W*Demo_2'])], axis = 1)

# Data prep

dXi = data['Democracy']*data['GDP_per_capita']
data = pd.concat([data, pd.DataFrame(dXi, columns = ['D X GDP'])], axis = 1)

df1 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Continent']].dropna()
df2 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Continent']].dropna()
df3 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Tariff_Rate', 'Continent']].dropna()

d1 = pd.get_dummies(df1['Continent'])
d2 = pd.get_dummies(df2['Continent'])
d3 = pd.get_dummies(df3['Continent'])

X1 = stats.add_constant(df1[['W*Demo', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP']])
X2 = stats.add_constant(df2[['W*Demo', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate']])
X3 = stats.add_constant(df3[['W*Demo', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Tariff_Rate']])

X4 = X1.join(d1).drop('Oceania', axis = 1)
X5 = X2.join(d2).drop('Oceania', axis = 1)
X6 = X3.join(d3).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df1['Rate'], df2['Rate'], df3['Rate'], df1['Rate'], df2['Rate'], df3['Rate']]
Xs = [X1, X2, X3, X4, X5, X6]
res_list = []

for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit(cov_type = 'HC1')
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Spatial/Differenced_Model_ROB_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Spatial/restab_differenced_spatial_ROB.txt')

# Create binary indicator for whether or not a nation's neighbors were, on average, more democratic

bi = [1 if (data['W*Demo'][i] > data['Democracy'][i]) else 0 for i in range(len(data))]
data = pd.concat([data, pd.DataFrame(bi, columns = ['W*D>D'])], axis = 1)

# Run second set of regressions with binary indicator

# Data prep

df11 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Continent']].dropna()
df12 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Continent']].dropna()
df13 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Tariff_Rate', 'Continent']].dropna()

d11 = pd.get_dummies(df11['Continent'])
d12 = pd.get_dummies(df12['Continent'])
d13 = pd.get_dummies(df13['Continent'])

X11 = stats.add_constant(df11[['W*D>D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP']])
X12 = stats.add_constant(df12[['W*D>D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate']])
X13 = stats.add_constant(df13[['W*D>D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Tariff_Rate']])

X11 = X11.join(d11).drop('Oceania', axis = 1)
X12 = X12.join(d12).drop('Oceania', axis = 1)
X13 = X13.join(d13).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df11['Rate'], df12['Rate'], df13['Rate']]
Xs = [X11, X12, X13]
res_list = []

for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit(cov_type = 'HC1')
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Spatial/Differenced_Model_Binary_ROB_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Spatial/restab_differenced_binary_ROB.txt')

# Create nonbinary indicator for whether or not a nation's neighbors were, on average, more democratic

nbi = [data['W*Demo'][i] - data['Democracy'][i] for i in range(len(data))]
data = pd.concat([data, pd.DataFrame(nbi, columns = ['W*D-D'])], axis = 1)

# Run third set of regressions with nonbinary indicator

# Data prep

df21 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent']].dropna()
df22 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent']].dropna()
df23 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Tariff_Rate', 'Continent']].dropna()

d21 = pd.get_dummies(df21['Continent'])
d22 = pd.get_dummies(df22['Continent'])
d23 = pd.get_dummies(df23['Continent'])

X21 = stats.add_constant(df21[['W*D-D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land']])
X22 = stats.add_constant(df22[['W*D-D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate']])
X23 = stats.add_constant(df23[['W*D-D', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Tariff_Rate']])

X21 = X21.join(d21).drop('Oceania', axis = 1)
X22 = X22.join(d22).drop('Oceania', axis = 1)
X23 = X23.join(d23).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df21['Rate'], df22['Rate'], df23['Rate']]
Xs = [X21, X22, X23]
res_list = []
for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit(cov_type = 'HC1')
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Spatial/Differenced_Model_NonBinary_ROB_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Spatial/restab_differenced_nonbinary_ROB.txt')

