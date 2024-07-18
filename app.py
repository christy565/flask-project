from flask import Flask, redirect, request
import redis
import os
import random

app = Flask(__name__)

# Connect to Redis
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

# List of popular links for redirection
popular_links = [
    'https://example.com/popular1',
    'https://example.com/popular2',
    'https://example.com/popular3',
]

@app.route('/<obfuscated_link>')
def redirect_link(obfuscated_link):
    final_destination = r.get(obfuscated_link)

    if not final_destination:
        return "Invalid link", 404

    # Check access count
    access_count = r.incr(f"{obfuscated_link}_count")
    if access_count > 2:
        # Redirect to a random popular link
        return redirect(random.choice(popular_links), code=302)

    return redirect(final_destination.decode('utf-8'), code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
