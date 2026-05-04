from flask import Flask, render_template
from database import init_db
from config import SECRET_KEY
from controllers.employees   import employees_bp
from controllers.offices     import offices_bp
from controllers.departments import departments_bp
from controllers.analytics   import analytics_bp
from services.analytics_service import get_dashboard_stats, get_top_earners
from services.audit_service     import get_recent

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(employees_bp)
app.register_blueprint(offices_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(analytics_bp)


@app.route('/')
def index():
    stats = get_dashboard_stats()
    top   = get_top_earners(5)
    recent_activity = get_recent(8)
    return render_template('index.html', stats=stats,
                           top_earners=top, recent_activity=recent_activity)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)