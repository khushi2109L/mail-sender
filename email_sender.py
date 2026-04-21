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

RESUME_LINK = "https://drive.google.com/file/d/1GXsBwwCUo8LzAHQ7ID52CPmZT5N8Mnp6/view?usp=drivesdk"

SUBJECT = "Seeking Career Opportunities for Data Analyst role"


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

My name is Shreya Srivastava, and I am currently working as a Data Analyst at Jio Platforms.

I have 2+ years of experience working with large-scale user data, analyzing 3M+ daily users and 2M+ survey responses to derive actionable insights. In my current role, I have defined KPIs across multiple product modules, built dashboards for 300K+ daily users, and improved response relevance by 25% through data-driven analysis and visualization.

My skill set includes SQL, Python, Power BI, Excel, and data visualization tools like Matplotlib, Apache Superset and Databricks. I have also worked on projects involving customer behavior analysis and market insights, helping drive data-backed decisions.

I am currently exploring Data Analyst opportunities and would love to connect regarding relevant roles at your organization.

You can view my resume here:
{RESUME_LINK}

I’d be happy to have a quick chat if there’s a potential fit.

Best regards,  
Shreya Srivastava  
+91-7021829256  
https://www.linkedin.com/in/shreyaa2109/
https://github.com/khushi2109L
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
