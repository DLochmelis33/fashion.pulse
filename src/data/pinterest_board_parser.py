from typing import Callable, Dict, List, TypeVar
from selenium import webdriver
from requests import get
from bs4 import BeautifulSoup
import time

PinsCollection = Dict[str, None]


def _get_html(url: str) -> str:
    """Gets html by the given url. It does nothing with possible pagination."""
    response = get(url)
    if response.status_code != 200:
        raise ValueError(
            f"Failed to fetch {url}: HTTP code {response.status_code}")
    return response.text


def _parse_pin_count(source: str) -> int:
    soup = BeautifulSoup(source, 'html.parser')
    pin_count_div = soup.find('div', {'data-test-id': 'pin-count'})
    if pin_count_div is None:
        raise ValueError(
            "Failed to parse pin count: no pin count element on the given page")
    pin_count_text = pin_count_div.text.strip()
    pin_count = int(pin_count_text.split()[0])
    return pin_count


def _parse_pins_from_html(source: str) -> PinsCollection:
    soup = BeautifulSoup(source, 'html.parser')
    div_tags = soup.find_all('div', class_='PinCard__imageWrapper')

    pins_src = {}
    for div_tag in div_tags:
        img_tag = div_tag.find('img')
        if img_tag and 'src' in img_tag.attrs:
            src_attribute = img_tag['src']
            pins_src[src_attribute] = None

    return pins_src


# can be used as a stop criterion for scrolling web pages of large boards
# def _check_large_board_end_reached(source: str) -> bool:
#     soup = BeautifulSoup(source, 'html.parser')
#     return soup.find('h2', text='More like this') is not None


T = TypeVar('T')
R = TypeVar('R')


def _parse_page_while_scrolling(
    url: str,
    parser: Callable[[str], T],
    results_combiner: Callable[[R, T], R],
    initial: R,
    check_should_stop_scrolling: Callable[[str, R], bool] = None,
    scroll_pause_time_seconds: float = 1
) -> R:
    driver = webdriver.Chrome()
    driver.get(url)

    def get_scroll_height() -> int:
        return driver.execute_script("return document.body.scrollHeight")

    last_height = None
    results = initial
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time_seconds)  # wait to load page
        page = driver.page_source

        page_result = parser(page)
        results = results_combiner(results, page_result)

        if check_should_stop_scrolling is not None:
            if check_should_stop_scrolling(page, results):
                break
        else:
            new_height = get_scroll_height()
            if new_height == last_height:
                break
            last_height = new_height

    driver.quit()
    return results


def _get_pin_count(board_url: str) -> int:
    board_start_page = _get_html(board_url)
    return _parse_pin_count(board_start_page)


def parse_pins_from_large_board(board_url: str) -> List[str]:
    pin_count = _get_pin_count(board_url)
    print(f"Board's pin count: {pin_count}", end='\n\n')

    def page_pins_combiner(all_pins: PinsCollection, page_pins: PinsCollection) -> PinsCollection:
        all_pins.update(page_pins)
        return all_pins

    pins_ordered_dict = _parse_page_while_scrolling(
        url=board_url,
        parser=_parse_pins_from_html,
        results_combiner=page_pins_combiner,
        initial={},
        check_should_stop_scrolling=lambda _, results: len(
            results) >= pin_count,
        scroll_pause_time_seconds=0.5
    )

    return list(pins_ordered_dict.keys())[:pin_count]


board_url = 'https://www.pinterest.com/garrettguadiana/rustic-mens-fashion/'
# board_url = 'https://www.pinterest.com/tarateilhaber/cute-bulletin-boards/'

pins = parse_pins_from_large_board(board_url)
print("First 5 pins:")
print(pins[:5], end='\n\n')
print("Last 5 pins:")
print(pins[-5:], end='\n\n')
print(f"Parsed pins, total: {len(pins)}")
