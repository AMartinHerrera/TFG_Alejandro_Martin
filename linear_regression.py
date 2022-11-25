import pandas as pd
from sklearn.linear_model import LinearRegression
from statistics import mean, stdev


input_file = "data/players_data_November_18_OK.csv"

# I WILL EXECUTE AT FIRST WITH ALL DATA, NO FILTER

all_data = pd.read_csv(input_file, header = 0)

# imp = SimpleImputer(nan, strategy='constant', fill_value=-50)

x_train = all_data[['Id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus4', 'J_minus3', 'J_minus2']].values
y_train = all_data['J_minus1'].values

x_test = all_data[['Id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus3', 'J_minus2', 'J_minus1']].values
y_test = all_data['J_actual'].values


regressor = LinearRegression() 
regressor.fit(x_train, y_train) #Entrena el algoritmo

y_pred = regressor.predict(x_test)

df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()}).round().astype(object)

error=[]

for x, y in zip(y_test.flatten(), y_pred.flatten()):
    y = round(y)
    error.append(abs(y-x))

errorTotal = (sum(error)/(len(df)))

accuracy=100-errorTotal
print(f'The results have been written in the results folder/ -- The Linear regression accuracy is (NO FILTERED DATA)--> %.4f'%accuracy + ' %')

f = open ('results/linear_regression_with_NO_data_filter_ROUND.data','a+')
f.write(f'Linear regression accuracy is --> %.4f'%accuracy + ' %')
f.write('\n\n')
f.write(str(df.to_string()))

f.close()


# --------------------------------------------------------------------------------------------
# THIS TIME I WILL EXECUTE AT FIRST WITH DATA FILTERED (NO TRAINING WITH 0.0 POINT AVERAGE PLAYERS)


all_data = pd.read_csv(input_file, header = 0)

# imp = SimpleImputer(nan, strategy='constant', fill_value=-50)

to_delete_element_indexes=[]
i=0
for index, row in all_data.iterrows():
    if row.at["Average_points_last_5_games"] == 0.0:
        to_delete_element_indexes.append(i)
    i+=1

all_data=all_data.drop(to_delete_element_indexes)

x_train = all_data[['Id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus4', 'J_minus3', 'J_minus2']].values
y_train = all_data['J_minus1'].values

x_test = all_data[['Id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus3', 'J_minus2', 'J_minus1']].values
y_test = all_data['J_actual'].values


regressor = LinearRegression() 
regressor.fit(x_train, y_train) #Entrena el algoritmo

y_pred = regressor.predict(x_test)

df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()}).round().astype(object)

error=[]

for x, y in zip(y_test.flatten(), y_pred.flatten()):
    y = round(y)
    error.append(abs(y-x))

errorTotal = (sum(error)/(len(df)))

accuracy=100-errorTotal
print(f'The results have been written in the results folder/ -- The Linear regression accuracy is (FILTERED DATA)--> %.4f'%accuracy + ' %')

f = open ('results/linear_regression_with_data_filter_ROUND.data','a+')
f.write(f'Linear regression accuracy is --> %.4f'%accuracy + ' %')
f.write('\n\n')
f.write(str(df.to_string()))

f.close()
