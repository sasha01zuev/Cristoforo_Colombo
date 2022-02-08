import random
import time
from loguru import logger
from bot import Bot, scrolling
import undetected_chromedriver.v2 as uc
from config import ACCOUNTS, QUERIES, BOT
from multiprocessing import Pool


accounts = list(ACCOUNTS.keys())
process_count = len(list(ACCOUNTS.keys()))


def bot_executor(account: str, searching_queries: list, video_title: str, video_duration: int, filter_type: str,
                 scrolling_times: int, chromedriver_executable_path: str, repeats: int = 1
                 ):
    profile_number = ACCOUNTS[f'{account}'][0]
    logger.add(f'info{profile_number}.log', format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
               rotation="10 MB", compression='zip', level="DEBUG", backtrace=True, diagnose=True)
    channels = ACCOUNTS[f'{account}'][1]
    options = uc.ChromeOptions()

    # setting profile
    options.user_data_dir = f"c:\\temp\\profile{profile_number}"

    browser = uc.Chrome(options=options,
                        executable_path=chromedriver_executable_path)
    bot = Bot(browser=browser)
    logger.success('Successfully created instance of Bot')

    for repeat in range(repeats):
        logger.info(f'Current repeat: {repeat}')
        for query in searching_queries:
            logger.info(f'Current searching query: {query}')
            for channel in channels:
                logger.info(f'Current channel: {channel}')

                bot.inputting_query(f'{query}')
                logger.success('Successfully inputting of query')
                bot.choosing_video(video_title=f'{video_title}', video_duration=video_duration,
                                   filter_type=f'{filter_type}', scrolling_times=scrolling_times)
                logger.debug('After finding video')
                bot.change_channel(channel_name=f'{channel}')
                logger.success('Successfully changing channel')
            logger.success('Successful passage of the circle of channels')
        logger.success('Successful passage of the circle of searching queries')
    logger.success('Successful passage of the circle of repeats')

    time.sleep(10)
    bot.close_browser()
    logger.success('Successfully closing browser')


def main(accounts: list):
    searching_queries = QUERIES['searching_queries']
    video_title = QUERIES['video_title']
    video_duration = QUERIES['video_duration']
    filter_type = QUERIES['filter_type']
    scrolling_times = QUERIES['scrolling_times']
    repeats = QUERIES['repeats']
    chromedriver_executable_path = BOT['chromedriver_executable_path']
    account = str(accounts)

    bot_executor(account=account, searching_queries=searching_queries, video_title=video_title,
                 video_duration=video_duration, filter_type=filter_type,
                 scrolling_times=scrolling_times, repeats=repeats,
                 chromedriver_executable_path=chromedriver_executable_path)

    # # If u need to add new account with new profile - uncomment the code, then comment out code above
    # options = uc.ChromeOptions()
    # options.user_data_dir = f"c:\\temp\\profile5"
    # # just some options passing in to skip annoying popups
    # browser = uc.Chrome(options=options)
    # # setting profile
    # browser.get('https://youtube.com')
    # time.sleep(400)


if __name__ == '__main__':
    # p = Pool(processes=1)
    p = Pool(processes=process_count)
    p.map(main, accounts)
