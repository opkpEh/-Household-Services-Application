import datetime

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Service, ServiceRequest, Professional, User


@main.route('/')
def index():
    services = Service.query.filter_by(is_active=True).all()
    return render_template('index.html', services=services)


@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    pending_professionals = Professional.query.filter_by(is_verified=False).all()
    service_requests = ServiceRequest.query.all()
    return render_template('admin/dashboard.html',
                           pending_professionals=pending_professionals,
                           service_requests=service_requests)


@main.route('/service/create', methods=['GET', 'POST'])
@login_required
def create_service():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        service = Service(
            name=request.form.get('name'),
            base_price=float(request.form.get('base_price')),
            time_required=int(request.form.get('time_required')),
            description=request.form.get('description')
        )
        db.session.add(service)
        db.session.commit()
        flash('Service created successfully')
        return redirect(url_for('main.admin_dashboard'))

    return render_template('admin/create_service.html')


@main.route('/service/requests')
@login_required
def view_requests():
    if current_user.role == 'professional':
        professional = Professional.query.filter_by(user_id=current_user.id).first()
        requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()
    elif current_user.role == 'customer':
        requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    else:  # admin
        requests = ServiceRequest.query.all()
    return render_template('service_requests.html', requests=requests)


@main.route('/service/request/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_request(request_id):
    if current_user.role != 'professional':
        return redirect(url_for('main.index'))

    professional = Professional.query.filter_by(user_id=current_user.id).first()
    request = ServiceRequest.query.get_or_404(request_id)

    if request.status == 'requested':
        request.professional_id = professional.id
        request.status = 'assigned'
        db.session.commit()
        flash('Service request accepted')

    return redirect(url_for('main.view_requests'))


@main.route('/service/request/<int:request_id>/close', methods=['POST'])
@login_required
def close_request(request_id):
    request = ServiceRequest.query.get_or_404(request_id)

    if current_user.id == request.customer_id and request.status == 'assigned':
        request.status = 'closed'
        request.date_of_completion = datetime.utcnow()
        db.session.commit()
        flash('Service request closed')

    return redirect(url_for('main.view_requests'))