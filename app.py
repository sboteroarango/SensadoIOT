import flask
from crate import client
from flask import send_file
import matplotlib.pyplot as plt
import io
import pandas as pd
import requests
from datetime import datetime, timedelta
import os
app = flask.Flask(__name__)
connection_string = 'http://3.226.223.131:4200/'
urlImage = 'https://www.viverotierranegra.com/wp-content/uploads/2020/03/Mesa-de-trabajo-1-copia-4.jpg'
connection = client.connect(connection_string,timeout = 60)
cursor = connection.cursor()
def organizarData(tiempos,valores):
  fechaMayor = max(tiempos)
  limit_datetime = fechaMayor - timedelta(hours=5)
  indexInicio = 0
  for i in range(len(tiempos)):
    if tiempos[i] > limit_datetime:
      indexInicio = i
      break
  tiempos = tiempos[indexInicio:]
  valores = valores[indexInicio:]
  tiempos = list(map(lambda i: (i-tiempos[0]).total_seconds()/60,tiempos))
  return tiempos,valores

def indicarRiesgo():
    cursor.execute("SELECT * FROM etsensortemperatura ORDER BY time_index DESC LIMIT 1")
    result = cursor.fetchone()
    temperatura = result[-1]
    cursor.execute("SELECT * FROM etsensorhumedad ORDER BY time_index DESC LIMIT 1")
    result = cursor.fetchone()
    humedad = result[-1]
    #Las plantas a temperaturas superiores de 28 grados centígrados deben tener humedades del 50% al 70%, más humedad las pone en riesgo 
    #Las plantas a temperaturas por debajo de 10 grados centígrados deben tener humedades entre el 10% al 50%, más humedad las pone en riesgo de quemadura por frío
    temperatura = float(temperatura)
    humedad = float(humedad)
    try:
        if temperatura > 28:
            if humedad < 50:
                return 'Riesgo de deshidratación'
            elif humedad > 70:
                return 'Riesgo de Hongos'
            else:
                return 'Condiciones normales'
        elif temperatura < 10:
            if humedad < 10:
                return 'Riesgo de destrucción de tejidos celulares'
            elif humedad > 50:
                return 'Riesgo de quemadura por frío'
            else:
                return 'Condiciones normales'
        else:
            return 'Condiciones normales'
    except:
        return 'Error en la lectura de datos'
@app.route('/mostrar_temperatura')
def temperatura():
    cursor.execute("select * from (select* from etsensortemperatura order by time_index desc limit 500) subquery order by time_index asc")
    results = cursor.fetchall()
    tiempo = []
    valor = []
    for row in results:
        tiempo.append(row[2])
        valor.append(row[-1])
    tiempo = pd.to_datetime(tiempo,unit='ms')
    tiempo,valor = organizarData(tiempo,valor)
    plt.figure(figsize=(10, 6))
    plt.ylim(0, 50)
    plt.plot(tiempo,valor)
    plt.plot(tiempo,[10]*len(tiempo),color = 'red')
    plt.plot(tiempo,[35]*len(tiempo),color = 'red')
    plt.xlabel('Tiempo(min)')
    plt.ylabel('Temperatura(°C)')
    plt.title('Temperatura vs Tiempo')
    filename = "temperatura.png"
    filepath = os.path.join('/home/ubuntu/graphs', filename)
    plt.savefig(filepath, format='png')
    plt.close()
    return send_file(filepath, mimetype='image/png')

@app.route('/mostrar_humedad')
def humedad():
    cursor.execute("select * from (select* from etsensorhumedad order by time_index desc limit 500) subquery order by time_index asc")
    results = cursor.fetchall()
    tiempo = []
    valor = []
    for row in results:
        tiempo.append(row[2])
        valor.append(row[-1])
    tiempo = pd.to_datetime(tiempo,unit='ms')
    tiempo,valor = organizarData(tiempo,valor)
    plt.figure(figsize=(10, 6))
    plt.ylim(0, 100)
    plt.plot(tiempo,valor)
    plt.plot(tiempo,[35]*len(tiempo),color = 'red')
    plt.xlabel('Tiempo(min)')
    plt.ylabel('Humedad(%)')
    plt.title('Humedad vs Tiempo')
    filename = "humedad.png"
    filepath = os.path.join('/home/ubuntu/graphs', filename)
    plt.savefig(filepath, format='png')
    plt.close()
    return send_file(filepath, mimetype='image/png')


