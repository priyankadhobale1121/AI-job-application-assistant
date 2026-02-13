import os
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/generate-cover-letter", methods=["POST"])
def generate_cover_letter():
    try:
        data = request.json
        resume = data.get("resume", "")
        job_description = data.get("job_description", "")
        tone = data.get("tone", "professional")

        if not resume or not job_description:
            return jsonify({"error": "Resume and Job Description required"}), 400

        prompt = f"""
Write a {tone} cover letter under 300 words.

Resume:
{resume}

Job Description:
{job_description}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return jsonify({"result": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():
    try:
        resume = request.json.get("resume", "")
        if not resume:
            return jsonify({"error": "Resume required"}), 400

        prompt = f"""
Analyze this resume:
1. Strengths
2. Weaknesses
3. Improvements
4. Missing Skills

{resume}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({"analysis": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ats-score", methods=["POST"])
def ats_score():
    try:
        data = request.json
        resume = data.get("resume", "").lower()
        job_description = data.get("job_description", "").lower()

        words = re.findall(r'\b[a-zA-Z]+\b', job_description)
        stopwords = ["the", "and", "for", "with", "are", "this"]
        keywords = [w for w in words if w not in stopwords and len(w) > 3]

        matched = [word for word in set(keywords) if word in resume]
        score = round((len(matched) / len(set(keywords))) * 100) if keywords else 0

        return jsonify({
            "score": score,
            "matched_keywords": matched[:15],
            "total_keywords": len(set(keywords))
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/career-advice", methods=["POST"])
def career_advice():
    try:
        resume = request.json.get("resume", "")
        if not resume:
            return jsonify({"error": "Resume required"}), 400

        prompt = f"""
Based on this resume:
- Suggest career path
- Skills to learn in 2026
- Interview questions
- Growth roadmap

{resume}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({"advice": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
