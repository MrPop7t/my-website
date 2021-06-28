from flask import (
    Flask,
    render_template,
    send_from_directory,
    jsonify,
    redirect,
    request,
    session,
    make_response,
    abort,
)

from flask_frozen import Freezer
from src import constants
import requests
import datetime
import time
import os

config = {
    "TEMPLATES_AUTO_RELOAD": True,  
}

app = Flask(
    __name__, static_url_path="/", static_folder="static", template_folder="templates"
)
app.config.from_mapping(config)

ssr = Freezer(app)

@app.route("/")
def index():
    return render_template(
        "index.html",
        **{
            "discord": get_discord_status(),
            "me": constants.me,
            "social": constants.social_metadata,
            "experiences": constants.experiences,
            "education": constants.education,
            "technologies": constants.technologies,
        },
    )

@app.route("/r/<name>/")
def social_redirect(name):
    if name in constants.social_metadata:
        social_data = constants.social_metadata[name]
        social_data['title'] = str(name).capitalize()

        return render_template(
            "redirect.html", **{"social": constants.social_metadata[name]}
        )

@app.route("/blog/")
def blog_redirect():
    return render_template(
        "redirect.html", **{"social": constants.social_metadata['medium']}
    )

@app.route("/story/")
def latest_story():
    if constants.redirections['story']:
        return render_template(
            "redirect.html", **{
                "social": {
                    "author": "Edwin Louis Cole",
                    "title": "Tag Java - GeekForGeeks, Medium",
                    "desc": "12 Tips to Optimize Java Code Performance",
                    "color": "#c4c4c4",
                    "url": constants.redirections['story']
                }
            }
        )

def get_discord_status():
    r = requests.get(f"https://api.lanyard.rest/v1/users/{constants.discord_id}")
    i = r.json()
    try:
        return {
            "success": True,
            "listening": True if i["data"]["listening_to_spotify"] else False,
            "avatar": f"https://cdn.discordapp.com/avatars/{constants.discord_id}/{i['data']['discord_user']['avatar']}.png",
        }
    except Exception:
        return {"success": False, "listening": False}


@app.context_processor
def checkers():
    def main_metadata(value):
        return constants.main_metadata[value]

    def social_metadata(name, value):
        return constants.social_metadata[name][value]

    return dict(main_metadata=main_metadata, social_metadata=social_metadata)