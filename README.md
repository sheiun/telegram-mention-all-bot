# Metion All Members Bot (MAMBot)

> A Telegram Bot implemented fetch all users automatically in the group and replace the keywords like `@all` to tag all users like `@sheiun @tom ...`.

## What problem we solved?

> Since there is no telegram api for fetching all users there is only `chat.get_administrators` and it cannot achieve our aim, tagging all users, so we propose a method to use `telethon` to login as a user and get all users' id via `GetParticipantsRequest` and retreive correspond user via `chat.get_member(user_id)`.

## Step to build your own `Metion All Memebers Bot`

> Or you can use our bot [Metion All Members Bot](https://t.me/MentionAllMembersBot)

1. Register a bot via [Bot Father](https://t.me/botfather)
2. Add the bot into your group and give it 'Invite users via link' and 'Delete messages' permissions
3. Register api key from <https://my.telegram.org/auth>
4. Edit your `config.json` like [config.example.json](config.example.json) to fill bot token, api id and api hash
5. Run `python dump_users.py` to dump users in a group via invite link
6. Run `python bot.py`
