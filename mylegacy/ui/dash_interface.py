import traceback

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from mylegacy.ui.rpc_interface import init_legacy, redeem

app = dash.Dash(
    __name__,
    external_stylesheets=[
        'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css'
    ],
)
app.title = "My Legacy"
app.layout = html.Div(
    html.Div(
        html.Div(
            dbc.Container(
                dbc.Tabs(
                    [
                        dbc.Tab(
                            dbc.Card(
                                [
                                    dbc.CardHeader([html.H1('Init Legacy')]),
                                    dbc.CardBody(
                                        [
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label("Private Key"),
                                                    dbc.Input(
                                                        id="init_legacy-private_key",
                                                        placeholder="992e5...",
                                                    ),
                                                    dbc.FormText(
                                                        "I know it's crazy to ask for your private key. "
                                                        "But anyway, it's just Barnard.",
                                                        color="secondary",
                                                    ),
                                                ],
                                            ),
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label("Payee Address"),
                                                    dbc.Input(
                                                        id="init_legacy-payee_address",
                                                        placeholder="004daef...",
                                                    ),
                                                    dbc.FormText(
                                                        "Who do you wanna leave your legacy to?",
                                                        color="secondary",
                                                    ),
                                                ]
                                            ),
                                            dbc.FormGroup(
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Label(
                                                                    "Total Value"
                                                                ),
                                                                dbc.Input(
                                                                    id="init_legacy-total_value",
                                                                    value="1.0",
                                                                    inputMode="numeric",
                                                                    pattern=r"^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$|[1-9]\d*",
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Label("Times"),
                                                                dbc.Input(
                                                                    id="init_legacy-times",
                                                                    value="10",
                                                                    inputMode="numeric",
                                                                    pattern=r"^[1-9]\d*$",
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            dbc.FormGroup(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    dbc.Label("Freq"),
                                                                    dbc.Input(
                                                                        id="init_legacy-freq_num",
                                                                        value="1",
                                                                        inputMode="numeric",
                                                                        pattern=r"^[1-9]\d*$",
                                                                    ),
                                                                ]
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    dbc.Label(
                                                                        "Time Unit"
                                                                    ),
                                                                    dbc.Select(
                                                                        id="init_legacy-freq_unit",
                                                                        options=[
                                                                            {
                                                                                "label": "Years",
                                                                                "value": "1",
                                                                            },
                                                                            {
                                                                                "label": "Months",
                                                                                "value": "2",
                                                                            },
                                                                            {
                                                                                "label": "Days",
                                                                                "value": "3",
                                                                            },
                                                                            {
                                                                                "label": "Hours",
                                                                                "value": "4",
                                                                            },
                                                                            {
                                                                                "label": "Minutes",
                                                                                "value": "5",
                                                                            },
                                                                            {
                                                                                "label": "Seconds",
                                                                                "value": "6",
                                                                            },
                                                                        ],
                                                                        value="2",
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                            ),
                                            dbc.Button(
                                                "Submit",
                                                color="primary",
                                                id='init_legacy-button',
                                            ),
                                            dbc.Alert(
                                                "",
                                                id='init_legacy-alert',
                                                style={'white-space': 'pre-wrap'},
                                                is_open=False,
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            label='Init Legacy',
                        ),
                        dbc.Tab(
                            dbc.Card(
                                [
                                    dbc.CardHeader([html.H1('Redeem')]),
                                    dbc.CardBody(
                                        [
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label("Private Key"),
                                                    dbc.Input(
                                                        id="redeem-private_key",
                                                        placeholder="992e5...",
                                                    ),
                                                    dbc.FormText(
                                                        "I know it's crazy to ask for your private key. "
                                                        "But anyway, it's just Barnard.",
                                                        color="secondary",
                                                    ),
                                                ]
                                            ),
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label("Payer Address"),
                                                    dbc.Input(
                                                        id="redeem-payer_address",
                                                        placeholder="004daef...",
                                                    ),
                                                    dbc.FormText(
                                                        "Who is leaving you the legacy?",
                                                        color="secondary",
                                                    ),
                                                ]
                                            ),
                                            dbc.Button(
                                                "Submit",
                                                color="primary",
                                                id='redeem-button',
                                            ),
                                            dbc.Alert(
                                                "",
                                                id='redeem-alert',
                                                style={'white-space': 'pre-wrap'},
                                                is_open=False,
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            label="Redeem",
                        ),
                    ],
                )
            ),
            style={"margin-left": "auto", "margin-right": "auto", "width": "600px"},
        ),
        style={"display": "table-cell", "vertical-align": "middle"},
    ),
    style={
        "display": "table",
        "position": "absolute",
        "top": 0,
        "left": 0,
        "height": "100%",
        "width": "100%",
    },
)


@app.callback(
    Output("init_legacy-alert", "is_open"),
    Output("init_legacy-alert", "children"),
    Output("init_legacy-alert", "color"),
    Input("init_legacy-button", "n_clicks"),
    State("init_legacy-private_key", "value"),
    State("init_legacy-payee_address", "value"),
    State("init_legacy-total_value", "value"),
    State("init_legacy-times", "value"),
    State("init_legacy-freq_num", "value"),
    State("init_legacy-freq_unit", "value"),
)
def inti_legacy_calback(
    n_clicks, private_key, payee_address, total_value, times, freq_num, freq_unit
):
    if n_clicks is None:
        raise PreventUpdate

    try:
        freq = int(freq_num) * {
            '1': 60 * 60 * 24 * 365,  # Years
            '2': 60 * 60 * 24 * 30,  # Months
            '3': 60 * 60 * 24,  # Days
            '4': 60 * 60,  # Hours
            '5': 60,  # Minutes
            '6': 1,  # Seconds
        }[freq_unit]
        txn_hash = init_legacy(
            sender_private_key=private_key,
            payee_adress=payee_address,
            total_value=float(total_value),
            times=int(times),
            freq=freq,
        )
        return (
            True,
            "Successfully submitted your transaction. "
            "Check it out at "
            f"https://stcscan.io/barnard/transactions/detail/{txn_hash}",
            "success",
        )
    except Exception:
        return (
            True,
            traceback.format_exc(),
            "danger",
        )


@app.callback(
    Output("redeem-alert", "is_open"),
    Output("redeem-alert", "children"),
    Output("redeem-alert", "color"),
    Input("redeem-button", "n_clicks"),
    State("redeem-private_key", "value"),
    State("redeem-payer_address", "value"),
)
def redeem_calback(n_clicks, private_key, payer_address):
    if n_clicks is None:
        raise PreventUpdate

    try:
        txn_hash = redeem(
            sender_private_key=private_key,
            payer_adress=payer_address,
        )
        return (
            True,
            "Successfully submitted your transaction. "
            "Check it out at "
            f"https://stcscan.io/barnard/transactions/detail/{txn_hash}",
            "success",
        )
    except Exception:
        return (
            True,
            traceback.format_exc(),
            "danger",
        )


if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        debug=False,
    )