"""Bunny word server."""

from flask import Flask, request

app = Flask(__name__)


with open("/usr/share/dict/words") as f:
	words = [w.strip().lower() for w in f if w.strip().isalpha()]


@app.route("/")
def api():
	"""Return newline-separated list of words.

	Can pass difficulty in as a GET parameter; this will determine length of words.
	"""

	difficulty = int(request.args.get("difficulty", 1))
	wlen = 2 + 2 * difficulty
	return "\n".join(w for w in words if wlen <= len(w) <= wlen + 2)


if __name__ == "__main__":
	app.run(debug=True)