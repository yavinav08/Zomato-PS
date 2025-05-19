from django.core.management.base import BaseCommand
import pandas as pd
from zomato_restaurants.models import Restaurant

class Command(BaseCommand):
    help = 'Load Zomato data from CSV into the database'

    def handle(self, *args, **kwargs):
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv('data/zomato.csv', encoding=encoding).fillna('')
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                self.stdout.write(self.style.ERROR('❌ Could not read the CSV file with any of the attempted encodings'))
                return

            for _, row in df.iterrows():
                Restaurant.objects.update_or_create(
                    id=row['Restaurant ID'],
                    defaults={
                        'name': row['Restaurant Name'],
                        'country_code': row['Country Code'],
                        'city': row['City'],
                        'address': row['Address'],
                        'locality': row['Locality'],
                        'locality_verbose': row['Locality Verbose'],
                        'longitude': row['Longitude'],
                        'latitude': row['Latitude'],
                        'cuisines': row['Cuisines'],
                        'average_cost_for_two': row['Average Cost for two'],
                        'currency': row['Currency'],
                        'has_table_booking': row['Has Table booking'] == 'Yes',
                        'has_online_delivery': row['Has Online delivery'] == 'Yes',
                        'is_delivering_now': row['Is delivering now'] == 'Yes',
                        'switch_to_order_menu': row['Switch to order menu'] == 'Yes',
                        'price_range': row['Price range'],
                        'aggregate_rating': row['Aggregate rating'],
                        'rating_color': row['Rating color'],
                        'rating_text': row['Rating text'],
                        'votes': row['Votes'],
                    }
                )
            self.stdout.write(self.style.SUCCESS('✅ Zomato data loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error loading data: {str(e)}'))
