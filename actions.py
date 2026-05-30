from googleapiclient.errors import HttpError

def apply_actions(service, decisions, dry_run=True, permanent_delete=False):
    for item in decisions:
        email_id = item['id']
        action = item['action']
        print(f"[{action}] {email_id} — {item['reason']}")
        
        
        if dry_run:
            continue  # preview only

        try:
            if action == 'ARCHIVE':
                service.users().messages().modify(
                    userId='me', id=email_id,
                    body={'removeLabelIds': ['INBOX']}
                ).execute()
            elif action == 'DELETE':
                if permanent_delete:
                    # Delete permanently
                    service.users().messages().delete(
                    userId='me',
                    id=email_id).execute()
                else:
                    # Moves to trash folder
                    service.users().messages().trash(
                        userId='me', id=email_id
                    ).execute()
            # KEEP: do nothing
        except HttpError as e:
            print(f"Skipping {email_id}: {e}")
            continue