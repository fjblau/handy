# Handy - Goals Tracking App

Handy is a goals-tracking app that helps you organize your life goals across different areas, track progress, and maintain motivation through regular reflection.

## Features

- **Profile Setup**: Create your user profile with job information, hobbies, and life area prioritization
- **Goals Management**: Track goals organized by life areas with detailed goal information
- **Affirmations**: Create and manage personal affirmations
- **Daily Reflection**: Track daily affirmation adherence and mood
- **Dashboard**: Visualize progress and trends

## Running the App

### Standard Mode

To run the app in standard mode:

```bash
streamlit run handy.py
```

### Mobile-Friendly Mode

To run the app with mobile-friendly settings:

```bash
./run_pwa.sh
```

Or manually:

```bash
streamlit run handy.py --server.enableCORS=false --server.enableXsrfProtection=false
```

## Mobile-Optimized Features

The mobile version includes:
- Responsive design that adapts to screen size
- Mobile-friendly UI with optimized touch targets
- Bottom navigation bar for easy access to all sections
- Condensed content for better mobile viewing
- Larger buttons and input fields for easier interaction

## Using on Mobile Devices

1. Access the app from your mobile browser
2. Use the bottom navigation bar to switch between sections
3. For the best experience, bookmark the app for easy access

## Development

### Project Structure

- `handy.py`: Main application file with mobile-friendly enhancements
- `run_pwa.sh`: Script to run the app with mobile-friendly settings

### Mobile UI Components

The mobile UI includes:
- Bottom navigation bar with icons for each section
- Responsive layouts that adapt to screen size
- Touch-optimized buttons and input fields
- Condensed content for smaller screens

## Data Management

- User data is stored in Streamlit's session state
- Export/import functionality is available through JSON files
- No persistent database is currently implemented