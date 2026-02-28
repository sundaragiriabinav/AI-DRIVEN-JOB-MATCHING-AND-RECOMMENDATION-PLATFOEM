async function processMatch() {
    const resume = document.getElementById('resumeInput').value;
    const job = document.getElementById('jobInput').value;
    const btn = document.getElementById('analyzeBtn');

    if(!resume || !job) {
        alert("Please fill in both fields!");
        return;
    }

    btn.innerText = "Processing AI Analysis...";
    btn.disabled = true;

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume, job })
        });

        const data = await response.json();
        
        // Update UI
        document.getElementById('resultCard').classList.remove('hidden');
        document.getElementById('scoreValue').innerText = data.score;
        
        const feedback = document.getElementById('feedbackText');
        if(data.score > 70) {
            feedback.innerText = "Strong Match: Candidate is highly qualified.";
            feedback.style.color = "#10b981";
        } else if(data.score > 40) {
            feedback.innerText = "Partial Match: Some skill gaps identified.";
            feedback.style.color = "#f59e0b";
        } else {
            feedback.innerText = "Low Match: Not recommended for this role.";
            feedback.style.color = "#ef4444";
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Server Error. Make sure app.py is running.");
    } finally {
        btn.innerText = "Analyze Match Percent";
        btn.disabled = false;
    }
}