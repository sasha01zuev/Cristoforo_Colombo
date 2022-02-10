import time
import random

import selenium.common.exceptions as se
from loguru import logger
from selenium.webdriver.common.keys import Keys


def slow_typing(element, text, end_enter: bool = False):
    try:
        time.sleep(random.randint(1, 2))
        for character in text:
            element.send_keys(character)
            time.sleep(random.uniform(0.2, 0.5))

        if end_enter:
            element.send_keys(Keys.ENTER)
        time.sleep(random.randint(1, 2))
    except Exception as err:
        logger.error(f"Error while typing characters query. Error: {err}")


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
            no_results = browser.find_elements_by_xpath("//*[contains(text(), 'Больше нет результатов')]")

            if video_elements:
                browser.execute_script("arguments[0].scrollIntoViewIfNeeded();", video_elements[-1])
                logger.debug(f'Founded elements with video title: {len(video_elements)}')
                time.sleep(time_sleep)
                try:
                    try:
                        video_elements[-1].click()
                    except:
                        for i in range(0, len(video_elements)-1):
                            try:
                                video_elements[i].click()
                                break
                            except:
                                pass
                        else:
                            raise se.NoSuchElementException
                    video_exist = True
                    logger.info(f'Video "{video_title}" was found and clicked!')
                    break
                except Exception as err:
                    logger.info(f'Exception in searching video. More details:\n {err}')
            else:
                pass

            if no_results:
                raise se.NoSuchElementException
        else:
            raise se.NoSuchElementException
            # pass

        if video_exist:
            time.sleep(video_duration)
            logger.success(f'Successful video watched: Time sleep: {video_duration}, Video: {video_title}')


def filtration(browser, filtration_type: str, time_sleep: random = random.randint(2, 3)):
    logger.info(f'Trying to find video for the all {filtration_type.upper()}...')
    scrolling(browser, direction="UP")

    for i in range(10):
        time.sleep(time_sleep)
        try:
            browser.find_element_by_xpath(f"//*[contains(text(), 'Фильтры')]").click()
            break
        except:
            time.sleep(time_sleep)
            browser.refresh()
    else:
        raise se.NoSuchElementException

    logger.info(f'Filter clicked')
    time.sleep(time_sleep)

    if filtration_type.lower() == 'month':
        try:
            browser.find_element_by_xpath('''//div [@title='С фильтром "За этот месяц"']''').click()
        except:
            raise se.NoSuchElementException

    elif filtration_type.lower() == 'week':
        try:
            browser.find_element_by_xpath('''//div [@title='С фильтром "За эту неделю"']''').click()
        except:
            raise se.NoSuchElementException

    elif filtration_type.lower() == 'day':
        try:
            browser.find_element_by_xpath('''//div [@title='С фильтром "Сегодня"']''').click()
        except:
            raise se.NoSuchElementException

    elif filtration_type.lower() == 'hour':
        try:
            browser.find_element_by_xpath('''//div [@title='С фильтром "За последний час"']''').click()
        except:
            raise se.NoSuchElementException

    else:
        logger.warning('Invalid filtration type. Available types: "month", "week", "day", "hour"!')
        raise Exception('Invalid filtration type. Available types: "month", "week", "day", "hour"')
    logger.debug(f"Filter for last {filtration_type.upper()} clicked!")
    time.sleep(time_sleep)


class Bot:
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
        error = ''
        for i in range(5):
            try:
                logger.info(f'Enter into inputting. Searching text: {searching_text}')
                search_field = self.browser.find_element_by_xpath('//input [@id="search"]')
                slow_typing(search_field, searching_text, end_enter=True)
                time.sleep(time_sleep)
                logger.info(f'Inputting finished')
                break
            except Exception as err:
                self.browser.get(self.link)
                time.sleep(time_sleep)
                error = err
        else:
            logger.error(f"Error while inputting query: {error}")
            raise se.NoSuchElementException

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
        try:  # try to find video for the all time
            logger.info(f"Enter into choosing_video. Video title = {video_title}")
            logger.info(f'Trying to find video for the all TIME...')

            searching_video(browser=self.browser, video_title=video_title,
                            video_duration=video_duration, scrolling_times=scrolling_times, time_sleep=time_sleep)

        except se.NoSuchElementException:
            logger.warning(f'Video \"{video_title}" was NOT found for ALL TIME. Filer type - {filter_type}')
            if filter_type == "N":
                scrolling(self.browser, direction="UP")
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

    def change_channel(self, channel_name: str, time_sleep: random = random.randint(3, 8)):
        """
        Changing channel to next from list of names

        :param channel_name: 
        :param int time_sleep: delay between func invoking
        :return: 
        """

        logger.info(f"Enter into changing channel. Current channel: {channel_name}")
        time.sleep(time_sleep)
        self.browser.get(self.link)

        for i in range(10):
            time.sleep(time_sleep)
            try:
                logger.info(f"Pre avatar click")
                self.browser.find_element_by_id('avatar-btn').click()
                logger.info(f"Avatar clicked")
                break
            except:
                time.sleep(time_sleep)
                self.browser.get(self.link)
        else:
            logger.error(f"Error while clicking avatar")
            self.browser.get(self.link)
            raise se.NoSuchElementException

        try:
            time.sleep(time_sleep)
            logger.info(f"Pre 'changing account' clicked")
            self.browser.find_element_by_xpath(f"//*[contains(text(), 'Сменить аккаунт')]").click()
            # self.browser.find_elements_by_class_name('style-scope.yt-multi-page-menu-section-renderer')[7].click()
            logger.info(f"Change account button clicked")
        except:
            time.sleep(time_sleep)
            self.browser.get(self.link)
            raise se.NoSuchElementException

        time.sleep(time_sleep)
        channels = self.browser.find_elements_by_xpath(f"//*[contains(text(), '{channel_name}')]")

        for channel in channels[::-1]:
            try:
                channel.click()
                break
            except:
                pass
        else:
            time.sleep()
            logger.error(f"Error while clicking channel name")
            self.browser.get(self.link)
            raise se.NoSuchElementException

        logger.info(f"Channel successfully changed")
        time.sleep(time_sleep)

    def close_browser(self, time_sleep: random = random.randint(1, 3)):
        time.sleep(time_sleep)
        self.browser.close()
        self.browser.quit()
