from os import environ
import sentry_sdk

sentry_sdk.init(
    dsn="https://22e6351ffaa747a196f10d8b48b4aaf2@o4504010287284224.ingest.sentry.io/4504010287284224",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

SESSION_CONFIGS = [
    dict(
        name='SRI_new',
        app_sequence=['consent', 'survey', 'SRI_new', 'payment_info'],
        num_demo_participants=4,
        completionlink='https://app.prolific.co/submissions/complete?cc=CJZCNOVZ',
    ),
]

ROOMS = [
    dict(
        name='SRI',
        display_name='Social investment game',
        participant_label_file='_rooms/sri_1.txt',
        # use_secure_urls=True,
    ),
    dict(
        name='SRI_prolific',
        display_name='SRI prolific',
        # participant_label_file='_rooms/your_study.txt',
        # use_secure_urls=True,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=100.00, doc=""
)


PARTICIPANT_FIELDS = ['consent']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7937348957020'
