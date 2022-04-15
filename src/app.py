# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser. Test

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

stats = importr('stats')

app = Dash(__name__)

# import data (genebass)
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)

pcsk9_e78_df = pd.read_csv("../../genebass/pcsk9_E78_disorders_of_lipoprotein_metabolism_genebass.csv")
pcsk9_ldl_df = pd.read_csv("../../genebass/pcsk9_ldl_direct_genebass.csv")

df = pcsk9_e78_df.merge(pcsk9_ldl_df, on = ["variant_id", 'consequence', 'hgvsp', 'allele_count', 'homozygote_count', 
                                            'allele_number', 'allele_frequency'], suffixes = ("_e78", '_ldl'))

# calculate FDR
fdr_e78 = stats.p_adjust(FloatVector(df.pval_e78), method = 'fdr')
fdr_ldl = stats.p_adjust(FloatVector(df.pval_ldl), method = 'fdr')

# add FDR to df
df['fdr_e78'] = fdr_e78
df['fdr_ldl'] = fdr_ldl

# plot data
#fig = px.scatter(df.query, 
#           x = 'beta_e78', 
#           y = 'beta_ldl', color = 'consequence', 
#           hover_data = ['variant_id','allele_count', 'homozygote_count', 'allele_number', 'pval_e78', 'pval_ldl'],
#           template = 'plotly_white',
#           height = 500, width = 700)

app.layout = html.Div(children=[
    html.H1(children='Human Genetics Dashboard'),

    html.Div(children='''
        Allelic Series Identifiction in genebass (UKBB)
    '''),

    dcc.Graph(id='genebass-graph'),
    
    dcc.Slider(
        0,
        0.30,
        step=None,
        marks={
            0: '0%',
            0.01: '1%',
            0.05: '5%',
            0.10: '10%',
            0.15: '15%',
            0.20: '20%',
            0.25: '25%',
            0.30: '30%'
        },
        value=10,
        id='pval-slider',
        tooltip={"placement": "bottom", "always_visible": True}
    )
])

@app.callback(
    Output('genebass-graph', 'figure'),
    Input('pval-slider', 'value'))
def update_figure(selected_fdr):
    filtered_fdr = df[df.fdr_e78 <= selected_fdr]

    fig = px.scatter(filtered_fdr, 
           x = 'beta_e78', 
           y = 'beta_ldl', color = 'consequence', 
           hover_data = ['variant_id','allele_count', 'homozygote_count', 'allele_number', 'pval_e78', 'pval_ldl', 'fdr_e78', 'fdr_ldl'],
           template = 'plotly_white',
           height = 500, width = 700)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    #app.run_server(debug=True)
 	app.run_server(debug=True,host = '127.0.0.1')
