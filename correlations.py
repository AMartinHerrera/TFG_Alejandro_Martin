import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import top_k_accuracy_score
from statistics import mean, stdev
from scipy import stats


input_file = "data/players_data_November_18_OK.csv"

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

pearson = stats.pearsonr(y_pred, y_test)

spearmanr = stats.spearmanr(y_pred, y_test)

kendalltau = stats.kendalltau(y_pred, y_test)

score_predictions = pd.DataFrame({'score':y_pred.flatten()}).to_numpy()
players_name = all_data['Name'].to_numpy()


player_name_and_it_predicted_score_dict = {
  players_name[0]: round(float(score_predictions[0]))
}

for i in range(1, len(df)):
    player_name_and_it_predicted_score_dict.update({players_name[i]: round(float(score_predictions[i]))})

sorted_dict = sorted(player_name_and_it_predicted_score_dict.items(), key=lambda x:x[1], reverse=True)
sorted_player_name_and_it_predicted_score_dict = {k: v for k, v in sorted_dict}


f = open ('results/correlations_and_ranking_linear_regression.data','a+')
f.write(f'Pearson correlation coefficient is --> %.4f'%pearson[0])
f.write('\n')
f.write(f'Spearman correlation coefficient is --> %.4f'%spearmanr[0])
f.write('\n')
f.write(f'Kendall correlation coefficient is --> %.4f'%kendalltau[0])

f.write('\n\n')
f.write(f'PLAYERS RANKING (AND ITS SCORE) ACCORDING TO LINEAR REGRESSION: ')
f.write('\n')
f.write('\n'.join("{}: {}".format(k, v) for k, v in sorted_player_name_and_it_predicted_score_dict.items()))
f.close()

print(f'The results have been written in the results folder/ ')
