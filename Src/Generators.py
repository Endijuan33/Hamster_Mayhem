import logging

import asyncio

from Src.Colors import *
from Src.db_SQlite import ConfigDB
from Src.Login import hamster_client
from Src.utils import get_games_data, localized_text

import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

config = ConfigDB()


choice_text = f"{DARK_GRAY}{localized_text('apply_promo_after_generate')}{CYAN}\n▶️  {localized_text('yes_enter')}: {WHITE}"


def generate_promocodes(prefix='', apply_promo=False):
    count = input(f"\n{DARK_GRAY}{localized_text('count_promocodes_to_generate')}{CYAN}\n▶️  {localized_text('enter_one')}: {WHITE}")
    if count == '':
        count = 1
        print(f"\n⚠️  {localized_text('count_not_specified')}")

    if int(count) <= 0:
        print(localized_text('error_count_must_great_0'))

    try:
        asyncio.run(hamster_client().get_promocodes(int(count), config.send_to_group, apply_promo, prefix, config.save_to_file, one_game=True))

    except Exception as e:
        logging.error(e)
        print(f"🚫  {localized_text('error_generate_failed')}")

    finally:
        pass


def generate_for_game(prefix):
    if config.hamster_token:
        if config.apply_promo:
            generate_promocodes(prefix=prefix, apply_promo=config.apply_promo)
        else:
            choice = input(choice_text)
            if choice.lower() == 'y':
                generate_promocodes(prefix=prefix, apply_promo=True)
            elif choice == '':
                generate_promocodes(prefix=prefix)
            else:
                print(f"ℹ️  {localized_text('no_such_option')}")
    else:
        generate_promocodes(prefix=prefix)


async def genetare_for_all_games(task_count=None):
    games_data = [app for app in get_games_data()['apps'] if app.get('available')]

    if config.hamster_token:
        choice = input(choice_text)
        apply_promo = str(choice.lower()) == 'y'.lower()

    count = input(f"\n{DARK_GRAY}{localized_text('count_promocodes_to_generate_all_games')}{CYAN}\n▶️  {localized_text('enter_one')}: {WHITE}")
    if count == '':
        count = 1
        print(f"\n⚠️  {localized_text('count_not_specified')}")

    if int(count) <= 0:
        print(localized_text('error_count_must_great_0'))
        exit(1)

    if task_count is None:
        limited_games_data = games_data
    else:
        limited_games_data = games_data[:task_count]

    tasks = [hamster_client().get_promocodes(int(count), config.send_to_group, apply_promo, app["prefix"], config.save_to_file, one_game=False) for app in limited_games_data]
    await asyncio.gather(*tasks)
