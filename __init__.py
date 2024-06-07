from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

import requests
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
                                                                                                                                       
app = Flask(__name__)                                                                                                                  

GITHUB_API_URL = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        #minutes = date_object.minute
        return date_object.minute

@app.route('/commits/')
def NbCommits():
    # Requête pour obtenir les commits depuis l'API GitHub
    response = requests.get(GITHUB_API_URL)
    commits_data = response.json()
    
    # Extraction des minutes de chaque commit
    commit_minutes = [extract_minutes(commit['commit']['author']['date']) for commit in commits_data]
    
    # Comptage des commits par minute
    minutes_count = [commit_minutes.count(i) for i in range(60)]
    
    # Création du graphique
    plt.figure(figsize=(10, 5))
    plt.bar(range(60), minutes_count, color='skyblue')
    plt.xlabel('Minutes')
    plt.ylabel('Nombre de Commits')
    plt.title('Nombre de Commits par Minute')
    plt.xticks(range(0, 60, 5))
    
    # Sauvegarde du graphique dans un objet BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encodage de l'image en base64 pour l'afficher sur la page HTML
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # Rendu du template avec le graphique
    return render_template('commits.html', plot_url=plot_url)





@app.route("/contact/")
def MaPremiereAPI():
    return render_template("formulaire.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("graphique2.html")


#@app.route("/contact/")
#def MaPremiereAPI():
    #return "<h2>Ma page de contact</h2>"

@app.route('/')
def hello_world():
    return render_template('hello.html')
  
if __name__ == "__main__":
  app.run(debug=True)
