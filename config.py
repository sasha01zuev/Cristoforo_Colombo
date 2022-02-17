import os


ACCOUNTS = {
    'captainprice2701@gmail.com': (1, ['Patronim', 'Cringe', 'Нурлан Сакиров',
                                       'Altakglag', 'Саня Фогель', 'Tanker_25_17', 'Captain Price'])
    # ,
    # 'mareekawp@gmail.com': (2, ['Tambovskiy', 'Тот Самый Колян',
    #                             'Sa Sea', 'Коля Гантеля', 'cTpum_cHaunep', 'Mareek Awp'])
    # ,
    # 'altakglag02@gmail.com': (3, ['харошая работа Алек', 'Лёша Круглов', 'Farengiheat freek'])
    # ,
    # 'vazonezalex@gmail.com': (4, ['Skill Sky', 'Ufpnj without H', 'Subject Supreme', 'Скала Миланов', 'Flamme Eternelle', 'Sleepy', 'V for Vendetta', 'Дарлин', 'Cameu', 'No Stress'])
    # ,
    # 'kremovyjpirog27@gmail.com': (5, ['Кремовый Пирог', 'Мятный Лёд'])
    
}


BOT = {
    # Default path = C:\Users\{User}\AppData\Roaming\undetected_chromedriver\chromedriver.exe'
    'chromedriver_executable_path': fr'C:\Users\{os.environ.get("USERNAME")}'
                                    fr'\AppData\Roaming\undetected_chromedriver\chromedriver.exe'
}

QUERIES = {
    'searching_queries': [
        'как заработать деньги в интернете школьнику без вложений ',
        'заработок в интернете без вложений на телефоне телеграм ',
        'телеграм боты для заработка',
        'заработок в интернете на играх',
        'Просто заработок без вложений'
        'Простой заработок в интернете',
        'як легко заробити грошей',
        'как быстро заработать деньги в интернете',
        'заработок в интернете без вложений',
        'як швидко заробити гроші в інтернеті'

    ],
    'video_title': 'WHO MORE | Простой ЗАРАБОТОК без вложений и с вложениями! Сможет КАЖДЫЙ!',
    'video_duration': 5,  # Продолжительность ролика в секундах
    'filter_type': 'MWD',  # (D, MDH, MWD, HD, H, N). M - month, W - week, D - day, H - hour, N - None
    'scrolling_times': 40,  # Сколько раз нужно скролить на определённом типе фильтра
    'repeats': 200  # Сколько повторений
}

PROXY = [
    {'https': 'https://wdTZtV:r8Euj6@217.29.63.240:11494'},
    {'https': 'https://wdTZtV:r8Euj6@217.29.63.240:11495'}
]
