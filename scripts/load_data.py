import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Restaurant
from app.database import Base

# Create tables
Base.metadata.create_all(bind=engine)

def load_data(csv_path):
    df = pd.read_csv(csv_path)

    # Clean missing values
    df = df.fillna('')

    db: Session = SessionLocal()
    for _, row in df.iterrows():
        restaurant = Restaurant(
            id=row['Restaurant ID'],
            name=row['Restaurant Name'],
            country_code=row['Country Code'],
            city=row['City'],
            address=row['Address'],
            locality=row['Locality'],
            locality_verbose=row['Locality Verbose'],
            longitude=row['Longitude'],
            latitude=row['Latitude'],
            cuisines=row['Cuisines'],
            average_cost_for_two=row['Average Cost for two'],
            currency=row['Currency'],
            has_table_booking=row['Has Table booking'] == 'Yes',
            has_online_delivery=row['Has Online delivery'] == 'Yes',
            is_delivering_now=row['Is delivering now'] == 'Yes',
            switch_to_order_menu=row['Switch to order menu'] == 'Yes',
            price_range=row['Price range'],
            aggregate_rating=row['Aggregate rating'],
            rating_color=row['Rating color'],
            rating_text=row['Rating text'],
            votes=row['Votes']
        )
        db.add(restaurant)
    db.commit()
    db.close()

if __name__ == "__main__":
    load_data("data/zomato.csv")
