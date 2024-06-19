import csv
import plotly.graph_objects as go

def orchid_results(csv_file):
    timestamp = []
    orchids = []
    sunlight = []
    humidity = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            timestamp.append(float(row['timestamp']))
            orchids.append(float(row['ORCHIDS']))
            sunlight.append(float(row['SUNLIGHT']))
            humidity.append(float(row['HUMIDITY']))

    return timestamp, orchids, sunlight, humidity

orchid_path_0 = "orchid-1.csv"
orchid_path_1 = "orchid0.csv"
orchid_path_2 = "orchid1.csv"

timestamp_0, orchids_0, sunlight_0, humidity_0 = orchid_results(orchid_path_0)

timestamp_1, orchids_1, sunlight_1, humidity_1 = orchid_results(orchid_path_1)

timestamp_2, orchids_2, sunlight_2, humidity_2 = orchid_results(orchid_path_2)


fig = go.Figure()

# Plot y1
fig.add_trace(go.Scatter(x=timestamp_2, y=orchids_2, mode='lines', name='Orchids'))

# Plot y2
fig.add_trace(go.Scatter(x=timestamp_2, y=sunlight_2, mode='lines', name='Sunlight', yaxis='y2'))

# Plot y3
fig.add_trace(go.Scatter(x=timestamp_2, y=humidity_2, mode='lines', name='Humidity', yaxis='y3'))

# Update layout
fig.update_layout(
    title='Orchids',
    xaxis=dict(title='Time'),
    yaxis=dict(title='Orchids', color='blue'),
    yaxis2=dict(title='Sunlight', color='red', overlaying='y', side='right'),
    yaxis3=dict(title='Humidity', color='green', overlaying='y', side='right')
)

fig.show()
