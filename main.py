import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Country to currency mapping
country_currency = {
    "USA": "USD", "Canada": "CAD", "Mexico": "MXN", "Brazil": "BRL", "Argentina": "ARS",
    "UK": "GBP", "France": "EUR", "Germany": "EUR", "Italy": "EUR", "Spain": "EUR",
    "Switzerland": "CHF", "Sweden": "SEK", "Norway": "NOK", "Russia": "RUB",
    "China": "CNY", "Japan": "JPY", "South Korea": "KRW", "India": "INR", "Pakistan": "PKR",
    "Bangladesh": "BDT", "Nepal": "NPR", "Sri Lanka": "LKR", "KSA": "SAR", "UAE": "AED",
    "Qatar": "QAR", "Kuwait": "KWD", "Oman": "OMR", "Iran": "IRR", "Iraq": "IQD",
    "Egypt": "EGP", "South Africa": "ZAR", "Nigeria": "NGN", "Kenya": "KES",
    "Turkey": "TRY", "Australia": "AUD", "New Zealand": "NZD", "Singapore": "SGD",
    "Malaysia": "MYR", "Indonesia": "IDR", "Vietnam": "VND", "Thailand": "THB",
    "Philippines": "PHP", "Poland": "PLN", "Czech Republic": "CZK", "Hungary": "HUF",
    "Romania": "RON", "Israel": "ILS", "Ukraine": "UAH", "Venezuela": "VES",
    "Colombia": "COP", "Chile": "CLP"
}

currency_country = {v: k for k, v in country_currency.items()}


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💱 Currency Converter")
        self.root.geometry("500x550")
        self.root.configure(bg="#1e1e1e")

        # Dark Theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#1e1e1e", foreground="white", fieldbackground="#2e2e2e")
        style.configure("TButton", background="#333", foreground="white")
        style.configure("TLabel", background="#1e1e1e", foreground="white")
        style.configure("TEntry", fieldbackground="#2e2e2e", foreground="white")
        style.map("TButton", background=[("active", "#444")])

        # Title
        ttk.Label(root, text="Currency Converter", font=("Segoe UI", 18, "bold")).pack(pady=10)

        # Amount input
        self.amount_var = tk.StringVar()
        ttk.Label(root, text="Amount:").pack()
        ttk.Entry(root, textvariable=self.amount_var).pack()

        # Country selection
        ttk.Label(root, text="From Country:").pack(pady=(10, 0))
        self.from_country = ttk.Combobox(root, values=list(country_currency.keys()), state="readonly")
        self.from_country.pack()
        self.from_country.bind("<<ComboboxSelected>>", self.update_from_currency)

        ttk.Label(root, text="To Country:").pack(pady=(10, 0))
        self.to_country = ttk.Combobox(root, values=list(country_currency.keys()), state="readonly")
        self.to_country.pack()
        self.to_country.bind("<<ComboboxSelected>>", self.update_to_currency)

        # Convert button
        ttk.Button(root, text="Convert", command=self.convert).pack(pady=10)

        # Result label
        self.result_label = ttk.Label(root, text="", font=("Segoe UI", 12))
        self.result_label.pack(pady=10)

        ttk.Separator(root, orient='horizontal').pack(fill='x', pady=15)

        # COUNTRY TO CURRENCY LOOKUP
        ttk.Label(root, text="🔍 Country to Currency").pack()
        self.ctc_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.ctc_var).pack()
        ttk.Button(root, text="Lookup", command=self.lookup_currency).pack(pady=5)
        self.ctc_result = ttk.Label(root, text="")
        self.ctc_result.pack()

        # CURRENCY TO COUNTRY LOOKUP
        ttk.Label(root, text="🔍 Currency to Country").pack(pady=(20, 0))
        self.cty_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.cty_var).pack()
        ttk.Button(root, text="Lookup", command=self.lookup_country).pack(pady=5)
        self.cty_result = ttk.Label(root, text="")
        self.cty_result.pack()

    def update_from_currency(self, event):
        self.from_curr = country_currency.get(self.from_country.get(), "")

    def update_to_currency(self, event):
        self.to_curr = country_currency.get(self.to_country.get(), "")

    def convert(self):
        try:
            amount = float(self.amount_var.get())
            from_curr = country_currency.get(self.from_country.get(), "")
            to_curr = country_currency.get(self.to_country.get(), "")

            if not from_curr or not to_curr:
                raise ValueError("Missing currency codes.")

            url = f"https://v6.exchangerate-api.com/v6/36e633b1a8bfd73363fa4f05/latest/{from_curr}"
            response = requests.get(url)
            data = response.json()

            if data["result"] != "success":
                raise Exception("API Error")

            rate = data["conversion_rates"].get(to_curr)
            if not rate:
                raise Exception("Rate not available.")

            converted = amount * rate
            self.result_label.config(
                text=f"{amount:.2f} {from_curr} = {converted:.2f} {to_curr}"
            )

        except ValueError:
            messagebox.showerror("Error", "Enter valid number and select countries.")
        except Exception as e:
            messagebox.showerror("Conversion Failed", str(e))

    def lookup_currency(self):
        country = self.ctc_var.get().strip().title()
        code = country_currency.get(country)
        if code:
            self.ctc_result.config(text=f"{country} → 💱 {code}")
        else:
            self.ctc_result.config(text="❌ Country not found.")

    def lookup_country(self):
        code = self.cty_var.get().strip().upper()
        country = currency_country.get(code)
        if country:
            self.cty_result.config(text=f"{code} → 🌍 {country}")
        else:
            self.cty_result.config(text="❌ Currency code not found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
