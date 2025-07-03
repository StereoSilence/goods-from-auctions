# src/scraper/auction_scraper.py
# Класс для скраппинга сайта justiz-auktion.de
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class AuctionScraper:
    BASE_URL = "https://www.justiz-auktion.de/neu-eingestellt"

    def fetch_latest_items(self):
        """
        Получить новые позиции с главной страницы или раздела аукционов.
        Возвращает список словарей с данными позиций.
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.BASE_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        seen_ids = set()
        for link in soup.find_all("a", title="Zur Auktion"):
            title = link.get_text(strip=True)
            href = link.get("href")
            if href and title:
                ext_id = href.split("-")[-1]
                if ext_id.isdigit() and ext_id not in seen_ids and title.lower() != "details":
                    seen_ids.add(ext_id)
                    lot_url = "https://www.justiz-auktion.de/" + href
                    start_price, current_price = self.get_prices(lot_url, headers)
                    items.append({
                        "external_id": ext_id,
                        "title": title,
                        "url": lot_url,
                        "current_price": current_price,
                        "start_price": start_price,
                    })
        return items

    def get_prices(self, url, headers):
        try:
            html = get_html_selenium(url)
            soup = BeautifulSoup(html, 'html.parser')
            # Стартовая цена
            start_price = None
            for p in soup.find_all("p"):
                if p.text.strip().startswith("Startgebot:"):
                    start_price = float(
                        p.text.strip().split(":")[1].replace("€", "").replace(".", "").replace(",", ".").strip()
                    )
                    break
            # Текущая цена
            current_price = None
            gebot = soup.find("p", class_="gebot")
            if gebot:
                current_price = float(
                    gebot.text.replace("€", "").replace(".", "").replace(",", ".").strip()
                )
            print(f"[DEBUG] {url} -> start_price: {start_price}, current_price: {current_price}")
            return start_price, current_price
        except Exception as e:
            print(f"Ошибка при получении цен: {e}")
        return None, None

from selenium.webdriver.chrome.service import Service

def get_html_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("C:/Users/Alex/Desktop/justiz-auktion/chrome-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    input("Откройте браузер, пройдите капчу/авторизацию если нужно, затем нажмите Enter...")
    html = driver.page_source
    driver.quit()
    return html