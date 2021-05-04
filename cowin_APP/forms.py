from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField
from wtforms.validators import DataRequired,Length,InputRequired
from wtforms.validators import NumberRange
import re

class Data_Required(FlaskForm):
    Age = IntegerField('Age', validators=[InputRequired(message="Age Required"),NumberRange(min=1, max=100,message="Age must be between 1 and 100")])
    Pincode = StringField('Pincode', validators=[InputRequired(message="Pincode Required"),Length(min=6,max=6,message="Pincode Must be 6 digits")])
    def validate_pincode(self,Pincode):

        # Regex to check valid pin code
        # of India.
        regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$";

        # Compile the ReGex
        p = re.compile(regex);

        # If the pin code is empty
        # return false
        if (pinCode == ''):
            return False;

        # Pattern class contains matcher() method
        # to find matching between given pin code
        # and regular expression.
        m = re.match(p, pinCode);

        # Return True if the pin code
        # matched the ReGex else False
        if m is None:
            pass
        else:
          raise ValidationError("Enter a Valid Pincode of India")
    submit = SubmitField('Check Seat-Avaiblity')



