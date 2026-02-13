from flask import render_template, request, session, redirect, url_for
from database import get_all_notes, create_note, delete_note, get_note_by_id
import markdown
import bleach

tags=["p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "ul", "ol", "li", "pre", "hr", "em", "strong", "code", "a", "img", "br"]
attributes={
    "a": ["href"],
    "img": ["src", "alt"],
    "*": ["class", "title"]
        }
protocols=['http','https'] 
from regestration import app


@app.route("/")
def index():
    return redirect(url_for('login_password'))


@app.route("/home")
def home():
    if 'user_id' not in session:
        return redirect(url_for('login_password'))

    user_id = session['user_id']
    notes = get_all_notes(user_id)

    return render_template("home.html", email=session['email'], notes=notes)


@app.route("/add_note", methods=['POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login_password'))

    user_id = session['user_id']
    markdown_text = request.form.get('markdown')
    
    if markdown_text:
        create_note(user_id, markdown_text)
    return redirect(url_for('home'))


@app.route("/note/<int:note_id>")
def view_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login_password'))

    user_id = session['user_id']
    note = get_note_by_id(note_id, user_id)

    if not note:
        return redirect(url_for('home'))

   
    rendered = markdown.markdown(note['content'])
    clean_html=bleach.clean(rendered, tags=tags, attributes=attributes, protocols=protocols, strip=False)

    return render_template("view_note.html", note=note, rendered=clean_html)


@app.route("/delete_note/<int:note_id>", methods=['POST'])
def delete_note_route(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login_password'))

    user_id = session['user_id']
    delete_note(note_id, user_id)

    return redirect(url_for('home'))