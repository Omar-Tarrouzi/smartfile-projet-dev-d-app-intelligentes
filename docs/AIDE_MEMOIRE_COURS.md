# Aide-mémoire du cours : syntaxes essentielles

## 01 - Repères et démarrage

# L’essentiel du développement web Python
Fiche de révision - SmartFiles / 5IAD G1 - 16 novembre 2026.
Synthèse liée aux projets disponibles, pas un remplacement du support officiel du cours.

## Choisir le bon outil
- Streamlit : dashboard de données écrit en Python ; le script est généralement réexécuté après une interaction.
- Gradio : interface de démonstration pour une fonction ou un modèle ; relie des composants à des événements.
- Flask : serveur web léger ; on définit les routes, les réponses et les templates.
- Django : framework plus complet avec ORM, migrations et administration ; utilisé par GameScope.
- API REST : échange client/serveur par HTTP, souvent avec des données JSON.

## Installer les exemples sans modifier SmartFiles
Dans un dossier de révision séparé, avec uv déjà installé :
```powershell
mkdir revision-web
cd revision-web
uv init
uv add streamlit gradio flask requests pandas
```
Ne pas nommer ses fichiers streamlit.py, gradio.py ou flask.py : ils masqueraient les bibliothèques.

## Trois fichiers, trois lancements
```powershell
uv run streamlit run dashboard.py
uv run python demo_gradio.py
uv run flask --app mini_api run
```
Ports locaux habituels : Streamlit 8501, Gradio 7860, Flask 5000. Ils peuvent changer si occupés.
Arrêt du serveur : Ctrl+C dans son terminal.

## Le lien avec les projets
GameScope : données / modèle ML -> API Django -> interface Streamlit.
SmartFiles : navigateur HTML/JS -> routes Flask -> validation -> scanner local -> rapport JSON.
Streamlit et Gradio sont présentés ici pour réviser ; ils ne sont pas installés dans SmartFiles.

À retenir : interface = interaction ; API = contrat HTTP ; service métier = traitement ; stockage = données.


---

## 02 - Streamlit : afficher et saisir

# Un dashboard en quelques lignes
Fichier dashboard.py. Chaque widget retourne sa valeur Python ; st.write affiche un résultat.
```python
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Révision", layout="wide")
st.title("Tableau de bord")
nom = st.text_input("Nom", value="Omar")
seuil = st.slider("Seuil", 0, 100, 50)
mode = st.selectbox("Vue", ["Résumé", "Détail"])
actif = st.checkbox("Afficher les données", value=True)

gauche, droite = st.columns(2)
gauche.metric("Seuil choisi", seuil)
droite.write(f"Bonjour {nom}")

if actif:
    df = pd.DataFrame({"jour": [1, 2, 3],
                       "valeur": [12, 18, 15]})
    st.dataframe(df)
    st.line_chart(df.set_index("jour"))

with st.sidebar:
    st.info("Paramètres de la démonstration")
```

## Formulaire : envoyer plusieurs valeurs ensemble
Ajouter à dashboard.py :
```python
with st.form("formulaire"):
    email = st.text_input("Email")
    age = st.number_input("Âge", min_value=0, step=1)
    envoyer = st.form_submit_button("Valider")

if envoyer:
    st.success(f"Reçu : {email}, {age} ans")
```
Hors formulaire, un changement de widget provoque habituellement une réexécution.
Dans un formulaire, les valeurs sont transmises ensemble à la soumission.
Un bouton est vrai lors de la réexécution liée au clic ; ce n’est pas un stockage durable.

Autres syntaxes utiles : st.markdown("**gras**"), st.warning("Attention"), st.error("Erreur"), st.spinner("Patientez").
Source : https://docs.streamlit.io/develop/concepts/architecture/forms


---

## 03 - Streamlit : état, cache et API

# Conserver un état entre deux interactions
Une variable locale ordinaire est recréée à chaque réexécution. Session State conserve une valeur pour la session.
```python
import streamlit as st

if "compteur" not in st.session_state:
    st.session_state.compteur = 0

if st.button("Ajouter 1"):
    st.session_state.compteur += 1

st.write("Compteur :", st.session_state.compteur)
```
Un rechargement complet peut réinitialiser la session. Pour conserver des données après fermeture, utiliser un stockage persistant.

