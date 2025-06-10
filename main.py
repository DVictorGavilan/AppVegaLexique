import json

from appvega import scraper


def main(target_url):
    data = scraper.download_data(target_url)
    return data


if __name__ == "__main__":
    vega_raw = []
    initial = 8000
    final = 17000
    for i in range(initial, final):
        print(i)
        try:
            vega_raw.append(main(f"https://app.vega-lexique.fr/?entries=w{i}"))
        except Exception as e:
            print(e)
    with open(f'output/raw/data_{initial}_{final}.json', 'w', encoding="utf-8") as file:
        json.dump(vega_raw, file, ensure_ascii=False, indent=2)
