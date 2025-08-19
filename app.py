from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Birthday Age Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }
        .container { max-width: 400px; margin: 60px auto; background: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; }
        label { display: block; margin-bottom: 0.5em; color: #555; }
        input[type="date"], select { width: 100%; padding: 0.5em; margin-bottom: 1em; border: 1px solid #ccc; border-radius: 4px; }
        button { width: 100%; padding: 0.7em; background: #0078d7; color: #fff; border: none; border-radius: 4px; font-size: 1em; cursor: pointer; }
        button:hover { background: #005fa3; }
        .result { margin-top: 1.5em; text-align: center; font-size: 1.2em; color: #0078d7; }
        .toggle { margin-bottom: 1em; text-align: right; }
        .toggle label { font-size: 0.95em; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Birthday Age Calculator</h1>
        <div class="toggle">
            <label for="modeToggle">Experience: </label>
            <select id="modeToggle">
                <option value="auto">Auto</option>
                <option value="mobile">Mobile</option>
                <option value="desktop">Desktop</option>
            </select>
        </div>
        <form method="post" id="birthForm">
            <label for="birthdate">Enter your birthdate:</label>
            <div id="dateInputContainer"></div>
            <input type="hidden" id="birthdate" name="birthdate" value="{{ birthdate|default('') }}">
            <button type="submit">Calculate Age</button>
        </form>
        {% if age is not none %}
        <div class="result">
            You are <strong>{{ age }}</strong> years old.
        </div>
        {% endif %}
    </div>
    <script>
    // Detect mobile OS
    function isMobileOS() {
        const ua = navigator.userAgent || navigator.vendor || window.opera;
        if (/android/i.test(ua)) return true;
        if (/iPad|iPhone|iPod/.test(ua) && !window.MSStream) return true;
        return false;
    }

    // Render date input based on mode
    function renderDateInput(mode, value) {
        const container = document.getElementById('dateInputContainer');
        container.innerHTML = '';
        if (mode === 'mobile') {
            // Scroll wheel style: 3 selects for year, month, day
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
            for (let i = y; i >= y-120; i--) {
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
            container.innerHTML = `<div style="display:flex; gap:4px;">${yearSel}${monthSel}${daySel}</div>`;
        } else {
            // Desktop: keyboard date input
            container.innerHTML = `<input type="date" id="dateInput" value="${value||''}" required>`;
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

    // Initial mode
    let mode = 'auto';
    let value = document.getElementById('birthdate').value;
    function updateInput() {
        let m = mode;
        if (m === 'auto') m = isMobileOS() ? 'mobile' : 'desktop';
        renderDateInput(m, value);
        if (m === 'mobile') {
            syncMobileDate();
            document.getElementById('yearSel').addEventListener('change', syncMobileDate);
            document.getElementById('monthSel').addEventListener('change', syncMobileDate);
            document.getElementById('daySel').addEventListener('change', syncMobileDate);
        } else {
            syncDesktopDate();
            document.getElementById('dateInput').addEventListener('input', syncDesktopDate);
        }
    }
    document.getElementById('modeToggle').addEventListener('change', function() {
        mode = this.value;
        updateInput();
    });
    updateInput();
    // On form submit, ensure hidden input is synced
    document.getElementById('birthForm').addEventListener('submit', function() {
        let m = mode;
        if (m === 'auto') m = isMobileOS() ? 'mobile' : 'desktop';
        if (m === 'mobile') syncMobileDate();
        else syncDesktopDate();
    });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    age = None
    birthdate = ''
    if request.method == 'POST':
        birthdate = request.form.get('birthdate', '')
        try:
            bdate = datetime.strptime(birthdate, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
        except Exception:
            age = None
    return render_template_string(HTML, age=age, birthdate=birthdate)

if __name__ == '__main__':
    app.run(debug=True)
