from flask import Flask, render_template, request
import language_tool_python
import spacy
from spacy import displacy

app = Flask(__name__)

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

class GrammarChecker:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US')

    def check_grammar(self, text):
        matches = self.tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)


        # Tokenization using spaCy
        doc = nlp(corrected_text)
        tokens = [token.text for token in doc]

        # Named Entity Recognition using spaCy
        ner_entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Highlight Named Entities in the corrected text
        corrected_text_with_ner = displacy.render(doc, style="ent", page=False)

        return corrected_text, tokens, ner_entities, corrected_text_with_ner

grammar_checker = GrammarChecker()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            input_text = request.form["input_text"]
            corrected_text, tokens, ner_entities, corrected_text_with_ner = grammar_checker.check_grammar(input_text)
            return render_template("index.html", original_text=input_text, corrected_text=corrected_text,
                                   tokens=tokens, ner_entities=ner_entities, corrected_text_with_ner=corrected_text_with_ner)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template("index.html", error_message=error_message)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
