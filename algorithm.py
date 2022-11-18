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


input_file = "data/players_data_November_18_OK.csv"

# comma delimited is the default
all_data = pd.read_csv(input_file, header = 0)
# imp = SimpleImputer(nan, strategy='constant', fill_value=-50)

# remove the non-numeric columns
# all_data = all_data._get_numeric_data()

# put the numeric column names in a python list
# numeric_headers = list(all_data.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
numpy_array = all_data.as_matrix()


x_train = all_data[['Id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus4', 'J_minus3', 'J_minus2']].values
y_train = all_data['J_minus1'].values

x_test = all_data[['Id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus3', 'J_minus2', 'J_minus1']].values
y_test = all_data['J_actual'].values


regressor = LinearRegression() 
regressor.fit(x_train, y_train) #Entrena el algoritmo

print('---------------------------------------')
#Para obtener el intercepto:
print(regressor.intercept_)

print('---------------------------------------')
#Para obtener la pendiente
print(regressor.coef_)

y_pred = regressor.predict(x_test)

df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
print('RESULT---------')
print(df)

# plt.figure(figsize=(15,10))
# plt.tight_layout()
# seabornInstance.distplot(all_data['Goals_OR_saved_penalties'])

# all_data.plot(x='Goals_OR_saved_penalties', y='Assists', style='o') 
# plt.title('Goals_OR_saved_penalties vs Assists') 
# plt.xlabel('Goals_OR_saved_penalties') 
# plt.ylabel('Assists') 
# plt.show()

