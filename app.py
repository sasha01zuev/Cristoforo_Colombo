import random
import time
from multiprocessing import Pool

from loguru import logger

from bot import Bot, scrolling
import seleniumwire.undetected_chromedriver.v2 as uc
from seleniumwire import webdriver
from config import ACCOUNTS, QUERIES, BOT, PROXY
import concurrent.futures
import selenium.common.exceptions as se


accounts = list(ACCOUNTS.keys())
process_count = len(list(ACCOUNTS.keys()))


def bot_executor(account: str, searching_queries: list, video_title: str, video_duration: int, filter_type: str,
                 scrolling_times: int, chromedriver_executable_path: str, repeats: int = 1
                 ):
    profile_number = ACCOUNTS[f'{account}'][0]
    logger.add(f'info{profile_number}.log', format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
               rotation="10 MB", compression='zip', level="DEBUG", backtrace=True, diagnose=True)
    channels = ACCOUNTS[f'{account}'][1]
    for repeat in range(repeats):
        if PROXY:
            for proxy in PROXY:
                options = webdriver.ChromeOptions()
                options.headless = False

                # setting profile
                options.user_data_dir = f"c:\\temp\\profile{profile_number}"
                proxy_options = {'proxy': proxy}
                with uc.Chrome(options=options, seleniumwire_options=proxy_options,
                               executable_path=chromedriver_executable_path) as browser:
                    bot = Bot(browser=browser)

                for query in searching_queries:
                    for channel in channels:
                        logger.info(f'Current channel: {channel}')

                        try:
                            bot.inputting_query(f'{query}')
                            bot.choosing_video(video_title=f'{video_title}', video_duration=video_duration,
                                               filter_type=f'{filter_type}', scrolling_times=scrolling_times)
                        except se.NoSuchElementException:
                            bot.change_channel(channel_name=f'{channel}')
                            break

                        try:
                            bot.change_channel(channel_name=f'{channel}')
                        except se.NoSuchElementException:
                            break

                        logger.success('Successfully changing channel')
                    logger.success('Successful passage of the circle of channels')
                bot.close_browser()
                logger.success('Successful passage of the circle of searching queries')
            logger.success('Successful passage of Proxy')
        else:
            options = webdriver.ChromeOptions()
            options.headless = False
            # setting profile
            options.user_data_dir = f"c:\\temp\\profile{profile_number}"
            with uc.Chrome(options=options, executable_path=chromedriver_executable_path) as browser:
                bot = Bot(browser=browser)

            for query in searching_queries:
                for channel in channels:
                    logger.info(f'Current channel: {channel}')

                    try:
                        bot.inputting_query(f'{query}')
                        bot.choosing_video(video_title=f'{video_title}', video_duration=video_duration,
                                           filter_type=f'{filter_type}', scrolling_times=scrolling_times)
                    except se.NoSuchElementException:
                        bot.change_channel(channel_name=f'{channel}')
                        break

                    try:
                        bot.change_channel(channel_name=f'{channel}')
                    except se.NoSuchElementException:
                        break

                    logger.success('Successfully changing channel')
                logger.success('Successful passage of the circle of channels')
            logger.success('Successful passage of the circle of searching queries')
    logger.success('Successful passage of the circle of repeats')

    time.sleep(10)

    logger.success('Closing...')
    raise SystemExit(1)


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

    # with Pool(processes=process_count) as p:
    #     p.map(main, accounts)

    # for account in accounts:
    with concurrent.futures.ThreadPoolExecutor(max_workers=process_count) as my_thread:
        my_thread.map(main, accounts)

