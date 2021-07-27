import traceback

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import visdcc

from mylegacy.cli.rpc import (
    redeem,
    utils,
    init_legacy,
    TransactionPayload__ScriptFunction,
)

app = dash.Dash(
    __name__,
    external_stylesheets=[
        'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css'
    ],
)
app.title = "MyLegacy"
app.layout = html.Div(
    html.Div(
        html.Div(
            dbc.Container(
                [
                    visdcc.Run_js(id='javascript'),
                    visdcc.Run_js(id='javascript2'),
                    html.H1("MyLegacy"),
                    html.P("Leave your legacy wisely."),
                    html.Br(),
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                dbc.Card(
                                    [
                                        dbc.CardHeader([html.H2('Init Legacy')]),
                                        dbc.CardBody(
                                            [
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
                                                                        dbc.Label(
                                                                            "Freq"
                                                                        ),
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
                                        dbc.CardHeader([html.H2('Redeem')]),
                                        dbc.CardBody(
                                            [
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
                    ),
                ]
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


def js_send_txn(script: TransactionPayload__ScriptFunction, alert_id) -> str:
    payloadInHex = "0x02" + script.value.bcs_serialize().hex()
    return f"""
        window.initialize().then(
            async () => {{
                await window.connect()
                await window.send_transaction({payloadInHex!r}, {alert_id!r})
            }}
        )
    """


@app.callback(
    Output('javascript', 'run'),
    Output("init_legacy-alert", "is_open"),
    Output("init_legacy-alert", "children"),
    Output("init_legacy-alert", "color"),
    Input("init_legacy-button", "n_clicks"),
    State("init_legacy-payee_address", "value"),
    State("init_legacy-total_value", "value"),
    State("init_legacy-times", "value"),
    State("init_legacy-freq_num", "value"),
    State("init_legacy-freq_unit", "value"),
)
def inti_legacy_calback(
    n_clicks, payee_address, total_value, times, freq_num, freq_unit
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

        script = init_legacy(
            payee=utils.account_address(payee_address),
            total_value=float(total_value),
            times=int(times),
            freq=freq,
        )
        js_script = js_send_txn(script, "init_legacy-alert")
    except Exception:
        return (
            "",
            True,
            traceback.format_exc(),
            "danger",
        )
    else:
        return (
            js_script,
            True,
            "Submitting your transaction...",
            "success",
        )


@app.callback(
    Output('javascript2', 'run'),
    Output("redeem-alert", "is_open"),
    Output("redeem-alert", "children"),
    Output("redeem-alert", "color"),
    Input("redeem-button", "n_clicks"),
    State("redeem-payer_address", "value"),
)
def redeem_calback(n_clicks, payer_address):
    if n_clicks is None:
        raise PreventUpdate

    try:
        script = redeem(utils.account_address(payer_address))
        js_script = js_send_txn(script, 'redeem-alert')
    except Exception:
        return (
            "",
            True,
            traceback.format_exc(),
            "danger",
        )
    else:
        return (
            js_script,
            True,
            "Submitting your transaction...",
            "success",
        )


if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port='10123',
        debug=False,
    )
