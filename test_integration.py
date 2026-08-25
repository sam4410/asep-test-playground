import pytest
import pandas as pd
import streamlit as st
from db import create_tables, drop_tables, get_connection
from pages.dashboard import load_data
from pages.feature import add_reminder, load_reminders
from auth import login, signup

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup and teardown for the database."""
    create_tables()
    yield
    drop_tables()

def test_dashboard_integration(mocker):
    """Test the integration of the dashboard components."""
    # Mock the data loading
    mocker.patch('pages.dashboard.load_data', return_value=pd.DataFrame({
        'client_name': ['John Doe'],
        'client_relationship': ['Regular'],
        'reminder_message': ['Payment due']
    }))
    
    # Call the main function of the dashboard
    from pages.dashboard import main
    main()
    
    # Verify that metrics are displayed
    assert st.session_state['authenticated'] is True
    assert st.metric.called

def test_feature_integration(mocker):
    """Test the integration of the feature components."""
    # Mock the reminder addition
    mocker.patch('pages.feature.add_reminder')
    mocker.patch('pages.feature.load_reminders', return_value=pd.DataFrame({
        'client_name': ['Alice'],
        'client_relationship': ['Regular'],
        'reminder_message': ['Payment due next week']
    }))
    
    # Call the main function of the feature
    from pages.feature import main
    main()
    
    # Verify that reminders are displayed
    assert st.session_state['authenticated'] is True
    assert st.table.called

def test_auth_integration(mocker):
    """Test the integration of the authentication components."""
    # Mock the login process
    mocker.patch('streamlit.text_input', side_effect=["test_user", "test_pass"])
    mocker.patch('streamlit.button', return_value=True)
    
    # Call the login function
    login()
    
    # Verify that the user is authenticated
    assert st.session_state['authenticated'] is True
    assert st.success.called

def test_add_reminder_integration():
    """Test adding a reminder and loading it back."""
    add_reminder("Bob", "VIP", "Invoice overdue")
    
    reminders_df = load_reminders()
    assert len(reminders_df) == 1
    assert reminders_df['client_name'][0] == "Bob"
    assert reminders_df['client_relationship'][0] == "VIP"
    assert reminders_df['reminder_message'][0] == "Invoice overdue"

def test_load_data_integration():
    """Test loading data from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (client_name, client_relationship, reminder_message) VALUES (?, ?, ?)",
                   ("John Doe", "Regular", "Payment due"))
    conn.commit()
    conn.close()

    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[0] == 1
    assert df['client_name'][0] == "John Doe"

def test_imports():
    """Test that required modules can be imported."""
    try:
        import streamlit
        import pandas
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_requirements():
    """Test that required packages are installed."""
    try:
        import streamlit
        import pandas
    except ImportError as e:
        pytest.fail(f"Required package not installed: {e}")