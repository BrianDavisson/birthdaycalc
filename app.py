from flask import Flask, render_template_string, request
from datetime import datetime
import json
import os
import logging
from collections import deque

app = Flask(__name__)

# Logging setup
LOG_DIR = 'log'
USAGE_LOG = os.path.join(LOG_DIR, 'usage.log')
TECHNICAL_LOG = os.path.join(LOG_DIR, 'techx.json')
MAX_USAGE_ENTRIES = 100000

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_usage(birthdate_selected, timestamp):
    """Log usage data in simple format"""
    try:
        log_entry = f"{timestamp} | {birthdate_selected}\n"
        
        # Read existing entries
        entries = []
        if os.path.exists(USAGE_LOG):
            with open(USAGE_LOG, 'r', encoding='utf-8') as f:
                entries = f.readlines()
        
        # Add new entry
        entries.append(log_entry)
        
        # Keep only last 100k entries
        if len(entries) > MAX_USAGE_ENTRIES:
            entries = entries[-MAX_USAGE_ENTRIES:]
        
        # Write back to file
        with open(USAGE_LOG, 'w', encoding='utf-8') as f:
            f.writelines(entries)
            
    except Exception as e:
        print(f"Error logging usage: {e}")

def log_technical_info(request_obj):
    """Log comprehensive technical information in JSON format"""
    try:
        timestamp = datetime.now().isoformat()
        
        # Gather comprehensive technical data
        technical_data = {
            "timestamp": timestamp,
            "request_info": {
                "method": request_obj.method,
                "url": request_obj.url,
                "base_url": request_obj.base_url,
                "path": request_obj.path,
                "query_string": request_obj.query_string.decode('utf-8'),
                "remote_addr": request_obj.remote_addr,
                "remote_user": request_obj.remote_user,
                "scheme": request_obj.scheme,
                "server": request_obj.server,
                "environ": {
                    "SERVER_NAME": request_obj.environ.get('SERVER_NAME'),
                    "SERVER_PORT": request_obj.environ.get('SERVER_PORT'),
                    "REQUEST_METHOD": request_obj.environ.get('REQUEST_METHOD'),
                    "PATH_INFO": request_obj.environ.get('PATH_INFO'),
                    "QUERY_STRING": request_obj.environ.get('QUERY_STRING'),
                    "CONTENT_TYPE": request_obj.environ.get('CONTENT_TYPE'),
                    "CONTENT_LENGTH": request_obj.environ.get('CONTENT_LENGTH'),
                    "HTTP_HOST": request_obj.environ.get('HTTP_HOST'),
                    "HTTP_CONNECTION": request_obj.environ.get('HTTP_CONNECTION'),
                    "HTTP_UPGRADE_INSECURE_REQUESTS": request_obj.environ.get('HTTP_UPGRADE_INSECURE_REQUESTS'),
                    "HTTP_DNT": request_obj.environ.get('HTTP_DNT'),
                    "HTTP_SEC_FETCH_DEST": request_obj.environ.get('HTTP_SEC_FETCH_DEST'),
                    "HTTP_SEC_FETCH_MODE": request_obj.environ.get('HTTP_SEC_FETCH_MODE'),
                    "HTTP_SEC_FETCH_SITE": request_obj.environ.get('HTTP_SEC_FETCH_SITE'),
                    "HTTP_SEC_FETCH_USER": request_obj.environ.get('HTTP_SEC_FETCH_USER'),
                    "HTTP_CACHE_CONTROL": request_obj.environ.get('HTTP_CACHE_CONTROL'),
                    "HTTP_SEC_CH_UA": request_obj.environ.get('HTTP_SEC_CH_UA'),
                    "HTTP_SEC_CH_UA_MOBILE": request_obj.environ.get('HTTP_SEC_CH_UA_MOBILE'),
                    "HTTP_SEC_CH_UA_PLATFORM": request_obj.environ.get('HTTP_SEC_CH_UA_PLATFORM'),
                    "REMOTE_ADDR": request_obj.environ.get('REMOTE_ADDR'),
                    "REMOTE_HOST": request_obj.environ.get('REMOTE_HOST'),
                    "REMOTE_USER": request_obj.environ.get('REMOTE_USER'),
                    "REQUEST_URI": request_obj.environ.get('REQUEST_URI'),
                    "SERVER_PROTOCOL": request_obj.environ.get('SERVER_PROTOCOL'),
                    "SERVER_SOFTWARE": request_obj.environ.get('SERVER_SOFTWARE'),
                    "GATEWAY_INTERFACE": request_obj.environ.get('GATEWAY_INTERFACE')
                }
            },
            "headers": {
                "User-Agent": request_obj.headers.get('User-Agent'),
                "Accept": request_obj.headers.get('Accept'),
                "Accept-Language": request_obj.headers.get('Accept-Language'),
                "Accept-Encoding": request_obj.headers.get('Accept-Encoding'),
                "Referer": request_obj.headers.get('Referer'),
                "Origin": request_obj.headers.get('Origin'),
                "Host": request_obj.headers.get('Host'),
                "Connection": request_obj.headers.get('Connection'),
                "Upgrade-Insecure-Requests": request_obj.headers.get('Upgrade-Insecure-Requests'),
                "Sec-Fetch-Dest": request_obj.headers.get('Sec-Fetch-Dest'),
                "Sec-Fetch-Mode": request_obj.headers.get('Sec-Fetch-Mode'),
                "Sec-Fetch-Site": request_obj.headers.get('Sec-Fetch-Site'),
                "Sec-Fetch-User": request_obj.headers.get('Sec-Fetch-User'),
                "Sec-Ch-Ua": request_obj.headers.get('Sec-Ch-Ua'),
                "Sec-Ch-Ua-Mobile": request_obj.headers.get('Sec-Ch-Ua-Mobile'),
                "Sec-Ch-Ua-Platform": request_obj.headers.get('Sec-Ch-Ua-Platform'),
                "Cache-Control": request_obj.headers.get('Cache-Control'),
                "Pragma": request_obj.headers.get('Pragma'),
                "DNT": request_obj.headers.get('DNT'),
                "X-Forwarded-For": request_obj.headers.get('X-Forwarded-For'),
                "X-Real-IP": request_obj.headers.get('X-Real-IP'),
                "X-Forwarded-Proto": request_obj.headers.get('X-Forwarded-Proto')
            },
            "form_data": dict(request_obj.form) if request_obj.form else None,
            "args": dict(request_obj.args) if request_obj.args else None,
            "files": list(request_obj.files.keys()) if request_obj.files else None,
            "cookies": dict(request_obj.cookies) if request_obj.cookies else None,
            "is_json": request_obj.is_json,
            "is_secure": request_obj.is_secure,
            "access_route": list(request_obj.access_route) if hasattr(request_obj, 'access_route') else None
        }
        
        # Write to technical log
        with open(TECHNICAL_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(technical_data, indent=None, separators=(',', ':')) + '\n')
            
    except Exception as e:
        print(f"Error logging technical info: {e}")

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Birthday Age Calculator</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            margin: 0; 
            padding: 20px; 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            min-width: 400px;
            max-width: 600px;
            width: auto;
            background: rgba(255, 255, 255, 0.95); 
            padding: 2.5em; 
            border-radius: 20px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(0,0,0,0.07);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        h1 { 
            text-align: center; 
            color: #2c3e50; 
            margin-bottom: 1.5em;
            font-weight: 300;
            font-size: 2.2em;
            letter-spacing: -0.5px;
        }
        label { 
            display: block; 
            margin-bottom: 0.8em; 
            color: #34495e; 
            font-weight: 500;
            font-size: 1.1em;
        }
        input[type="date"], select { 
            width: 100%; 
            padding: 1em; 
            margin-bottom: 1.5em; 
            border: 2px solid #e1e8ed; 
            border-radius: 12px; 
            font-size: 1em;
            transition: all 0.3s ease;
            background: #fff;
        }
        input[type="date"]:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .btn-primary { 
            width: 100%; 
            padding: 1em; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: #fff; 
            border: none; 
            border-radius: 12px; 
            font-size: 1.1em; 
            cursor: pointer; 
            transition: all 0.3s ease;
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        .btn-primary:hover { 
            transform: translateY(-2px);
            box-shadow: 0 7px 25px rgba(102, 126, 234, 0.3);
        }
        .btn-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 0.5em 1em;
            background: rgba(255, 255, 255, 0.9);
            color: #667eea;
            border: 2px solid #667eea;
            border-radius: 20px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .btn-toggle:hover {
            background: #667eea;
            color: white;
            transform: scale(1.05);
        }
        .result { 
            margin-top: 2em; 
            text-align: center; 
            font-size: 1.3em; 
            color: #2c3e50;
            padding: 1.5em;
            background: rgba(102, 126, 234, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(102, 126, 234, 0.1);
        }
        .result strong {
            color: #667eea;
            font-size: 1.2em;
        }
        #detailedAge {
            margin-top: 15px !important;
            font-size: 1em !important;
            color: #7f8c8d !important;
            font-family: 'Courier New', monospace;
            background: rgba(0,0,0,0.02);
            padding: 10px;
            border-radius: 8px;
        }
        .joke {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            color: #2c3e50;
            padding: 1.5em;
            border-radius: 12px;
            margin-top: 1em;
            font-style: italic;
            font-size: 1.1em;
            text-align: center;
        }
        .date-selects {
            display: flex;
            gap: 8px;
        }
        .date-selects select {
            margin-bottom: 1.5em;
        }
    </style>
</head>
<body>
    <div class="container">
        <button id="modeToggle" class="btn-toggle"></button>
        <h1>Birthday Age Calculator</h1>
        <form method="post" id="birthForm">
            <label for="birthdate">Enter your birthdate:</label>
            <div id="dateInputContainer"></div>
            <input type="hidden" id="birthdate" name="birthdate" value="{{ birthdate|default('') }}">
            <button type="submit" class="btn-primary">Calculate Age</button>
        </form>
        {% if age is not none %}
        <div class="result">
            {% if joke %}
            <div class="joke">{{ joke }}</div>
            {% else %}
            You are <strong>{{ age }}</strong> years old.
            <div id="detailedAge" style="margin-top: 10px; font-size: 0.9em; color: #555;">
                <span id="timeAlive"></span>
            </div>
            {% endif %}
        </div>
        <script>
        // Calculate detailed time alive
        function updateDetailedAge() {
            const birthdate = new Date('{{ birthdate }}');
            const now = new Date();
            
            // Calculate differences
            let years = now.getFullYear() - birthdate.getFullYear();
            let months = now.getMonth() - birthdate.getMonth();
            let days = now.getDate() - birthdate.getDate();
            let hours = now.getHours() - birthdate.getHours();
            let minutes = now.getMinutes() - birthdate.getMinutes();
            let seconds = now.getSeconds() - birthdate.getSeconds();
            
            // Adjust for negative values
            if (seconds < 0) {
                seconds += 60;
                minutes--;
            }
            if (minutes < 0) {
                minutes += 60;
                hours--;
            }
            if (hours < 0) {
                hours += 24;
                days--;
            }
            if (days < 0) {
                const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0);
                days += prevMonth.getDate();
                months--;
            }
            if (months < 0) {
                months += 12;
                years--;
            }
            
            document.getElementById('timeAlive').innerHTML = 
                `${years} years, ${months} months, ${days} days, ${hours} hours, ${minutes} minutes, ${seconds} seconds`;
        }
        
        // Update every second
        {% if not joke %}
        updateDetailedAge();
        setInterval(updateDetailedAge, 1000);
        {% endif %}
        </script>
        {% endif %}
    </div>
    </div>
    <script>
    // Detect mobile OS
    function isMobileOS() {
        const ua = navigator.userAgent || navigator.vendor || window.opera;
        if (/android/i.test(ua)) return true;
        if (/iPad|iPhone|iPod/.test(ua) && !window.MSStream) return true;
        return false;
    }

    // Current mode state
    let isDesktopMode = !isMobileOS();

    // Render date input based on mode
    function renderDateInput(isDesktop, value) {
        const container = document.getElementById('dateInputContainer');
        const toggleBtn = document.getElementById('modeToggle');
        
        container.innerHTML = '';
        
        if (isDesktop) {
            // Desktop: keyboard date input
            container.innerHTML = `<input type="date" id="dateInput" value="${value||''}" required>`;
            toggleBtn.textContent = 'Switch to Mobile';
            toggleBtn.style.display = 'block';
        } else {
            // Mobile: scroll wheel style
            const today = new Date();
            let y = today.getFullYear();
            let selected = { year: '', month: '', day: '' };
            if (value) {
                let parts = value.split('-');
                if (parts.length === 3) {
                    selected.year = parts[0];
                    selected.month = parts[1];
                    selected.day = parts[2];
                }
            }
            
            let yearSel = '<select id="yearSel">';
            for (let i = y; i >= y-125; i--) {
                yearSel += `<option value="${i}"${selected.year==i?" selected":''}>${i}</option>`;
            }
            yearSel += '</select>';
            
            let monthSel = '<select id="monthSel">';
            for (let i = 1; i <= 12; i++) {
                let m = i.toString().padStart(2,'0');
                monthSel += `<option value="${m}"${selected.month==m?" selected":''}>${m}</option>`;
            }
            monthSel += '</select>';
            
            let daySel = '<select id="daySel">';
            for (let i = 1; i <= 31; i++) {
                let d = i.toString().padStart(2,'0');
                daySel += `<option value="${d}"${selected.day==d?" selected":''}>${d}</option>`;
            }
            daySel += '</select>';
            
            container.innerHTML = `<div class="date-selects">${yearSel}${monthSel}${daySel}</div>`;
            toggleBtn.textContent = 'Switch to Desktop';
            toggleBtn.style.display = 'block';
        }
    }

    // Sync selects to hidden input
    function syncMobileDate() {
        const y = document.getElementById('yearSel').value;
        const m = document.getElementById('monthSel').value;
        const d = document.getElementById('daySel').value;
        document.getElementById('birthdate').value = `${y}-${m}-${d}`;
    }

    // Sync date input to hidden input
    function syncDesktopDate() {
        document.getElementById('birthdate').value = document.getElementById('dateInput').value;
    }

    // Initialize
    let value = document.getElementById('birthdate').value;
    
    function updateInput() {
        renderDateInput(isDesktopMode, value);
        if (isDesktopMode) {
            syncDesktopDate();
            if (document.getElementById('dateInput')) {
                document.getElementById('dateInput').addEventListener('input', syncDesktopDate);
            }
        } else {
            syncMobileDate();
            if (document.getElementById('yearSel')) {
                document.getElementById('yearSel').addEventListener('change', syncMobileDate);
                document.getElementById('monthSel').addEventListener('change', syncMobileDate);
                document.getElementById('daySel').addEventListener('change', syncMobileDate);
            }
        }
    }
    
    // Toggle button functionality
    document.getElementById('modeToggle').addEventListener('click', function() {
        isDesktopMode = !isDesktopMode;
        updateInput();
    });
    
    // Initialize
    updateInput();
    
    // On form submit, ensure hidden input is synced
    document.getElementById('birthForm').addEventListener('submit', function() {
        if (isDesktopMode) {
            syncDesktopDate();
        } else {
            syncMobileDate();
        }
    });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    # Log technical information for every request
    log_technical_info(request)
    
    age = None
    birthdate = ''
    joke = None
    
    funny_jokes = [
        "Wow! You're older than sliced bread! (Literally, it was invented in 1928)",
        "Are you sure you didn't personally know Moses? 🏺",
        "I bet you remember when the Dead Sea was just feeling a little under the weather! 🌊",
        "You must have some great stories from the Civil War! ⚔️",
        "Did you help build the pyramids? 🏜️",
        "I think your birthday candles are a fire hazard! 🔥",
        "You're so old, your birth certificate is written in hieroglyphics! 📜",
        "Time to update your driver's license... oh wait, cars weren't invented yet! 🏇",
        "I bet you knew Methuselah personally! 👴",
        "Your age has more digits than my phone number! 📱"
    ]
    
    if request.method == 'POST':
        birthdate = request.form.get('birthdate', '')
        timestamp = datetime.now().isoformat()
        
        # Log usage data
        log_usage(birthdate, timestamp)
        
        try:
            bdate = datetime.strptime(birthdate, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
            
            # Check if age is over 125 years
            if age > 125:
                import random
                joke = random.choice(funny_jokes)
                age = None  # Don't show the age, just the joke
                
        except Exception:
            age = None
            
    return render_template_string(HTML, age=age, birthdate=birthdate, joke=joke)

if __name__ == '__main__':
    app.run(debug=True)
