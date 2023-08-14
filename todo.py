from flask import Flask,render_template,request,redirect,url_for
import sqlite3


app = Flask(__name__)

@app.route("/")
def index():
    
    baglanti = sqlite3.connect("todo.db")
    isaretci = baglanti.cursor()
    x=isaretci.execute("""SELECT * FROM todo""")
    todos = x.fetchall()
    baglanti.commit()
    baglanti.close()
    
    return render_template("index.html",todos = todos)

@app.route("/complete/<string:id>",methods=["GET"])#Tek tek giremeyeceğimiz için dinamik id girdik!
def complete_todo(id):
    
    baglanti = sqlite3.connect("todo.db")
    isaretci = baglanti.cursor()
    an = isaretci.execute("""SELECT complete FROM todo WHERE id=%d"""%(int(id)))
    durum = an.fetchone()[0]
    if durum == 0:
        isaretci.execute("""UPDATE todo SET complete=1 WHERE id=%d"""%(int(id)))
    else:
        isaretci.execute("""UPDATE todo SET complete=0 WHERE id=%d"""%(int(id)))
    baglanti.commit()
    baglanti.close()
    
    return redirect(url_for("index"))

@app.route("/delete/<string:id>",methods=["GET"])
def delete_todo(id):
    
    baglanti = sqlite3.connect("todo.db")
    isaretci = baglanti.cursor()
    isaretci.execute("""DELETE FROM todo WHERE id=%d"""%(int(id)))
    baglanti.commit()
    baglanti.close()
    
    return redirect(url_for("index"))

@app.route("/detail/<string:id>")
def detail_todo(id):
    
    baglanti = sqlite3.connect("todo.db")
    isaretci = baglanti.cursor()
    x = isaretci.execute("""SELECT * FROM todo WHERE id=%d"""%(int(id)))
    todo = x.fetchone()
    baglanti.commit()
    baglanti.close()
    
    if not todo:
        return redirect(url_for('index')) # anasayfaya yönlendirme yapar
    
    return render_template("detail.html",todo = todo)

@app.route("/add", methods=["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")
    
    baglanti = sqlite3.connect("todo.db")
    isaretci = baglanti.cursor()
    isaretci.execute("""INSERT INTO todo (id, title, content, complete) VALUES (NULL, '%s', '%s', 0)"""%(title,content))
    baglanti.commit()
    baglanti.close()
    
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
