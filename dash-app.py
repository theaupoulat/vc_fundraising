# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# colors = {"background":"#111111", 'text' : '#7FDBFF'}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------ data parsing section ------------------

df = pd.read_csv(
    "https://raw.githubusercontent.com/theaupoulat/vc_fundraising/master/levee2019.csv")

# format amount raised
df["amount_raised"] = (df["amount_raised"]
                       .str.replace("M", "000000")
                       .str.replace(" ", "")
                       .str.replace(".", "")
                       .str.replace("€", "")
                       .str.replace("NC", "0")
                       .str.replace('\D', '')
                       .astype(int)
                       ) / 1000000

# groupby object to extract aggregate values
per_week = df.groupby("week_number")

# dataframe creation for plotting purposes
d = {'weekly_amount': per_week.amount_raised.sum(
), "total_fundraisings": per_week.size()}
df_week_recap = pd.DataFrame(data=d)
weekly_data = [
    {
        "x": df_week_recap.index,
        "y": df_week_recap["weekly_amount"],
        "mode": "lines",
        "line":{
            "color": "rgb(219, 64, 82)"
        },
        "name": "millions"
    },
    {
        "x": df_week_recap.index,
        "y": df_week_recap["total_fundraisings"],
        "type": "bar",
        "name":"fundraisings",
        "yaxis": 'y2',
        "color":"red"
    }
]


# ------------------ app design section ------------------

app.layout = html.Div([
    dcc.Graph(id='graph_with_slider',
              figure={
                  "data": weekly_data,
                  "layout": {
                      "title": "Weekly summary",
                      "yaxis": {
                          "title": "Weekly amount",
                          "overlaying": "y2"
                      },
                      "yaxis2": {
                          "title": "Fundraisings",
                          "tick0": 0,
                          "dtick": 4,
                          "side": "right",
                          "showgrid": False
                      }
                  }
              }
              ),

])


"""
@app.callback(
    Output('graph_with_slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df.continent == i]
        traces.append(go.Scatter(
            x=df_by_continent["gdpPercap"],
            y=df_by_continent["lifeExp"],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

"""
# ------------------ debugger activation ------------------
if __name__ == '__main__':
    app.run_server(debug=True)
