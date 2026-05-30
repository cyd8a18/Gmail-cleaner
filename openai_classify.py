import json
from openai import OpenAI

client = OpenAI()

def classify_emails(emails):
    email_list = "\n\n".join([
        f"ID: {e['id']}\nFrom: {e['from']}\nSubject: {e['subject']}\nPreview: {e['snippet']}"
        for e in emails
    ])

    prompt = f"""
You are cleaning an old Gmail inbox aggressively.

The user ONLY wants to preserve emails that are genuinely important.

PRIORITY RULES:
- When uncertain, DELETE.
- Only KEEP emails that clearly match the KEEP rules.
- Most emails should be DELETE.
- ARCHIVE should be used rarely.

KEEP ONLY:
- University or academic records, transcripts, tuition, graduation, certificates.
- Health documents, hospital records, insurance, prescriptions, appointments.
- Academic papers, manuals, technical documentation, invoices for expensive purchases.
- Banking, contracts, legal documents.
- Flight tickets, hotel reservations, or travel documents from the last 6 months or future trips.
- Personal emails from real people that appear meaningful.

DELETE:
- ALL newsletters.
- ALL promotions.
- ALL marketing emails.
- ALL social media notifications.
- ALL noreply emails unless they match KEEP.
- ALL app progress emails (Duolingo, Fitbit, achievements, streaks, summaries).
- ALL shopping notifications.
- ALL discount emails.
- ALL old transactions older than 6 months.
- ALL emails before 2019 unless they clearly match KEEP.
- ALL spam or low-value emails.

ALWAYS DELETE emails from:
- amazon
- facebook
- x
- duolingo

ARCHIVE:
- Use only for emails that are not important enough to KEEP but may still have some small future value.

The desired behavior is:
- KEEP very few emails.
- DELETE most emails.
- ARCHIVE occasionally.

Return ONLY valid JSON:
[
  {{"id":"...","action":"KEEP|ARCHIVE|DELETE","reason":"..."}}
]

Emails:
{email_list}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return json.loads(response.output_text)