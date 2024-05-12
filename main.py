from flask import Flask, render_template
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# Function to fetch COVID-19 data from the API
def fetch_covid_data():
    url = "https://api.covidactnow.org/v2/states.json?apiKey=55599929545143aaa03b76cdbffb798d"  # Replace with the actual API endpoint
    response = requests.get(url)
    data = response.json()
    return data

# Function to generate plots using Plotly
def generate_plots(data):
    # Extract relevant data for plotting
    states = [state_data['state'] for state_data in data]
    total_cases = [state_data['actuals']['cases'] for state_data in data]
    total_deaths = [state_data['actuals']['deaths'] for state_data in data]
    
    # Create Plotly bar chart for total cases
    total_cases_fig = go.Figure(data=[go.Bar(x=states, y=total_cases)])
    total_cases_fig.update_layout(title="Total COVID-19 Cases by State")
    
    # Create Plotly bar chart for total deaths
    total_deaths_fig = go.Figure(data=[go.Bar(x=states, y=total_deaths)])
    total_deaths_fig.update_layout(title="Total COVID-19 Deaths by State")
    
    return total_cases_fig, total_deaths_fig

# Route to display the COVID-19 dashboard
@app.route('/')
def covid_dashboard():
    data = fetch_covid_data()
    total_cases_fig, total_deaths_fig = generate_plots(data)
    
    return render_template('dashboard.html', total_cases=total_cases_fig.to_html(full_html=False), 
                           total_deaths=total_deaths_fig.to_html(full_html=False))

if __name__ == '__main__':
    app.run(debug=True)
