from flask import Flask, request, render_template
from collections import Counter

app = Flask(__name__)

# Initialize analytics data
analytics_data = {
    'total_queries': 0,
    'topic_counter': Counter(),
    'user_satisfaction': [],
    'chat_history': []  # New list to store chat history
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query']
    satisfaction_rating = int(request.form['satisfaction'])

    # Update analytics
    analytics_data['total_queries'] += 1
    analytics_data['topic_counter'][user_query] += 1
    analytics_data['user_satisfaction'].append(satisfaction_rating)
    
    # Store the chat in history
    analytics_data['chat_history'].append({
        'query': user_query,
        'satisfaction': satisfaction_rating
    })

    # Here you would typically process the query and return a response
    response = f"Processed query: {user_query}"
    
    return response

@app.route('/analytics')
def analytics():
    average_satisfaction = sum(analytics_data['user_satisfaction']) / len(analytics_data['user_satisfaction']) if analytics_data['user_satisfaction'] else 0
    most_common_topic = analytics_data['topic_counter'].most_common(1)
    
    return render_template('analytics.html', 
                           total_queries=analytics_data['total_queries'],
                           average_satisfaction=average_satisfaction,
                           most_common_topic=most_common_topic,
                           chat_history=analytics_data['chat_history'])  # Pass chat history to template

if __name__ == '__main__':
    app.run(debug=True)
