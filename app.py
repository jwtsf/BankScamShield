import time
from flask import Flask, render_template, request, jsonify
from bankscammerscanner.crew import BankScamShieldCrew
from database import init_db, log_scan, get_history

app = Flask(__name__)

# Initialize the database once when the server starts
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    try:
        # 1. Prepare inputs for CrewAI
        msg_content = data.get('message', '')
        sender_id = data.get('sender', 'Unknown')
        
        inputs = {
            'message_text': msg_content, 
            'sender_id': sender_id
        }
        
        # 2. Run the Agentic Crew (retry once on rate limit)
        for attempt in range(2):
            try:
                result = BankScamShieldCrew().crew().kickoff(inputs=inputs)
                break
            except Exception as e:
                if "rate_limit_exceeded" in str(e) and attempt == 0:
                    time.sleep(10)
                else:
                    raise
        raw_text = str(result)

        # 3. Extract individual agent outputs
        tasks_output = result.tasks_output
        linguist_raw = tasks_output[0].raw if len(tasks_output) > 0 else ""
        auditor_raw = tasks_output[1].raw if len(tasks_output) > 1 else ""

        # 4. Process the final recommendation into structured parts
        # Extract RISK LEVEL line
        risk_label = "Low Risk/Suspicious"
        for line in raw_text.splitlines():
            if line.strip().upper().startswith("RISK LEVEL:"):
                if "HIGH" in line.upper():
                    risk_label = "High Risk"
                break

        stripped = raw_text
        if "RISK LEVEL:" in raw_text.upper():
            stripped = raw_text[raw_text.upper().index("RISK LEVEL:"):]
            stripped = stripped.split("\n", 1)[1] if "\n" in stripped else ""

        parts = stripped.split("ACTIONS:")
        analysis_part = parts[0].replace("ANALYSIS:", "").strip()
        actions_part = parts[1].strip() if len(parts) > 1 else "No specific actions provided."

        # Helper function for HTML formatting
        def to_html_bullets(text):
            bullets = text.split("- ")
            return "".join([f"<li>{b.strip()}</li>" for b in bullets if b.strip()])

        analysis_html = to_html_bullets(analysis_part)
        actions_html = to_html_bullets(actions_part)

        # Convert agent raw text to paragraphs
        def to_html_paragraphs(text):
            lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
            return "".join([f"<p>{l}</p>" for l in lines])

        # 5. Persistence Layer (SQLite Logging)
        log_scan(sender_id, msg_content, risk_label)

        # 6. Return JSON to the frontend
        return jsonify({
            "status": "success",
            "risk_label": risk_label,
            "linguist_output": to_html_paragraphs(linguist_raw),
            "auditor_output": to_html_paragraphs(auditor_raw),
            "analysis_bullets": analysis_html,
            "action_bullets": actions_html,
            "history": get_history()
        })

    except Exception as e:
        print(f"Error during analysis: {e}") # Helpful for debugging in terminal
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)