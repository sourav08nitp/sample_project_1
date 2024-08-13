from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///influencer_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Admin, Sponsor, Influencer
    niche = db.Column(db.String(100))  # Niche for influencers
    reach = db.Column(db.Integer)  # Reach for influencers
    flagged = db.Column(db.Boolean, default=False)  # Flagged status

    def __repr__(self):
        return f'<User {self.username}>'



class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    visibility = db.Column(db.Boolean)  # Public or Private
    sponsor_id = db.Column(db.Integer, ForeignKey('user.id'))
    sponsor = relationship('User', foreign_keys=[sponsor_id])
    niche = db.Column(db.String(100))  # New field for categorization

    def __repr__(self):
        return f'<Campaign {self.name}>'


class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('campaign.id'))
    influencer_id = db.Column(db.Integer, ForeignKey('user.id'))
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(50))  # Pending, Accepted, Rejected

    campaign = relationship('Campaign', backref=db.backref('ad_requests', lazy=True))
    influencer = relationship('User', foreign_keys=[influencer_id])

    def __repr__(self):
        return f'<AdRequest {self.id}>'

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' in session and session['role'] == 'Admin':
        users_count = User.query.count()
        campaigns_count = Campaign.query.count()
        ad_requests_count = AdRequest.query.count()
        flagged_users_count = User.query.filter_by(flagged=True).count()

        return render_template('admin_dashboard.html', users_count=users_count,
                               campaigns_count=campaigns_count, ad_requests_count=ad_requests_count,
                               flagged_users_count=flagged_users_count)
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin/manage_users')
def manage_users():
    if 'username' in session and session['role'] == 'Admin':
        users = User.query.all()
        return render_template('manage_users.html', users=users)
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin/manage_campaigns')
def manage_campaigns():
    if 'username' in session and session['role'] == 'Admin':
        campaigns = Campaign.query.all()
        return render_template('manage_campaigns.html', campaigns=campaigns)
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin/manage_ad_requests')
def manage_ad_requests():
    if 'username' in session and session['role'] == 'Admin':
        ad_requests = AdRequest.query.all()
        return render_template('manage_ad_requests.html', ad_requests=ad_requests)
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin/analytics')
def admin_analytics():
    if 'username' in session and session['role'] == 'Admin':
        return render_template('analytics.html')
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin/manage_flagged_users')
def manage_flagged_users():
    if 'username' in session and session['role'] == 'Admin':
        flagged_users = User.query.filter_by(flagged=True).all()
        return render_template('manage_flagged_users.html', flagged_users=flagged_users)
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))
    



@app.route('/admin/settings')
def admin_settings():
    if 'username' in session and session['role'] == 'Admin':
        return render_template('settings.html')
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

# Route to edit a user
@app.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if 'username' in session and session['role'] == 'Admin':
        user = User.query.get_or_404(id)
        if request.method == 'POST':
            user.username = request.form['username']
            user.password = request.form['password']
            user.role = request.form['role']
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('manage_users'))
        return render_template('edit_user.html', user=user)
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

# Route to delete a user
@app.route('/admin/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    if 'username' in session and session['role'] == 'Admin':
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('manage_users'))
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))
    
# Edit Campaign route for Admin
@app.route('/admin/edit_campaign/<int:id>', methods=['GET', 'POST'])
def admin_edit_campaign(id):
    if 'username' in session and session['role'] == 'Admin':
        campaign = Campaign.query.get_or_404(id)
        if request.method == 'POST':
            campaign.name = request.form['name']
            campaign.description = request.form['description']
            start_date_str = request.form['start_date']
            end_date_str = request.form['end_date']
            campaign.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            campaign.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            campaign.budget = float(request.form['budget'])
            campaign.visibility = True if request.form.get('visibility') == 'public' else False
            campaign.niche = request.form['niche']
            db.session.commit()
            flash('Campaign updated successfully!', 'success')
            return redirect(url_for('manage_campaigns'))
        return render_template('edit_campaign.html', campaign=campaign)
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

# Delete Campaign route for Admin
@app.route('/admin/delete_campaign/<int:id>', methods=['POST'])
def admin_delete_campaign(id):
    if 'username' in session and session['role'] == 'Admin':
        campaign = Campaign.query.get_or_404(id)
        db.session.delete(campaign)
        db.session.commit()
        flash('Campaign deleted successfully!', 'success')
        return redirect(url_for('manage_campaigns'))
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

# Route to flag & unflag a user
@app.route('/admin/flag_user/<int:id>', methods=['POST'])
def flag_user(id):
    if 'username' in session and session['role'] == 'Admin':
        user = User.query.get_or_404(id)
        user.flagged = True
        db.session.commit()
        flash(f'User {user.username} flagged successfully!', 'warning')
        return redirect(url_for('manage_users'))
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin/unflag_user/<int:id>', methods=['POST'])
def unflag_user(id):
    if 'username' in session and session['role'] == 'Admin':
        user = User.query.get_or_404(id)
        user.flagged = False
        db.session.commit()
        flash(f'User {user.username} unflagged successfully!', 'success')
        return redirect(url_for('manage_users'))
    else:
        flash('Unauthorized access. Please log in as Admin.', 'danger')
        return redirect(url_for('login'))


