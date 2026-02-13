async function generateCover() {
    const resume = document.getElementById("resume").value;
    const job_description = document.getElementById("job_description").value;
    const tone = document.getElementById("tone").value;

    const response = await fetch("/generate-cover-letter", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({resume, job_description, tone})
    });

    const data = await response.json();
    document.getElementById("output").textContent = data.result || data.error;
}

async function analyzeResume() {
    const resume = document.getElementById("resume").value;

    const response = await fetch("/analyze-resume", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({resume})
    });

    const data = await response.json();
    document.getElementById("output").textContent = data.analysis || data.error;
}

async function checkATS() {
    const resume = document.getElementById("resume").value;
    const job_description = document.getElementById("job_description").value;

    const response = await fetch("/ats-score", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({resume, job_description})
    });

    const data = await response.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}

async function careerAdvice() {
    const resume = document.getElementById("resume").value;

    const response = await fetch("/career-advice", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({resume})
    });

    const data = await response.json();
    document.getElementById("output").textContent = data.advice || data.error;
}
