from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField(default=str(" "))
    name = models.StringField(label='What is your name?')
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    student_id = models.IntegerField(label='What is your student number?')


# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['name', 'age', 'gender', 'student_id']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.prolific_id = player.participant.label


class Results(Page):
    pass


page_sequence = [Demographics, Results]
