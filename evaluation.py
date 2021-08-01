from objects import Card, Coin
import yaml
from pprint import pprint
from pathlib import Path

from config import interesting_coins, card_prices


scraped_dir = Path('scraped_data')
evaluated_dir = Path('evaluated_data')


def get_coin(name, coins):
    try:
        return next(coin for coin in coins if coin.name == name)
    except StopIteration:
        return Coin('', '', 0, 0, 0)


def output_table(cards: list[Card], coin_key, file: Path):
    '''Creates a table with coins mapped by 'coin_key' and writes it as csv to 'file'.'''
    all_coin_names = interesting_coins.keys()

    head = ('Card', *all_coin_names)
    content = [(card.name, *[str(coin_key(get_coin(name, card.coins), card))
                for name in all_coin_names]) for card in cards]

    print(f'Writing {file}')
    file.write_text('\n'.join(([','.join(l) for l in [head, *content]])))


def evaluate_scraped_data(file: Path):
    print(f'Reading {file}')
    cards: list[Card] = yaml.load(file.read_text(), Loader=yaml.Loader)
    # print(cards)

    # Filter relevant cards and coins
    cards = list(filter(lambda card: card.name in card_prices, cards))
    for card in cards:
        card.coins = list(
            filter(lambda coin: coin.name in interesting_coins, card.coins))
        # card.coins.sort(key=lambda coin: coin.profit_24h, reverse=True)

    output_table(cards, coin_key=lambda coin, _: coin.profit_24h,
                 file=evaluated_dir / f'{file.stem}_profit.csv')
    output_table(cards, coin_key=lambda coin, card: round(card_prices[card.name] / coin.profit_24h) if coin.profit_24h > 0 else 0,
                 file=evaluated_dir / f'{file.stem}_roi.csv')
    print()


def main():
    assert scraped_dir.exists()
    evaluated_dir.mkdir(exist_ok=True)

    for scraped_data in scraped_dir.iterdir():
        evaluate_scraped_data(scraped_data)


if __name__ == '__main__':
    main()
