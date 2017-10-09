import bot_functions
import time


def main():
    last_update_id = None

    while True:
        updates_json = bot_functions.get_updates(last_update_id)
        if len(updates_json['result']) > 0:
            last_update_id = bot_functions.get_last_id(updates_json) + 1
            for update in updates_json['result']:
                text, chat_id = bot_functions.get_chat_info(update)
                print(text)
                print(chat_id)
                print('end of this chat')
                print('\n\n\n')
        time.sleep(0.5)


if __name__ == '__main__':
    main()


