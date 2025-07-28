# This is the main Flask application file.
# More code will be added here later.
from flask import Flask

app = Flask(__name__)
from data_processing import load_and_clean_data

# Load and process data once when the app starts
data_df = load_and_clean_data()

# Get the list of unique countries for the dropdown
if data_df is not None:
    country_list = sorted(data_df['Paises'].unique().tolist())
else:
    country_list = []


@app.route('/')
def index():
    # This route will render the main HTML template.
    return render_template('index.html', countries=country_list)

@app.route('/plot', methods=['POST'])
def plot_country_data():
    data = request.get_json()
    selected_country = data.get('country')

    # Ensure data_df is accessible (it's loaded when the app starts)
    global data_df
    if data_df is None or data_df.empty:
        return jsonify({'error': 'Data not loaded or empty'}), 500

    # Create the base scatter plot with all filtered data
    fig = go.Figure()

    # Use the filtered data (data_df) directly as it already has the population filter
    # Recalculate bubble sizes as they are not stored in data_df
    scaling_factor = 0.5e-5 # Use the same scaling factor as in the notebook
    bubble_sizes = data_df['Población'] * scaling_factor

    # Add all countries as faint points
    fig.add_trace(
        go.Scatter(
            x=data_df['porcentaje de uso de internet'],
            y=data_df['Demanda per capita'],
            mode='markers',
            name='All Countries (Population >= 5M)',
            text=data_df['Paises'], # Use country names as hover text
            marker=dict(
                size=bubble_sizes,
                opacity=0.3 # Make them faint
            )
        )
    )

    # Highlight the selected country
    if selected_country and selected_country != '' and selected_country in data_df['Paises'].values:
        country_data = data_df[data_df['Paises'] == selected_country]
        # Ensure highlight bubble size is calculated for the single selected country
        highlight_bubble_size = country_data['Población'].values[0] * scaling_factor
        fig.add_trace(
            go.Scatter(
                x=country_data['porcentaje de uso de internet'],
                y=country_data['Demanda per capita'],
                mode='markers',
                name=selected_country,
                text=country_data['Paises'], # Use country name as hover text
                marker=dict(
                    size=highlight_bubble_size,
                    color='red', # Highlight color
                    line=dict(width=2, color='DarkRed') # Add a border
                )
            )
        )

    # Update layout for better readability
    fig.update_layout(
        title='Demanda per cápita de papel y cartón vs. Uso de Internet',
        xaxis_title='Porcentaje de uso de internet',
        yaxis_title='Demanda per cápita de papel y cartón en KG',
        hovermode='closest', # Show closest data on hover
        showlegend=True # Show legend
    )

    # Convert Plotly figure to JSON
    graph_json = pio.to_json(fig)

    return jsonify(graph_json)

if __name__ == '__main__':
    app.run(debug=True)
