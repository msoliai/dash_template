from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option('display.float_format', '{:.2g}'.format) #for scientific notation

# read in data (incidence estimates from gnomad, topmed, and ukbb)
PANK2_gnomAD = pd.read_csv("../../IE/CoA/tier3_incidence_PANK2_AR_gnomad.tsv", sep='\t')
PANK2_TopMed = pd.read_csv("../../IE/CoA/tier3_incidence_PANK2_AR_topmed.tsv", sep='\t')
PANK2_UKBB = pd.read_csv("../../IE/CoA/tier3_incidence_PANK2_AR_ukb.tsv", sep='\t')

def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='PKAN Incidence Estimates gnomAD'),
    generate_table(PANK2_gnomAD)
])

if __name__ == '__main__':
 	app.run_server(debug=True,host = '127.0.0.1')