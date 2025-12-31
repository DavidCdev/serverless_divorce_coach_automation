# audit.py
import hashlib

def compute_event_hash(deadline, rule, send_date):
    ''' 
    Deduplication event hash: sensitive-details-free. Combine deadline id, rule id, send ISO date.
    '''
    s = f"{deadline['id']}|{rule.id}|{str(send_date)}"
    return hashlib.sha256(s.encode()).hexdigest()


