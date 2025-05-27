import pandas as pd
import os
import shutil
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(50)
random.seed(50)

# Number of records per country
num_records = 1000000

# Country code and number formats
country_mobile_formats = {
    "BE": "+32 4{0:02d} {1:03d} {2:03d}",
    "FR": "+33 6 {0:02d} {1:02d} {2:02d} {3:02d}",
    "DE": "+49 15{0:01d} {1:03d} {2:04d}",
    "CH": "+41 7{0:01d} {1:03d} {2:02d} {3:02d}",
    "IT": "+39 3{0:02d} {1:03d} {2:03d}",
    "ES": "+34 6{0:01d} {1:02d} {2:02d} {3:02d}",
    "MA": "+212 6{0:01d} {1:02d} {2:02d} {3:02d}",
    "UK": "+44 7{0:02d} {1:03d} {2:04d}",
    "SE": "+46 7{0:01d} {1:03d} {2:03d}",
    "PT": "+351 9{0:02d} {1:03d} {2:03d}",
    "NL": "+31 6 {0:02d} {1:03d} {2:03d}"
}

# Kies een land
print("Beschikbare landen:", ", ".join(country_mobile_formats.keys()))
country_code = input("Voer een landcode in (bijv. NL, BE, PT): ").upper()

if country_code not in country_mobile_formats:
    print("❌ Ongeldige landcode.")
    exit()

# Nummergenerator op basis van landcode
def generate_mobile_number(code):
    fmt = country_mobile_formats[code]
    if code == "BE":
        return fmt.format(random.randint(70, 99), random.randint(100, 999), random.randint(100, 999))
    elif code == "FR":
        return fmt.format(*(random.randint(0, 99) for _ in range(4)))
    elif code == "DE":
        return fmt.format(random.randint(0, 9), random.randint(100, 999), random.randint(1000, 9999))
    elif code == "CH":
        return fmt.format(random.randint(0, 9), random.randint(100, 999), random.randint(0, 99), random.randint(0, 99))
    elif code == "IT":
        return fmt.format(random.randint(0, 99), random.randint(100, 999), random.randint(100, 999))
    elif code == "ES" or code == "MA":
        return fmt.format(*(random.randint(0, 99) for _ in range(4)))
    elif code == "UK":
        return fmt.format(random.randint(0, 99), random.randint(100, 999), random.randint(1000, 9999))
    elif code == "SE":
        return fmt.format(random.randint(0, 9), random.randint(100, 999), random.randint(100, 999))
    elif code == "PT" or code == "NL":
        return fmt.format(random.randint(0, 99), random.randint(100, 999), random.randint(100, 999))

# Gegevens genereren
data = {
    "COUNTRY CODE": [],
    "MOBILE NUMBER": [],
    "SONG NUMBER": [],
    "TIMESTAMP": []
}

now = datetime.now()
for _ in range(num_records):
    data["COUNTRY CODE"].append(country_code)
    data["MOBILE NUMBER"].append(generate_mobile_number(country_code))
    data["SONG NUMBER"].append(random.randint(1, 25))
    timestamp = now - timedelta(seconds=random.randint(0, 3600))
    data["TIMESTAMP"].append(timestamp.strftime('%Y-%m-%dT%H:%M:%S'))

df = pd.DataFrame(data)

# Opslaan
output_filename = f"generated_votes_{country_code}.txt"
df.to_csv(output_filename, index=False, header=False)
print(f"\n✅ Bestand '{output_filename}' is opgeslagen met {num_records} stemmen voor {country_code}.")



# Zorg dat output directory bestaat
output_dir = os.path.expanduser("~/EUV_TEST/euv-pipeline/repo_2_shuffle_1")
os.makedirs(output_dir, exist_ok=True)

# Bestand dat je wilt opslaan
output_file_path = os.path.join(output_dir, f"generated_votes_{country_code}.txt")

# Sla dataframe eerst lokaal op in huidige map
local_filename = f"generated_votes_{country_code}.txt"
df.to_csv(local_filename, index=False, header=False)

# Kopieer het bestand naar stap 2 directory
shutil.copy(local_filename, output_file_path)

#print(f"\n✅ Bestand '{local_filename}' is opgeslagen met {num_records} stemmen voor {country_code}.")
print(f"📁 Bestand is gekopieerd naar repo_2_shuffle_1: {output_file_path}")

