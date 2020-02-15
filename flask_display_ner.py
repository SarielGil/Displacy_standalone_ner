

from flask import Flask, render_template, request, Markup
from spacy import displacy
import pandas as pd
import spacy
from flask_cors import CORS


nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)
cors = CORS(app)


app = Flask(__name__)

def displacy_service(doc):
    # doc = nlp(text)
    return spacy.displacy.render(doc, style="ent", page=False)

@app.route('/')
def index():
    return render_template("new_htm.html")


@app.route('/process', methods=["POST"])
def process():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        doc = nlp(rawtext)
        UI_results = displacy_service(doc)
        d=[]
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
            df = pd.DataFrame(d, columns=('named entity', 'output'))
        df1 = df.pivot(columns='named entity', values='output').fillna('')
        return render_template("new_htm.html", UI_results=Markup(UI_results), table_result=Markup(df1.to_html(classes='data'
                                                                                                       ,header="true")))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# Result:
# Keren, the UI is now operational. I hope that during the next 3 days  Roy  will get to the US  the extra dictionaries will be added. 5 KG of stones and 2 Ton  of feathers.
# 30 cubic meter of water.