# Sponsor Routes
@app.route('/sponsor/dashboard')
def sponsor_dashboard():
    if 'username' in session and session['role'] == 'Sponsor':
        sponsor_id = session['user_id']
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
        return render_template('sponsor_dashboard.html', campaigns=campaigns)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/create_campaign', methods=['GET', 'POST'])
def create_campaign():
    if 'username' in session and session['role'] == 'Sponsor':
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            start_date_str = request.form['start_date']
            end_date_str = request.form['end_date']
            budget = float(request.form['budget'])
            visibility = True if request.form.get('visibility') == 'public' else False
            niche = request.form['niche']

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

            sponsor_id = session['user_id']
            campaign = Campaign(name=name, description=description, start_date=start_date,
                                end_date=end_date, budget=budget, visibility=visibility, sponsor_id=sponsor_id, niche=niche)

            db.session.add(campaign)
            db.session.commit()
            flash('Campaign created successfully!', 'success')
            return redirect(url_for('sponsor_dashboard'))

        return render_template('create_campaign.html')
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/edit_campaign/<int:id>', methods=['GET', 'POST'])
def edit_campaign(id):
    if 'username' in session and session['role'] == 'Sponsor':
        campaign = Campaign.query.get_or_404(id)

        if request.method == 'POST':
            campaign.name = request.form['name']
            campaign.description = request.form['description']
            start_date_str = request.form['start_date']
            end_date_str = request.form['end_date']
            campaign.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            campaign.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            campaign.budget = float(request.form['budget'])
            campaign.visibility = True if request.form.get('visibility') == 'public' else False
            campaign.niche = request.form['niche']

            db.session.commit()
            flash('Campaign updated successfully!', 'success')
            return redirect(url_for('sponsor_dashboard'))

        return render_template('edit_campaign.html', campaign=campaign)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/delete_campaign/<int:id>', methods=['POST'])
def delete_campaign(id):
    if 'username' in session and session['role'] == 'Sponsor':
        campaign = Campaign.query.get_or_404(id)
        db.session.delete(campaign)
        db.session.commit()
        flash('Campaign deleted successfully!', 'success')
        return redirect(url_for('sponsor_dashboard'))
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/ad_requests')
def ad_requests():
    if 'username' in session and session['role'] == 'Sponsor':
        sponsor_id = session['user_id']
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
        ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor_id).all()

        return render_template('ad_requests.html', campaigns=campaigns, ad_requests=ad_requests)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))
    
@app.route('/sponsor/create_ad_request/<int:campaign_id>', methods=['GET', 'POST'])
def create_ad_request(campaign_id):
    if 'username' in session and session['role'] == 'Sponsor':
        campaign = Campaign.query.get_or_404(campaign_id)

        if request.method == 'POST':
            influencer_id = request.form['influencer_id']
            messages = request.form['messages']
            requirements = request.form['requirements']
            payment_amount = float(request.form['payment_amount'])
            status = 'Pending'

            ad_request = AdRequest(campaign_id=campaign_id, influencer_id=influencer_id,
                                   messages=messages, requirements=requirements,
                                   payment_amount=payment_amount, status=status)

            db.session.add(ad_request)
            db.session.commit()
            flash('Ad request created successfully!', 'success')
            return redirect(url_for('ad_requests'))

        return render_template('create_ad_request.html', campaign=campaign)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))


@app.route('/sponsor/edit_ad_request/<int:id>', methods=['GET', 'POST'])
def edit_ad_request(id):
    if 'username' in session and session['role'] == 'Sponsor':
        ad_request = AdRequest.query.get_or_404(id)

        if request.method == 'POST':
            ad_request.campaign_id = request.form['campaign_id']
            ad_request.influencer_id = request.form['influencer_id']
            ad_request.messages = request.form['messages']
            ad_request.requirements = request.form['requirements']
            ad_request.payment_amount = float(request.form['payment_amount'])
            ad_request.status = request.form['status']

            db.session.commit()
            flash('Ad request updated successfully!', 'success')
            return redirect(url_for('ad_requests'))

        campaigns = Campaign.query.filter_by(sponsor_id=session['user_id']).all()
        influencers = User.query.filter_by(role='Influencer').all()
        return render_template('edit_ad_request.html', ad_request=ad_request, campaigns=campaigns, influencers=influencers)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/delete_ad_request/<int:id>', methods=['POST'])
def delete_ad_request(id):
    if 'username' in session and session['role'] == 'Sponsor':
        ad_request = AdRequest.query.get_or_404(id)
        db.session.delete(ad_request)
        db.session.commit()
        flash('Ad request deleted successfully!', 'success')
        return redirect(url_for('ad_requests'))
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))


