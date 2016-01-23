from flask import Flask, render_template, request
import urllib.request
from bs4 import BeautifulSoup

featured = {
	"All-Craft": "/reader/www.all-craft.de/feed/",
	"Crap-App ~ Blog": "/reader/blog.crap-app.de/feed/",
	"Nitohu": "/reader/www.nitohu.de/feed/"
}

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html", featured = featured)

"""
@app.route("/reader/", methods=["GET", "POST"])
def readerPageDefault():
	if request.method == "POST":
		return render_template("reader.html")
	return render_template("reader.html", default = True)
"""

@app.route("/reader/", methods=["POST", "GET"])
@app.route("/reader/<name>/<typ>/", methods=["POST", "GET"])
def readerPage(name = None, typ = None):
	if name:
		titles = []
		urls = []
		descs = []
		pubDate = []
		url = "http://" + name + "/" + typ
		try:
			content = urllib.request.urlopen(url)
			xml = BeautifulSoup(content, "xml")
			for item in xml.findAll("title")[1:]:
				titles.append(item.text)
			for item in xml.findAll("link")[2:]:
				urls.append(item.text)
			for item in xml.findAll("description")[1:]:
				descs.append(item.text)
			for item in xml.findAll("pubDate"):
				pubDate.append(item.text)
			return render_template("reader.html", name = name, titles = titles, urls = urls, descs = descs, pubDate = pubDate)

		except Exception as e:
			return render_template("reader.html", name = name, error = e)
	return render_template("reader.html")

@app.errorhandler(404)
def page_not_found(error):
	return render_template("notfound.html", featured = featured), 404

if __name__ == "__main__":
	app.run(debug = True)