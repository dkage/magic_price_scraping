from tbot import Telegram


def main():
    print(Telegram.get_me())


if __name__ == '__main__':
    bot = Telegram()
    bot.get_me()
