"""
Common constants and choices used across the application
"""

# Pakistan Regions - Single source for PK states and cities
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

# Generate STATE_CHOICES for forms
STATE_CHOICES = [("", "Select State / Province")] + [
    (state, state) for state in PAKISTAN_REGIONS.keys()
]

# Generate CITY_CHOICES for forms
CITY_CHOICES = [("", "Select City")]
for state_cities in PAKISTAN_REGIONS.values():
    CITY_CHOICES.extend((city, city) for city in state_cities)
