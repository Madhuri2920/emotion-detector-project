
function RunSentimentAnalysis() {
    let textToAnalyze = document.getElementById("textToAnalyze").value;
    let responseBox = document.getElementById("system_response");

    responseBox.innerHTML = "Analyzing...";

    fetch("/emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze))
        .then(response => response.text())
        .then(data => {
            responseBox.innerHTML = data;
        })
        .catch(error => {
            responseBox.innerHTML = "Error: " + error;
        });
}
