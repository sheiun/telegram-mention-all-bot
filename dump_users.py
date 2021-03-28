from json import dump, load
from typing import Any

from lib import get_chatid_usersid, get_client


def dump_users(client, config: dict[str, Any]):
    try:
        chatid_usersid = load(open("chatid_usersid.json"))
    except:
        chatid_usersid = {}
        new_chatid_usersid = get_chatid_usersid(client, config["links"])
        dump({**chatid_usersid, **new_chatid_usersid}, open("chatid_usersid.json", "w"))


if __name__ == "__main__":
    config = load(open("config.json"))
    client = get_client(config)
    dump_users(client, config)
