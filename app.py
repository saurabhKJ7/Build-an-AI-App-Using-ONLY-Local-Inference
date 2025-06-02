from flask import Flask, render_template_string, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Constants
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Local AI Writer</title>
    <style>
        body {
            font-family: -apple-system, system-ui, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        textarea {
            width: 100%;
            height: 150px;
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        .controls {
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        #response {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #f8f9fa;
            min-height: 100px;
            white-space: pre-wrap;
        }
        .error { color: #dc3545; }
        .loading { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Local AI Writer</h1>
        <div>
            <textarea id="prompt" placeholder="Enter your prompt here..."></textarea>
        </div>
        <div class="controls">
            <label>
                Temperature: 
                <input type="range" id="temperature" min="0" max="1" step="0.1" value="0.7">
                <span id="tempValue">0.7</span>
            </label>
        </div>
        <button onclick="generate()">Generate</button>
        <div id="loading" class="loading">Generating...</div>
        <div id="error" class="error"></div>
        <div id="response"></div>
    </div>

    <script>
        document.getElementById('temperature').addEventListener('input', function() {
            document.getElementById('tempValue').textContent = this.value;
        });

        async function generate() {
            const prompt = document.getElementById('prompt').value.trim();
            const temperature = parseFloat(document.getElementById('temperature').value);
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const response = document.getElementById('response');
            
            if (!prompt) {
                error.textContent = 'Please enter a prompt';
                return;
            }
            
            error.textContent = '';
            loading.style.display = 'block';
            response.textContent = '';
            
            try {
                const res = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt, temperature})
                });
                
                const data = await res.json();
                if (data.error) {
                    error.textContent = data.error;
                } else {
                    response.textContent = data.response;
                }
            } catch (err) {
                error.textContent = 'Error: ' + err.message;
            } finally {
                loading.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

def generate_response(prompt: str, temperature: float = 0.7) -> str:
    """Generate response using LM Studio API"""
    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error connecting to LM Studio API: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def log_interaction(prompt: str, response: str, temperature: float):
    """Log interaction to file"""
    try:
        os.makedirs('logs', exist_ok=True)
        with open('logs/interactions.log', 'a', encoding='utf-8') as f:
            f.write(f"\n[{datetime.now().isoformat()}]\n")
            f.write(f"Temperature: {temperature}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Response: {response}\n")
            f.write("-" * 50)
    except Exception:
        pass  # Fail silently if logging fails

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '').strip()
    temperature = float(data.get('temperature', 0.7))
    
    if not prompt:
        return jsonify({'error': 'Please provide a prompt'}), 400
    
    response = generate_response(prompt, temperature)
    log_interaction(prompt, response, temperature)
    return jsonify({'response': response})

if __name__ == '__main__':
    print("\n🚀 Local AI Writer")
    print("Make sure LM Studio is running at:", LM_STUDIO_URL)
    app.run(port=5000)