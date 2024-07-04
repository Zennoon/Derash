#!/usr/bin/python3
"""
Script to run the flask application
"""
from derash import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
