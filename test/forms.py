from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from test.models import User, Player
from wtforms_validators import AlphaSpace, Integer, DisposableEmail, Alpha


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), DisposableEmail()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'{username.data} is already taken please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
             raise ValidationError(f'{email.data} is already taken please choose another one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), DisposableEmail()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'{username.data} is already taken please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'{email.data} is already taken please choose another one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), DisposableEmail()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PlayerForm(FlaskForm):
    player_name = StringField('Player Name', validators=[DataRequired(), AlphaSpace('Only string value allowed')])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    player_style = SelectField('Playing Style', choices=[('N/A', 'N/A'), ('Right Hand Batsman', 'Right Hand Batsman'),
                            ('Left Hand Batsman', 'Left Hand Batsman')], validators=[DataRequired()])
    player_mat = IntegerField('Player Matches')
    player_inns = IntegerField('Player Innings')
    player_runs = IntegerField('Player Runs')
    player_hs = IntegerField('Player High Score')
    player_sr = FloatField('Players Strike Rate')
    player_ave = FloatField('Player Average')
    player_century = IntegerField('Player Century')
    player_country  = SelectField('Player Country', choices=[('N/A', 'N/A'), ('Pakistan', 'Pakistan'),
                             ('Australia', 'Australia'), ('England', 'England'), ('India', 'India')],
                                  validators=[DataRequired()])
    player_type = SelectField('Player Type', choices=[('N/A', 'N/A'), ('All Rounder', 'All Rounder'),
                                                      ('Batsman', 'Batsman'), ('Bowler', 'Bowler')])
    player_bruns = IntegerField('Players bowling runs')
    player_wkts = IntegerField('Wickets taken')
    player_bave = FloatField('Players bowling Average')
    player_bsr = FloatField('Player Bowling Strike Rate')
    submit = SubmitField('Save')


    #def validate_player_id(self, player_id):
     #   player = Player.query.filter_by(player_id=player_id.data).first()
      #  if player:
       #      raise ValidationError(f' {player_id.data} already exist.')



class SquadForm(FlaskForm):
    country = SelectField('Rival Country', choices=[(' ', '-- Select Country --'), ('En', 'England'), ('Au', 'Australia'), ('In', 'India')],
                          validators=[DataRequired()])
    submit = SubmitField('Submit Query')

class Upload(FlaskForm):
    country = SelectField('Rival Country', choices=[(' ', '-- Select Country --'), ('En', 'England'), ('Au', 'Australia'), ('In', 'India')],
                          validators=[DataRequired()])
    position = SelectField('Position', choices=[(' ', '-- Select Category --'), ('BO', 'Bowlers'), ('BA', 'Batsmans')],
                          validators=[DataRequired()])
    file = FileField('File to upload',validators=[DataRequired(), FileAllowed(['csv', 'xslx'])])
    submit = SubmitField('Submit Query')

class AddBowler(FlaskForm):

    PlayerName = StringField('Player Name', validators=[DataRequired(), AlphaSpace()])
    country = SelectField('Country', choices=[('Bowlers Dataset (Australia).csv', 'Australia'), 
        ('Bowlers Dataset (India).csv', 'India'), ('Bowlers Dataset (England).csv', 'England')], 
        validators=[DataRequired()])

    m1_run = IntegerField('M1(Run)', validators=[DataRequired(), Integer()])
    m1_bowl = IntegerField('M1(Bowl)', validators=[DataRequired(), Integer()])
    m1_op = StringField('M1(OP)', validators=[DataRequired(), AlphaSpace()])
    m1_vnu = StringField('M1(VNU)', validators=[DataRequired(), AlphaSpace()])

    m2_run = IntegerField('M2(Run)', validators=[DataRequired(), Integer()])
    m2_bowl = IntegerField('M2(Bowl)', validators=[DataRequired(), Integer()])
    m2_op = StringField('M2(OP)', validators=[DataRequired(), AlphaSpace()])
    m2_vnu = StringField('M2(VNU)', validators=[DataRequired(), AlphaSpace()])

    m3_run = IntegerField('M3(Run)', validators=[DataRequired(), Integer()])
    m3_bowl = IntegerField('M3(Bowl)',validators=[DataRequired(), Integer()])
    m3_op = StringField('M3(OP)', validators=[DataRequired(), AlphaSpace()])
    m3_vnu = StringField('M3(VNU)', validators=[DataRequired(), AlphaSpace()])

    m4_run = IntegerField('M4(Run)', validators=[DataRequired(), Integer()])
    m4_bowl = IntegerField('M4(Bowl)', validators=[DataRequired(), Integer()])
    m4_op = StringField('M4(OP)', validators=[DataRequired(), AlphaSpace()])
    m4_vnu = StringField('M4(VNU)', validators=[DataRequired(), AlphaSpace()])

    m5_run = IntegerField('M5(Run)', validators=[DataRequired(), Integer()])
    m5_bowl = IntegerField('M5(Bowl)', validators=[DataRequired(), Integer()])
    m5_op = StringField('M5(OP)', validators=[DataRequired(), AlphaSpace()])
    m5_vnu = StringField('M5(VNU)', validators=[DataRequired(), AlphaSpace()])

    m6_run = IntegerField('M6(Run)', validators=[DataRequired(), Integer()])
    m6_bowl = IntegerField('M6(Bowl)', validators=[DataRequired(), Integer()])
    m6_op = StringField('M6(OP)', validators=[DataRequired(), AlphaSpace()])
    m6_vnu = StringField('M6(VNU)', validators=[DataRequired(), AlphaSpace()])

    m7_run = IntegerField('M7(Run)', validators=[DataRequired(), Integer()])
    m7_bowl = IntegerField('M7(Bowl)', validators=[DataRequired(), Integer()])
    m7_op = StringField('M7(OP)', validators=[DataRequired(), AlphaSpace()])
    m7_vnu = StringField('M7(VNU)', validators=[DataRequired(), AlphaSpace()])

    m8_run = IntegerField('M8(Run)', validators=[DataRequired(), Integer()])
    m8_bowl = IntegerField('M8(Bowl)', validators=[DataRequired(), Integer()])
    m8_op = StringField('M8(OP)', validators=[DataRequired(), AlphaSpace()])
    m8_vnu = StringField('M8(VNU)', validators=[DataRequired(), AlphaSpace()])

    m9_run = IntegerField('M9(Run)', validators=[DataRequired(), Integer()])
    m9_bowl = IntegerField('M9(Bowl)', validators=[DataRequired(), Integer()])
    m9_op = StringField('M9(OP)', validators=[DataRequired(), AlphaSpace()])
    m9_vnu = StringField('M9(VNU)', validators=[DataRequired(), AlphaSpace()])

    m10_run = IntegerField('M10(Run)', validators=[DataRequired(), Integer()])
    m10_bowl = IntegerField('M10(Bowl)', validators=[DataRequired(), Integer()])
    m10_op = StringField('M10(OP)', validators=[DataRequired(), AlphaSpace()])
    m10_vnu = StringField('M10(VNU)', validators=[DataRequired(), AlphaSpace()])

    t50 = IntegerField('T(50)', validators=[DataRequired(), Integer()])
    t100 = IntegerField('T(100)', validators=[DataRequired(), Integer()])
    truns = IntegerField('TRuns', validators=[DataRequired(), Integer()])
    tbf = IntegerField('TBF', validators=[DataRequired(), Integer()])
    avgrun = FloatField('Agv.Run', validators=[DataRequired()])
    avgsr = FloatField('Agv.SR', validators=[DataRequired()])
    rf50 = FloatField('RF(50)', validators=[DataRequired()])
    rf100 = FloatField('RF(100)', validators=[DataRequired()])
    wickets = IntegerField('Wickets', validators=[DataRequired(), Integer()])
    truns_percentage = FloatField('TRuns(%)', validators=[DataRequired()])
    tbf_percentage = FloatField('TBF(%)', validators=[DataRequired()])

    submit = SubmitField('Submit')


class AddBatsman(FlaskForm):

    PlayerName = StringField('Player Name', validators=[DataRequired(), AlphaSpace()])
    country = SelectField('Country', choices=[('Batsman Dataset (Australia).csv', 'Australia'), ('Batsman Dataset (India).csv', 'India'), ('Batsman Dataset (England).csv', 'England')], validators=[DataRequired()])

    m1_run = IntegerField('M1(Run)', validators=[DataRequired(), Integer()])
    m1_bowl = IntegerField('M1(Bowl)', validators=[DataRequired(), Integer()])
    m1_sr = FloatField('M1(SR)', validators=[DataRequired(), Integer()])
    average = FloatField('Average', validators=[DataRequired(), Integer()])
    m1_6 = IntegerField('M1(6)', validators=[DataRequired(), Integer()])
    m1_op = StringField('M1(OP)', validators=[DataRequired(), AlphaSpace()])
    m1_vnu = StringField('M1(VNU)', validators=[DataRequired(), AlphaSpace()])

    m2_run = IntegerField('M2(Run)', validators=[DataRequired(), Integer()])
    m2_bowl = IntegerField('M2(Bowl)', validators=[DataRequired(), Integer()])
    m2_sr = FloatField('M2(SR)', validators=[DataRequired(), Integer()])
    m2_6 = IntegerField('M2(6)', validators=[DataRequired(), Integer()])
    m2_4= IntegerField('M2(4)', validators=[DataRequired(), Integer()])
    m2_op = StringField('M2(OP)', validators=[DataRequired(), AlphaSpace()])
    m2_vnu = StringField('M2(VNU)', validators=[DataRequired(), AlphaSpace()])

    m3_run = IntegerField('M3(Run)', validators=[DataRequired(), Integer()])
    m3_bowl = IntegerField('M3(Bowl)', validators=[DataRequired(), Integer()])
    m3_sr = FloatField('M3(SR)', validators=[DataRequired(), Integer()])
    m3_6 = IntegerField('M3(6)', validators=[DataRequired(), Integer()])
    m3_4= IntegerField('M3(4)', validators=[DataRequired(), Integer()])
    m3_op = StringField('M3(OP)', validators=[DataRequired(), AlphaSpace()])
    m3_vnu = StringField('M3(VNU)', validators=[DataRequired(), AlphaSpace()])

    m4_run = IntegerField('M4(Run)', validators=[DataRequired(), Integer()])
    m4_bowl = IntegerField('M4(Bowl)', validators=[DataRequired(), Integer()])
    m4_sr = FloatField('M4(SR)', validators=[DataRequired(), Integer()])
    m4_6 = IntegerField('M4(6)', validators=[DataRequired(), Integer()])
    m4_4= IntegerField('M4(4)', validators=[DataRequired(), Integer()])
    m4_op = StringField('M4(OP)', validators=[DataRequired(), AlphaSpace()])
    m4_vnu = StringField('M4(VNU)', validators=[DataRequired(), AlphaSpace()])

    m5_run = IntegerField('M5(Run)', validators=[DataRequired(), Integer()])
    m5_bowl = IntegerField('M5(Bowl)', validators=[DataRequired(), Integer()])
    m5_sr = FloatField('M5(SR)', validators=[DataRequired(), Integer()])
    m5_6 = IntegerField('M5(6)', validators=[DataRequired(), Integer()])
    m5_4= IntegerField('M5(4)', validators=[DataRequired(), Integer()])
    m5_op = StringField('M5(OP)', validators=[DataRequired(), AlphaSpace()])
    m5_vnu = StringField('M5(VNU)', validators=[DataRequired(), AlphaSpace()])

    m6_run = IntegerField('M6(Run)', validators=[DataRequired(), Integer()])
    m6_bowl = IntegerField('M6(Bowl)', validators=[DataRequired(), Integer()])
    m6_sr = FloatField('M6(SR)', validators=[DataRequired(), Integer()])
    m6_6 = IntegerField('M6(6)', validators=[DataRequired(), Integer()])
    m6_4= IntegerField('M6(4)', validators=[DataRequired(), Integer()])
    m6_op = StringField('M6(OP)', validators=[DataRequired(), AlphaSpace()])
    m6_vnu = StringField('M6(VNU)', validators=[DataRequired(), AlphaSpace()])

    m7_run = IntegerField('M7(Run)', validators=[DataRequired(), Integer()])
    m7_bowl = IntegerField('M7(Bowl)', validators=[DataRequired(), Integer()])
    m7_sr = FloatField('M7(SR)', validators=[DataRequired(), Integer()])
    m7_6 = IntegerField('M7(6)', validators=[DataRequired(), Integer()])
    m7_4= IntegerField('M7(4)', validators=[DataRequired(), Integer()])
    m7_op = StringField('M7(OP)', validators=[DataRequired(), AlphaSpace()])
    m7_vnu = StringField('M7(VNU)', validators=[DataRequired(), AlphaSpace()])

    m8_run = IntegerField('M8(Run)', validators=[DataRequired(), Integer()])
    m8_bowl = IntegerField('M8(Bowl)', validators=[DataRequired(), Integer()])
    m8_sr = FloatField('M8(SR)', validators=[DataRequired(), Integer()])
    m8_6 = IntegerField('M8(6)', validators=[DataRequired(), Integer()])
    m8_4= IntegerField('M8(4)', validators=[DataRequired(), Integer()])
    m8_op = StringField('M8(OP)', validators=[DataRequired(), AlphaSpace()])
    m8_vnu = StringField('M8(VNU)', validators=[DataRequired(), AlphaSpace()])

    m9_run = IntegerField('M9(Run)', validators=[DataRequired(), Integer()])
    m9_bowl = IntegerField('M9(Bowl)', validators=[DataRequired(), Integer()])
    m9_sr = FloatField('M9(SR)', validators=[DataRequired(), Integer()])
    m9_6 = IntegerField('M9(6)', validators=[DataRequired(), Integer()])
    m9_4= IntegerField('M9(4)', validators=[DataRequired(), Integer()])
    m9_op = StringField('M9(OP)', validators=[DataRequired(), AlphaSpace()])
    m9_vnu = StringField('M9(VNU)', validators=[DataRequired(), AlphaSpace()])

    m10_run = IntegerField('M10(Run)', validators=[DataRequired(), Integer()])
    m10_bowl = IntegerField('M10(Bowl)', validators=[DataRequired(), Integer()])
    m10_sr = FloatField('M10(SR)', validators=[DataRequired(), Integer()])
    m10_6 = IntegerField('M10(6)', validators=[DataRequired(), Integer()])
    m10_4 = IntegerField('M10(4)', validators=[DataRequired(), Integer()])
    m10_op = StringField('M10(OP)', validators=[DataRequired(), AlphaSpace()])
    m10_vnu = StringField('M10(VNU)', validators=[DataRequired(), AlphaSpace()])

    t50 = IntegerField('T(50)', validators=[DataRequired(), Integer()])
    t100 = IntegerField('T(100)', validators=[DataRequired(), Integer()])
    t4 = IntegerField('T(4)', validators=[DataRequired(), Integer()])
    t6 = IntegerField('T(6)', validators=[DataRequired(), Integer()])
    truns = IntegerField('TRuns', validators=[DataRequired(), Integer()])
    tbf = IntegerField('TBF', validators=[DataRequired(), Integer()])
    avgrun = FloatField('Avg.Run', validators=[DataRequired(), Integer()])
    avgsr = FloatField('Avg.SR', validators=[DataRequired(), Integer()])
    rf50 = FloatField('RF(50)', validators=[DataRequired(), Integer()])
    rf100 = FloatField('RF100', validators=[DataRequired(), Integer()])
    drb = FloatField('DRB', validators=[DataRequired(), Integer()])
    truns_percentage = FloatField('TRuns(%)', validators=[DataRequired(), Integer()])
    tbf_percentage = FloatField('TBF(%)', validators=[DataRequired(), Integer()])

    submit = SubmitField('Submit')
