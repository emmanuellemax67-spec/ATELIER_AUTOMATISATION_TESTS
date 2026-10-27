import json
from flask import Flask, render_template, redirect, url_for, request, jsonify

from tester.runner import run_tests
from storage import init_db, save_run, list_runs, get_latest_run

app = Flask(__name__)

# Initialise la base de données
init_db()


@app.get("/")
def consignes():
    return render_template("consignes.html")


@app.get("/dashboard")
def dashboard():
    latest = get_latest_run()
    tests = []

    if latest:
        tests = json.loads(latest["results_json"])

    run = None
    if latest:
        run = {
            "id": latest["id"],
            "timestamp": latest["timestamp"],
            "total": latest["total"],
            "passed": latest["passed"],
            "failed": latest["failed"],
            "errors": latest["errors"],
            "error_rate": latest["error_rate"],
            "latency_avg": latest["latency_avg"],
            "latency_p95": latest["latency_p95"],
        }

    return render_template("dashboard.html", run=run, tests=tests)


@app.post("/run")
def run_api_tests():
    result = run_tests()
    save_run(result)
    return redirect(url_for("dashboard"))


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/history")
def history():
    runs = list_runs(limit=20)
    return jsonify(runs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
