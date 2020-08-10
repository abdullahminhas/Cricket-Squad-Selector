from test.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PlayerForm, SquadForm, Upload, AddBatsman, 
                        AddBowler, RequestResetForm, ResetPasswordForm)
from test.teamselection.australia.australiabatsman import returnAustraliaBatsman
from test.teamselection.australia.australiabowlers import returnAustraliaBowlers
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, abort
from test.teamselection.england.englandbowlers import returnEnglandBowlers
from test.teamselection.england.englandbatsman import returnEnglandBatsman
from test.teamselection.india.indiabowlers import returnIndiaBowlers
from test.teamselection.india.indiabatsman import returnIndiaBatsman
from test.teamselection.wicketkeeper import return_wicketkeeper
from test.teamselection.captain import return_captain
from test import app, db, bcrypt, mail
from test.models import User, Player
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from flask_mail import Message
from PIL import Image
from math import sqrt
import pandas as pd
import numpy as np
import secrets
import os



@app.route("/")
def home():
    return render_template('home.html', title='home')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Success!, Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful for {form.username.data}.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check Username and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, '/Users/mac/Desktop/FYP/CSS/project_env/project_env/test/static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)



@app.route("/squad", methods=['GET', 'POST'])
def squad():
    form = SquadForm()
    if form.validate_on_submit():

        wicketkeeper1, wicketkeeper2 = return_wicketkeeper()
        captain = return_captain()

        if form.country.data == 'En':
            batsmans = returnEnglandBatsman()
            bowlers = returnEnglandBowlers()
            return render_template("squad.html", title='England Squad', form=form, list="list.html",
                                    wicketkeeper1=wicketkeeper1,wicketkeeper2=wicketkeeper2,
                                    captain=captain,batsmans=batsmans,bowlers=bowlers)
        if form.country.data == 'Au':
            batsmans = returnAustraliaBatsman()
            bowlers = returnAustraliaBowlers()
            return render_template("squad.html", title='Australia Squad', form=form, list="list.html",
                                    wicketkeeper1=wicketkeeper1,wicketkeeper2=wicketkeeper2,
                                    captain=captain,batsmans=batsmans,bowlers=bowlers)
        if form.country.data == 'In':
            batsmans = returnIndiaBatsman()
            bowlers = returnIndiaBowlers()
            return render_template("squad.html", title='India Squad', form=form, list="list.html",
                                    wicketkeeper1=wicketkeeper1,wicketkeeper2=wicketkeeper2,
                                    captain=captain,batsmans=batsmans,bowlers=bowlers)

        #print(form.country.data)
        #print(type(form.country.data))

    return render_template('squad.html', title='squad', form=form, list="none.html")


@app.route("/player/new", methods=['GET', 'POST'])
@login_required
def new_player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(player_name=form.player_name.data, 
                        player_style=form.player_style.data,
                        player_mat=form.player_mat.data, player_ave=form.player_ave.data,
                        player_country=form.player_country.data, player_century=form.player_century.data,
                        player_inns=form.player_inns.data, 
                        player_runs=form.player_runs.data,
                        player_hs=form.player_hs.data, player_type=form.player_type.data,
                        player_sr=form.player_sr.data, player_bruns=form.player_bruns.data,
                        player_bave=form.player_bave.data, player_bsr=form.player_bsr.data,
                        player_id=form.player_id.data, player_wkts=form.player_wkts.data)
        db.session.add(player)
        db.session.commit()
        flash('Player added successfully', 'success')
        return redirect(url_for('player'))
    return render_template('create_player.html', title='New Player',  form=form, legend='New Player')


@app.route("/player")
def player():
    playerss = []
    players = Player.query.all()
    for player in players:
        image_file = url_for('static', filename='profile_pics/' + player.player_image)
        player.player_image = image_file
        playerss.append(player)
    return render_template('player.html', title='Players', players=players)


@app.route("/playerinfo/<int:player_id>", methods=['GET', 'POST'])
def playerinfo(player_id):
    players = []
    player = Player.query.get(player_id)
    image_file = url_for('static', filename='profile_pics/' + player.player_image)
    player.player_image = image_file
    players.append(player)
    return render_template('playerinfo.html', title='Player information', players=players)


