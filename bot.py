import bot_functions as bot
import time
import search_card as mtg

def main():
    last_update_id = None

    while True:
        updates_json = bot.get_updates(last_update_id)
        if len(updates_json['result']) > 0:
            last_update_id = bot.get_last_id(updates_json) + 1
            for update in updates_json['result']:
                text, chat_id = bot.get_chat_info(update)
                data = mtg.get_card_info(text)
                reply = mtg.message_layout(data)
                bot.send_message(reply, chat_id)
                # print(chat_id)
                # print('end of this chat')
                # print('\n')
        time.sleep(0.5)


if __name__ == '__main__':
    main()


