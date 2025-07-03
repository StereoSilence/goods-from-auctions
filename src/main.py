# src/main.py
# Точка входа для запуска скраппинга и обновления базы

from scraper.auction_scraper import AuctionScraper
from db.session import SessionLocal
from db.models import AuctionItem
from utils.average_price import get_average_price

def main():
    session = SessionLocal()
    scraper = AuctionScraper()
    items = scraper.fetch_latest_items()
    print(f"Получено позиций: {len(items)}")
    for item in items:
        # Проверяем, есть ли уже такая позиция по external_id
        exists = session.query(AuctionItem).filter_by(external_id=item['external_id']).first()
        if not exists:
            print(f"Добавляю: {item['title']}")
            avg_price = get_average_price(item['title'])
            auction_item = AuctionItem(
                external_id=item['external_id'],
                title=item['title'],
                url=item['url'],
                current_price=item.get('current_price'),
                average_price=avg_price,
                start_price=item.get('start_price'),
            )
            session.add(auction_item)
    session.commit()
    print("Коммит выполнен.")
    # Проверка: вывести все записи
    all_items = session.query(AuctionItem).all()
    print(f"Всего записей в БД: {len(all_items)}")
    for i in all_items:
        print(i)
    session.close()

if __name__ == "__main__":
    main()
