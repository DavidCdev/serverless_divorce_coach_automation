# test_mock.py
import datetime
from main import main

def get_env():
    return {
        'CLIO_ACCESS_TOKEN': 'test-token',
        'GOHIGHLEVEL_API_KEY': 'ghl-token',
        'GSHEET_DOC': 'TEST_DOC',
        'GS_CREDS': {
            # Put mock or testing Google Service Account dict here or mock gspread
        }
    }

def test_main():
    # Set up mock pd for Pipedream event input if needed
    pd = {}
    env = get_env()
    # You should mock out clio, sheets, ghl imports for pure test
    try:
        main(pd, env)
        print('Workflow ran (mock)')
    except Exception as e:
        print('Workflow error:', str(e))

if __name__ == "__main__":
    test_main()