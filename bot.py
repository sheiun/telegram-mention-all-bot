from json import dump, load

from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

from lib import get_chatid_usersid, get_client

config = load(open("config.json"))
chatid_usersid: dict[str, list[int]] = load(open("chatid_usersid.json"))


def tag_user(user, parse_mode: str = ParseMode.MARKDOWN) -> str:
    if parse_mode == ParseMode.MARKDOWN:
        return (
            f"[{user.first_name or ''} {user.last_name or ''}](tg://user?id={user.id})"
        )
    if parse_mode == ParseMode.HTML:
        return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    raise NotImplementedError(parse_mode + " is not supported!")


def tag_user_empty(user, parse_mode: str = ParseMode.MARKDOWN) -> str:
    if parse_mode == ParseMode.MARKDOWN:
        return f"[\u200b](tg://user?id={user.id})"
    if parse_mode == ParseMode.HTML:
        return f"<a href='tg://user?id={user.id}'>\u200b</a>"
    raise NotImplementedError(parse_mode + " is not supported!")


def update_chatid_usersid(chat_id: int, link: str):
    client = get_client(config)
    usersid = get_chatid_usersid(client, [link])[chat_id]
    chatid_usersid[str(chat_id)] = usersid
    dump(chatid_usersid, open("chatid_usersid.json", "w"))


def mention_all(update: Update, context: CallbackContext) -> None:
    if not update.message:
        return
    if any(filter(lambda x: x in update.message.text, config["keywords"])):
        chat = update.message.chat
        global chatid_usersid
        if str(chat.id) not in chatid_usersid:
            try:
                link = chat.export_invite_link()
            except BadRequest:
                update.message.reply_text(
                    "Users are not recorded! Please promote the bot as an admin and give it permission 'Invite users via link' and 'Delete messages'!"
                )
                return
            update_chatid_usersid(chat.id, link)
        users = []
        for userid in chatid_usersid[str(chat.id)]:
            try:
                user = chat.get_member(userid).user
                users.append(user)
            except BadRequest:
                pass
        tag_text = ""
        for user in users:
            if user == update.message.from_user:
                continue
            tag_text += tag_user_empty(user)
        try:
            update.message.delete()
            context.bot.send_message(
                chat.id,
                text=f"{tag_user(update.message.from_user)}: {update.message.text}{tag_text}",
                parse_mode=ParseMode.MARKDOWN,
            )
        except BadRequest:
            update.message.reply_text(
                f"通知了其他 {len(users)} 個人！" + tag_text.rstrip(),
                parse_mode=ParseMode.MARKDOWN,
            )


def main() -> None:
    """Start the bot."""
    c = get_client(config)
    c.disconnect()

    updater = Updater(config["token"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        MessageHandler(
            Filters.chat_type.groups & Filters.text & ~Filters.command, mention_all
        )
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
