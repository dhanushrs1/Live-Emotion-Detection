// Developed by Dhanush RS



// Function to start the live video feed from the webcam
function startWebcam() {
    const videoElement = document.getElementById('videoFeed');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            videoElement.srcObject = stream;
            videoElement.play();
        })
        .catch(function (error) {
            console.error("Error accessing the webcam: ", error);
            showAlert("Error accessing webcam. Please allow webcam access or try another browser.");
        });
    } else {
        showAlert("Webcam not supported by your browser.");
    }
}

// Function to continuously fetch the real-time video stream from the Flask backend
function loadVideoFeed() {
    const videoElement = document.getElementById('videoFeed');
    
    setInterval(function () {
        videoElement.src = "/video_feed?" + new Date().getTime();  // Prevent caching
    }, 100);  // Refresh every 100 milliseconds
}

// Debounce function to prevent rapid emotion switching
let debounceTimeout;
const debounceDelay = 1000; // 1 second debounce delay
let lastEmotion = '';

function debounceEmotionSwitch(emotion) {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
        if (emotion !== lastEmotion) {
            lastEmotion = emotion; // Update last emotion
            displayEmotionMessage(emotion);
        }
    }, debounceDelay);
}

// Function to display messages based on the detected emotions
function displayEmotionMessage(emotion) {
    const emotionMessage = document.getElementById('emotionMessage');

    switch (emotion) {
        case 'Happy':
            emotionMessage.innerText = "Keep smiling! 😊";
            showAlert("You seem happy! Keep it up!");
            break;
        case 'Sad':
            emotionMessage.innerText = "It's okay to feel sad. Everything will be fine. 💖";
            showAlert("Feeling down? It's okay to express your emotions.");
            break;
        case 'Angry':
            emotionMessage.innerText = "Take a deep breath. Relax! 🧘‍♂️";
            showAlert("Feeling angry? Take a moment to breathe.");
            break;
        case 'Neutral':
            emotionMessage.innerText = "You're doing great!";
            break;
        default:
            emotionMessage.innerText = "You are amazing! 😎";
            break;
    }
}

// Function to show alert pop-ups
function showAlert(message) {
    const alertBox = document.createElement('div');
    alertBox.className = 'alert-box';
    alertBox.innerText = message;
    document.body.appendChild(alertBox);

    // Fade out the alert after a few seconds
    setTimeout(() => {
        alertBox.classList.add('fade-out');
        setTimeout(() => {
            alertBox.remove();
        }, 500);
    }, 3000);
}

// Event listener to start webcam and video feed on page load
window.addEventListener('load', function () {
    startWebcam();
    loadVideoFeed();
});
