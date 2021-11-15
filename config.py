import os


ACCOUNTS = {
    'captainprice2701@gmail.com': (1, ['Captain Price', 'Patronim', 'Cringe', 'Нурлан Сакиров',
                                       'Altakglag', 'Саня Фогель', 'Tanker_25_17']),
    'mareekawp@gmail.com': (2, ['Mareek Awp', 'Tambovskiy', 'Тот Самый Колян',
                                'Sa Sea', 'Коля Гантеля', 'cTpum_cHaunep']),
    'altakglag02@gmail.com': (3, ['Farengiheat freek', 'харошая работа Алек', 'Лёша Круглов'])
}


BOT = {
    # Default path = C:\Users\{User}\AppData\Roaming\undetected_chromedriver\chromedriver.exe'
    'chromedriver_executable_path': fr'C:\Users\{os.environ.get("USERNAME")}'
                                    fr'\AppData\Roaming\undetected_chromedriver\chromedriver.exe',
}

QUERIES = {
    'searching_queries': [
        'контейнеры вот блиц',
        'открытие мистических сундуков вот блиц',
        'мистические контейнеры вот блиц',
        'открытие мистических сундуков wot blitz',
        'контейнеры вот блиц',
        'мистические контейнеры вот блиц 100к голды',
        'мистические контейнеры wot blitz',
        'открытие контейнеров вот блиц',
        'контейнеры вот блиц',
        'мистические сундуки wot blitz',
        'открытие мистических сундуков wot blitz',
        'открытие мистических сундуков вот блиц'

    ],
    'video_title': 'Открытие МИСТИЧЕСКИХ КОНТЕЙНЕРОВ в Wot Blitz | Выпало 100к золота?!',
    'video_duration': 382,
    'filter_type': 'MWD',  # (D, MDH, MWD, HD, H, N). M - month, W - week, D - day, H - hour, N - None
    'scrolling_times': 8,
    'repeats': 200
}
