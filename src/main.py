# src/main.py
# Entry point for running scraping and updating the database

from scraper.auction_scraper import AuctionScraper
from db.session import SessionLocal
from db.models import AuctionItem
from utils.average_price import get_average_price

def main():
    session = SessionLocal()
    scraper = AuctionScraper()
    items = scraper.fetch_latest_items()
    print(f"Items fetched: {len(items)}")
    for item in items:
        # Check if this item already exists by external_id
        exists = session.query(AuctionItem).filter_by(external_id=item['external_id']).first()
        if not exists:
            print(f"Adding: {item['title']}")
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
    print("Commit completed.")
    # Check: print all records
    all_items = session.query(AuctionItem).all()
    print(f"Total records in DB: {len(all_items)}")
    for i in all_items:
        print(i)
    session.close()

if __name__ == "__main__":
    main()
