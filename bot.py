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


def searching_video(browser,  video_title: str, video_duration: int,
                    video_exist: bool = False, scrolling_times: int = 5, time_sleep: random = random.randint(2, 3)):
    for _ in range(scrolling_times):
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
        time.sleep(random.randint(1, 2))
        video_elements = browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')
        if len(video_elements) > 0:
            browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_elements[-1])
            logger.debug(f'Founded elements with video title: {len(video_elements)}')
            time.sleep(time_sleep)
            try:
                video_elements[-1].click()
                logger.info(f'Video "{video_title}" was found and clicked!')
                video_exist = True
                break
            except Exception as err:
                logger.info(f'Exception in searching video. More details:\n {err}')

        else:
            pass
    else:
        raise se.NoSuchElementException
        # pass

    if video_exist:
        time.sleep(video_duration)
        logger.success(f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')


def filtration(browser, filtration_type: str, time_sleep: random = random.randint(2, 3)):
    logger.info(f'Trying to find video for the all {filtration_type.upper()}...')
    scrolling(browser, direction="UP")

    browser.find_element_by_xpath(f"//*[contains(text(), 'Фильтры')]").click()
    logger.info(f'Filter clicked')
    time.sleep(time_sleep)
    if filtration_type.lower() == 'month':
        browser.find_element_by_xpath('''//div [@title='С фильтром "За этот месяц"']''').click()
    elif filtration_type.lower() == 'week':
        browser.find_element_by_xpath('''//div [@title='С фильтром "За эту неделю"']''').click()
    elif filtration_type.lower() == 'day':
        browser.find_element_by_xpath('''//div [@title='С фильтром "Сегодня"']''').click()
    elif filtration_type.lower() == 'hour':
        browser.find_element_by_xpath('''//div [@title='С фильтром "За последний час"']''').click()
    else:
        logger.warning('Invalid filtration type. Available types: "month", "week", "day", "hour"!')
        raise Exception('Invalid filtration type. Available types: "month", "week", "day", "hour"')
    logger.debug(f"Filter for last {filtration_type.upper()} clicked!")
    time.sleep(time_sleep)


class Bot:
    @logger.catch()
    def __init__(self, browser, time_sleep: int = random.randint(2, 3)):
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
                       scrolling_times: int = 3, time_sleep: random = random.randint(2, 4)):
        """
        Trying to find specific video which equal video_title.
        If not found for all time -> going to filters in the assigned order

        :param str video_title: Precise video title for precise searching
        :param int video_duration: Video duration in seconds
        :param int time_sleep: delay between func invoking
        :param int scrolling_times: how many times to scroll down
        :param str filter_type: filter sequence (D, MWD, MDH, HD,  H, N). M - month, W - week, D - day, H - hour, N - None
        :return:
        """
        try:  # try to find video for all time
            logger.info(f"Enter into choosing_video. Video title = {video_title}")
            logger.info(f'Trying to find video for the all TIME...')

            video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

            searching_video(browser=self.browser, video_title=video_title,
                            video_duration=video_duration, scrolling_times=scrolling_times, time_sleep=time_sleep)

        except se.NoSuchElementException:
            logger.warning(f'Video \"{video_title}" was NOT found for ALL TIME. Filer type - {filter_type}')
            if filter_type == "N":
                time.sleep(time_sleep)
            if filter_type == "D":
                try:
                    filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    searching_video(browser=self.browser,  video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video \"{video_title}" was NOT found for all DAY. Filer type - {filter_type}')
                    time.sleep(time_sleep)
                except Exception as err:
                    logger.exception(f"Error: {err}")
                    raise Exception(f"Error: {err}")
            if filter_type == "H":
                try:
                    filtration(browser=self.browser, filtration_type='hour', time_sleep=time_sleep)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    searching_video(browser=self.browser,  video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video \"{video_title}" was NOT found for all HOUR. Filer type - {filter_type}')
                    time.sleep(time_sleep)
                except Exception as err:
                    logger.exception(f"Error: {err}")
                    raise Exception(f"Error: {err}")
            if filter_type == "MDH":
                try:
                    filtration(browser=self.browser, filtration_type='month', time_sleep=time_sleep)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    searching_video(browser=self.browser, video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video \"{video_title}" was NOT found for ALL MONTH. Filer type - {filter_type}')
                    try:
                        filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                        video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                        searching_video(browser=self.browser, video_title=video_title,
                                        video_duration=video_duration, scrolling_times=scrolling_times,
                                        time_sleep=time_sleep)

                    except se.NoSuchElementException:
                        logger.warning(f'Video \"{video_title}" was NOT found for ALL DAY. Filer type - {filter_type}')
                        try:
                            filtration(browser=self.browser, filtration_type='hour', time_sleep=time_sleep)

                            video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                            searching_video(browser=self.browser,
                                            video_title=video_title,
                                            video_duration=video_duration, scrolling_times=scrolling_times,
                                            time_sleep=time_sleep)

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
            if filter_type == "MWD":
                try:
                    filtration(browser=self.browser, filtration_type='month', time_sleep=time_sleep)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    searching_video(browser=self.browser, video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video \"{video_title}" was NOT found for ALL MONTH. Filer type - {filter_type}')
                    try:
                        filtration(browser=self.browser, filtration_type='week', time_sleep=time_sleep)

                        video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                        searching_video(browser=self.browser, video_title=video_title,
                                        video_duration=video_duration, scrolling_times=scrolling_times,
                                        time_sleep=time_sleep)

                    except se.NoSuchElementException:
                        logger.warning(f'Video \"{video_title}" was NOT found for ALL WEEK. Filer type - {filter_type}')
                        try:
                            filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                            video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')
                            searching_video(browser=self.browser,
                                            video_title=video_title,
                                            video_duration=video_duration, scrolling_times=scrolling_times,
                                            time_sleep=time_sleep)

                        except se.NoSuchElementException:
                            logger.warning(
                                f'Video \"{video_title}" was NOT found for all DAY. Filer type - {filter_type}')
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
            if filter_type == "HD":
                try:
                    filtration(browser=self.browser, filtration_type='hour', time_sleep=time_sleep)

                    video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                    searching_video(browser=self.browser,
                                    video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)
                except se.NoSuchElementException:
                    logger.warning(
                        f'Video \"{video_title}" was NOT found for all HOUR. Filer type - {filter_type}')
                    try:
                        filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                        video_elements = self.browser.find_elements_by_xpath(f'''//a [@title='{video_title}']''')

                        searching_video(browser=self.browser,
                                        video_title=video_title,
                                        video_duration=video_duration, scrolling_times=scrolling_times,
                                        time_sleep=time_sleep)
                    except se.NoSuchElementException:
                        logger.warning(
                            f'Video \"{video_title}" was NOT found for all DAY. Filer type - {filter_type}')
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

    def change_channel(self, channel_name: str, time_sleep: random = random.randint(2, 4)):
        """
        Changing channel to next from list of names

        :param channel_name: 
        :param int time_sleep: delay between func invoking
        :return: 
        """
        try:
            logger.info(f"Enter into changing channel. Current channel: {channel_name}")
            time.sleep(time_sleep)
            self.browser.get(self.link)
            time.sleep(time_sleep)

            try:
                logger.info(f"Pre avatar click")
                self.browser.find_element_by_id('avatar-btn').click()
                logger.info(f"Avatar clicked")
            except se.NoSuchElementException:
                logger.info(f"Pre avatar clicked in NoSuchElementException")
                self.browser.refresh()
                time.sleep(time_sleep)
                self.browser.find_element_by_id('avatar-btn').click()
                logger.info(f"Avatar clicked in NoSuchElementException")
            except Exception as err:
                logger.exception(f"Error in avatar click: {err}")
                raise Exception(f"Error: {err}")

            time.sleep(time_sleep)

            try:
                self.browser.find_elements_by_class_name('style-scope.yt-multi-page-menu-section-renderer')[7].click()
                logger.info(f"Change account button clicked")
            except se.NoSuchElementException:
                logger.info(f"Pre 'changing account' clicked in NoSuchElementException")
                self.browser.find_element_by_xpath(f"//*[contains(text(), 'Сменить аккаунт')]").click()
                logger.info(f"Change account button clicked in NoSuchElementException")
            except Exception as err:
                logger.exception(f"Error in changing account click: {err}")
                raise Exception(f"Error: {err}")

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
