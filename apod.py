# A python app to retrieve the NASA astronomical picture of the day as an
# exercise in acessing REST APIs.
# 2022-08-02

import requests
import sys
import os
from datetime import date
from mimetypes import guess_extension



def get_app_path():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path




app_path = get_app_path()

# Get API key from apikey file in script path
# (See apikey.example)
try:
    print(f'Fetching API key from "{app_path}{os.sep}apikey.txt"')
    with open(f'{app_path}{os.sep}apikey.txt', 'r') as apikey_file:
        api_key=apikey_file.read().strip()
    print(f'API key is "{api_key}"')
except:
    print("No apikey.txt file found.")
    sys.exit()

api_parms = {
    'api_key':      api_key,
    'date':         date.today().strftime("%Y-%m-%d")
}
api_url = f'https://api.nasa.gov/planetary/apod'

save_path = f'{app_path}{os.sep}received{os.sep}' 
save_file = f'{save_path}apod-{api_parms["date"]}'

print(f'Requesting data from {api_url}...')
# Do get request on URL
resp = requests.api.get(url=api_url, params=api_parms)

# If there was an error
if(resp.status_code != 200):
    print(resp.reason)
    sys.exit()

# Convert received JSON string to dictionary
data = resp.json()

# Get the image
im = requests.get(data["hdurl"])
#print(im.headers)
if im.status_code != 200:
    print(im.reason)
    sys.exit()

f_ext = guess_extension(im.headers["content-type"])

if not os.path.exists(save_path):
    os.mkdir(save_path)

print(f'Saving image to "{save_file}{f_ext}..."\n')
with open(rf'{save_file}{f_ext}', 'wb') as f:
    f.write(im.content)

output_str = \
f'{data["title"]} - {data["date"]}\n\n\
{data["explanation"]}\n\n\
(c) {data["copyright"]}'
print(output_str)
print(f'\nSaving description to "{save_file}.txt..."')
with open(rf'{save_file}.txt', 'w') as f:
    f.write(output_str)