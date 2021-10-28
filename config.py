import os
ACCOUNTS = {
    'account1@gmail.com': (1, ['Channel_1', 'Channel_2']),
    'account2@gmail.com': (2, ['Channel_1', 'Channel_2']),
    'account3@gmail.com': (3, ['Channel_1', 'Channel_2'])
}

BOT = {
    # Default path = C:\Users\{User}\AppData\Roaming\undetected_chromedriver\chromedriver.exe'
    'chromedriver_executable_path': fr'C:\Users\{os.environ.get("USERNAME")}'
                                    fr'\AppData\Roaming\undetected_chromedriver\chromedriver.exe',
}
QUERIES = {

    'searching_queries': [
        'Query_1',
        'Query_2'

    ],
    'video_title': '',
    'video_duration': 15,
    'filter_type': 'MWD',  # (D, MWD, H, N). M - month, W - week, D - day, H - hour, N - None
    'scrolling_times': 7,
    'repeats': 20
}
