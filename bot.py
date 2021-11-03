import time
import random

import selenium.common.exceptions as se
from loguru import logger
from selenium.webdriver.common.keys import Keys


def slow_typing(element, text, end_enter: bool = False):
    time.sleep(random.randint(1, 2))
    for character in text:
        element.send_keys(character)
        time.sleep(random.uniform(0.2, 0.5))

    if end_enter:
        element.send_keys(Keys.ENTER)
    time.sleep(random.randint(1, 2))


def scrolling(browser, direction: str = "DOWN", scrolling_times: int = 5):
    if direction == "DOWN":
        for i in range(scrolling_times):
            browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
            time.sleep(random.randint(1, 3))
    else:
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(random.randint(1, 3))


class Bot:
    @logger.catch()
    def __init__(self, browser, time_sleep: int = random.randint(1, 3)):
        """
        Class constructor with simultaneous automatic opening site

        :param browser: instance of undetected_chromedriver
        :param time_sleep: delay between func invoking
        """
        self.browser = browser
        self.link = 'https://youtube.com'
        self.time_sleep = time_sleep

        browser.get(self.link)
        time.sleep(time_sleep)
        logger.info('Class constructed!')

    def inputting_query(self, searching_text, time_sleep: int = random.randint(1, 3)):
        """
        Inputting query in inputting field

        :param str searching_text: Query for inputting into input field
        :param time_sleep: delay between func invoking
        :return:
        """
        try:
            logger.info(f'Enter into inputting. Searching text: {searching_text}')
            search_field = self.browser.find_element_by_xpath('//input [@id="search"]')
            slow_typing(search_field, searching_text, end_enter=True)
            time.sleep(time_sleep)
            logger.info(f'Inputting finished')
        except Exception as err:
            raise Exception(f"Error: {err}")

    def choosing_video(self, video_title, video_duration: int = 5, filter_type: str = "D",
                       scrolling_times: int = 3, time_sleep: random = random.randint(1, 3)):
        """
        Trying to find specific video which equal video_title.
        If not found for all time -> going to filters in the assigned order

        :param str video_title: Precise video title for precise searching
        :param int video_duration: Video duration in seconds
        :param int time_sleep: delay between func invoking
        :param int scrolling_times: how many times to scroll down
        :param str filter_type: filter sequence (D, MWD, H, N). M - month, W - week, D - day, H - hour, N - None
        :return:
        """
        try:  # try to find video for all time
            logger.info(f"Enter into choosing_video. Video title = {video_title}")
            logger.info(f'Trying to find video for the all TIME...')

            scrolling(self.browser, scrolling_times=scrolling_times)

            video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

            if len(video_elements) > 0:
                self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_elements[-1])
                logger.debug(f'Founded elements with video title: {len(video_elements)}')
                time.sleep(time_sleep)
                video_elements[-1].click()
                logger.info(f'Video "{video_title}" was found!')
                time.sleep(video_duration)
                logger.success(f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')
            else:
                logger.debug(f'Raised NoSuchElementException')
                raise se.NoSuchElementException

        except se.NoSuchElementException:
            logger.warning(f'Video \"{video_title}" was NOT found for ALL TIME. Filer type - {filter_type}')
            if filter_type == "N":
                time.sleep(time_sleep)
            if filter_type == "D":
                try:
                    logger.info(f'Trying to find video for the all DAY...')
                    scrolling(self.browser, direction="UP")

                    self.browser.find_element_by_xpath(f"//*[contains(text(), 'Фильтры')]").click()
                    logger.info(f'Filter clicked')
                    time.sleep(time_sleep)
                    self.browser.find_element_by_xpath('''//div [@title='С фильтром "Сегодня"']''').click()
                    logger.debug(f"Filter for last DAY clicked!")
                    time.sleep(time_sleep)

                    scrolling(self.browser, scrolling_times=scrolling_times)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    if len(video_elements) > 0:
                        self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_elements[-1])
                        logger.debug(f'Founded elements with video title: {len(video_elements)}')
                        logger.info(f'Video "{video_title}" was found!')
                        time.sleep(time_sleep)
                        video_elements[-1].click()
                        time.sleep(video_duration)
                        logger.success(f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')
                    else:
                        logger.debug(f'Raised NoSuchElementException')
                        raise se.NoSuchElementException
                except se.NoSuchElementException:
                    logger.warning(f'Video \"{video_title}" was NOT found for all DAY. Filer type - {filter_type}')
                    time.sleep(time_sleep)
                except Exception as err:
                    logger.exception(f"Error: {err}")
                    raise Exception(f"Error: {err}")
            if filter_type == "H":
                try:
                    logger.info(f'Trying to find video for the all HOUR...')
                    scrolling(self.browser, direction="UP")

                    self.browser.find_element_by_xpath(f"//*[contains(text(), 'Фильтры')]").click()
                    logger.info(f'Filter clicked')
                    time.sleep(time_sleep)
                    self.browser.find_element_by_xpath('''//div [@title='С фильтром "За последний час"']''').click()
                    logger.debug(f"Filter for last HOUR clicked!")
                    time.sleep(time_sleep)

                    scrolling(self.browser, scrolling_times=scrolling_times)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    if len(video_elements) > 0:
                        self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_elements[-1])
                        logger.debug(f'Founded elements with video title: {len(video_elements)}')
                        time.sleep(time_sleep)
                        video_elements[-1].click()
                        logger.info(f'Video "{video_title}" was found!')
                        time.sleep(video_duration)
                        logger.success(f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')
                    else:
                        logger.debug(f'Raised NoSuchElementException')
                        raise se.NoSuchElementException
                except se.NoSuchElementException:
                    logger.warning(f'Video \"{video_title}" was NOT found for all HOUR. Filer type - {filter_type}')
                    time.sleep(time_sleep)
                except Exception as err:
                    logger.exception(f"Error: {err}")
                    raise Exception(f"Error: {err}")
            if filter_type == "MWD":
                try:
                    logger.info(f'Trying to find video for the all MONTH...')
                    scrolling(self.browser, direction="UP")

                    self.browser.find_element_by_xpath(f"//*[contains(text(), 'Фильтры')]").click()
                    logger.info(f'Filter clicked')
                    time.sleep(time_sleep)
                    self.browser.find_element_by_xpath('''//div [@title='С фильтром "За этот месяц"']''').click()
                    logger.debug(f"Filter for last MONTH clicked!")
                    time.sleep(time_sleep)

                    scrolling(self.browser, scrolling_times=scrolling_times)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    if len(video_elements) > 0:
                        self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_elements[-1])
                        logger.debug(f'Founded elements with video title: {len(video_elements)}')
                        time.sleep(time_sleep)
                        video_elements[-1].click()
                        logger.info(f'Video "{video_title}" was found!')
                        time.sleep(video_duration)
                        logger.success(f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')
                    else:
                        logger.debug(f'Raised NoSuchElementException')
                        raise se.NoSuchElementException
                except se.NoSuchElementException:
                    try:
                        logger.info(f'Trying to find video for the all DAY...')
                        scrolling(self.browser, direction="UP")

                        self.browser.find_element_by_xpath(f"//*[contains(text(), 'Фильтры')]").click()
                        logger.info(f'Filter clicked')
                        time.sleep(time_sleep)
                        self.browser.find_element_by_xpath('''//div [@title='С фильтром "Сегодня"']''').click()
                        logger.debug(f"Filter for last DAY clicked!")
                        time.sleep(time_sleep)

                        scrolling(self.browser, scrolling_times=scrolling_times)

                        video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')
                        if len(video_elements) > 0:
                            self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_elements[-1])
                            logger.debug(f'Founded elements with video title: {len(video_elements)}')
                            time.sleep(time_sleep)
                            video_elements[-1].click()
                            logger.info(f'Video "{video_title}" was found!')
                            time.sleep(video_duration)
                            logger.success(
                                f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')
                        else:
                            logger.debug(f'Raised NoSuchElementException')
                            raise se.NoSuchElementException
                    except se.NoSuchElementException:
                        try:
                            logger.info(f'Trying to find video for the all HOUR...')
                            scrolling(self.browser, direction="UP")

                            self.browser.find_element_by_xpath(f"//*[contains(text(), 'Фильтры')]").click()
                            logger.info(f'Filter clicked')
                            time.sleep(time_sleep)
                            self.browser.find_element_by_xpath(
                                '''//div [@title='С фильтром "За последний час"']''').click()
                            logger.debug(f"Filter for last HOUR clicked!")
                            time.sleep(time_sleep)

                            scrolling(self.browser, scrolling_times=scrolling_times)

                            video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                            if len(video_elements) > 0:
                                self.browser.execute_script("arguments[0].scrollIntoViewIfNeeded();",
                                                            video_elements[-1])
                                logger.debug(f'Founded elements with video title: {len(video_elements)}')
                                time.sleep(time_sleep)
                                video_elements[-1].click()
                                logger.info(f'Video "{video_title}" was found!')
                                time.sleep(video_duration)
                                logger.success(
                                    f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')
                            else:
                                logger.debug(f'Raised NoSuchElementException')
                                raise se.NoSuchElementException
                        except se.NoSuchElementException:
                            logger.warning(
                                f'Video \"{video_title}" was NOT found for all HOUR. Filer type - {filter_type}')
                            time.sleep(time_sleep)
                        except Exception as err:
                            logger.exception(f"Error: {err}")
                            raise Exception(f"Error: {err}")
                    except Exception as err:
                        logger.exception(f"Error: {err}")
                        raise Exception(f"Error: {err}")
                except Exception as err:
                    logger.exception(f"Error: {err}")
                    raise Exception(f"Error: {err}")
        except Exception as err:
            logger.exception(f"Error: {err}")
            raise Exception(f"Error: {err}")

    def change_channel(self, channel_name: str, time_sleep: random = random.randint(2, 4)):
        """
        Changing channel to next from list of names

        :param channel_name: 
        :param int time_sleep: delay between func invoking
        :return: 
        """
        try:
            logger.info(f"Enter into changing channel. Current channel: {channel_name}")
            self.browser.get(self.link)
            time.sleep(time_sleep)
            self.browser.find_element_by_id('avatar-btn').click()
            logger.info(f"Avatar clicked")
            time.sleep(time_sleep)
            self.browser.find_elements_by_class_name('style-scope.yt-multi-page-menu-section-renderer')[7].click()
            logger.info(f"Change account button clicked")
            time.sleep(time_sleep)

            channel = self.browser.find_elements_by_xpath(f"//*[contains(text(), '{channel_name}')]")
            logger.debug(f'Founded elements with channel name: {len(channel)}')
            if 1 <= len(channel) < 5:
                channel[-1].click()
                time.sleep(time_sleep)
            else:
                logger.warning(f'So many elements of channel name on the page. Quantity: {len(channel)}')
                # raise Exception(f"So many elements of channel name on the page. Quantity: {len(channel)}")
            logger.info(f"Channel successfully changed")
            time.sleep(time_sleep)
        except se.NoSuchElementException:
            logger.warning(f'Inputted wrong channel name')
            raise Exception(f"Inputted wrong channel name! Current channel name: {channel_name}")
        except Exception as err:
            logger.exception(f"Error: {err}")
            raise Exception(f"Error: {err}")

    def close_browser(self, time_sleep: random = random.randint(1, 3)):
        time.sleep(time_sleep)
        self.browser.close()
        self.browser.quit()