@app.route('/mostrar_luz')
def luz():
    cursor.execute("select * from (select* from etsensorluz order by time_index desc limit 500) subquery order by time_index asc")
    results = cursor.fetchall()
    
    tiempo = []
    valor = []
    for row in results:
        tiempo.append(row[2])
        valor.append(row[-1])
    tiempo = pd.to_datetime(tiempo,unit='ms')
    tiempo,valor = organizarData(tiempo,valor)
    plt.figure(figsize=(10, 6))
    plt.ylim(0, 4000)
    plt.plot(tiempo,valor)
    plt.plot(tiempo,[200]*len(tiempo),color = 'red')
    plt.xlabel('Tiempo(min)')
    plt.ylabel('Luz(lux)')
    plt.title('Luz vs Tiempo')
    filename = "luz.png"
    filepath = os.path.join('/home/ubuntu/graphs', filename)
    plt.savefig(filepath, format='png')
    plt.close()
    return send_file(filepath, mimetype='image/png')

@app.route('/mostrar_description')
def description():
    title = "Planta Pescadito"
    description = """La planta pescadito, también conocida como Nematanthus, es una planta de interior muy popular debido a su atractivo follaje verde y sus flores en forma de tubo que pueden ser de color naranja, amarillo o rojo. Su nombre se debe a la forma de las flores, que se asemejan a pequeños peces. Es una planta de fácil cuidado y se adapta bien a diferentes condiciones de luz y humedad, lo que la hace ideal para cualquier hogar u oficina."""
    


    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f4f4f9;
        }}
        .container {{
            max-width: 800px;
            padding: 20px;
            margin: 20px;
            background: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            text-align: center;
        }}
        h1 {{
            color: #333;
        }}
        p {{
            color: #666;
            line-height: 1.6;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
    </style>
    
</head>
<body>
<h1>{title}</h1>
<p>{description}</p>
<img src="{urlImage}" alt="Imagen">
</body>
</html>
"""
    return html_content

@app.route('/dashboard')
def dashboard():
    riesgo = indicarRiesgo()
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .container {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                max-width: 1200px;
                width: 100%;
            }
            .chart {
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin: 20px;
                padding: 20px;
                width: calc(50% - 40px);
                text-align: center;
            }
            .chart img {
                max-width: 100%;
                border-radius: 4px;
            }
            @media (max-width: 768px) {
                .chart {
                    width: calc(50% - 40px);
                }
            }
            @media (max-width: 480px) {
                .chart {
                    width: 100%;
                }
            }
        </style>
    </head>
    <body>'''+f'''
        <h1>Control de condiciones de planta</h1>
        <p>El modelo indica: {riesgo}</p>
        <div class="container">
            <div id="chart-temperature" class="chart">
                <img src="http://3.226.223.131/mostrar_temperatura" alt="Temperature Chart">
            </div>
            <div id="chart-humidity" class="chart">
                <img src="http://3.226.223.131/mostrar_humedad" alt="Humidity Chart">
            </div>
            <div id="chart-light" class="chart">
                <img src="http://3.226.223.131/mostrar_luz"alt="Light Chart">
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/transformation')
def transformation():
    cantidadImages = 0
    contador = 1
    url = 'https://github.com/sboteroarango/SensadoIOT/blob/main/images/'
    listaImagenes = []
    while True:
        response = requests.get(url+str(contador)+'.jpg?raw=true')
        cantidadImages+=1
        contador+=1
        if response.status_code != 200:
            break
        else:
            listaImagenes.append(url+str(contador-1)+'.jpg?raw=true')
    title = "Transformación de planta"
    agregarHtml = ''
    contador = 1
    for x in listaImagenes:
        description = f'Dia : {contador}'
        agregarHtml += f"""<p>{description}</p><img src="{x}" alt="Imagen">"""
        contador+=1

    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f4f4f9;
        }}
        .container {{
            max-width: 800px;
            padding: 20px;
            margin: 20px;
            background: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            text-align: center;
        }}
        h1 {{
            color: #333;
        }}
        p {{
            color: #666;
            line-height: 1.6;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
    </style>
    
</head>
<body>
<h1>{title}</h1>
{agregarHtml}
</body>
</html>
"""
    return html_content
            
    
    
    

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0',port=80)