import dash
from layout import get_layout
from callback import register_callbacks

app = dash.Dash(__name__)

server = app.server

app.layout = get_layout()

register_callbacks()


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="8050")
