import smtplib
from email.message import EmailMessage
import csv
import os
import time
# from dotenv import load_dotenv
# load_dotenv()

# -------- CONFIG --------
DRY_RUN = False   # Set to False to actually send emails
DELAY_SECONDS = 6  # Delay between emails to avoid rate limits

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

RESUME_LINK = "https://drive.google.com/file/d/1dYZZdwBXEOYBHB_QaFLGjE2zknlkoV2n/view?usp=drivesdk"

SUBJECT = "Backend Engineer - Exploring Opportunities"


# -------- HELPER FUNCTION --------
def extract_name(email):
    """Extracts a readable first name from email if CSV doesn't contain one."""
    name_part = email.split("@")[0]
    name_part = name_part.replace("_", ".")
    return name_part.split(".")[0].capitalize()


# -------- EMAIL SENDER --------
def send_email(to_email, recruiter_name):

    body = f"""Hi {recruiter_name},

I hope you're doing well!

My name is Riya Kesaria, and I am currently working as a Software Engineer at Jio Platforms, specializing in backend development.

I have 2+ years of experience building scalable backend systems using Java and Spring Boot. In my current role, I’ve worked on microservices handling 20K+ active users, designed and optimized REST APIs, improved performance, and implemented secure authentication mechanisms.

I’m currently exploring Backend / SDE-1 opportunities and would love to connect regarding relevant roles at your organization.

You can view my resume here:
{RESUME_LINK}

I’d be happy to have a quick chat if there’s a potential fit.

Best regards,  
Riya Kesaria  
+91-7309509080  
https://www.linkedin.com/in/riya-kesaria/  
https://github.com/kriyaaa
"""

    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    if DRY_RUN:
        print(f"[DRY RUN] Would send email to {recruiter_name} ({to_email})")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Sent email to {recruiter_name} ({to_email})")

    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")


# -------- MAIN --------
def main():
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("ERROR: Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
        return

    try:
        with open("recruiters.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                email = row.get("Email")
                name = row.get("FirstName") or extract_name(email)

                if email:
                    send_email(email, name)
                    time.sleep(DELAY_SECONDS)

    except FileNotFoundError:
        print("ERROR: recruiters.csv not found.")


if __name__ == "__main__":
    main()
