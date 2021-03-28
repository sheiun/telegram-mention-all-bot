from __future__ import annotations

from asyncio import get_event_loop, new_event_loop, set_event_loop

import telethon.sync as _
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import InviteHashExpiredError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


def get_chatid_usersid(client, links: list[str]) -> dict[int, list[int]]:
    chatid_users = {}
    for link in links:
        try:
            group = client.get_entity(link)
        except InviteHashExpiredError:
            continue
        participants = client(
            GetParticipantsRequest(
                group,
                filter=ChannelParticipantsSearch(""),
                offset=0,
                limit=int(1e5),
                hash=0,
            )
        )
        usersid = []
        for user in participants.users:
            if not user.bot:
                usersid.append(user.id)
        group_id = int(f"-100{group.id}")
        chatid_users[group_id] = usersid
    return chatid_users


def get_client(config) -> TelegramClient:
    try:
        get_event_loop()
    except RuntimeError:
        set_event_loop(new_event_loop())
    return TelegramClient(
        session="_", api_id=config["api_id"], api_hash=config["api_hash"],
    ).start()

