import plotly.express as px


def get_initial_map():
    fig = px.scatter_geo()
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        width=1800,
        height=800,
    )
    return fig
