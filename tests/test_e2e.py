import os
import pytest
from playwright.sync_api import Page

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

def test_quiz_creation_and_taking(page: Page):
    # Navigate to the quiz creation page
    page.goto(f"{BASE_URL}/")

    # Create a new quiz
    page.fill('input#title', 'Sample Quiz')
    page.fill('textarea#questions', '[{"question_text": "What is the capital of France?", "question_type": "multiple_choice", "options": ["Paris", "London", "Berlin"], "correct_answer": "Paris"}]')
    page.click('button:has-text("Create Quiz")')

    # Verify quiz creation success
    page.wait_for_selector('text=Quiz created successfully')

    # Navigate to the quiz taking interface
    page.goto(f"{BASE_URL}/quizzes/sample-quiz-id")  # Replace with actual quiz ID after creation

    # Fill in answers for the quiz
    page.fill('input[type="text"]', 'Paris')  # Assuming the first question is displayed
    
    # Submit the quiz
    page.click('button#submitQuiz')

    # Verify quiz submission success
    page.wait_for_selector('text=Quiz submitted successfully')
    
    # Optionally, check for score display if implemented
    # page.wait_for_selector('text=Score:')