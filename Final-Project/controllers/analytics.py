from flask import Blueprint, render_template, request, jsonify
from services.analytics_service import (
    get_salary_by_department, get_office_utilization,
    get_status_distribution, get_headcount_by_year,
    get_top_earners
)
from services.employee_service import search_employees
from services.office_service import search_offices
from services.audit_service import get_recent
from database import get_db

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/search')
def global_search():
    q = request.args.get('q', '').strip()
    employees, offices = [], []
    if q:
        employees = search_employees(q)
        offices   = search_offices(q)
    return render_template('search.html', q=q, employees=employees, offices=offices)


@analytics_bp.route('/audit-log')
def audit_log():
    events = get_recent(100)
    return render_template('audit_log.html', events=events)


@analytics_bp.route('/health')
def health():
    try:
        conn = get_db()
        conn.cursor().execute('SELECT 1')
        conn.close()
        return jsonify({'status': 'ok', 'db': 'connected'})
    except Exception as e:
        return jsonify({'status': 'error', 'db': str(e)}), 503


@analytics_bp.route('/api/analytics/salary-by-department')
def api_salary_by_dept():
    return jsonify(get_salary_by_department())


@analytics_bp.route('/api/analytics/office-utilization')
def api_office_util():
    return jsonify(get_office_utilization())


@analytics_bp.route('/api/analytics/status-distribution')
def api_status_dist():
    return jsonify(get_status_distribution())


@analytics_bp.route('/api/analytics/headcount-by-year')
def api_headcount():
    return jsonify(get_headcount_by_year())


@analytics_bp.route('/api/analytics/top-earners')
def api_top_earners():
    limit = int(request.args.get('limit', 5))
    return jsonify(get_top_earners(limit))
