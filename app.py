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
        
        # 2. Run the Agentic Crew
        # Note: Ensure the class name matches what is in your crew.py
        result = BankScamShieldCrew().crew().kickoff(inputs=inputs)
        raw_text = str(result)

        # 3. Process the AI response into structured parts
        parts = raw_text.split("ACTIONS:")
        analysis_part = parts[0].replace("ANALYSIS:", "").strip()
        actions_part = parts[1].strip() if len(parts) > 1 else "No specific actions provided."

        # Helper function for HTML formatting
        def to_html_bullets(text):
            bullets = text.split("- ")
            return "".join([f"<li>{b.strip()}</li>" for b in bullets if b.strip()])

        analysis_html = to_html_bullets(analysis_part)
        actions_html = to_html_bullets(actions_part)

        # 4. Persistence Layer (SQLite Logging)
        # Determine risk for the database log
        risk_label = "High Risk" if "high risk" in raw_text.lower() else "Low Risk/Suspicious"
        log_scan(sender_id, msg_content, risk_label)
        
        # 5. Return JSON to the frontend
        return jsonify({
            "status": "success",
            "analysis_bullets": analysis_html,
            "action_bullets": actions_html,
            "history": get_history() # Sends the latest 5 scans back to the dashboard
        })

    except Exception as e:
        print(f"Error during analysis: {e}") # Helpful for debugging in terminal
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)