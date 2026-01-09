from django import forms


# Single source for PK states and cities; used for choices and JS.
PAKISTAN_REGIONS = {
    "Punjab": [
        "Lahore",
        "Faisalabad",
        "Rawalpindi",
        "Gujranwala",
        "Multan",
        "Sialkot",
        "Bahawalpur",
        "Sargodha",
        "Sheikhupura",
        "Gujrat",
        "Jhelum",
        "Rahim Yar Khan",
        "Kasur",
    ],
    "Sindh": [
        "Karachi",
        "Hyderabad",
        "Sukkur",
        "Larkana",
        "Nawabshah",
        "Mirpur Khas",
        "Jacobabad",
        "Shikarpur",
        "Dadu",
    ],
    "Khyber Pakhtunkhwa": [
        "Peshawar",
        "Abbottabad",
        "Mardan",
        "Swat",
        "Kohat",
        "Dera Ismail Khan",
        "Haripur",
    ],
    "Balochistan": [
        "Quetta",
        "Gwadar",
        "Khuzdar",
        "Turbat",
        "Chaman",
        "Sibi",
    ],
    "Islamabad Capital Territory": ["Islamabad"],
    "Gilgit-Baltistan": ["Gilgit", "Skardu", "Hunza"],
    "Azad Jammu and Kashmir": ["Muzaffarabad", "Mirpur", "Kotli", "Rawalakot"],
}

STATE_CHOICES = [("", "Select State / Province")] + [
    (state, state) for state in PAKISTAN_REGIONS.keys()
]
CITY_CHOICES = [("", "Select City")]
for state_cities in PAKISTAN_REGIONS.values():
    CITY_CHOICES.extend((city, city) for city in state_cities)


class ShippingForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    company_name = forms.CharField(max_length=150, required=False)
    area_code = forms.CharField(max_length=10)
    primary_phone = forms.CharField(max_length=20)
    address_1 = forms.CharField(max_length=255)
    address_2 = forms.CharField(max_length=255, required=False)
    state = forms.ChoiceField(choices=STATE_CHOICES)
    city = forms.ChoiceField(choices=CITY_CHOICES)
    country = forms.ChoiceField(choices=[('', 'Select Country'), ('Pakistan', 'Pakistan')])
    zip_code = forms.CharField(max_length=20)
    business_address = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set common widget classes/ids for consistent styling and JS hooks.
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['area_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['address_1'].widget.attrs.update({'class': 'form-control m-b-10'})
        self.fields['address_2'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'id': 'city-select'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'id': 'state-select'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'id': 'country-select'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['business_address'].widget.attrs.update({'value': '1'})


PAYMENT_TYPE_CHOICES = [
    ('Cash on Delivery', 'Cash on Delivery'),
    ('Stripe', 'Stripe'),
    ('Paypal', 'Paypal'),
    ('Visa', 'Visa'),
    ('Master Card', 'Master Card'),
    ('Credit Card', 'Credit Card'),
]


class PaymentForm(forms.Form):
    cardholder = forms.CharField(max_length=200, required=False)
    cardnumber = forms.CharField(max_length=20, required=False)
    payment_type = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES)
    mm = forms.CharField(max_length=2, required=False)
    yy = forms.CharField(max_length=2, required=False)
    csc = forms.CharField(max_length=4, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cardholder'].widget.attrs.update({'class': 'form-control required', 'placeholder': 'Cardholder Name'})
        self.fields['cardnumber'].widget.attrs.update({'class': 'form-control required', 'placeholder': 'Card Number'})
        self.fields['payment_type'].widget.attrs.update({'data-id': 'payment-type'})
        self.fields['payment_type'].widget = forms.HiddenInput(attrs={'data-id': 'payment-type'})
        self.fields['mm'].widget.attrs.update({'class': 'form-control required p-l-5 p-r-5 text-center', 'placeholder': 'MM'})
        self.fields['yy'].widget.attrs.update({'class': 'form-control required p-l-5 p-r-5 text-center', 'placeholder': 'YY'})
        self.fields['csc'].widget.attrs.update({'class': 'form-control required p-l-5 p-r-5 text-center', 'placeholder': 'CSC'})