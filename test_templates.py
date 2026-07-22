import pytest
import sys
sys.path.insert(0, '/path/to/your/flask/app')  # Adjust this path to your Flask app

from flask import session

def test_dashboard_template(client):