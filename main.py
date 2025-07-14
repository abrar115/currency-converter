import requests

country_currency = {
    "usa": "USD",
    "canada": "CAD",
    "mexico": "MXN",
    "brazil": "BRL",
    "argentina": "ARS",
    "uk": "GBP",
    "france": "EUR",
    "germany": "EUR",
    "italy": "EUR",
    "spain": "EUR",
    "portugal": "EUR",
    "netherlands": "EUR",
    "belgium": "EUR",
    "switzerland": "CHF",
    "sweden": "SEK",
    "norway": "NOK",
    "denmark": "DKK",
    "russia": "RUB",
    "china": "CNY",
    "japan": "JPY",
    "south_korea": "KRW",
    "north_korea": "KPW",
    "india": "INR",
    "pakistan": "PKR",
    "bangladesh": "BDT",
    "nepal": "NPR",
    "sri_lanka": "LKR",
    "ksa": "SAR",
    "uae": "AED",
    "qatar": "QAR",
    "kuwait": "KWD",
    "oman": "OMR",
    "iran": "IRR",
    "iraq": "IQD",
    "egypt": "EGP",
    "south_africa": "ZAR",
    "nigeria": "NGN",
    "kenya": "KES",
    "turkey": "TRY",
    "australia": "AUD",
    "new_zealand": "NZD",
    "singapore": "SGD",
    "malaysia": "MYR",
    "indonesia": "IDR",
    "vietnam": "VND",
    "thailand": "THB",
    "philippines": "PHP",
    "poland": "PLN",
    "czech_republic": "CZK",
    "hungary": "HUF",
    "romania": "RON",
    "israel": "ILS",
    "ukraine": "UAH",
    "venezuela": "VES",
    "colombia": "COP",
    "chile": "CLP"
}

def convert(amount, c1, c2, use_country):
    try:
        if use_country == "n":
            base = country_currency.get(c1.lower())
            target = country_currency.get(c2.lower())
        else:
            base = c1.upper()
            target = c2.upper()

        if not base or not target:
            print("❌ Invalid currency or country name.")
            return

        link = f"https://v6.exchangerate-api.com/v6/36e633b1a8bfd73363fa4f05/latest/{base}"
        response = requests.get(link)
        data = response.json()

        if response.status_code != 200 or data.get("result") != "success":
            print("❌ Failed to fetch exchange rate.")
            return

        rate = data["conversion_rates"].get(target)
        if rate:
            print(f"💱 {amount} {base} = {amount * rate:.2f} {target}")
        else:
            print(f"❌ Currency code {target} not found in rates.")
    except Exception as e:
        print(f"❌ Error: {e}")

# === Main Program ===
print("===================================")
print("         💱 Currency Converter")
print("===================================")

use_country = input("Use country name or currency code? (N/C): ").strip().lower()
amount_input = input("Enter amount to convert: ").strip()
c1 = input("From currency or country: ").strip()
c2 = input("To currency or country: ").strip()

# Validate amount
if amount_input.isdigit() and int(amount_input) > 0:
    amount = int(amount_input)
    convert(amount, c1, c2, use_country)
else:
    print("❌ Enter a valid, positive amount.")
