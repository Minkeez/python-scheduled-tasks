##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import datetime as dt
import pandas as pd
import os
import random
import smtplib

from pathlib import Path

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

folder_path = Path("./letter_templates")
files_list = [f.name for f in folder_path.iterdir() if f.is_file()]

today = dt.date.today()

df = pd.read_csv("birthdays.csv")
birthdays = df.to_dict(orient="records")
for birthday in birthdays:
    name = birthday["name"]
    email = birthday["email"]
    year = birthday["year"]
    month = birthday["month"]
    day = birthday["day"]
    birthday = dt.date(year, month, day)

    is_birthday = (today.month, today.day) == (birthday.month, birthday.day)
    if is_birthday:
        random_file = random.choice(files_list)

        with open(f"./letter_templates/{random_file}", "r") as file:
            content = file.read().replace("[NAME]", name)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(MY_EMAIL, MY_PASSWORD)
            smtp.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email,
                msg=f"Subject:Happy Birthday!\n\n{content}",
            )