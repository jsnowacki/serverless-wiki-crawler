import datetime

import bs4
import wikipedia


def parse_main_pl():
    wikipedia.set_lang('pl')

    main_page = wikipedia.page('Wikipedia:Strona główna')

    soup = bs4.BeautifulSoup(main_page.html(), 'lxml')

    news = soup.find('div', {'id': 'main-page-news'})

    news_day = [n.text for n in news.findAll('li')]

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "lang": "pl",
        "url": main_page.url,
        "title": main_page.title,
        "content": {
            "news": news_day
        }
    }


def parse_main(lang):
    if lang == 'pl':
        return parse_main_pl()
    else:
        return None


if __name__ == '__main__':
    print(parse_main('pl'))
