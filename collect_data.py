import csv

def cook_soup_from_url(url, parser='lxml', sleep_time=0, timeout=50):
  """Uses requests to retreive webpage and returns a BeautifulSoup made using lxml parser."""
  import requests
  from time import sleep
  from bs4 import BeautifulSoup
  from fake_useragent import UserAgent
  
  sleep(sleep_time)

  ua = UserAgent()
  header = {'user-agent':ua.chrome}
  # print(url)
  response = requests.get(url, timeout=timeout, headers=header)
  
  # check status of request
  if response.status_code != 200:
    raise Exception(f'Error: Status_code !=200.\n status_code={response.status_code}')

  c = response.content
  # feed content into a beautiful soup using lxml
  soup = BeautifulSoup(c,'lxml')
  return soup

def get_all_links(soup):
  """Finds all links inside of soup that have the attributes(attr_kwds),which will be used in soup.findAll(attrs=attr_kwds).
  Returns a list of links.
  tag_type = 'a' or 'href'"""
  all_a_tags = soup.findAll("a") 
  link_list = []
  for link in all_a_tags:
    test_link = link.get('href')
    link_list.append(test_link)
  return link_list



main_url="https://www.comuniate.com/"
all_links = get_all_links(cook_soup_from_url(main_url))

teams_main_links=[]
teams_squad_links_with_duplicates=[]
all_players_list_with_duplicates=[]
all_players_list=[]

for l in all_links:
  if l.startswith('https://www.comuniate.com/equipos'):
    teams_main_links.append(l)

for url in teams_main_links:
  auxiliar_teams_squad_links = get_all_links(cook_soup_from_url(url))

  for t in auxiliar_teams_squad_links:
    if t.startswith('https://www.comuniate.com/plantilla'):
      teams_squad_links_with_duplicates.append(t)

teams_squad_links = list(dict.fromkeys(teams_squad_links_with_duplicates))

for url_team in teams_squad_links:
  auxiliar_team_players_links = get_all_links(cook_soup_from_url(url_team))
  
  for pl in auxiliar_team_players_links:
    if pl.startswith('https://www.comuniate.com/jugadores'):
      all_players_list_with_duplicates.append(pl)

all_players_list = list(dict.fromkeys(all_players_list_with_duplicates))
all_players_list = all_players_list[4:]


# FUNCTION WHICH OBTAINS THE PLAYER ID (FROM THE URL)
def find_player_id(url):
  divided_url = url.split('/')
 
  for sub in divided_url:
    if sub.isdigit():
      id = sub
    else:
      id=-1
      raise ValueError ("ERROR! The id can not be negative")
  return id


# FUNCTION WHICH OBTAINS THE PLAYER NAME
def find_player_name(url):
  soup = cook_soup_from_url(url)
  all_div_names = soup.findAll("div", "col-xs-12") 

  name_list_unfiltered = []
  filtered_name_list = []

  for div_price in all_div_names:
    div_price_aux = div_price.find("strong", "")
    name_list_unfiltered.append(div_price_aux)

  for n in name_list_unfiltered:
    if n != None:
      filtered_name_list.append(n)

  name = filtered_name_list[0]
  return name.text.strip()


# FUNCTION WHICH OBTAINS THE PLAYER POSITION AND THE RANK OUT OF POSITION
def find_player_position_and_positionrank(url):
  soup = cook_soup_from_url(url)
  all_div_position = soup.findAll("div", "col-xs-6") 

  info_list_unfiltered = []

  for div_price in all_div_position:
    info_list_unfiltered.append(div_price.text.strip())
  
  subs = 'POSICION'    
  res = [i for i in info_list_unfiltered if subs in i]
  position = res[0]
  position = position[-2:]

  subs = 'RANK'    
  res = [i for i in info_list_unfiltered if subs in i]
  resAux = res[0]
  divided_res = resAux.split('\n')
  for sub in divided_res:
    if sub.startswith('RANK.'):
      rank = sub

  rank = rank.replace('RANK.', '')
  rank = rank.replace('º', '')

  return position, rank


# FUNCTION WHICH OBTAINS THE PLAYER BOOLEAN OF STARTING ELEVEN
def find_player_currently_starting_eleven(url):
  soup = cook_soup_from_url(url)
  all_div_starting_eleven = soup.findAll("div", "col-xs-6") 

  info_list_unfiltered = []

  for div in all_div_starting_eleven:
    info_list_unfiltered.append(div.text.strip())
  
  subs = '¿Titular?'
  res = [i for i in info_list_unfiltered if subs in i]
  resAux = res[0]
  divided_res_unfiltered = resAux.split()

  yesno_info = divided_res_unfiltered[-1]
  yesno_info = yesno_info.replace('¿Titular?', '')

  if yesno_info == "SI":
    return True
  else:
    return False


# FUNCTION WHICH OBTAINS THE PLAYER ASISTS GOALS/SAVED PENALTIES PENALTYGOALS/CLEAN SHEETS YELLOW CARDS AND RED CARDS
def find_player_asists_goalsORsavedpenalties_penaltygoalsORcleansheets_yellowcards_redcards(url):
  soup = cook_soup_from_url(url)
  all_div_stats = soup.findAll("div", "col-xs-6") 

  info_list_unfiltered = []
  filtered_divided_res =[]

  for div in all_div_stats:
    info_list_unfiltered.append(div.text.strip())
  
  subs = '¿Titular?'
  res = [i for i in info_list_unfiltered if subs in i]
  resAux = res[0]
  divided_res_unfiltered = resAux.split()

  return divided_res_unfiltered[5:10]


