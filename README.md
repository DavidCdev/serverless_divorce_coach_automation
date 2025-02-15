# Clio Deadline Reminder Orchestrator (Serverless, Python, Pipedream)

## Overview

This workflow automates deadline reminders for your legal practice, utilizing Clio for deadline data, Google Sheets for flexible rule management, and GoHighLevel for client messaging—all on a serverless, auditable, and extendable stack.

**Workflow Architecture:**  
1. **Trigger:** Scheduled or webhook-triggered execution on Pipedream.  
2. **Fetch Deadlines:** Uses OAuth 2.0 to securely pull all relevant deadlines from Clio.  
3. **Fetch Reminder Rules:** Reads a Google Sheet for reminder/notification rules, allowing easy non-dev updates.  
4. **Deduplicate:** Cross-references logs to prevent duplicate sends.  
5. **Schedule & Send:** Schedules/sends reminders via GoHighLevel API.  
6. **Audit Logging:** All reminders are robustly audit-logged, with errors and successes, without persistently storing client-sensitive data.

---

## Features

- **No local/server database.** All state and audit logs use affordable/redundant storage (such as Google Sheets or Pipedream Data Store) storing only safe metadata (no client contacts or case data).
- **OAuth 2.0 with Clio:** Securely integrates with Clio’s API for deadline pulls, with token refresh.
- **Spreadsheet-Based Rules:** Easily tailor reminder logic with a Google Sheet (`ReminderRules`), e.g., “Send 3 days and 1 day before X type of deadline.”
- **Reliable Deduplication:** Each sent reminder is logged with a hash (from non-personal fields: deadline ID, rule, timestamp), ensuring idempotency.
- **GoHighLevel Messaging:** Sends via GoHighLevel API (SMS, email, etc.) as per each rule.
- **Rich Logging:** Unified audit log with timestamps, actions, success/errors, and event hashes. Issues are flagged for follow-up.
- **Strong error handling:** All remote/API failures are logged, with automatic retries for transient faults.
- **Extendable:** Modular Python functions—swap out providers or add logic with minimal friction.

---

## Sheet Structure

**1. ReminderRules (Google Sheets)**
| Deadline Type | DaysOut | Channel    | TemplateID    |
|---------------|---------|------------|--------------|
| Court Date    | 3       | SMS        | ghl_sms_1     |
| Filing Date   | 1       | Email      | ghl_email_2   |
| ...           | ...     | ...        | ...           |

**2. AuditLog (Google Sheets or Pipedream Data Store)**
| Hash                            | Timestamp (ISO)     | DeadlineID | RuleID | Status    | Error Details  |
|----------------------------------|---------------------|------------|--------|-----------|----------------|
| 57ef3c6bb9e820...                | 2024-05-20T16:12Z   | 1245       | SMS-3d | success   |                |
|                                  
---

## How It Works

1. **Fetch Deadlines:**  
   Authenticates via Clio OAuth 2.0 and collects all open deadlines.

2. **Determine Reminders:**  
   For each deadline, the system:
   - Checks all applicable rules from the Google Sheet.
   - For each rule (e.g., “SMS 3 days before”), computes if a send is due today.

3. **Deduplication Check:**  
   Computes an event hash (e.g., SHA256 of deadline id + rule + scheduled date). If this hash exists in the log, skips send.

4. **Schedule/Send:**  
   Calls GoHighLevel API to send the message via the defined channel/template.

5. **Log Result:**  
   Appends an entry in the AuditLog including the hash, result (success/failure), timestamp, and error info off-case data (no phone or email logged).

6. **Error/Alert:**  
   All send or sync failures are logged and can be optionally forwarded to an admin Slack/pager channel.

---

## Security & Privacy

- **No case-sensitive or client contact data stored** after orchestration.
- **OAuth tokens are handled using Pipedream’s managed secrets**.
- **Audit logs** only contain hashes, datestamps, and non-sensitive metadata.

---

## Easy Maintenance

- **Change rules anytime** in the connected Google Sheet—no redeployment needed.
- **Add new messaging platforms** or integrate with other API services by editing a single function.
- **Extend audit log storage** to other providers (BigQuery, Airtable, etc.) if needed.

---

## Deployment

- Clone this workflow in Pipedream.
- Connect/integrate Clio, Google Sheets, and GoHighLevel accounts using managed secrets/OAuth.
- Insert your Google Sheet links and GoHighLevel template IDs into the Pipedream step/environment variables.
- Copy the sample ReminderRules and AuditLog sheet structures.

---

## Special Features

- 🔑 **Real OAuth (Clio), no manual token handling**
- 🕒 **Audit logging with deduplication** (never double-message for the same rule)
- 🚫 **No retention of client contacts or case facts**
- 🧩 **Modular/extensible Python design**
- 📜 **Sheet-based rules for easy non-dev updates**
- ⚡ **Serverless + auto-scaled (never manage infra or scheduled jobs)**

---

## Support

Want to extend? Add a new column to your rules, or swap GoHighLevel for another sender in the message function. For error alerting (Slack/email), fork the error-handling step and plug in your target.

---

## Example Repo Structure

```
pipedream/
  └── main.py  # Orchestrates the workflow
  └── clio.py  # Clio API logic
  └── sheets.py  # Google Sheets API logic
  └── ghl.py    # GoHighLevel messaging
  └── audit.py  # Audit logging and deduplication functions
  └── README.md
```
