# main.py
"""
Serverless workflow orchestrator for Clio deadlines → reminder scheduling → audit logging on Pipedream
"""
from clio import fetch_deadlines
from sheets import get_reminder_rules, log_audit, is_duplicate_hash
from ghl import send_ghl_message
from audit import compute_event_hash
import datetime, traceback


def main(pd: dict, env: dict):
    try:
        deadlines = fetch_deadlines(env)
        rules = get_reminder_rules(env)
        need_to_send = []
        today = datetime.date.today()
        for dl in deadlines:
            for rule in rules:
                if rule.matches(dl):
                    due_date = dl['date']
                    delta = (due_date - today).days
                    if delta == int(rule['DaysOut']):
                        ev_hash = compute_event_hash(dl, rule, today)
                        if not is_duplicate_hash(ev_hash, env):
                            need_to_send.append((dl, rule, ev_hash))

        for dl, rule, ev_hash in need_to_send:
            try:
                status, error = send_ghl_message(dl, rule, env)
            except Exception as send_exc:
                status, error = 'failure', str(send_exc)
            log_audit(ev_hash, dl['id'], rule['id'], status, error, env)
    except Exception as exc:
        log_audit('system', 'n/a', 'n/a', 'failure', traceback.format_exc(), env)
        raise
