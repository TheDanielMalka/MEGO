from flask import Flask, render_template
from database import init_db
from controllers.employees import employees_bp
from controllers.offices import offices_bp
from services.employee_service import get_all_employees
from services.office_service import get_all_offices

app = Flask(__name__)
app.secret_key = 'mego-final-project-2026'

app.register_blueprint(employees_bp)
app.register_blueprint(offices_bp)


@app.route('/')
def index():
    employees = get_all_employees()
    offices   = get_all_offices()
    overcrowded = sum(1 for o in offices if o['employee_count'] > o['capacity'])
    available   = sum(1 for o in offices if o['employee_count'] < o['capacity'])
    unassigned  = sum(1 for e in employees if not e['office_id'])
    return render_template(
        'index.html',
        total_employees=len(employees),
        total_offices=len(offices),
        overcrowded=overcrowded,
        available=available,
        unassigned=unassigned,
    )


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
