# utils.py
def format_currency(amount):
    formatted_amount = f"{amount:.2f}"
    whole, decimal = formatted_amount.split('.')
    formatted_whole = f"{int(whole):,}".replace(',', '.')
    return f"${formatted_whole},{decimal}"
