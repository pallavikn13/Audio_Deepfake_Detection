let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusText = document.getElementById("status");
const predictionText = document.getElementById("prediction");
const confidenceBar = document.getElementById("confidenceBar");
const aiBreakdown = document.getElementById("aiBreakdown");

// START RECORDING
startBtn.onclick = async function () {

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.start();
        audioChunks = [];

        startBtn.classList.add("recording");
        statusText.innerText = "🎙 Recording...";
        stopBtn.disabled = false;

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

    } catch (error) {
        statusText.innerText = "Microphone access denied!";
    }
};

// STOP RECORDING
stopBtn.onclick = function () {

    mediaRecorder.stop();
    statusText.innerText = "Processing audio...";

    mediaRecorder.onstop = async () => {

        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append("audio", audioBlob, "recorded_audio.wav");

        try {
            const response = await fetch("/record", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            startBtn.classList.remove("recording");

            if (result.error) {
                predictionText.innerText = "❌ Error: " + result.error;
            } else {

                predictionText.innerText =
                    "🔍 Result: " + result.result;

                confidenceBar.style.width =
                    result.score + "%";

                aiBreakdown.innerHTML =
                    "<h3>🧠 AI Analysis Breakdown</h3>" +
                    "<p>Confidence Score: " + result.score.toFixed(1) + "%</p>" +
                    "<p>Threat Level: " +
                    (result.score < 50
                        ? "<span class='risk'>HIGH RISK</span>"
                        : "<span class='safe'>SAFE</span>") +
                    "</p>";
            }

        } catch (error) {
            predictionText.innerText = "Server error. Try again.";
        }

        statusText.innerText = "";
        stopBtn.disabled = true;
    };
};