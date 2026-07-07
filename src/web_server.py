"""
Web server for accessing screen time statistics.
Provides REST API and optional web dashboard.
Useful for headless deployments and multi-user setups.
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import os

app = Flask(__name__)
CORS(app)

# Configuration
DATA_DIR = Path(os.getenv('DATA_DIR', 'data'))
DATA_DIR.mkdir(exist_ok=True)

SESSION_FILE = DATA_DIR / 'sessions.json'
CURRENT_SESSION_FILE = DATA_DIR / 'current_session.json'


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_sessions():
    """Load all session data."""
    if not SESSION_FILE.exists():
        return []
    
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def load_current_session():
    """Load current session data."""
    if not CURRENT_SESSION_FILE.exists():
        return None
    
    try:
        with open(CURRENT_SESSION_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def format_time(seconds):
    """Format seconds to HH:MM:SS."""
    return str(timedelta(seconds=int(seconds)))


def calculate_daily_stats():
    """Calculate daily usage statistics."""
    sessions = load_sessions()
    daily_data = defaultdict(lambda: {'phone': 0, 'laptop': 0, 'sessions': 0})
    
    for session in sessions:
        try:
            date = datetime.fromisoformat(session['timestamp']).date()
            daily_data[date]['phone'] += session.get('phone_time', 0)
            daily_data[date]['laptop'] += session.get('laptop_time', 0)
            daily_data[date]['sessions'] += 1
        except (KeyError, ValueError):
            continue
    
    return {
        str(date): {
            'phone': int(data['phone']),
            'laptop': int(data['laptop']),
            'sessions': data['sessions']
        }
        for date, data in sorted(daily_data.items())
    }


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/current', methods=['GET'])
def get_current_session():
    """Get current session data."""
    current = load_current_session()
    
    if current:
        return jsonify({
            'status': 'active',
            'session': current
        })
    
    return jsonify({
        'status': 'no_session',
        'message': 'No active session'
    }), 404


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get overall statistics summary."""
    sessions = load_sessions()
    
    if not sessions:
        return jsonify({
            'status': 'no_data',
            'message': 'No session data collected yet'
        }), 404
    
    total_phone = sum(s.get('phone_time', 0) for s in sessions)
    total_laptop = sum(s.get('laptop_time', 0) for s in sessions)
    total_duration = sum(s.get('session_duration', 0) for s in sessions)
    
    return jsonify({
        'total_sessions': len(sessions),
        'total_monitoring_time': int(total_duration),
        'total_monitoring_time_formatted': format_time(total_duration),
        'total_phone_time': int(total_phone),
        'total_phone_time_formatted': format_time(total_phone),
        'total_laptop_time': int(total_laptop),
        'total_laptop_time_formatted': format_time(total_laptop),
        'phone_percentage': round((total_phone / total_duration * 100) if total_duration > 0 else 0, 1),
        'laptop_percentage': round((total_laptop / total_duration * 100) if total_duration > 0 else 0, 1),
    })


