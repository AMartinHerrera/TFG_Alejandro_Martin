import csv
import sqlite3

file = open('players_data_November_18_OK_copy.csv')

data = csv.reader(file, delimiter=';')
lista = list(data)

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

values = "VALUES("
def_values = ''
def_list = []

splited = []
list_splited = []

for lis in lista:
    for li in lis:
        splited = li.split(',')
        splited[1] = "'" + splited[1] + "'"
        list_splited.append(splited)

list_aux = []

cad = "['"
cad_def = ''

for elems in list_splited:
    for e in elems:
        cad += str(e)
        cad += ','
    cad += "']"
    cad_def = cad.replace(",']", "")
    list_aux.append(cad_def)
    cad=''
    cad_def=''


for li in list_aux:
    
    aux = li.split(",")
    for l in aux:
        values+=str(l)
        values+=','
    values += ');'

    def_values = values.replace(",);", ");")
    values="VALUES("
    def_list.append(def_values)
    def_values=''

raws=[]

main_raw = """
INSERT INTO player_player (Player_id, Name, Position, Ranking_position, Matches_played, Matches_played_percentage, Usually_starting, Goals_OR_saved_penalties, Penalty_goals_OR_clean_sheets, Assists, Yellow_cards, Red_cards, Points, Average_points, Current_price, Max_price, Min_price, Average_points_last_5_games, J_minus4, J_minus3, J_minus2, J_minus1, J_actual) 
    """

for v in def_list:
    raw = main_raw + v
    raws.append(raw)

for r in raws:
    try:
        print(r)
        # cursor.execute(r)
    except (Exception) as error:
        print("ERROR WHILE LOADING DATA INTO SQLITE", error)

connection.commit()
connection.close()


# # f = open ('RAWS.data','a+')
# # f.write(str(raws))

# with open('RAWS.data') as f:
#     lines = f.read()
# # print(lines)
# # f.close()

# cursor.execute(lines)
