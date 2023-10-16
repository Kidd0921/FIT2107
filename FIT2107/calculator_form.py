from os import pipe
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Optional
from datetime import datetime

# validation for form inputs
class Calculator_Form(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    BatteryPackCapacity = StringField("Battery Pack Capacity", [DataRequired()])
    InitialCharge = StringField("Initial Charge", [DataRequired()])
    FinalCharge = StringField("Final Charge", [DataRequired()])
    StartDate = DateField("Start Date", [DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y')
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you
    def validate_BatteryPackCapacity(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValidationError("cannot fetch data")
        else:
            try:
                capacity = float(field.data)
                if capacity < 0:
                    raise ValidationError("Battery Capacity cannot be less than 0")
            except:
                raise ValidationError("Battery Capacity must be a number")

    # validate initial charge here
    def validate_InitialCharge(self, field):
        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValidationError("cannot fetch data")
        else:
            try:
                initCharge = int(field.data)
                if initCharge < 0:
                   raise ValidationError("Initial Charge cannot be less than 0")
                elif initCharge > 99:
                    raise ValidationError("Initial Charge cannot be 100%")
            except:
                raise ValidationError("Initial Charge must be an integer between 0 and 99")

    # validate final charge here
    def validate_FinalCharge(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValidationError("cannot fetch data")
        else:
            try:
                initCharge = int(self.InitialCharge.data)
                finalCharge = int(field.data)
                if finalCharge < 1:
                   raise ValidationError("Final Charge cannot be less than 1")
                elif finalCharge > 100:
                    raise ValidationError("Final Charge cannot be more than 100%")
                elif finalCharge < initCharge:
                    raise ValidationError("Final charge cannot be less than initial charge")
            except:
                raise ValidationError("Initial Charge must be an integer between 1 and 100")

    # validate start date here
    def validate_StartDate(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.id != "StartDate":
            if field.data == '':
                raise ValidationError("cannot fetch data")
            try:
                datetime.strptime(field.data, "%d/%m/%Y").strftime('%d/%m/%Y')
            except ValueError:
                raise ValidationError("Date entered is not valid")


    # validate start time here
    def validate_StartTime(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.id != "StartTime":
            if field.data == '':
                raise ValidationError("cannot fetch data")
            try:
                datetime.strptime(field.data, "%H:%M").strftime('%H:%M')
            except ValueError:
                raise ValidationError("Date entered is not valid")

    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
    
        configuration_list = [1,2,3,4,5,6,7,8]

        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValidationError("cannot fetch data")
        else:
            try:
                config = int(field.data)
                if config not in configuration_list:
                    raise ValidationError("Charger configuration must be an integer between 1 and 8 inclusive")
            except:
                raise ValidationError("Charger configuration must be an integer")


    # validate postcode here
    def validate_PostCode(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValidationError("cannot fetch data")
        try:
            postcode = int(field.data)
            if len(str(postcode)) != 4:
                raise ValidationError("Wrong format of postcode (must be 4 digit)")
        except:
            raise ValidationError("postcode has to be an integer")

