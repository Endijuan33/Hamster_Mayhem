import asyncio
import logging

from Src.Login import hamster_client
from Src.Settings import load_settings, load_setting
from Src.utils import get_games_data

settings = load_settings()


def generate_promocodes(prefix='', apply_promo=False):
    count = input(f"\nКакое количество промокодов генерировать?\nEnter(по умолчанию 1): ")
    if count == '':
        count = 1
        print(f"⚠️  Количество промокодов не указано. Генерируется 1 по умолчанию")

    if int(count) <= 0:
        logging.error(f"\nКоличество должно быть числом больше 0")

    try:
        asyncio.run(hamster_client().get_promocodes(int(count), apply_promo, prefix, load_setting('spinner')))

    except Exception:
        print(f"🚫  Произошла ошибка во время генерации. Попробуйте снова, если ошибки прололжаться, то попробуйте позже.")

    finally:
        pass


def generate_for_game(prefix):
    choice_text = "\nХотите применить промокоды после получения?\nY(да) / Enter(Нет): "
    if load_setting('hamster_token'):
        if settings.get('apply_promo'):
            generate_promocodes(prefix=prefix, apply_promo=load_setting('apply_promo'))
        else:
            choice = input(choice_text).lower()
            if choice == 'y':
                generate_promocodes(prefix=prefix, apply_promo=True)
            elif choice == '':
                generate_promocodes(prefix=prefix)
            else:
                print("Такой опции нет")
    else:
        generate_promocodes(prefix=prefix)


async def genetare_for_all_games():
    apps = get_games_data()['apps']

    if load_setting('hamster_token'):
        choice = input(f"\nХотите применить промокоды после получения?\nY(да) / Enter(Нет): ")
        apply_promo = str(choice.lower()) == 'y'.lower()

    count = input(f"\nКоличество промокодов для всех игр Enter(по умолчанию 1): ")
    if count == '':
        count = 1
        print("\nКоличество промокодов не предоставлено. Генерируется 1 по умолчанию")

    if int(count) <= 0:
        logging.error(f"\nКоличество должно быть числом больше 0")
        exit(1)

    tasks = [hamster_client().get_promocodes(int(count), apply_promo, app["prefix"], load_setting('spinner')) for app in apps]
    await asyncio.gather(*tasks)
