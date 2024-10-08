import logging
import os

from Src.Colors import *
from Src.db_SQlite import ConfigDB
from Src.Hamster import HamsterKombatClicker
from Src.Login import hamster_client
from Src.utils import localized_text

config = ConfigDB()


def choose_account():
    accounts = [{'key': key, 'token': value} for key, value in os.environ.items() if key.startswith('HAMSTER')]
    current_account = hamster_client().get_account_info()

    if len(accounts) > 1:
        print(f"{localized_text('detected_accounts')} {len(accounts)}: ")
        account_dict = {}

        for e, account in enumerate(accounts):
            token = account['token']
            key = account['key']

            try:
                hamster = HamsterKombatClicker(token)
                account_info = hamster.get_account_info()
                username = account_info.get('username', 'n/a')
                first_name = account_info.get('firstName', 'n/a')
                last_name = account_info.get('lastName', 'n/a')

                if username == current_account.get('username', 'n/a'):
                    print(f"[{e + 1}] · {LIGHT_BLUE}{first_name} {last_name} ({username}){WHITE} ({localized_text('logged_in')})")
                else:
                    print(f"[{e + 1}] · {first_name} {last_name} ({username})")
                account_dict[str(e + 1)] = token

            except Exception as e:
                print(f"[X] · {LIGHT_RED}{localized_text('error_dont_recieved_account_data', key)}{WHITE}")
                logging.error(e)

        account_choice = input(f"\n{DARK_GRAY}{localized_text('choose_account')}{WHITE}\n{CYAN}▶️  {localized_text('choose_number')}: {WHITE}")
        return f"HAMSTER_TOKEN_{account_choice}" if account_choice in account_dict else None
    else:
        print(localized_text('one_account_detected'))
        return "HAMSTER_TOKEN_1"
