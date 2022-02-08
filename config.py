import os


ACCOUNTS = {
    'captainprice2701@gmail.com': (1, ['Patronim', 'Cringe', 'Нурлан Сакиров',
                                       'Altakglag', 'Саня Фогель', 'Tanker_25_17', 'Captain Price'])
    # ,
    # 'mareekawp@gmail.com': (2, ['Tambovskiy', 'Тот Самый Колян',
    #                             'Sa Sea', 'Коля Гантеля', 'cTpum_cHaunep', 'Mareek Awp']),
    # 'altakglag02@gmail.com': (3, ['харошая работа Алек', 'Лёша Круглов', 'Farengiheat freek'])
    # ,
    # 'vazonezalex@gmail.com': (4, ['Skill Sky', 'Ufpnj without H', 'Subject Supreme', 'Скала Миланов', 'Flamme Eternelle', 'Sleepy', 'V for Vendetta', 'Дарлин', 'Cameu', 'No Stress'])
    # ,
    # 'altakglag01@gmail.com': (5, ['CeBepHoe_Cu9Hue', 'ХУМОР', 'Domant'])
    
}


BOT = {
    # Default path = C:\Users\{User}\AppData\Roaming\undetected_chromedriver\chromedriver.exe'
    'chromedriver_executable_path': fr'C:\Users\{os.environ.get("USERNAME")}'
                                    fr'\AppData\Roaming\undetected_chromedriver\chromedriver.exe',
}

QUERIES = {
    'searching_queries': [
        'заработок в интернете без вложений на телефоне телеграм'

    ],
    'video_title': 'WHO MORE | Простой ЗАРАБОТОК без вложений и с вложениями! Сможет КАЖДЫЙ!',
    'video_duration': 2230,  # Продолжительность ролика в секундах
    'filter_type': 'D',  # (D, MDH, MWD, HD, H, N). M - month, W - week, D - day, H - hour, N - None
    'scrolling_times': 8,  # Сколько раз нужно скролить на определённом типе фильтра
    'repeats': 200  # Сколько повторений
}
