from flask import Flask, jsonify
import random
from faker import Faker
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Initialize Faker for generating fake data
fake = Faker()

# Global variables to store logs and count
web_logs = []
log_count = 0

# Function to generate a random web server log entry
def generate_web_log():
    global log_count
    ip_address = fake.ipv4()
    timestamp = fake.date_time_this_month().isoformat()  # Convert datetime to ISO string
    requested_url = fake.uri()
    request_method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
    status_code = random.choice([200, 404, 500])
    referrer_method = random.choice(['search_engine', 'direct_link', 'social_media'])
    user_agent = fake.user_agent()
    num_users = random.randint(1, 1000)
    num_unique_visitors = random.randint(1, num_users)
    location = fake.country()  # Add country field
    peak_traffic_period = fake.time(pattern='%H:%M:%S')
    visit_duration = random.randint(10, 600)  # Random visit duration in seconds
    page_views_per_visit = random.randint(1, 10)
    top_viewed_page = fake.uri()
    http_referrer = fake.uri()
    http_status = random.choice(['OK', 'Not Found', 'Server Error'])
    http_errors = random.randint(0, 5)
    sports_related = random.choice(['Football', 'Basketball', 'Tennis', 'Swimming', 'Running'])

    # Generate search terms based on sports-related field
    if sports_related == 'Football':
        search_terms = ['football', 'soccer', 'goal', 'penalty', 'stadium']
    elif sports_related == 'Basketball':
        search_terms = ['basketball', 'hoop', 'dunk', 'court', 'player']
    elif sports_related == 'Tennis':
        search_terms = ['tennis', 'racket', 'serve', 'match', 'court']
    elif sports_related == 'Swimming':
        search_terms = ['swimming', 'pool', 'stroke', 'laps', 'competition']
    else:  # Running
        search_terms = ['running', 'jogging', 'race', 'sprint', 'marathon']

    # Additional fields
    content_type = random.choice(['article', 'video', 'event_schedule'])
    referral_traffic = referrer_method
    
    if referrer_method == 'search_engine':
        search_engine = fake.random_element(elements=('Google', 'Bing', 'Yahoo', 'DuckDuckGo'))
        user_agent += f' {search_engine}'
        referral_traffic = f'{search_engine} (Search Engine)'
    elif referrer_method == 'social_media':
        social_media = fake.random_element(elements=('Facebook', 'Twitter', 'Instagram', 'LinkedIn'))
        user_agent += f' {social_media}'
        referral_traffic = f'SM-{social_media}'
    
    log = {
        'ip_address': ip_address,
        'timestamp': timestamp,  # Store as ISO string
        'requested_url': requested_url,
        'request_method': request_method,
        'status_code': status_code,
        'referrer_method': referrer_method,
        'user_agent': user_agent,
        'num_users': num_users,
        'num_unique_visitors': num_unique_visitors,
        'location': location,
        'peak_traffic_period': peak_traffic_period,
        'visit_duration': visit_duration,
        'page_views_per_visit': page_views_per_visit,
        'top_viewed_page': top_viewed_page,
        'http_referrer': http_referrer,
        'http_status': http_status,
        'http_errors': http_errors,
        'search_terms': search_terms,
        'sports_related': sports_related,
        'content_type': content_type,
        'referral_traffic': referral_traffic
    }

    # Append log to the list and update count
    web_logs.append(log)
    log_count += 1

# Function to continuously generate web server logs
def continuous_web_logs():
    while True:
        for _ in range(200):  # Generate 200 logs
            generate_web_log()
        time.sleep(5)  # Adjust the interval to 5 seconds

# Start generating web server logs in a separate thread
thread = threading.Thread(target=continuous_web_logs)
thread.daemon = True
thread.start()

# API endpoint for retrieving the continuously generated web server logs and count
@app.route('/web_logs')
def get_web_logs():
    global web_logs, log_count
    print("Request received for web logs")
    print("Returning response:", {'web_logs': web_logs, 'log_count': log_count})
    return jsonify({'web_logs': web_logs, 'log_count': log_count})

# API endpoint for cleaning and transforming the data
@app.route('/clean_data')
def clean_data():
    global web_logs
    cleaned_logs = []
    for log in web_logs:
        try:
            # Anonymize IP addresses
            log['ip_address'] = 'xxx.xxx.xxx.xxx'
            
            # Convert numerical variables stored as strings to numeric data types
            log['num_users'] = int(log['num_users'])
            log['num_unique_visitors'] = int(log['num_unique_visitors'])
            log['visit_duration'] = int(log['visit_duration'])
            log['page_views_per_visit'] = int(log['page_views_per_visit'])
            log['http_errors'] = int(log['http_errors'])
            
            cleaned_logs.append(log)
        except Exception as e:
            print(f"Error processing log: {log}")
            print(f"Exception: {e}")

    return jsonify({'cleaned_data': cleaned_logs})

if __name__ == '__main__':
    app.run(debug=True)