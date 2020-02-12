

from flask import Flask, render_template, url_for, request, jsonify, Markup
from spacy import displacy
import re
import pandas as pd
import spacy
import json
from spacy import displacy
from flask_cors import CORS, cross_origin
from flaskext.markdown import Markdown


nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)
cors = CORS(app)
# Markdown(app)



def style_df(df):
    # Set CSS properties for th elements in dataframe
    th_props = [
        ('font-size', '11px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#6d6d6d'),
        ('background-color', '#f7f7f9')
    ]
    # Set CSS properties for td elements in dataframe
    td_props = [
        ('font-size', '11px')
    ]
    # Set table styles
    styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
    ]
    (df.style
     .set_table_styles(styles))
    return df

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
        df1 = style_df(df1)
        # print(df1)
        # print(UI_results)
        return render_template("new_htm.html", UI_results=Markup(UI_results), table_result=Markup(df1.to_html(classes='data'
                                                                                                       ,header="true")))


if __name__ == '__main__':
    app.run(debug=True)


# Result:
# Keren, the UI is now operational. I hope that during the next 3 days  Roy  will get to the US  the extra dictionaries will be added. 5 KG of stones and 2 Ton  of feathers.
# 30 cubic meter of water.