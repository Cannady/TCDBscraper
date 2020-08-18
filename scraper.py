from bs4 import BeautifulSoup
import requests


domain = "https://www.tcdb.com"


def __get_soup(url: str):
    c = requests.get(url)
    return BeautifulSoup(c.text, features="html.parser")


def get_sets(sport: str, year: int):
    link = f"https://www.tcdb.com/ViewAll.cfm/sp/{sport.capitalize()}/year/{year}"
    soup = __get_soup(link)
    ul = soup.find_all("div", class_="block1")[1].find("ul")
    sets = {li.find("a").text: {"url": domain + (li.find("a")["href"]).replace("ViewSet.cfm", "Checklist.cfm")} for li in ul.find_all("li")}

    return sets


def get_cards(set_url: str):
    pages = 1
    soup = __get_soup(set_url)
    p = soup.find("a", text="»")
    if p is not None:
        pages = int(p["href"][p["href"].rfind("=") + 1:])
    card_urls = []
    for i in range(pages):
        p_no = i + 1
        if p_no != 1:
            soup = __get_soup(set_url + '?PageIndex=' + str(p_no))
        main_div = soup.find("div", class_="col-md-6 nopadding")
        table = main_div.find_all("table")[1]
        card_urls += [domain + tr.find("a", href=True)["href"] for tr in table.find_all("tr")]
    return card_urls


def get_card_info(card_url: str, card_set=None, card_year=None):
    card_info = {
        "url": card_url,
        "set": card_set,
        "year": card_year,
        "card_number": None,
        "subject": None,
        "front_image_url": None,
        "back_image_url": None,
    }
    soup = __get_soup(card_url)
    main_block = soup.find("div", class_="col-md-9 nopadding").find("div", class_="block1")
    title = soup.find("h4", class_="site")
    card_info['card_number'] = title.text[title.text.find("#"):title.text.find(" ")]
    card_info['subject'] = title.text[title.text.find("- ") + 2:title.text.rfind(" -")].replace("\n", "").replace("\r", "")
    imgs = main_block.find_all("img")
    card_info['front_image_url'] = domain + imgs[0]['src']
    card_info['back_image_url'] = domain + imgs[1]['src']

    return card_info
