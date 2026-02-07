import json
import os
from flask import Flask, render_template, abort

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_dysfunctions():
    with open(os.path.join(DATA_DIR, "dysfunctions.json"), "r") as f:
        return json.load(f)

CATEGORY_LABELS = {
    "head_neck": "Head & Neck",
    "shoulders_upper_back": "Shoulders & Upper Back",
    "lower_back_pelvis": "Lower Back & Pelvis",
    "knees_lower_body": "Knees & Lower Body",
}

CATEGORY_ORDER = ["head_neck", "shoulders_upper_back", "lower_back_pelvis", "knees_lower_body"]


@app.route("/")
def home():
    dysfunctions = load_dysfunctions()
    grouped = {}
    for d in dysfunctions:
        cat = d["category"]
        grouped.setdefault(cat, []).append(d)
    return render_template(
        "home.html",
        grouped=grouped,
        category_labels=CATEGORY_LABELS,
        category_order=CATEGORY_ORDER,
    )


@app.route("/dysfunction/<dysfunction_id>")
def dysfunction_detail(dysfunction_id):
    dysfunctions = load_dysfunctions()
    lookup = {d["id"]: d for d in dysfunctions}
    d = lookup.get(dysfunction_id)
    if d is None:
        abort(404)

    connected = [lookup[cid] for cid in d.get("connected_dysfunctions", []) if cid in lookup]
    caused_by = [lookup[cid] for cid in d.get("caused_by_dysfunctions", []) if cid in lookup]

    return render_template(
        "dysfunction.html",
        d=d,
        connected=connected,
        caused_by=caused_by,
        category_labels=CATEGORY_LABELS,
    )


if __name__ == "__main__":
    app.run(debug=True)