@app.route("/playerinfo/<int:player_id>/update", methods=['GET', 'POST'])
@login_required
def update(player_id):
    player = Player.query.get_or_404(player_id)
    form = PlayerForm()
    if form.validate_on_submit():
        player.player_name = form.player_name.data
        player.player_country = form.player_country.data
        player.player_ave = form.player_ave.data
        player.player_mat = form.player_mat.data
        player.player_style = form.player_style.data
        player.player_inns = form.player_inns.data
        player.player_runs = form.player_runs.data
        player.player_hs = form.player_hs.data
        player.player_century = form.player_century.data
        player.player_type = form.player_type.data
        player.player_sr = form.player_sr.data
        player.player_bsr = form.player_bsr.data
        player.player_bave = form.player_bave.data
        player.player_bruns = form.player_bave.data
        player.player_wkts = form.player_wkts.data
        db.session.commit()
        flash('Your player has been updated!', 'success')
        return redirect(url_for('player', player_id=player.player_id))
    elif request.method == 'GET':
        form.player_name.data = player.player_name
        form.player_country.data = player.player_country
        form.player_ave.data = player.player_ave
        form.player_mat.data = player.player_mat
        form.player_inns.data = player.player_inns
        form.player_style.data = player.player_style
        form.player_runs.data = player.player_runs
        form.player_hs.data = player.player_hs
        form.player_century.data = player.player_century
        form.player_type.data = player.player_type
        form.player_sr.data = player.player_sr
        form.player_bsr.data = player.player_bsr
        form.player_bave.data = player.player_bave
        form.player_bruns.data = player.player_bruns
        form.player_wkts.data = player.player_wkts
    image_file = url_for('static', filename='profile_pics/' + player.player_image)
    return render_template('create_player.html', title='Update Player',
                           form=form, legend='Update Player')


