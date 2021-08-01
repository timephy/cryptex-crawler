from typing import Protocol
from selenium.webdriver import Safari
from time import sleep
# from selenium.webdriver.safari import Options
from objects import Card, Coin
import yaml
from datetime import datetime
from pathlib import Path

url = 'https://www.kryptex.org/en/mining-calculator?q_380=1&q_fury=1&q_470=1&q_480=1&q_570=1&q_580=1&q_vega56=1&q_vega64=1&q_5600xt=1&q_5700=1&q_5700xt=1&q_vii=1&q_1050Ti=1&q_10606=1&q_1070=1&q_1070Ti=1&q_1080=1&q_1080Ti=1&q_1660=1&q_1660Ti=1&q_2060=1&q_2070=1&q_2080=1&q_2080Ti=1&q_68=1&q_3060=1&q_3070=1&q_3080=1&q_3090=1&q_166s=1&q_3060Ti=1&eth_hr=0.0&eth_p=0.0&e4g_hr=0.0&e4g_p=0.0&zh_hr=0.0&zh_p=0.0&cnh_hr=0.0&cnh_p=0.0&cng_hr=0.0&cng_p=0.0&cnr_hr=0.0&cnr_p=0.0&cnf_hr=0.0&cnf_p=0.0&eqa_hr=0.0&eqa_p=0.0&cc_hr=0.0&cc_p=0.0&cr29_hr=0.0&cr29_p=0.0&ct31_hr=0.0&ct31_p=0.0&ct32_hr=0.0&ct32_p=0.0&eqb_hr=0.0&eqb_p=0.0&rmx_hr=0.0&rmx_p=0.0&ns_hr=0.0&ns_p=0.0&al_hr=0.0&al_p=0.0&ops_hr=0.0&ops_p=0.0&eqz_hr=0.0&eqz_p=0.0&zlh_hr=0.0&zlh_p=0.0&kpw_hr=0.0&kpw_p=0.0&ppw_hr=0.0&ppw_p=0.0&x25x_hr=0.0&x25x_p=0.0&mtp_hr=0.0&mtp_p=0.0&vh_hr=0.0&vh_p=0.0&cost=0.25'


def main():
    # opts = Options()
    # opts.set_headless()
    # assert opts.headless  # Operating in headless mode
    browser = Safari()

    browser.get(url)

    cards = []
    i = 0
    # for card_label in card_container.find_elements_by_xpath('//input[@type="checkbox"]'):
    while True:
        calculate_button = browser.find_element_by_xpath(
            '/html/body/main/form/div[2]/div/div[2]/div[2]/button')
        card_buttons = browser.find_elements_by_xpath(
            '/html/body/main/form/div[1]/div/div[2]/div/div[2]/label/span')
        card_button = card_buttons[i]

        coins = []
        card = Card(name=card_button.get_attribute("innerText"), coins=coins)
        print(f'Card: {card.name}')

        # enable
        card_button.click()
        sleep(2)
        calculate_button.click()
        sleep(13)
        coin_trs = browser.find_elements_by_xpath(
            '//tr[@class="line-middle table__middle-row border-0"]')
        print(f'Coin count: {len(coin_trs)}')

        for coin_tr in coin_trs:
            name = coin_tr.find_element_by_xpath('./td[1]/div/div/span[1]')
            algorithm = coin_tr.find_element_by_xpath(
                './td[1]/div/div/span[2]')
            mined_24h = coin_tr.find_element_by_xpath('./td[2]')
            revenue_24h = coin_tr.find_element_by_xpath('./td[4]')
            profit_24h = coin_tr.find_element_by_xpath('./td[5]')
            coin = Coin(name=name.get_attribute("innerText"),
                        algorithm=algorithm.get_attribute("innerText"),
                        mined_24h=float(mined_24h.get_attribute(
                            "innerText").split()[0]),
                        revenue_24h=float(
                            revenue_24h.get_attribute("innerText")[1:]),
                        profit_24h=float(profit_24h.get_attribute("innerText")[1:]))
            print(coin)
            coins.append(coin)

        cards.append(card)

        # disable
        card_buttons = browser.find_elements_by_xpath(
            '/html/body/main/form/div[1]/div/div[2]/div/div[2]/label/span')
        card_button = card_buttons[i]
        card_button.click()

        i += 1
        # Stop if all cards are scraped
        if i == len(card_buttons):
            break

    browser.close()

    now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    scraped_dir = Path('scraped_data')
    scraped_dir.mkdir(exist_ok=True)
    file = scraped_dir / f'scraped_data/{now_str}.yml'

    print(f'Writing {file}')
    file.write_text(yaml.dump(cards))


if __name__ == '__main__':
    main()