# FUNCTION WHICH OBTAINS THE PLAYER ACTUAL MAX AND MIN PRICE
def find_player_price_actual_max_min(url):
  soup = cook_soup_from_url(url)
  all_div_prices = soup.findAll("div", "col-md-4 col-xs-4") 

  price_list_unfiltered = []
  filtered_price = []
  
  for div_price in all_div_prices:
    price_content=div_price.text.strip()
    if price_content.startswith("Pre"):
      price_list_unfiltered.append(price_content)
  
  for pr in price_list_unfiltered:
    filtered_price.append(pr.split(" "))

  actualp=filtered_price[0][2].replace('.', '').replace('€', '')
  maxp=filtered_price[1][2].replace('.', '').replace('€', '')
  minp=filtered_price[2][2].replace('.', '').replace('€', '')

  return actualp, maxp, minp


# FUNCTION WHICH OBTAINS THE PLAYER POINTS ANF THE AVERAGE
def find_player_points_and_points_average(url):
  soup = cook_soup_from_url(url)
  all_div_points = soup.findAll("div", "col-xs-3 cuadro")

  points_pointsaverage = []

  for div in all_div_points:
    div_points_aux = div.find("strong", "")
    points_pointsaverage.append(div_points_aux.text.strip())

  return points_pointsaverage[0], points_pointsaverage[1]


# FUNCTION WHICH OBTAINS THE PLAYER PERCENTAGE OF STARTING ELEVEN IN THE SEASON
def find_player_matches_played_and_percentage_season_starting_eleven(url):
  soup = cook_soup_from_url(url)
  all_div_matches = soup.findAll("div", "col-xs-3 cuadro")

  percentage_starting_eleven = []

  for div in all_div_matches:
    div_percentage_aux = div.find("strong", "")
    percentage_starting_eleven.append(div_percentage_aux.text.strip())
  
  aux = percentage_starting_eleven[3].split("/")
  x = int(aux[0])
  y = int(aux[1])

  percent = (x*100)/y

  return x, ("%.2f"%percent)


def send_post_request(url, json_data):
  import requests
  x = requests.post(url, data = json_data)
  return x.text


# FUNCTION WHICH OBTAINS THE PLAYER 5 LAST PUNTUATIONS AND ITS AVERAGE
def find_player_last_5_punctuations_and_its_average(url):
  post_url_last_punctuations="https://www.comuniate.com/ajax/estadistica_carga_puntos.php"
  post_id_player=find_player_id(url)

  tablahtml_points = send_post_request(post_url_last_punctuations, {"id_jugador":post_id_player, "temporada": "22"})

  last_5_punctuations=[]
  list_def=[]

  tablilla = tablahtml_points.split('<tr style="padding:0px ">')
  spans = tablilla[0]
  spans = spans.split('<tr')

  for i in range(1, len(spans)):
    ej = spans[i]
    e = ej.splitlines()
    list_def.append(e)

  for x in range(0, 5):
    k=list_def[x].pop(6)
    rastreator = k.find('class="puntos')
    if rastreator == -1:
      last_5_punctuations.append('-')
    else:
      puncAux = k.split('>')
      puncAux.append("")
      punt = puncAux[1].replace('</span', '')
      last_5_punctuations.append(punt)

  rend=[]

  for av in last_5_punctuations:
    if av != '-':
      rend.append(int(av))
    else:
      rend.append(0)

  avg = sum(rend)/5

  return last_5_punctuations, ("%.1f"%avg)


header = ['Id', 'Name', 'Position', 'Ranking_position', 'Matches_played', 'Matches_played_%', 'Usually_starting', 'Goals_OR_saved_penalties', 'Penalty_goals_OR_clean_sheets', 'Assists', 'Yellow_cards', 'Red_cards', 'Points', 'Average_points', 'Points_last_5_games', 'Average_points_last_5_games', 'Current_price', 'Max_price', 'Min_price']

f = open('data/players_data_November_08.csv', 'a+')
writer = csv.writer(f)
writer.writerow(header)

for u in all_players_list:

  id = find_player_id(u)
  name = find_player_name(u)
  position, ranking_position = find_player_position_and_positionrank(u)
  matches_played, matches_played_percent = find_player_matches_played_and_percentage_season_starting_eleven(u)
  usually_starting = find_player_currently_starting_eleven(u)
  assists, goals_or_saved_penalties, penalty_goals_or_clean_sheets, yellow_cards, red_cards = find_player_asists_goalsORsavedpenalties_penaltygoalsORcleansheets_yellowcards_redcards(u)
  points, avg_points = find_player_points_and_points_average(u)
  points_last_5_games, avg_las_5_games = find_player_last_5_punctuations_and_its_average(u)
  current_price, max_price, min_price = find_player_price_actual_max_min(u)

  data = [id, name, position, ranking_position, matches_played, matches_played_percent, usually_starting, goals_or_saved_penalties, penalty_goals_or_clean_sheets, assists, yellow_cards, red_cards, points, avg_points, points_last_5_games, avg_las_5_games, current_price, max_price, min_price]
  # data = [id, name, position, ranking_position, matches_played, matches_played_percent, usually_starting, goals_or_saved_penalties, penalty_goals_or_clean_sheets, assists, yellow_cards, red_cards, points, avg_points, current_price, max_price, min_price]

  writer.writerow(data)

f.close()