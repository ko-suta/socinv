from otree.api import *
import random

doc = """
This is a 3-period investment game with 2 players.
"""


class Constants(BaseConstants):
    name_in_url = 'SRI_new'
    players_per_group = 2
    num_rounds = 3
    instructions_general = 'SRI_new/InstructionsGeneral.html'
    instructions_private = 'SRI_new/InstructionsPrivate.html'
    instructions_social = 'SRI_new/InstructionsSocial.html'
    # """Amount allocated to each player"""
    endowment = cu(100)
    social_multiplier = 2


class Subsession(BaseSubsession):

    pass


class Player(BasePlayer):
    private_multiplier = models.FloatField()
    past_private_multiplier = models.FloatField()
    past_private_contribution = models.CurrencyField()
    private_share = models.CurrencyField()
    private_contribution = models.CurrencyField(
        min=0,
        doc="""The amount of private contribution by the player""",
        label="How much will you contribute to the Private Project?",
    )
    social_contribution = models.CurrencyField(
        min=0,
        doc="""The amount of social contribution by the player""",
        label="How much will you contribute to the Social Project?",
    )
    total_contribution = models.CurrencyField()
    social_endowment = models.CurrencyField()
    past_payoff = models.CurrencyField()
    future_payoff = models.CurrencyField()
    social_payoff = models.CurrencyField()
    private_payoff = models.CurrencyField()
    money_kept = models.CurrencyField()


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    social_share = models.CurrencyField()


# FUNCTIONS
def private_contribution_max(player):
    if player.round_number == 1:
        return Constants.endowment
    else:
        prev_player = player.in_round(player.round_number - 1)
        player.past_payoff = prev_player.payoff
        return player.past_payoff


def social_contribution_max(player):
    if player.round_number == 1:
        player.social_endowment = Constants.endowment - player.private_contribution
        return player.social_endowment
    else:
        player.social_endowment = player.past_payoff - player.private_contribution
        return player.social_endowment


def set_payoffs(group: Group):
    player_list = group.get_players()
    group.total_contribution = sum([p.social_contribution for p in player_list])
    group.social_share = group.total_contribution * Constants.social_multiplier / Constants.players_per_group

    for p in player_list:
        p.private_multiplier = round(random.uniform(0.5, 5), 2)
        print('private multiplier is', p.private_multiplier)
        p.private_share = (
            round((p.private_contribution * p.private_multiplier), 2)
        )

        p.social_payoff = group.social_share - p.social_contribution
        p.total_contribution = p.social_contribution + p.private_contribution

        if p.round_number == 1:
            p.private_payoff = 0
            p.money_kept = Constants.endowment - p.total_contribution
        else:
            prev_player2 = p.in_round(p.round_number - 1)
            p.past_private_multiplier = prev_player2.private_multiplier  # created for html-invoking solely
            p.past_private_contribution = prev_player2.private_contribution  # created for html-invoking solely
            p.private_payoff = prev_player2.private_share - p.private_contribution
            p.money_kept = p.past_payoff - p.total_contribution

        p.payoff = p.social_payoff + p.private_payoff + p.money_kept
        p.future_payoff = p.social_payoff + p.private_payoff + p.money_kept + p.private_share  # for html solely


# PAGES
class Introduction(Page):
    """Description of the game: How to play and returns expected"""

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ContributePrivate(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['private_contribution']


class ContributeSocial(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['social_contribution']


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for other participants to contribute."
    after_all_players_arrive = set_payoffs


class Results(Page):
    """Players payoff: How much each has earned"""


class CombinedResults(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


page_sequence = [Introduction, ContributePrivate, ContributeSocial, ResultsWaitPage, Results, CombinedResults]
