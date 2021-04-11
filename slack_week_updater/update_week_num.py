#!/usr/bin/env python3
"""
This script updates week number in Slack workspace.

This can be deployed using simple cron job or AWS CloudWatch + Lambda.
"""
import slack
import datetime
import config
from slack.errors import SlackApiError



def update_channel_description(client, channel: str, new_week: int):
    """
        Update slack channel's description.

        Notifies author of script if there's issue with running the script.
    """

    current_topic = get_current_topic(client, channel)

    if f"[week {new_week}]" in current_topic.lower():
        print("Same topic already set, ignoring")
        return

    topic = f"[Week {new_week}] |  https://world-class.github.io/ | https://github.com/world-class/notes"

    try:
        client.conversations_setTopic(channel=channel, topic=topic)
    except SlackApiError:
        client.chat_postMessage(
            channel=config.slack_my_user_id,
            text=f":robot: Could not set following topic {channel}: \n {topic}",
        )


def get_current_topic(client, channel: str) -> str:
    try:
        channel_info = client.conversations_info(channel=channel)
        return channel_info["channel"]["topic"]["value"] or ""
    except Exception as e:
        # this is hacky script, don't expect too much!
        return ""


def get_next_week() -> int:
    """
        Get new week number.
    """
    start_date = config.start_date
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
            new_week
        )
    else:
        print("Invalid week")