@app.route('/sponsor/search_influencers', methods=['GET', 'POST'])
def search_influencers():
    if 'username' in session and session['role'] == 'Sponsor':
        influencers = []
        if request.method == 'POST':
            username = request.form.get('username')
            niche = request.form.get('niche')
            query = User.query.filter(User.role == 'Influencer')

            if username:
                query = query.filter(User.username.ilike(f'%{username}%'))
            if niche:
                query = query.filter(User.niche.ilike(f'%{niche}%'))

            influencers = query.all()

        return render_template('search_influencers.html', influencers=influencers)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))



@app.route('/influencer/search_campaigns', methods=['GET', 'POST'])
def search_campaigns():
    if 'username' in session and session['role'] == 'Influencer':
        if request.method == 'POST':
            niche = request.form['niche']
            campaigns = Campaign.query.filter(Campaign.visibility == True, 
                                              Campaign.niche.ilike(f'%{niche}%')).all()
            return render_template('search_campaigns.html', campaigns=campaigns)
        return render_template('search_campaigns.html')
    else:
        flash('Unauthorized access. Please log in as Influencer.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/my_campaigns')
def my_campaigns():
    if 'username' in session and session['role'] == 'Sponsor':
        sponsor_id = session['user_id']
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
        return render_template('my_campaigns.html', campaigns=campaigns)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/influencer_collaboration')
def influencer_collaboration():
    if 'username' in session and session['role'] == 'Sponsor':
        sponsor_id = session['user_id']
        ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor_id).all()
        return render_template('influencer_collaboration.html', ad_requests=ad_requests)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/analytics')
def analytics():
    if 'username' in session and session['role'] == 'Sponsor':
        return render_template('analytics.html')
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

@app.route('/sponsor/send_ad_request', methods=['GET', 'POST'])
def send_ad_request():
    if 'username' in session and session['role'] == 'Sponsor':
        campaigns = Campaign.query.filter_by(sponsor_id=session['user_id']).all()
        influencers = User.query.filter_by(role='Influencer').all()
        
        if request.method == 'POST':
            campaign_id = request.form['campaign_id']
            influencer_id = request.form['influencer_id']
            messages = request.form['messages']
            requirements = request.form['requirements']
            payment_amount = float(request.form['payment_amount'])
            status = 'Pending'

            ad_request = AdRequest(
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                messages=messages,
                requirements=requirements,
                payment_amount=payment_amount,
                status=status
            )

            db.session.add(ad_request)
            db.session.commit()
            flash('Ad request sent successfully!', 'success')
            return redirect(url_for('ad_requests'))

        return render_template('send_ad_request.html', campaigns=campaigns, influencers=influencers)
    else:
        flash('Unauthorized access. Please log in as Sponsor.', 'danger')
        return redirect(url_for('login'))

# Influencer Routes
@app.route('/influencer/dashboard')
def influencer_dashboard():
    if 'username' in session and session['role'] == 'Influencer':
        influencer_id = session['user_id']
        ad_requests = AdRequest.query.filter_by(influencer_id=influencer_id).all()
        return render_template('influencer_dashboard.html', ad_requests=ad_requests)
    else:
        flash('Unauthorized access. Please log in as Influencer.', 'danger')
        return redirect(url_for('login'))

@app.route('/influencer/ad_requests')
def influencer_ad_requests():
    if 'username' in session and session['role'] == 'Influencer':
        influencer_id = session['user_id']
        ad_requests = AdRequest.query.filter_by(influencer_id=influencer_id).all()
        return render_template('influencer_ad_requests.html', ad_requests=ad_requests)
    else:
        flash('Unauthorized access. Please log in as Influencer.', 'danger')
        return redirect(url_for('login'))

@app.route('/influencer/respond_ad_request/<int:id>', methods=['GET', 'POST'])
def respond_ad_request(id):
    if 'username' in session and session['role'] == 'Influencer':
        ad_request = AdRequest.query.get_or_404(id)

        if request.method == 'POST':
            ad_request.payment_amount = float(request.form['payment_amount'])
            ad_request.status = request.form['status']

            db.session.commit()
            flash('Ad request responded successfully!', 'success')
            return redirect(url_for('influencer_ad_requests'))

        return render_template('respond_ad_request.html', ad_request=ad_request)
    else:
        flash('Unauthorized access. Please log in as Influencer.', 'danger')
        return redirect(url_for('login'))

@app.route('/influencer/profile_settings', methods=['GET', 'POST'])
def profile_settings():
    if 'username' in session and session['role'] == 'Influencer':
        influencer_id = session['user_id']
        user = User.query.get_or_404(influencer_id)

        if request.method == 'POST':
            user.username = request.form['username']
            user.password = request.form['password']
            user.niche = request.form['niche']
            user.reach = request.form['reach']
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('influencer_dashboard'))

        return render_template('profile_settings.html', user=user)
    else:
        flash('Unauthorized access. Please log in as Influencer.', 'danger')
        return redirect(url_for('login'))

@app.route('/influencer/analytics')
def influencer_analytics():
    if 'username' in session and session['role'] == 'Influencer':
        return render_template('influencer_analytics.html')
    else:
        flash('Unauthorized access. Please log in as Influencer.', 'danger')
        return redirect(url_for('login'))
    
# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            session['role'] = user.role
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html')

        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
