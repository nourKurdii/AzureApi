import asyncio

import TelegramBot
import Menu


def main():
    # create menu object
    menu = Menu.Menu()
    # create telegram bot
    bot = TelegramBot.TelegramBot()
    # call menus' pick client method
    menu.pick_client(bot)
    # reference run_menu function
    run_menu = menu.run_menu()
    # if the chosen client is async let asyncio handle the run
    if asyncio.iscoroutinefunction(run_menu):
        asyncio.run(run_menu())
    # if chosen client is sync run normally
    else:
        run_menu()


if __name__ == "__main__":
    main()
