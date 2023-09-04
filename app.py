import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

def format_number(number):
    return '{:,.0f}'.format(number).replace(',', '.')

header = dbc.Row([
        dbc.Col(html.H1('Modelo de Valorización: Reutilización de aguas grises en recintos educacionales', 
                        style={'fontSize': '3em', 'color': '#000000','margin-top':'2px', 'text-align': 'left'}), width=10),
        dbc.Col(html.Img(src="/assets/icon.png", height='180px'), style={'margin-top':'2px', 'text-align': 'right'}, width=2)
    ],
    style={'backgroundColor': '#ADD8E6'},  # Color de fondo celeste para el rectángulo
    className="mb-4"  # Margen inferior
)   

app.layout = html.Div([
    header,
    html.H2('Selección de Escuela'),
    dcc.Dropdown(
        id='dropdown-escuela',
        options=[
            {'label':'--Seleccionar--','value':'__seleccionar__'},
            {'label': 'San Antonio de Naltahua (227 estudiantes)', 'value': 'San Antonio de Naltahua ( 227 estudiantes )'},
            {'label': 'Colegio Challay (200 estudiantes)', 'value': 'Colegio Challay ( 200 estudiantes )'},
            {'label': 'El Melocotón (213 estudiantes)', 'value': 'El Melocotón ( 213 estudiantes )'},
            {'label': 'Liceo de Montenegro (134 estudiantes)', 'value': 'Liceo de Montenegro ( 134 estudiantes )'},
            {'label': 'Escuela G-N°346 Santa Matilde (40 estudiantes)', 'value': 'Escuela G-N°346 Santa Matilde ( 40 estudiantes )'},
            {'label': 'Escuela Básica G-N°348 (12 estudiantes)', 'value': 'Escuela Básica G-N°348 ( 12 estudiantes )'},
            {'label': 'Escuela Básica G-N°352 Plazuela de Polpaico (169 estudiantes)', 'value': 'Escuela Básica G-N°352 Plazuela de Polpaico ( 169 estudiantes )'},
        ],
        value='__seleccionar__'
    ),
    html.Div(id='output-escuela'),
    html.Div(id='pregunta-matricula', style={'display': 'none', 'margin': '20px'}), 
    dcc.RadioItems(
        id='radio-matricula',
        options=[
            {'label': 'Sí', 'value': 'si'},
            {'label': 'No', 'value': 'no'},
        ],
        style={'display': 'none'}
    ),
    dcc.Input(
        id='input-matricula',
        type='number',
        style={'display': 'none'}
    ),

    html.Div(id='pregunta-lavamanos', style={'display': 'none', 'margin': '20px'}),
    dcc.RadioItems(
        id='radio-lavamanos',
        options=[
            {'label': 'Sí', 'value': 'si'},
            {'label': 'No', 'value': 'no'},
        ],
        style={'display': 'none'}
    ),
    dcc.Input(
        id='input-porcentaje',
        type='number',
        style={'display': 'none'}
    ),
    html.Div(id='output-porcentaje'),
    
    dbc.Button('Valorizar', id='btn-valorizar', n_clicks=0, color='success', style={'margin-top': '20px'}),
    
    dbc.Modal([
        dbc.ModalHeader(html.H4('Valorización de aguas grises reutilizadas', style={'font-size': '24px', 'font-weight': 'bold'})),
        dbc.ModalBody(id='modal-body'),
        dbc.ModalFooter(
            dbc.Button('Cerrar', id='close-modal', className='ml-auto', n_clicks=0)
        ),
    ], id='modal', size='lg', is_open=False)
])

@app.callback(
    [Output('output-escuela', 'children'),
     Output('pregunta-matricula', 'children'),
     Output('pregunta-matricula', 'style'),
     Output('radio-matricula', 'style'),
     Output('input-matricula', 'style'),
     Output('pregunta-lavamanos', 'children'),
     Output('pregunta-lavamanos', 'style'),
     Output('radio-lavamanos', 'style'),
     Output('input-porcentaje', 'style'),
     Output('output-porcentaje', 'children')],
    [Input('dropdown-escuela', 'value'),
     Input('radio-matricula', 'value'),
     Input('radio-lavamanos', 'value')],
)
def update_output(escuela_value, matricula_value, lavamanos_value):
    if escuela_value == '__seleccionar__':
        return (
            'Selecciona una escuela',
            None,
            {'display': 'none'},
            {'display': 'none'},
            {'display': 'none'},
            None,
            {'display': 'none'},
            {'display': 'none'},
            {'display': 'none'},
            None
        )

    output_escuela = f'Has seleccionado la escuela: {escuela_value}'
    pregunta_matricula = f'¿La escuela aún tiene una matrícula de {escuela_value.split(" ")[-3]} estudiantes?'
    pregunta_matricula_style = {'display': 'block', 'margin': '20px'}
    radio_matricula_style = {'display': 'block'}
    input_matricula_style = {'display': 'block' if matricula_value == 'no' else 'none'}

    pregunta_lavamanos = '¿El uso de lavamanos ha sido el de un periodo habitual en la última semana?'
    pregunta_lavamanos_style = {'display': 'block', 'margin': '20px'}
    radio_lavamanos_style = {'display': 'block'}
    input_porcentaje_style = {'display': 'block' if lavamanos_value == 'no' else 'none'}
    output_porcentaje = 'Ingrese el porcentaje de funcionamiento de los lavamanos, en relación al funcionamiento normal:' if lavamanos_value == 'no' else None

    return (
        output_escuela,
        pregunta_matricula,
        pregunta_matricula_style,
        radio_matricula_style,
        input_matricula_style,
        pregunta_lavamanos,
        pregunta_lavamanos_style,
        radio_lavamanos_style,
        input_porcentaje_style,
        output_porcentaje
    )