## Cache : éviter un traitement répété
```python
import pandas as pd

@st.cache_data(ttl=60)
def charger_csv(chemin):
    return pd.read_csv(chemin)

# df = charger_csv("donnees.csv")  # fichier à fournir
```
st.cache_data mémorise des données calculées. st.cache_resource sert plutôt aux ressources comme un modèle ML chargé ; les ressources partagées doivent supporter les accès concurrents.
Ne pas mettre un jeton personnel dans un cache global. Le cache n’est ni une base de données ni une autorisation d’accès.

## Appeler une API depuis Streamlit
Fragment à ajouter à un script Streamlit ; suppose une API locale en cours d’exécution :
```python
import requests

if st.button("Tester l'API"):
    try:
        r = requests.get("http://127.0.0.1:5000/health",
                         timeout=10)
        r.raise_for_status()
        st.json(r.json())
    except (requests.RequestException, ValueError) as exc:
        st.error(f"API indisponible ou réponse invalide : {exc}")
```
Toujours prévoir timeout, erreurs HTTP et réponse non JSON. requests.post(url, json={...}) envoie un objet JSON.
Sources : https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
https://docs.streamlit.io/get-started/fundamentals/advanced-concepts


---

## 04 - Gradio : fonctions et événements

# Interface : une fonction devient une démo
Fichier demo_gradio.py. Les composants fournissent les arguments ; la valeur retournée alimente la sortie.
```python
import gradio as gr

def saluer(nom):
    return f"Bonjour {nom or 'visiteur'} !"

demo = gr.Interface(
    fn=saluer,
    inputs=gr.Textbox(label="Nom"),
    outputs=gr.Textbox(label="Réponse"),
    title="Ma première démo",
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False)
```

## Blocks : disposer les composants et relier les actions
Autre version de demo_gradio.py, à utiliser à la place de la précédente :
```python
import gradio as gr

def calculer(prix, quantite):
    total = prix * quantite
    return total, f"Total : {total:.2f} EUR"

with gr.Blocks() as demo:
    gr.Markdown("## Calcul du total")
    with gr.Row():
        prix = gr.Number(label="Prix", value=10)
        quantite = gr.Slider(1, 20, value=2, step=1,
                             label="Quantité")
    bouton = gr.Button("Calculer")
    total = gr.Number(label="Montant")
    message = gr.Textbox(label="Résumé")
    bouton.click(fn=calculer, inputs=[prix, quantite],
                 outputs=[total, message])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False)
```
inputs suit l’ordre des paramètres ; outputs suit l’ordre des valeurs retournées.
.click réagit au clic ; .change à une modification du composant ; .submit à une soumission compatible.
gr.State permet de transporter un état de session entre événements. Éviter les variables globales pour les données personnelles.
share=True crée un lien de partage : le laisser désactivé pour une démo privée locale.
Sources : https://www.gradio.app/guides/quickstart
https://www.gradio.app/main/docs/gradio/blocks


---

## 05 - Flask, JSON et commandes de projet

# Flask : définir une API minimale
Fichier mini_api.py. GET lit ; POST soumet un traitement. Valider les entrées côté serveur.
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.post("/double")
def doubler():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Objet JSON requis"), 400
    n = data.get("n")
    if type(n) not in (int, float):
        return jsonify(error="Nombre requis"), 400
    return jsonify(resultat=n * 2)
```
JSON : objet = {...}, liste = [...], booléens = true/false, absence = null ; clés entre guillemets doubles.
HTTP : 200 succès ; 201 création ; 400 entrée invalide ; 401 authentification requise ; 403 accès refusé ; 404 absent ; 500 erreur serveur.
Source : https://flask.palletsprojects.com/en/stable/quickstart/

## Commandes à connaître
```powershell
# Dans SmartFiles : installer et lancer
uv sync --frozen
uv run python app.py
uv run pytest -q
uv run ruff check .

# Relire puis créer un commit (après revue des fichiers)
git status
git diff
git add docs
git diff --cached
git commit -m "docs: add course syntax memo"

# Docker Desktop doit être démarré
docker compose config --quiet
docker compose up --build -d
docker compose logs -f
docker compose down
```
uv add ajoute une dépendance ; uv.lock fixe les versions résolues. Docker image = recette construite ; conteneur = instance exécutée ; volume = stockage ; port = point d’accès réseau.
Sources : https://docs.astral.sh/uv/guides/projects/
https://docs.docker.com/compose/gettingstarted/
Dans SmartFiles : ne jamais committer .env ; ne pas exposer les dossiers personnels ; une proposition IA doit passer par une validation avant toute modification de fichier.


---
