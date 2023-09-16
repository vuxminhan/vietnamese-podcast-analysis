import os
import pandas as pd
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()
PATH = os.environ.get('P')

# Change directory to the path
os.chdir(PATH)

# Import your translation function (update this import accordingly)
from utils import translate_text

# Load the CSV file
file_path = os.path.join(PATH, 'modules/spotify/spotify_with_language.csv')
df = pd.read_csv(file_path)
vi_df = df[df['language'] == 'vi']


# Define a translation function
def translate_row(row):
    row['name'] = translate_text(row['name'])
    print(f"Translated row with name: {row['name']}")
    return row

# Multithreaded translation for vi_df
with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers as needed
    vi_df = pd.concat(executor.map(translate_row, vi_df.to_dict('records')))
    print("Translation of Vietnamese names completed.")


vi_df.to_csv(os.path.join(PATH, 'modules/spotify/vi_spotify_name_translated.csv'), index=False)
print("Data saved.")
