from auth_fetch import *
from openai_classify import *
from actions import *

BATCH_SIZE    = 100
MAX_RESULTS   = 4000
PERMANENT_DEL = False 

if __name__ == '__main__':
    service = get_gmail_service()

    emails = fetch_emails(service, max_results=MAX_RESULTS)
    print(len(emails))

    for i in range(0, len(emails), BATCH_SIZE):
        batch = emails[i:i+BATCH_SIZE]
        print(f"\nProcessing batch {i//BATCH_SIZE + 1}/{MAX_RESULTS//BATCH_SIZE}...")

        decisions = classify_emails(batch)

        # Apply actions for this batch
        apply_actions(service, decisions, dry_run=False, permanent_delete=PERMANENT_DEL)
