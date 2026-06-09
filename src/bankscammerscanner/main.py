#!/usr/bin/env python
import warnings
from datetime import datetime
from bankscammerscanner.crew import BankScamShieldCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the crew locally via terminal."""
    print("## BankScamShield: Agentic Security Analysis ##")
    print("-----------------------------------------------")

    msg = input("Paste the suspicious message: ")
    sender = input("Enter the Sender ID/Number (or press Enter for 'Unknown'): ")

    inputs = {
        'message_text': msg,
        'sender_id': sender if sender else "Unknown",
        'current_year': str(datetime.now().year)
    }

    try:
        result = BankScamShieldCrew().crew().kickoff(inputs=inputs)

        print("\n\n" + "="*30)
        print("FINAL SECURITY BRIEFING")
        print("="*30 + "\n")
        print(result)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run()