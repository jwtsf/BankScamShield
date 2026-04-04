#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
# Note: Ensure the import matches your actual project folder name
from bankscammerscanner.crew import BankScamShieldCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew locally via terminal for testing.
    """
    print("## BankScamShield: Agentic Security Analysis ##")
    print("-----------------------------------------------")
    
    # These inputs simulate what the user will eventually type into your website
    msg = input("Paste the suspicious message: ")
    sender = input("Enter the Sender ID/Number (or press Enter for 'Unknown'): ")

    inputs = {
        'message_text': msg,
        'sender_id': sender if sender else "Unknown",
        'current_year': str(datetime.now().year)
    }

    try:
        # Kickoff the crew and get the result
        result = BankScamShieldCrew().crew().kickoff(inputs=inputs)
        
        print("\n\n" + "="*30)
        print("FINAL SECURITY BRIEFING")
        print("="*30 + "\n")
        print(result)
        
    except Exception as e:
        print(f"Error: {e}")

def train():
    """
    (Optional) Not required for your weekend project.
    """
    print("Training mode is not configured for this project version.")

def replay():
    """
    (Optional) Not required for your weekend project.
    """
    print("Replay mode is not configured for this project version.")

def test():
    """
    (Optional) Not required for your weekend project.
    """
    print("Test mode is not configured for this project version.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If you run 'crewai run', it usually defaults to calling run()
        if sys.argv[1] == "train":
            train()
        elif sys.argv[1] == "replay":
            replay()
        elif sys.argv[1] == "test":
            test()
        else:
            run()
    else:
        run()