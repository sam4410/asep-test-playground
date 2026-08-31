import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SettingsPage from '../SettingsPage';
import * as settingsClient from '../src/lib/settingsClient';

jest.mock('../src/lib/settingsClient');

describe('SettingsPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state', () => {
    render(<SettingsPage />);
    expect(screen.getByText(/Loading settings…/)).toBeInTheDocument();
  });

  test('renders error state when settings fail to load', async () => {
    (settingsClient.fetchSettings as jest.Mock).mockRejectedValue(new Error('Network error'));
    render(<SettingsPage />);
    
    await waitFor(() => expect(screen.getByText(/Couldn't load settings. Please try again./)).toBeInTheDocument());
  });

  test('renders settings when loaded successfully', async () => {
    const mockSettings = { theme: 'light' };
    (settingsClient.fetchSettings as jest.Mock).mockResolvedValue(mockSettings);
    render(<SettingsPage />);
    
    await waitFor(() => expect(screen.getByText(/Settings/)).toBeInTheDocument());
    expect(screen.getByDisplayValue('light')).toBeInTheDocument();
  });

  test('updates settings successfully', async () => {
    const mockSettings = { theme: 'light' };
    (settingsClient.fetchSettings as jest.Mock).mockResolvedValue(mockSettings);
    (settingsClient.updateSettings as jest.Mock).mockResolvedValue({ theme: 'dark' });
    
    render(<SettingsPage />);
    await waitFor(() => expect(screen.getByText(/Settings/)).toBeInTheDocument());
    
    fireEvent.change(screen.getByLabelText(/Theme/i), { target: { value: 'dark' } });
    
    await waitFor(() => expect(screen.getByDisplayValue('dark')).toBeInTheDocument());
  });

  test('handles update settings error', async () => {
    const mockSettings = { theme: 'light' };
    (settingsClient.fetchSettings as jest.Mock).mockResolvedValue(mockSettings);
    (settingsClient.updateSettings as jest.Mock).mockRejectedValue(new Error('Failed to save your changes.'));
    
    render(<SettingsPage />);
    await waitFor(() => expect(screen.getByText(/Settings/)).toBeInTheDocument());
    
    fireEvent.change(screen.getByLabelText(/Theme/i), { target: { value: 'dark' } });
    
    await waitFor(() => expect(screen.getByText(/Failed to save your changes./)).toBeInTheDocument());
  });

  test('resets settings successfully', async () => {
    const mockSettings = { theme: 'light' };
    (settingsClient.fetchSettings as jest.Mock).mockResolvedValue(mockSettings);
    (settingsClient.resetSettings as jest.Mock).mockResolvedValue({ theme: 'light' });
    
    render(<SettingsPage />);
    await waitFor(() => expect(screen.getByText(/Settings/)).toBeInTheDocument());
    
    fireEvent.click(screen.getByText(/Reset/i));
    
    await waitFor(() => expect(screen.getByDisplayValue('light')).toBeInTheDocument());
  });

  test('handles reset settings error', async () => {
    const mockSettings = { theme: 'light' };
    (settingsClient.fetchSettings as jest.Mock).mockResolvedValue(mockSettings);
    (settingsClient.resetSettings as jest.Mock).mockRejectedValue(new Error('Failed to reset settings.'));
    
    render(<SettingsPage />);
    await waitFor(() => expect(screen.getByText(/Settings/)).toBeInTheDocument());
    
    fireEvent.click(screen.getByText(/Reset/i));
    
    await waitFor(() => expect(screen.getByText(/Failed to reset settings./)).toBeInTheDocument());
  });
});