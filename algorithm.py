import numpy as np
import pandas as pd

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# from sklearn import metrics%matplotlib inline

from statistics import mean, stdev
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import zero_one_loss
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction import DictVectorizer



# Duda sobre points_last_5_games en numerical_attributes (es una lista)

categorical_attributes = ['Name', 'Position', 'Usually_starting']
numerical_attributes = ['Id', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Points_last_5_games', 'Average_points_last_5_games', 'Current_price', 'Max_price', 'Min_price']

input_file = "data/players_data_November_03_OK.csv"

# comma delimited is the default
all_data = pd.read_csv(input_file, header = 0)
# imp = SimpleImputer(nan, strategy='constant', fill_value=-50)

# remove the non-numeric columns
# all_data = all_data._get_numeric_data()

# put the numeric column names in a python list
# numeric_headers = list(all_data.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
numpy_array = all_data.as_matrix()

print(numpy_array[0])
print('---------------------------------------')
# print(all_data.describe)
print('---------------------------------------')

# print(all_data.iloc[:, 1])

last5 = all_data['Points_last_5_games']


# OJO! SIN POINTS Y SIN LAST 5 PUNTUACIONES 
x = all_data[['Id', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Average_points', 'Average_points_last_5_games', 'Current_price', 'Max_price', 'Min_price']].values
# print(x)

y = all_data['Points'].values

# df1 = all_data.loc[:, all_data.columns != 'Id' and all_data.columns != 'Name']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.001, random_state=0)


print('XTRAINN')
# print(X_train)
print('---------------------------------------')
print('yTESSTTT')
# print(y_test)
print('---------------------------------------')

regressor = LinearRegression() 
regressor.fit(X_train, y_train) #Entrena el algoritmo

#Para obtener el intercepto:
print(regressor.intercept_)
#Para obtener la pendiente
print(regressor.coef_)

y_pred = regressor.predict(X_test)

df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
print('RESSSS---------')
print(df)

# plt.figure(figsize=(15,10))
# plt.tight_layout()
# seabornInstance.distplot(all_data['Goals_OR_saved_penalties'])

# all_data.plot(x='Goals_OR_saved_penalties', y='Assists', style='o') 
# plt.title('Goals_OR_saved_penalties vs Assists') 
# plt.xlabel('Goals_OR_saved_penalties') 
# plt.ylabel('Assists') 
# plt.show()

