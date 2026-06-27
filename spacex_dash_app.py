# spacex_dash_app.py
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign':'center'}),
    dcc.Dropdown(id='site-dropdown',
        options=[{'label':'All Sites','value':'ALL'}] +
                [{'label':s,'value':s} for s in spacex_df['Launch Site'].unique()],
        value='ALL', placeholder='Select a Launch Site', searchable=True),
    dcc.Graph(id='success-pie-chart'),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
        marks={i:str(i) for i in range(0,10001,2500)},
        value=[min_payload, max_payload]),
    dcc.Graph(id='success-payload-scatter-chart')
])

@app.callback(Output('success-pie-chart','figure'), Input('site-dropdown','value'))
def update_pie(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success by Site')
    else:
        df = spacex_df[spacex_df['Launch Site']==site]
        fig = px.pie(df, names='class', title=f'Success vs Failure for {site}')
    return fig

@app.callback(Output('success-payload-scatter-chart','figure'),
    [Input('site-dropdown','value'), Input('payload-slider','value')])
def update_scatter(site, payload):
    df = spacex_df[(spacex_df['Payload Mass (kg)']>=payload[0]) & (spacex_df['Payload Mass (kg)']<=payload[1])]
    if site != 'ALL':
        df = df[df['Launch Site']==site]
    fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload vs Outcome')
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)