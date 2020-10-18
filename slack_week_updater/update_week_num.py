#!/usr/bin/env python3
"""
This script updates week number in Slack workspace.

This can be deployed using simple cron job or AWS CloudWatch + Lambda.
Triggered every Sunday 6 PM IST.
"""
import slack
import datetime
import config
from slack.errors import SlackApiError


def update_channel_description(client, channel: str, topic: str):
    """
        Update slack channel's description.

        Notifies author of script if there's issue with running the script.
    """

    try:
        client.conversations_setTopic(channel=channel, topic=topic)
    except SlackApiError:
        client.chat_postMessage(
            channel=config.slack_my_user_id,
            text=f":robot: Could not set following topic {channel}: \n {topic}",
        )


def get_next_week() -> int:
    """
        Get new week number.
    """
    start_date = datetime.date(2020, 10, 12)
    today = datetime.date.today()
    week = round((today - start_date).days / 7) + 1
    return week


if __name__ == "__main__":
    client = slack.WebClient(config.slack_user_token)

    new_week = get_next_week()

    if 1 <= new_week <= 22:
        update_channel_description(
            client,
            config.slack_general_channel_id,
            f"[Week {new_week}] |  https://world-class.github.io/ | https://github.com/world-class/notes",
        )
    else:
        print("Invalid week")
