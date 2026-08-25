import pandas as pd
import pytest
from pages.feature import add_reminder, load_reminders, display_reminders, main
from db import create_tables, drop_tables, get_connection

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup and teardown for the database."""
    create_tables()
    yield
    drop_tables()

def test_add_reminder():
    """Test adding a reminder to the database."""
    add_reminder("Alice", "Regular", "Payment due next week")
    
    # Verify the reminder was added
    reminders_df = load_reminders()
    assert len(reminders_df) == 1
    assert reminders_df['client_name'][0] == "Alice"
    assert reminders_df['client_relationship'][0] == "Regular"
    assert reminders_df['reminder_message'][0] == "Payment due next week"

def test_add_reminder_edge_case_empty_fields():
    """Test adding a reminder with empty fields."""
    add_reminder("", "", "")
    
    # Verify no reminder was added
    reminders_df = load_reminders()
    assert len(reminders_df) == 0

def test_load_reminders():
    """Test loading reminders from the database."""
    add_reminder("Bob", "VIP", "Invoice overdue")
    reminders_df = load_reminders()
    
    assert isinstance(reminders_df, pd.DataFrame)
    assert not reminders_df.empty
    assert reminders_df.shape[0] == 1
    assert reminders_df['client_name'][0] == "Bob"

def test_display_reminders(mocker):
    """Test displaying reminders in a table."""
    df = pd.DataFrame({
        'client_name': ['Alice', 'Bob'],
        'client_relationship': ['Regular', 'VIP'],
        'reminder_message': ['Payment due next week', 'Invoice overdue']
    })
    
    mock_table = mocker.patch('streamlit.table')
    display_reminders(df)
    assert mock_table.called

def test_display_reminders_empty_dataframe(mocker):
    """Test displaying reminders with an empty dataframe."""
    df = pd.DataFrame(columns=['client_name', 'client_relationship', 'reminder_message'])
    mock_table = mocker.patch('streamlit.table')
    display_reminders(df)
    assert not mock_table.called

def test_main(mocker):
    """Test the main function of the automated reminder tool."""
    mock_add_reminder = mocker.patch('pages.feature.add_reminder')
    mock_load_reminders = mocker.patch('pages.feature.load_reminders', return_value=pd.DataFrame())
    mock_display_reminders = mocker.patch('pages.feature.display_reminders')

    main()
    mock_add_reminder.assert_called_once()
    mock_load_reminders.assert_called_once()
    mock_display_reminders.assert_called_once()

def test_streamlit_import():
    """Test if Streamlit can be imported."""
    try:
        import streamlit
    except ImportError:
        pytest.fail("Streamlit module is not installed.")

def test_streamlit_installed():
    """Check if Streamlit is installed."""
    import pkg_resources
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    assert 'streamlit' in installed_packages, "Streamlit is not installed."

def test_pandas_import():
    """Test if Pandas can be imported."""
    try:
        import pandas as pd
    except ImportError:
        pytest.fail("Pandas module is not installed.")