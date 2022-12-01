from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Player (models.Model):
    Player_id = models.IntegerField(_("Player_id"))
    Name = models.CharField(_("Name"), max_length=255)
    Position = models.IntegerField(_("Position"))
    Ranking_position = models.IntegerField(_("Ranking_position"))
    Matches_played = models.IntegerField(_("Matches_played"))
    Matches_played_percentage = models.FloatField(_("Matches_played"))
    Usually_starting = models.IntegerField(_("Usually_starting"))
    Goals_OR_saved_penalties = models.IntegerField(_("Goals_OR_saved_penalties"))
    Penalty_goals_OR_clean_sheets = models.IntegerField(_("Penalty_goals_OR_clean_sheets"))
    Assists = models.IntegerField(_("Assists"))
    Yellow_cards = models.IntegerField(_("Yellow_cards"))
    Red_cards = models.IntegerField(_("Red_cards"))
    Points = models.IntegerField(_("Points"))
    Average_points = models.FloatField(_("Average_points"))
    Current_price = models.BigIntegerField(_("Current_price"))
    Max_price = models.BigIntegerField(_("Max_price"))
    Min_price = models.BigIntegerField(_("Min_price"))
    Average_points_last_5_games = models.FloatField(_("Average_points_last_5_games"))
    J_minus4 = models.IntegerField(_("J_minus4"))
    J_minus3 = models.IntegerField(_("J_minus3"))
    J_minus2 = models.IntegerField(_("J_minus2"))
    J_minus1 = models.IntegerField(_("J_minus1"))
    J_actual = models.IntegerField(_("J_actual"))