@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all session data."""
    sessions = load_sessions()
    
    return jsonify({
        'count': len(sessions),
        'sessions': sessions
    })


@app.route('/api/sessions/recent/<int:limit>', methods=['GET'])
def get_recent_sessions(limit=10):
    """Get recent N sessions."""
    sessions = load_sessions()
    recent = sessions[-limit:] if limit > 0 else sessions
    
    return jsonify({
        'count': len(recent),
        'sessions': recent
    })


@app.route('/api/daily', methods=['GET'])
def get_daily_stats():
    """Get daily aggregated statistics."""
    daily_stats = calculate_daily_stats()
    
    return jsonify({
        'days': len(daily_stats),
        'daily_stats': daily_stats
    })


@app.route('/api/weekly', methods=['GET'])
def get_weekly_stats():
    """Get weekly aggregated statistics."""
    sessions = load_sessions()
    weekly_data = defaultdict(lambda: {'phone': 0, 'laptop': 0, 'sessions': 0})
    
    for session in sessions:
        try:
            date = datetime.fromisoformat(session['timestamp']).date()
            week = date.isocalendar()[1]
            year = date.isocalendar()[0]
            key = f"{year}-W{week:02d}"
            
            weekly_data[key]['phone'] += session.get('phone_time', 0)
            weekly_data[key]['laptop'] += session.get('laptop_time', 0)
            weekly_data[key]['sessions'] += 1
        except (KeyError, ValueError):
            continue
    
    return jsonify({
        'weeks': len(weekly_data),
        'weekly_stats': {
            key: {
                'phone': int(data['phone']),
                'laptop': int(data['laptop']),
                'sessions': data['sessions']
            }
            for key, data in sorted(weekly_data.items())
        }
    })


@app.route('/api/download', methods=['GET'])
def download_data():
    """Download all data as JSON."""
    from flask import send_file
    
    if SESSION_FILE.exists():
        return send_file(
            SESSION_FILE,
            as_attachment=True,
            download_name=f'screen-time-data-{datetime.now().strftime("%Y%m%d")}.json'
        )
    
    return jsonify({'error': 'No data available'}), 404


# ============================================================================
# WEB DASHBOARD
# ============================================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Screen Time Monitor Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            color: white;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .stat-card h3 {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .stat-phone { border-left: 4px solid #00d4ff; }
        .stat-laptop { border-left: 4px solid #ff6b6b; }
        .stat-session { border-left: 4px solid #51cf66; }
        
        .chart-container {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            position: relative;
            height: 400px;
        }
        
        .chart-title {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2em;
            font-weight: 600;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: white;
        }
        
        .error {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .refresh-btn {
            background: white;
            color: #667eea;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            float: right;
            margin-bottom: 20px;
        }
        
        .refresh-btn:hover {
            background: #f0f0f0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Screen Time Monitor</h1>
            <p>Real-time usage analytics dashboard</p>
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
        
        <div id="error" class="error" style="display:none;"></div>
        
        <div id="loading" class="loading">
            <h2>Loading data...</h2>
        </div>
        
        <div id="content" style="display:none;">
            <div class="stats-grid">
                <div class="stat-card stat-phone">
                    <h3>Phone Time</h3>
                    <div class="stat-value" id="phone-time">-</div>
                    <div id="phone-pct" style="color:#999;">0%</div>
                </div>
                
                <div class="stat-card stat-laptop">
                    <h3>Laptop Time</h3>
                    <div class="stat-value" id="laptop-time">-</div>
                    <div id="laptop-pct" style="color:#999;">0%</div>
                </div>
                
                <div class="stat-card stat-session">
                    <h3>Total Sessions</h3>
                    <div class="stat-value" id="session-count">-</div>
                    <div id="total-time" style="color:#999;">-</div>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Usage Overview</div>
                <canvas id="overviewChart"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Daily Trend</div>
                <canvas id="dailyChart"></canvas>
            </div>
        </div>
    </div>
    
    <script>
        async function loadData() {
            try {
                const response = await fetch('/api/summary');
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('phone-time').textContent = data.total_phone_time_formatted;
                    document.getElementById('phone-pct').textContent = data.phone_percentage + '%';
                    document.getElementById('laptop-time').textContent = data.total_laptop_time_formatted;
                    document.getElementById('laptop-pct').textContent = data.laptop_percentage + '%';
                    document.getElementById('session-count').textContent = data.total_sessions;
                    document.getElementById('total-time').textContent = data.total_monitoring_time_formatted;
                    
                    // Draw overview chart
                    drawOverviewChart(data.phone_percentage, data.laptop_percentage);
                    
                    // Load daily stats
                    await loadDailyStats();
                } else {
                    showError('No data available yet');
                }
            } catch (error) {
                showError('Error loading data: ' + error.message);
            }
            
            document.getElementById('loading').style.display = 'none';
            document.getElementById('content').style.display = 'block';
        }
        
        async function loadDailyStats() {
            try {
                const response = await fetch('/api/daily');
                const data = await response.json();
                
                if (response.ok && data.daily_stats) {
                    drawDailyChart(data.daily_stats);
                }
            } catch (error) {
                console.error('Error loading daily stats:', error);
            }
        }
        
        function drawOverviewChart(phone, laptop) {
            const ctx = document.getElementById('overviewChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Phone', 'Laptop'],
                    datasets: [{
                        data: [phone, laptop],
                        backgroundColor: ['#00d4ff', '#ff6b6b'],
                        borderColor: 'white',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        function drawDailyChart(dailyStats) {
            const dates = Object.keys(dailyStats).sort();
            const phoneData = dates.map(d => dailyStats[d].phone / 3600);
            const laptopData = dates.map(d => dailyStats[d].laptop / 3600);
            
            const ctx = document.getElementById('dailyChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [
                        {
                            label: 'Phone (hours)',
                            data: phoneData,
                            borderColor: '#00d4ff',
                            backgroundColor: 'rgba(0,212,255,0.1)',
                            tension: 0.3
                        },
                        {
                            label: 'Laptop (hours)',
                            data: laptopData,
                            borderColor: '#ff6b6b',
                            backgroundColor: 'rgba(255,107,107,0.1)',
                            tension: 0.3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Hours'
                            }
                        }
                    }
                }
            });
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        // Load data on page load
        window.addEventListener('load', loadData);
    </script>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def dashboard():
    """Render dashboard."""
    return render_template_string(DASHBOARD_HTML)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """500 error handler."""
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    print(f"\n{'='*60}")
    print("Screen Time Monitor - Web Server")
    print(f"{'='*60}")
    print(f"📊 Dashboard: http://localhost:{port}/")
    print(f"🔌 API: http://localhost:{port}/api/")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=debug)
