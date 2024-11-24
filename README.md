# AQI-
# Pakistan Air Quality Dashboard

🌤️ A Streamlit application that provides real-time air quality data and current temperature for major cities in Pakistan.

## Features

- Displays air quality index (AQI) levels for selected cities.
- Shows current temperature in Celsius.
- Provides recommendations based on AQI levels.
- User-friendly interface with city selection.

## Technologies Used

- [Streamlit](https://streamlit.io/) - For building the web application.
- [Requests](https://docs.python-requests.org/en/master/) - For making API calls to fetch weather and air quality data.
- [Pandas](https://pandas.pydata.org/) - For data manipulation and analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run weather.py
   ```

2. Open your web browser and go to `http://localhost:8501` to view the dashboard.

## API Key

This application uses the OpenWeatherMap API. You will need to sign up for an API key and replace the placeholder in the code with your actual API key.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
