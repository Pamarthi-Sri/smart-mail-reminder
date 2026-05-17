import schedule
import time

from mailapp.gmail_reader import read_emails

schedule.every(30).seconds.do(read_emails)

print("Mail checker started...")

while True:
    schedule.run_pending()
    time.sleep(1)