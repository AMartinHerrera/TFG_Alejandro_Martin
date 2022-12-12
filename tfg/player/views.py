from django.shortcuts import render
import sqlite3
from .forms import PlayerInputForm

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline


# Create your views here.

# This home function just redirects to home.html template, the main template 
def home(request):
    """View function for home page of site."""

    context = {
        
    }

    return render(request, 'home.html', context=context)


def input(request):

    description=""

    # Request with the form created to insert the query
    if request.method == 'POST':
        form = PlayerInputForm(request.POST)

    else:
        form = PlayerInputForm()

    # Create the context with the information and render the template with it
    context = {
        'form': form,
        # 'description': description,
    }

    return render(request, 'input.html', context)



def output(request):

    error_case = ""

    # No error case situation 
    if request.method == 'POST':
        form = PlayerInputForm(request.POST)
        if form.is_valid():
            list_player_form_res = []
            player_form_res = form.cleaned_data['player']
            list_player_form_res = player_form_res.split(',')

            input_file = "data/players_data_November_18_OK.csv"

            all_data = pd.read_csv(input_file, header = 0)

            x_train = all_data[['Player_id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus4', 'J_minus3', 'J_minus2']].values
            y_train = all_data['J_minus1'].values

            x_test = all_data[['Player_id', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_percentage', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Current_price', 'Max_price', 'Min_price', 'Average_points_last_5_games', 'J_minus3', 'J_minus2', 'J_minus1']].values
            y_test = all_data['J_actual'].values

            regressor = make_pipeline(StandardScaler(), LogisticRegression(penalty='l2', solver='newton-cg', max_iter=1000, multi_class='auto'))
                
            regressor.fit(x_train, y_train) #Entrena el algoritmo

            y_pred = regressor.predict(x_test)

            df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()}).round().astype(object)

            score_predictions = pd.DataFrame({'score':y_pred.flatten()}).to_numpy()
            players_name = all_data['Name'].to_numpy()

            player_name_and_it_predicted_score_dict = {
            players_name[0]: round(float(score_predictions[0]))
            }

            for i in range(1, len(df)):
                player_name_and_it_predicted_score_dict.update({players_name[i]: round(float(score_predictions[i]))})

            sorted_dict = sorted(player_name_and_it_predicted_score_dict.items(), key=lambda x:x[1], reverse=True)
            sorted_player_name_and_it_predicted_score_dict = {k: v for k, v in sorted_dict}

            to_be_printed_players_dict = sorted_player_name_and_it_predicted_score_dict.copy()
            to_be_printed_players_dict.clear()

            for p in list_player_form_res:
                for key, value in sorted_player_name_and_it_predicted_score_dict.items():
                    if key == p:
                        to_be_printed_players_dict[key] = value

            sorted_dict_aux = sorted(to_be_printed_players_dict.items(), key=lambda x:x[1], reverse=True)
            sorted_to_be_printed_players_dict = {k: v for k, v in sorted_dict_aux}

            DEF_sorted_to_be_printed_players_dict = sorted_to_be_printed_players_dict.copy()

            for key, value in sorted_to_be_printed_players_dict.items():
                if value == -50:
                    DEF_sorted_to_be_printed_players_dict[key] = '-'

            context = {'dict': DEF_sorted_to_be_printed_players_dict}

            return render(request, 'output.html', context)
    else:
        form = PlayerInputForm()

