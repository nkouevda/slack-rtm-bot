# slack-rtm-bot

[Slack](https://slack.com/) [RTM](https://api.slack.com/rtm) bot.

## Setup

    git clone https://github.com/nkouevda/slack-rtm-bot.git
    cd slack-rtm-bot
    virtualenv ~/.virtualenvs/slack-rtm-bot
    source ~/.virtualenvs/slack-rtm-bot/bin/activate
    pip install -r requirements.txt
    cp bot/settings{_example,}.py
    # Add API token to bot/settings.py

## Usage

    python bot/bot.py
