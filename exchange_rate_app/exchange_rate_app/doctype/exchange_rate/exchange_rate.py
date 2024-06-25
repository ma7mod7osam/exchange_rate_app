import requests
import frappe
from datetime import datetime

@frappe.whitelist()
def fetch_and_update_exchange_rate():
    url = "http://api.exchangerate.host/convert"
    params = {
        'access_key': '447208a764b5192e9fcc7f686c8ddcae',
        'amount': 1,
        'from': 'USD',
        'to': 'BHD'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    exchange_rate = data['info']['rate']
    
    create_currency_exchange_rate(exchange_rate)

def create_currency_exchange_rate(exchange_rate):
    exchange_rate_doc = frappe.get_doc({
        'doctype': 'Currency Exchange',
        'from_currency': 'USD',
        'to_currency': 'BHD',
        'exchange_rate': exchange_rate,
        'date': datetime.now().date()
    })
    
    exchange_rate_doc.insert()
    frappe.db.commit()
    frappe.msgprint("Exchange rate updated successfully")