@app.route("/player/<int:player_id>/delete", methods=['POST'])
@login_required
def delete(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    flash('Your Player has been deleted!', 'success')
    return redirect(url_for('player'))


@app.route("/add/bowler", methods=['POST', 'GET'])
def add_bowler():
    form = AddBowler()
    if request.method == "POST":
        df = pd.read_csv(os.path.join(app.root_path, 'static', 
          form.country.data))
        try:
            df = df.drop(['Unnamed: 0'], axis=1)
        except:
             print("")
        try:
            df.reset_index(drop=True, inplace=True)
        except:
            print("")
        df.loc[-1] = [form.PlayerName.data,
                      form.m1_run.data,
                      form.m1_bowl.data,
                      form.m1_op.data,
                      form.m1_vnu.data,
                      form.m2_run.data,
                      form.m2_bowl.data,
                      form.m2_op.data,
                      form.m2_vnu.data,
                      form.m3_run.data,
                      form.m3_bowl.data,
                      form.m3_op.data,
                      form.m3_vnu.data,
                      form.m4_run.data,
                      form.m4_bowl.data,
                      form.m4_op.data,
                      form.m4_vnu.data,
                      form.m5_run.data,
                      form.m5_bowl.data,
                      form.m5_op.data,
                      form.m5_vnu.data,
                      form.m6_run.data,
                      form.m6_bowl.data,
                      form.m6_op.data,
                      form.m6_vnu.data,
                      form.m7_run.data,
                      form.m7_bowl.data,
                      form.m7_op.data,
                      form.m7_vnu.data,
                      form.m8_run.data,
                      form.m8_bowl.data,
                      form.m8_op.data,
                      form.m8_vnu.data,
                      form.m9_run.data,
                      form.m9_bowl.data,
                      form.m9_op.data,
                      form.m9_vnu.data,
                      form.m10_run.data,
                      form.m10_bowl.data,
                      form.m10_op.data,
                      form.m10_vnu.data,
                      form.t50.data,
                      form.t100.data,
                      form.truns.data,
                      form.tbf.data,
                      form.avgrun.data,
                      form.avgsr.data,
                      form.rf50.data,
                      form.rf100.data,
                      form.wickets.data,
                      form.truns_percentage.data,
                      form.tbf_percentage.data]  # adding a row
        df.index = df.index + 1  # shifting index
        df.sort_index(inplace=True)
        try:
            df.reset_index(drop=True, inplace=True)
        except Exception as e:
            print("")
        df.to_csv(os.path.join(app.root_path, 'static', form.country.data))
        flash("Record added successfully",'success')
        return render_template("add_bowler.html", form=form)
    return render_template("add_bowler.html", title='Update Bowler', form=form)


@app.route("/add/batsman", methods=['POST', 'GET'])
def add_batsman():
    form = AddBatsman()
    if form.validate_on_submit():
        df = pd.read_csv(os.path.join(app.root_path, 'static', form.country.data))
        try:
            df = df.drop(['Unnamed: 0'], axis=1)
        except:
             print("")
        try:
            df.reset_index(drop=True, inplace=True)
        except:
            print("")

        df.loc[-1] = [form.PlayerName.data,
                      form.m1_run.data,
                      form.m1_bowl.data,
                      form.m1_sr.data,
                      form.m1_op.data,
                      form.m1_vnu.data,
                      form.m2_run.data,
                      form.m2_bowl.data,
                      form.m2_sr.data,
                      form.m2_4.data,
                      form.m2_6.data,
                      form.m2_op.data,
                      form.m2_vnu.data,
                      form.m3_run.data,
                      form.m3_bowl.data,
                      form.m3_sr.data,
                      form.m3_4.data,
                      form.m3_6.data,
                      form.m3_op.data,
                      form.m3_vnu.data,
                      form.m4_run.data,
                      form.m4_bowl.data,
                      form.m4_sr.data,
                      form.m4_4.data,
                      form.m4_6.data,
                      form.m4_op.data,
                      form.m4_vnu.data,
                      form.m5_run.data,
                      form.m5_bowl.data,
                      form.m5_sr.data,
                      form.m5_4.data,
                      form.m5_6.data,
                      form.m5_op.data,
                      form.m5_vnu.data,
                      form.m6_run.data,
                      form.m6_bowl.data,
                      form.m6_sr.data,
                      form.m6_4.data,
                      form.m6_6.data,
                      form.m6_op.data,
                      form.m6_vnu.data,
                      form.m7_run.data,
                      form.m7_bowl.data,
                      form.m7_sr.data,
                      form.m7_4.data,
                      form.m7_6.data,
                      form.m7_op.data,
                      form.m7_vnu.data,
                      form.m8_run.data,
                      form.m8_bowl.data,
                      form.m8_sr.data,
                      form.m8_4.data,
                      form.m8_6.data,
                      form.m8_op.data,
                      form.m8_vnu.data,
                      form.m9_run.data,
                      form.m9_bowl.data,
                      form.m9_sr.data,
                      form.m9_4.data,
                      form.m9_6.data,
                      form.m9_op.data,
                      form.m9_vnu.data,
                      form.m10_run.data,
                      form.m10_bowl.data,
                      form.m10_sr.data,
                      form.m10_4.data,
                      form.m10_6.data,
                      form.m10_op.data,
                      form.m10_vnu.data,
                      form.t50.data,
                      form.t100.data,
                      form.t4.data,
                      form.t6.data,
                      form.truns.data,
                      form.tbf.data,
                      form.avgrun.data,
                      form.avgsr.data,
                      form.rf50.data,
                      form.rf100.data,
                      form.drb.data,
                      form.truns_percentage.data,
                      form.tbf_percentage.data]  # adding a row
        df.index = df.index + 1  # shifting index
        df.sort_index(inplace=True)
        try:
            df.reset_index(drop=True, inplace=True)
        except Exception as e:
            print("")
        #df.drop_duplicates(subset='Player Name', keep='last', inplace=True)
        df.to_csv(os.path.join(app.root_path, 'static', form.country.data))
        flash("added record",'success')
        return render_template("add_batsman.html", form=form)
    return render_template("add_batsman.html", title='Update Batsman', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='YourEmailID',
                  recipients=[user.email])
    msg.body = f'''Dear {user.username},
To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made to your account.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/language")
def language():
    flash('Language Support not added yet', 'warning')
    return render_template('Error.html')


@app.route("/help")
def help():
    flash('Help Support not added yet', 'warning')
    return render_template('Error.html')


@app.route("/social")
def social():
    flash('No social media links found!', 'danger')
    return render_template('Error.html')


@app.route("/search")
def search():
    flash('No player found in list!', 'danger')
    return render_template('search.html')