@app.callback(
    [Output('modal', 'is_open'),
     Output('modal-body', 'children')],
    [Input('btn-valorizar', 'n_clicks'),
     Input('close-modal', 'n_clicks')],
    [State('dropdown-escuela', 'value'),
     State('radio-lavamanos', 'value'),
     State('input-porcentaje', 'value'),
     State('radio-matricula', 'value'),
     State('input-matricula', 'value')]
)
def valorizar(n_clicks_valorizar, n_clicks_cerrar, escuela_value, lavamanos_value, porcentaje_value, matricula_value, matricula_input_value):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'btn-valorizar' and n_clicks_valorizar > 0:
        p = 1 if lavamanos_value == 'si' else (float(porcentaje_value) / 100 if porcentaje_value else 0)
        x = int(escuela_value.split(" ")[-3]) if matricula_value == 'si' else (int(matricula_input_value) if matricula_input_value else 0)
        
        litros_dia = p * (2.2432 * x + 29.563)
        litros_semana = litros_dia * 5
        litros_anio = litros_dia * 180
        
        ahorro_dia = litros_dia * 2
        ahorro_semana = (litros_dia * 5) * 2
        ahorro_anio = (litros_dia * 180) * 2
        
        reduccion_estres_hidrico = (litros_dia / (27 * x)) * 100
        
        potencial_riego_pasto = litros_dia / 10
        potencial_riego_especies = litros_dia / 0.33

        reduccion_huella_aguaresidual = (litros_anio / 1000) * 0.325511442155919

        reduccion_huella_aguapotable = (litros_anio/1000) * 0.00342809683924821

        reduccion_huella_total = reduccion_huella_aguapotable + reduccion_huella_aguaresidual
        
        modal_content = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H4('Proyección de aguas grises reutilizadas', className='mb-4', style={'color': 'white'}),
                    html.H5('Litros de agua reutilizados al día:', className='mb-2', style={'color': 'white'}),
                    html.P(format_number(litros_dia), style={'color': 'white','font-size': '18px'}), 
                    html.H5('Litros de agua reutilizados a la semana:', className='mb-2', style={'color': 'white'}),
                    html.P(format_number(litros_semana), style={'color': 'white','font-size': '18px'}),  
                    html.H5('Litros de agua reutilizados al año:', className='mb-2', style={'color': 'white'}),
                    html.P(format_number(litros_anio), style={'color': 'white','font-size': '18px'}),  
                ], style={'background-color': '#03045D', 'padding': '20px', 'border-radius': '10px'}),
                
                dbc.Col([
                    html.H4('Ahorro económico proyectado', className='mb-4', style={'color': 'white'}),
                    html.H5('Al día:', className='mb-2', style={'color': 'white'}),
                    html.P(f'${format_number(ahorro_dia)}', style={'color': 'white','font-size': '18px'}),
                    html.H5('A la semana:', className='mb-2', style={'color': 'white'}),
                    html.P(f'${format_number(ahorro_semana)}', style={'color': 'white','font-size': '18px'}),
                    html.H5('Al año:', className='mb-2', style={'color': 'white'}),
                    html.P(f'${format_number(ahorro_anio)}', style={'color': 'white','font-size': '18px'}),
                ], style={'background-color': '#036566', 'padding': '20px', 'border-radius': '10px', 'margin-left': '20px'}),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4('Reducción del estrés hídrico', className='mb-4', style={'color': 'white'}),
                    html.P(f'Porcentaje de agua reutilizada en relación al consumo total: {reduccion_estres_hidrico:.2f} %', style={'color': 'white','font-size': '18px'}),
                ], style={'background-color': '#034D94', 'padding': '20px', 'border-radius': '10px', 'margin-top': '20px'}),
                
                dbc.Col([
                    html.H4('Potencial de riego de áreas verdes', className='mb-4', style={'color': 'white'}),
                    html.P(f'-Pasto: {potencial_riego_pasto:.2f} m²', style={'color': 'white','font-size': '18px'}),
                    html.P(f'-Especies nativas (ej: Quillay): {potencial_riego_especies:.2f} m²', style={'color': 'white','font-size': '18px'}),
                ], style={'background-color': '#2D897C', 'padding': '20px', 'border-radius': '10px', 'margin-top': '20px', 'margin-left': '20px'}),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4('Reducción huella de carbono anual', className='mb-4', style={'color': 'white'}),
                    html.P(f'-Reducción asociada al tratamiento de aguas residuales: {reduccion_huella_aguaresidual:.2f} kg CO₂ eq', style={'color': 'white','font-size': '18px'}),
                    html.P(f'-Reducción asociada a la producción de agua potable: {reduccion_huella_aguapotable:.2f} kg CO₂ eq', style={'color': 'white','font-size': '18px'}),
                    html.P(f'Reducción total huella de carbono: {reduccion_huella_total:.2f} kg CO₂ eq', style={'color': 'white','font-size': '20px'}),
                ], style={'background-color': '#5E4B80', 'padding': '20px', 'border-radius': '10px', 'margin-top': '20px'}),
            ]),
        ])
        
        return True, modal_content
    elif triggered_id == 'close-modal' and n_clicks_cerrar > 0:
        return False, None
    return False, None

if __name__ == '__main__':
    app.run_server(debug=True)
