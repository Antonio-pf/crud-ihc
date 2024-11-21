import requests
from .models import db, ExchangeRate

API_URL = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"  

def import_exchange_rates():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        for key, item in data.items():  
            
            existing_rate = ExchangeRate.query.filter_by(currency=item['code']).first()
            
            if existing_rate:
                existing_rate.value = item['bid']
                existing_rate.date = item['create_date']
                existing_rate.pctChange = item['pctChange']
            else:
                # If no entry exists, create a new one
                exchange_rate = ExchangeRate(
                    currency=item['code'],
                    value=item['bid'],       
                    date=item['create_date'] ,
                    pctChange=item['pctChange']
                )
                db.session.add(exchange_rate)
        
        db.session.commit()
    else:
        print(f"Error importing exchange rates: {response.status_code}")
