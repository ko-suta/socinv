from otree.api import *

doc = """
This is a consent form before playing a "Social Investment" game.
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(widget=widgets.CheckboxInput,
                                  initial=False
                                  )


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.consent = player.consent

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if not player.consent:
            return upcoming_apps[-1]


page_sequence = [Consent]
