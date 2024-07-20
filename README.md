# FunOlympics Dashboard

## Overview

The FunOlympics Dashboard is an interactive web application designed to visualize and analyze web server logs data. The application provides insights into user activities, popular sports, peak traffic periods, and more. It uses various data visualization techniques to present the information in an easily digestible format.

## Features

- **Dashboard**: 
  - Key Performance Indicators (KPIs)
  - Number of Visits per Country
  - Popular Sports
  - Referral Traffic and Status Codes
  - Heatmap of Peak Traffic Periods
  - Time Series Plot: Number of Requests Over Time

- **Report**: 
  - Descriptive Statistics of the web server logs

## Tech Stack

- **Programming Language**: Python
- **Libraries**:
  - `streamlit`
  - `pandas`
  - `requests`
  - `plotly`
  - `wordcloud`
  - `matplotlib`
  - `datetime`
- **Tools**:
  - Git and GitHub

## Hardware and Software Requirements

### Development Requirements
- **Hardware**: 
  - HP ProBook, 8 GB RAM, 120 MB storage, Intel i5 processor, Solid State Drive
- **Software**: 
  - Visual Studio Code, Python
- **Operating System**: 
  - Windows 10

### End User Requirements
- **Hardware**: 
  - Laptop with a good internet connection
- **Software**: 
  - Internet browser

## Deployment Strategy

The FunOlympics Dashboard is deployed using a staged deployment approach to ensure stability and minimize disruptions. The application is deployed to Streamlit Cloud via GitHub, making it accessible to users with minimal setup.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/funolympics-dashboard.git
   cd funolympics-dashboard
   ```

2. **Set up a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**:
   ```sh
   streamlit run app.py
   ```

## Deploying to Streamlit Cloud

1. **Push your code to GitHub**:
   Make sure you have pushed your latest changes to your GitHub repository.

2. **Create a Streamlit Cloud app**:
   - Go to [Streamlit Cloud](https://share.streamlit.io/)
   - Log in with your GitHub account.
   - Click on "New app" and select your repository.
   - Follow the instructions to deploy your app.

3. **Configuration**:
   Ensure that your repository contains:
   - `app.py`: Your main Streamlit application file.
   - `requirements.txt`: A file listing all the dependencies.

## API Endpoint

The application fetches data from a cleaned web server logs API. Update the `api_url` variable in `app.py` to point to your API endpoint:
```python
api_url = "http://localhost:5000/clean_data"
```

## Troubleshooting

### Common Errors

- **ModuleNotFoundError**: Ensure all dependencies are listed in `requirements.txt` and are correctly installed.
- **Connection Errors**: Check your API endpoint and ensure it is accessible.

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README to better fit your project and its specifics.
