# sheets.py
import gspread
from google.oauth2.service_account import Credentials
import datetime

def get_gsheet(env, sheet_name):
    creds = Credentials.from_service_account_info(env['GS_CREDS'], scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
    ])
    client = gspread.authorize(creds)
    return client.open(env['GSHEET_DOC']).worksheet(sheet_name)

def get_reminder_rules(env):
    ws = get_gsheet(env, 'ReminderRules')
    rows = ws.get_all_records()
    class Rule:
        def __init__(self, row):
            self.type = row['Deadline Type']
            self.days_out = int(row['DaysOut'])
            self.channel = row['Channel']
            self.template_id = row['TemplateID']
            self.id = f"{self.type}-{self.days_out}-{self.channel}"
        def matches(self, deadline):
            return self.type == deadline['type']
        def __getitem__(self, key):
            return getattr(self, key)
    return [Rule(r) for r in rows]

def log_audit(hash, deadline_id, rule_id, status, error, env):
    ws = get_gsheet(env, 'AuditLog')
    timestamp = datetime.datetime.utcnow().isoformat()
    ws.append_row([hash, timestamp, deadline_id, rule_id, status, error])

def is_duplicate_hash(hash, env):
    ws = get_gsheet(env, 'AuditLog')
    all_hashes = [r[0] for r in ws.get_all_values()[1:]] # skip header
    return hash in all_hashes


