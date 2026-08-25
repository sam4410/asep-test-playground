import streamlit as st
import pandas as pd
import pytest
from pages.dashboard import load_data, display_metrics, display_chart, main
from db import create_tables, drop_tables, get_connection

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup and teardown for the database."""
    create_tables()
    yield
    drop_tables()

def test_load_data():
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

def test_display_metrics(mocker):
    """Test displaying metrics on the dashboard."""
    df = pd.DataFrame({
        'client_name': ['John Doe', 'Jane Smith'],
        'client_relationship': ['Regular', 'VIP'],
        'reminder_message': ['Payment due', 'Invoice overdue']
    })

    mock_metric = mocker.patch('streamlit.metric')
    display_metrics(df)
    assert mock_metric.call_count == 2
    mock_metric.assert_any_call(label="Total Reminders", value=2)
    mock_metric.assert_any_call(label="Unique Clients", value=2)

def test_display_metrics_no_reminders(mocker):
    """Test displaying metrics when there are no reminders."""
    df = pd.DataFrame(columns=['client_name', 'client_relationship', 'reminder_message'])
    mock_metric = mocker.patch('streamlit.metric')
    display_metrics(df)
    assert mock_metric.call_count == 1
    mock_metric.assert_called_with(label="Total Reminders", value=0)

def test_display_chart(mocker):
    """Test displaying the chart with reminders data."""
    df = pd.DataFrame({
        'client_relationship': ['Regular', 'VIP', 'Regular', 'New']
    })
    mock_plotly_chart = mocker.patch('streamlit.plotly_chart')
    display_chart(df)
    assert mock_plotly_chart.called

def test_display_chart_empty_dataframe(mocker):
    """Test displaying the chart with an empty dataframe."""
    df = pd.DataFrame(columns=['client_relationship'])
    mock_plotly_chart = mocker.patch('streamlit.plotly_chart')
    display_chart(df)
    assert not mock_plotly_chart.called

def test_main(mocker):
    """Test the main function of the dashboard."""
    mock_load_data = mocker.patch('pages.dashboard.load_data', return_value=pd.DataFrame())
    mock_display_metrics = mocker.patch('pages.dashboard.display_metrics')
    mock_display_chart = mocker.patch('pages.dashboard.display_chart')

    main()
    mock_load_data.assert_called_once()
    mock_display_metrics.assert_called_once()
    mock_display_chart.assert_called_once()

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