import time
import random

import selenium.common.exceptions as se
from loguru import logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def slow_typing(element, text, end_enter: bool = False):
    time.sleep(random.randint(2, 4))
    for character in text:
        element.send_keys(character)
        time.sleep(random.uniform(0.2, 0.5))

    if end_enter:
        time.sleep(random.randint(1, 2))
        element.send_keys(Keys.ENTER)


def scrolling(browser, direction: str = "DOWN", scrolling_times: int = 5):
    if direction == "DOWN":
        for i in range(scrolling_times):
            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.END)
            time.sleep(random.randint(1, 3))
    else:
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(random.randint(1, 3))


def searching_video(browser,  video_title: str, video_duration: int,
                    video_exist: bool = False, scrolling_times: int = 5, time_sleep: random = random.randint(2, 4)):
    video_exist = False

    for _ in range(scrolling_times):
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.END)
        time.sleep(random.randint(2, 4))
        video_elements = browser.find_elements(By.XPATH, f'''//a [@title='{video_title}']''')
        if len(video_elements) > 0:
            logger.info(f'Founded elements with video title: {len(video_elements)}')
            for video_element in video_elements[::-1]:
                try:  # Try to scroll to video via script
                    browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_element)
                    time.sleep(time_sleep)
                except:
                    continue
                try:
                    video_element.click()
                    logger.info(f'Video "{video_title}" was found and clicked!')
                    video_exist = True
                    break
                except Exception as err:
                    logger.info(f'Video was not clicked!! More details:\n {err}')

            if video_exist:  # For exit from cycle
                break
        else:  # If not found via one scrolling
            pass
    else:  # If not found via all scrolls
        raise se.NoSuchElementException

    if video_exist:
        time.sleep(video_duration)
        logger.success(f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')


def filtration(browser, filtration_type: str, time_sleep: random = random.randint(2, 3)):
    logger.info(f'Trying to find video for the all {filtration_type.upper()}...')
    time.sleep(time_sleep)
    scrolling(browser, direction="UP")

    try:
        filter_element = browser.find_element(By.XPATH, f"//*[contains(text(), 'Фильтры')]")
        filter_element.click()
        logger.info(f'Filter clicked')
        time.sleep(time_sleep)
    except:
        logger.error('Filter element was not found!')
        raise se.NoSuchElementException

    if filtration_type.lower() == 'month':
        try:
            browser.find_element(By.XPATH, '''//div [@title='С фильтром "За этот месяц"']''').click()
        except:
            logger.error('Month filter element was not clicked!')
            raise se.NoSuchElementException
    elif filtration_type.lower() == 'week':
        try:
            browser.find_element(By.XPATH, '''//div [@title='С фильтром "За эту неделю"']''').click()
        except:
            logger.error('Week filter element was not clicked!')
            raise se.NoSuchElementException
    elif filtration_type.lower() == 'day':
        try:
            browser.find_element(By.XPATH, '''//div [@title='С фильтром "Сегодня"']''').click()
        except:
            logger.error('Day filter element was not clicked!')
            raise se.NoSuchElementException
    elif filtration_type.lower() == 'hour':
        try:
            browser.find_element(By.XPATH, '''//div [@title='С фильтром "За последний час"']''').click()
        except:
            logger.error('Hour filter element was not clicked!')
            raise se.NoSuchElementException
    else:
        logger.error('Invalid filtration type. Available types: "month", "week", "day", "hour"!')
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
        self.browser.maximize_window()
        self.link = 'https://youtube.com'
        self.time_sleep = time_sleep

        browser.get(self.link)
        time.sleep(time_sleep)

    def inputting_query(self, searching_text, time_sleep: int = random.randint(1, 4)):
        """
        Inputting query in inputting field
        :param str searching_text: Query for inputting into input field
        :param time_sleep: delay between func invoking
        :return:
        """
        logger.info(f'Inputting text: {searching_text}')

        # Try to find Searching field
        try:
            search_field = self.browser.find_element(By.XPATH, '//input [@id="search"]')
        except:
            logger.error('Searching field was not found!')
            raise se.NoSuchElementException

        # Try to typing query in searching field
        try:
            logger.info('Typing...')
            slow_typing(search_field, searching_text, end_enter=True)
        except:
            logger.error('Typing error!')
            raise se.NoSuchElementException

        time.sleep(time_sleep)
        logger.info(f'Typing finished')

    def choosing_video(self, video_title, video_duration: int = 5, filter_type: str = "N",
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
            logger.info('Searching video...')
            searching_video(browser=self.browser, video_title=video_title,
                            video_duration=video_duration, scrolling_times=scrolling_times, time_sleep=time_sleep)

        except se.NoSuchElementException:
            logger.warning(f'Video was NOT found for ALL TIME!')
            if filter_type == "N":
                time.sleep(time_sleep)
            if filter_type == "D":
                try:
                    filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                    searching_video(browser=self.browser,  video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video was NOT found for all DAY')
                    time.sleep(time_sleep)
                except Exception as err:
                    raise Exception(f"Error: {err}")
            if filter_type == "H":
                try:
                    filtration(browser=self.browser, filtration_type='hour', time_sleep=time_sleep)

                    searching_video(browser=self.browser,  video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video  was NOT found for all HOUR')
                    time.sleep(time_sleep)
                except Exception as err:
                    logger.exception(f"Error: {err}")
                    raise Exception(f"Error: {err}")
            if filter_type == "MDH":
                try:
                    filtration(browser=self.browser, filtration_type='month', time_sleep=time_sleep)

                    searching_video(browser=self.browser, video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video was NOT found for ALL MONTH')
                    try:
                        filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                        searching_video(browser=self.browser, video_title=video_title,
                                        video_duration=video_duration, scrolling_times=scrolling_times,
                                        time_sleep=time_sleep)

                    except se.NoSuchElementException:
                        logger.warning(f'Video was NOT found for ALL DAY')
                        try:
                            filtration(browser=self.browser, filtration_type='hour', time_sleep=time_sleep)

                            searching_video(browser=self.browser,
                                            video_title=video_title,
                                            video_duration=video_duration, scrolling_times=scrolling_times,
                                            time_sleep=time_sleep)

                        except se.NoSuchElementException:
                            logger.warning(
                                f'Video was NOT found for all HOUR')
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

                    searching_video(browser=self.browser, video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)

                except se.NoSuchElementException:
                    logger.warning(f'Video was NOT found for ALL MONTH')
                    try:
                        filtration(browser=self.browser, filtration_type='week', time_sleep=time_sleep)

                        searching_video(browser=self.browser, video_title=video_title,
                                        video_duration=video_duration, scrolling_times=scrolling_times,
                                        time_sleep=time_sleep)

                    except se.NoSuchElementException:
                        logger.warning(f'Video was NOT found for ALL WEEK')
                        try:
                            filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                            searching_video(browser=self.browser,
                                            video_title=video_title,
                                            video_duration=video_duration, scrolling_times=scrolling_times,
                                            time_sleep=time_sleep)

                        except se.NoSuchElementException:
                            logger.warning(f'Video was NOT found for all DAY')
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

                    searching_video(browser=self.browser,
                                    video_title=video_title,
                                    video_duration=video_duration, scrolling_times=scrolling_times,
                                    time_sleep=time_sleep)
                except se.NoSuchElementException:
                    logger.warning(
                        f'Video was NOT found for all HOUR')
                    try:
                        filtration(browser=self.browser, filtration_type='day', time_sleep=time_sleep)

                        searching_video(browser=self.browser,
                                        video_title=video_title,
                                        video_duration=video_duration, scrolling_times=scrolling_times,
                                        time_sleep=time_sleep)
                    except se.NoSuchElementException:
                        logger.warning(
                            f'Video was NOT found for all DAY')
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

    def change_channel(self, channel_name: str, time_sleep: random = random.randint(5, 9)):
        """
        Changing channel to next from list of names
        :param channel_name:
        :param int time_sleep: delay between func invoking
        :return:
        """

        logger.info(f"Changing channel...")

        for i in range(3):
            try:
                # Trying click avatar
                time.sleep(time_sleep)
                self.browser.get(self.link)
                time.sleep(time_sleep)

                self.browser.find_element(By.ID, 'avatar-btn')[-1].click()

                time.sleep(time_sleep)
                # Trying click change_channel element
                try:
                    change_account_element = self.browser.find_elements(By.CLASS_NAME,
                                                                        'style-scope yt-multi-page-menu-section-renderer')
                    ActionChains(self.browser).move_to_element_with_offset(change_account_element[0],
                                                                           145, 150).click().perform()
                    break
                except:
                    try:
                        self.browser.find_element(By.XPATH, f"//*[contains(text(), 'Сменить аккаунт')]").click()
                        logger.info(f"Change account button clicked in NoSuchElementException")
                    except:
                        raise Exception
            except:
                try:
                    # Trying click avatar
                    time.sleep(time_sleep)
                    self.browser.get(self.link)
                    time.sleep(time_sleep)
                    self.browser.find_element(By.XPATH, f'''//img [@alt='Фото профиля']''').click()

                    time.sleep(time_sleep)

                    # Trying click change_channel element
                    try:
                        change_account_element = self.browser.find_elements(By.CLASS_NAME,
                                                                            'style-scope yt-multi-page-menu-section-renderer')
                        ActionChains(self.browser).move_to_element_with_offset(change_account_element[0],
                                                                               145, 150).click().perform()
                        break
                    except:
                        try:
                            self.browser.find_element(By.XPATH, f"//*[contains(text(), 'Сменить аккаунт')]").click()
                            logger.info(f"Change account button clicked in NoSuchElementException")
                        except:
                            raise Exception

                except:
                    pass
        else:
            logger.error(f"Avatar or change channel elements was not found!")
            raise se.NoSuchElementException

        time.sleep(time_sleep)

        channels = self.browser.find_elements(By.XPATH, f"//*[contains(text(), '{channel_name}')]")

        if len(channels) > 0:
            for channel in channels[::-1]:
                try:
                    channel.click()
                    break
                except:
                    pass
            else:
                logger.error('Channel DO NOT changed!')
                raise se.NoSuchElementException

        else:
            logger.warning(f'Channel DO NOT changed! Maybe wrong channel name: {channel_name}')
            raise se.NoSuchElementException
        time.sleep(time_sleep)

    def close_browser(self, time_sleep: random = random.randint(1, 3)):
        time.sleep(time_sleep)
        self.browser.quit()
