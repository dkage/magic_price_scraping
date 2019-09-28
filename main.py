from tbot import Telegram
from time import sleep

def main():
    return True


if __name__ == '__main__':
    bot = Telegram()
    while not bot.get_me():
        print('Bot is offline for some reason, error during get_me checkup.')
        sleep(20)
    print('Bot ok')
