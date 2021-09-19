# conda install -c conda-forge dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

data = pd.read_csv('analog-data.csv')
data['Time'] = pd.to_datetime((data['Time']))

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Pulsed Data",),
        html.P(
            children="Data collected when using LM555 timer to drive output of LED",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Time"],
                        "y": data["Amplitude"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Pulsed Light Signal"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
