let isRecording = false;
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

// Configure speech recognition
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

function toggleVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    const questionInput = document.getElementById("question");
    
    if (!isRecording) {
        // Start recording
        try {
            recognition.start();
            voiceBtn.classList.add('active');
            voiceBtn.innerHTML = '⏹️ Stop';
            isRecording = true;
            questionInput.value = "Listening...";
        } catch (err) {
            console.error('Error starting speech recognition:', err);
            alert('Could not start speech recognition. Please make sure you have given microphone permissions.');
        }
    } else {
        // Stop recording
        recognition.stop();
        voiceBtn.classList.remove('active');
        voiceBtn.innerHTML = '🎤 Voice';
        isRecording = false;
    }
}

// Handle speech recognition results
recognition.onresult = (event) => {
    const questionInput = document.getElementById("question");
    const transcript = event.results[0][0].transcript;
    questionInput.value = transcript;
    
    // Automatically submit the question
    if (transcript) {
        ask();
    }
};

// Handle speech recognition end
recognition.onend = () => {
    const voiceBtn = document.getElementById('voiceBtn');
    voiceBtn.classList.remove('active');
    voiceBtn.innerHTML = '🎤 Voice';
    isRecording = false;
};

// Handle speech recognition errors
recognition.onerror = (event) => {
    const voiceBtn = document.getElementById('voiceBtn');
    const questionInput = document.getElementById("question");
    console.error('Speech recognition error:', event.error);
    questionInput.value = "";
    voiceBtn.classList.remove('active');
    voiceBtn.innerHTML = '🎤 Voice';
    isRecording = false;
    
    let errorMessage = 'Speech recognition failed. ';
    switch (event.error) {
        case 'network':
            errorMessage += 'Please check your internet connection.';
            break;
        case 'not-allowed':
        case 'permission-denied':
            errorMessage += 'Please allow microphone access.';
            break;
        case 'no-speech':
            errorMessage += 'No speech was detected.';
            break;
        default:
            errorMessage += 'Please try again.';
    }
    alert(errorMessage);
}

function toggleComparison() {
    document.querySelector('.feature-button:nth-child(3)').classList.toggle('active');
}

function handleFiles(files) {
    const preview = document.getElementById('filePreview');
    preview.innerHTML = '';
    preview.style.display = 'block';
    
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            const reader = new FileReader();
            reader.onload = e => img.src = e.target.result;
            reader.readAsDataURL(file);
            preview.appendChild(img);
        } else if (file.type === 'application/pdf') {
            const div = document.createElement('div');
            div.innerHTML = `📄 ${file.name}`;
            preview.appendChild(div);
        }
    });
}

async function ask(files = null, pdf = null, voiceData = null) {
    const question = document.getElementById("question").value;
    if (!question && !voiceData) {
        alert("Please enter a question or use voice input!");
        return;
    }

    document.getElementById("answers").innerHTML = "";
    document.getElementById("loading").style.display = "flex";

    try {
        const formData = new FormData();
        formData.append('question', question);
        
        const fileInput = document.getElementById('fileInput');
        if (fileInput.files.length > 0) {
            Array.from(fileInput.files).forEach(file => {
                if (file.type.startsWith('image/')) {
                    formData.append('files', file);
                } else if (file.type === 'application/pdf') {
                    formData.append('pdf_file', file);
                }
            });
        }
        
        if (voiceData) {
            formData.append('voice_data', voiceData);
        }
        
        const shouldCompare = document.querySelector('.feature-button:nth-child(3)').classList.contains('active');
        formData.append('compare', shouldCompare);

        const res = await fetch("/ask", {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("Server error " + res.status);

        const data = await res.json();
        const answersDiv = document.getElementById("answers");
        answersDiv.innerHTML = "";

        for (const [model, response] of Object.entries(data)) {
            const card = document.createElement("div");
            card.className = "card";
            
            const modelName = model.charAt(0).toUpperCase() + model.slice(1);
            let content;
            
            if (response.error) {
                content = `Error: ${response.error}`;
            } else {
                content = response.response;
                if (response.processing_time) {
                    content += `\n\nProcessing time: ${response.processing_time.toFixed(2)}s`;
                }
                if (response.tokens) {
                    content += `\nTokens used: ${response.tokens}`;
                }
            }
            
            // Create copy button
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.innerHTML = '📋';
            copyBtn.onclick = () => {
                navigator.clipboard.writeText(content);
                copyBtn.innerHTML = '✓';
                setTimeout(() => copyBtn.innerHTML = '📋', 2000);
            };
            
            content = content.replace(/\n/g, '<br>');
            card.innerHTML = `
                <h2>${modelName}</h2>
                <p>${content}</p>
            `;
            card.appendChild(copyBtn);
            
            setTimeout(() => answersDiv.appendChild(card), 100 * answersDiv.children.length);
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("answers").innerHTML = `
            <div class="card error">
                <h2>Error</h2>
                <p>Failed to get response: ${error.message}</p>
            </div>
        `;
    } finally {
        document.getElementById("loading").style.display = "none";
    }
}