from calculator_form import Calculator_Form
from calculator import *
import unittest
import calculator_app
from calculator_form import *

#class used to test calculator_form.py
class TestForm(unittest.TestCase):

    def test_validate_BatteryPackCapacity(self):
        '''
        Testing done for BatteryPack Capacity field. Tests cases are:
        Test 1: when field.data is none
        Test 2: when field.data is ''
        Test 3: when field.data cannot be converted into a float
        Test 4: when field.data is < 0
        Test 5: when field.data is a float > 0
        '''
        calculator_app.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with calculator_app.ev_calculator_app.app_context():

            calc = Calculator_Form()
            test_field = StringField()

            #test 1: when data is none
            test_field.data = None
            with self.assertRaises(ValidationError):
                calc.validate_BatteryPackCapacity(test_field)

            #test 2: when data is ''
            test_field.data = ''
            with self.assertRaises(ValidationError):
                calc.validate_BatteryPackCapacity(test_field)

            #test 3: when data cannot be converted into a float
            test_field.data = "ab"
            with self.assertRaises(ValidationError):
                calc.validate_BatteryPackCapacity(test_field)
        
            #test 4: when data is a float < 0
            test_field.data = "-0.1"
            with self.assertRaises(ValidationError):
                calc.validate_BatteryPackCapacity(test_field)

            #test 5: when data is a float > 0
            test_field.data = "1"
            self.assertEqual(None, calc.validate_BatteryPackCapacity(test_field))
    
    def test_validate_InitialCharge(self):
        '''
        Testing done for InitialCharge field. Tests cases are:
        Test 1: when field.data is none
        Test 2: when field.data is ''
        Test 3: when field.data cannot be converted into an int
        Test 4: when field.data is an int < 0
        Test 5: when field.data is an int > 99
        Test 6: when field.data is an int between 0 and 99
        '''
        calculator_app.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with calculator_app.ev_calculator_app.app_context():

            calc = Calculator_Form()
            test_field = StringField()

            #test 1: when data is none
            test_field.data = None
            with self.assertRaises(ValidationError):
                calc.validate_InitialCharge(test_field)

            #test 2: when data is ''
            test_field.data = ''
            with self.assertRaises(ValidationError):
                calc.validate_InitialCharge(test_field)

            #test 3: when data cannot be converted into an int
            test_field.data = "1.0"
            with self.assertRaises(ValidationError):
                calc.validate_InitialCharge(test_field)
        
            #test 4: when data is an int < 0
            test_field.data = "-1"
            with self.assertRaises(ValidationError):
                calc.validate_InitialCharge(test_field)

            #test 5: when data is an int > 99
            test_field.data = "100"
            with self.assertRaises(ValidationError):
                calc.validate_InitialCharge(test_field)

            #test 6: when data is an int between 0 and 99 inclusive
            test_field.data = "0"
            self.assertEqual(None, calc.validate_InitialCharge(test_field))

    def test_validate_FinalCharge(self):
        '''
        Testing done for FinalCharge field. Test cases are:
        Test 1: when field.data is none
        Test 2: when field.data is ''
        Test 3: when field.data cannot be converted into an int
        Test 4: when field.data is an int < 1
        Test 5: when field.data is an int > 100
        Test 6: when field.data is an int < InitialCharge.data
        Test 7: when field.data is an int that is between 1 and 100 and is larger than initialCharge
        '''
        calculator_app.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with calculator_app.ev_calculator_app.app_context():

            calc = Calculator_Form()
            test_field = StringField()
            calc.InitialCharge.data = "99"

            #test 1: when data is none
            test_field.data = None
            with self.assertRaises(ValidationError):
                calc.validate_FinalCharge(test_field)

            #test 2: when data is ''
            test_field.data = ''
            with self.assertRaises(ValidationError):
                calc.validate_FinalCharge(test_field)

            #test 3: when data cannot be converted into an int
            test_field.data = "1.0"
            with self.assertRaises(ValidationError):
                calc.validate_FinalCharge(test_field)
        
            #test 4: when data is an int < 0
            test_field.data = "0"
            with self.assertRaises(ValidationError):
                calc.validate_FinalCharge(test_field)

            #test 5: when data is an int > 99
            test_field.data = "101"
            with self.assertRaises(ValidationError):
                calc.validate_FinalCharge(test_field)
            
            # #test 6: when data is < InitialCharge.data
            test_field.data = "98"
            with self.assertRaises(ValidationError):
                calc.validate_FinalCharge(test_field)

            #test 7: when data is an int between 1 and 100 inclusive
            calc.InitialCharge.data = 0
            test_field.data = "1"
            self.assertEqual(None, calc.validate_FinalCharge(test_field))


    def test_validate_StartDate(self):
        '''
        Testing done for StartDate field. Test cases are:
        Test 1: when field.data is none
        Test 2: when field.data is ''
        Test 3: when field.data is not formatted correctly
        Test 4: when day is not an int
        Test 5: when month is not an int
        Test 6: when year is not an int
        Test 7: when day, month, year is not int
        Test 8: When the length of date is not correct
        Test 9: when day < 1
        Test 10: when day > max days in month (according to month_is_big)
        Test 11: when month is < 1
        Test 12: when month is > 12
        Test 13: when data is not a date at all
        Test 13: when date entered is valid with correct format
        '''
        calculator_app.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with calculator_app.ev_calculator_app.app_context():

            calc = Calculator_Form()
            date_test_field = DateField()
            string_test_field = StringField()
            date_test_field.id = "StartDate"
            string_test_field.id = "TestString"

            #test 1: when data is none
            date_test_field.data = None
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(date_test_field)

            #test 2: when data is ''
            string_test_field.data = ''
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 3: when data is not formatted correctly
            string_test_field.data = '11-11-2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)
            
            #test 4: when day is not an int
            string_test_field.data = 'aa/11/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 5: when month is not an int
            string_test_field.data = '11/aa/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 6: when year is not an int
            string_test_field.data = '11/11/aaaa'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 7: when day, month, and year is not an int
            string_test_field.data = 'aa/aa/aaaa'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 8: when length of data is not correct
            string_test_field.data = '11/11/11'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 9: when date entered is < 1
            string_test_field.data = '00/11/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 10: when date entered is > max date 
            string_test_field.data = '31/11/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 11: when month entered is < 1
            string_test_field.data = '11/00/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 12: when month entered is > 12
            string_test_field.data = '11/13/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 13: when data entered is not a date
            string_test_field.data = 'abcdefg'
            with self.assertRaises(ValidationError):
                calc.validate_StartDate(string_test_field)

            #test 13: when date entered is valid and is formatted correctly
            string_test_field.data = '11/11/2021'
            self.assertEqual(None, calc.validate_StartDate(string_test_field))


    def test_validate_StartTime(self):
        '''
        Testing done for StartTime field. Test cases are:
        Test 1: when field.data is none
        Test 2: when field.data is ''
        Test 3: when field.data is not formatted correctly
        Test 4: when hour is not an int
        Test 5: when minute is not an int
        Test 6: when hour and minute is not int
        Test 7: when hour < 1
        Test 8: when hour > 24
        Test 9: when minute is < 1
        Test 10: when minute is > 59
        Test 11: when data entered is not the time at all
        Test 11: when date entered is valid with correct format
        '''
        calculator_app.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with calculator_app.ev_calculator_app.app_context():

            calc = Calculator_Form()
            time_test_field = TimeField()
            string_test_field = StringField()
            time_test_field.id = "StartDate"
            string_test_field.id = "TestString"

            #test 1: when data is none
            time_test_field.data = None
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(time_test_field)

            #test 2: when data is ''
            string_test_field.data = ''
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

            #test 3: when data is not formatted correctly
            string_test_field.data = '1111'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)
            
            #test 4: when hour is not an int
            string_test_field.data = 'aa:11'
            with self.assertRaises(ValidationError):
               calc.validate_StartTime(string_test_field)

            #test 5: when time is not an int
            string_test_field.data = '11:aa'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

            #test 6: when hour and minute is not an int
            string_test_field.data = 'aa:aa'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

            #test 7: when hour entered is < 1
            string_test_field.data = '00/11/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

            #test 8: when hour entered is > 24
            string_test_field.data = '31/11/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

            #test 9: when minute entered is < 1
            string_test_field.data = '11/00/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

            #test 10: when minute entered is > 59
            string_test_field.data = '11/13/2021'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

             #test 11: when data entered is not the time
            string_test_field.data = 'hijklmnop'
            with self.assertRaises(ValidationError):
                calc.validate_StartTime(string_test_field)

            #test 11: when date entered is valid and is formatted correctly
            string_test_field.data = '11:11'
            self.assertEqual(None, calc.validate_StartTime(string_test_field))

    def test_validate_ChargerConfiguration(self):
        '''
        Testing done for Charger Configuration field. Test cases are:
        Test 1: when field.data is none
        Test 2: when field.data is ''
        Test 3: when field.data cannot be converted into an int
        Test 4: when field.data is not an int in the config list
        Test 5: when field.data is an integer inside the configuration list
        '''
        calculator_app.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with calculator_app.ev_calculator_app.app_context():

            calc = Calculator_Form()
            test_field = StringField()

            #test 1: when data is none
            test_field.data = None
            with self.assertRaises(ValidationError):
                calc.validate_ChargerConfiguration(test_field)

            #test 2: when data is ''
            test_field.data = ''
            with self.assertRaises(ValidationError):
                calc.validate_ChargerConfiguration(test_field)

            #test 3: when data cannot be converted into an int
            test_field.data = "1.0"
            with self.assertRaises(ValidationError):
                calc.validate_ChargerConfiguration(test_field)
        
            #test 4: when data is not in the config list
            test_field.data = "0"
            with self.assertRaises(ValidationError):
                calc.validate_ChargerConfiguration(test_field)

            #test 5: when data is an int in the config list
            test_field.data = "8"
            self.assertEqual(None, calc.validate_ChargerConfiguration(test_field))

    def test_validate_postcode(self):
        '''
        Testing done for Postcode field. Test cases are:
        Test 1: when field.data is none
        Test 2: when field.data is ''
        Test 3: when field.data cannot be converted into an int
        Test 4: when field.data is an int with length != 4
        Test 5: when field.data is an int with length 4
        '''
        calculator_app.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with calculator_app.ev_calculator_app.app_context():

            calc = Calculator_Form()
            test_field = StringField()

            #test 1: when data is none
            test_field.data = None
            with self.assertRaises(ValidationError):
                calc.validate_PostCode(test_field)

            #test 2: when data is ''
            test_field.data = ''
            with self.assertRaises(ValidationError):
                calc.validate_PostCode(test_field)

            #test 3: when data cannot be converted into an int
            test_field.data = "1.0"
            with self.assertRaises(ValidationError):
                calc.validate_PostCode(test_field)
        
            #test 4: when data is not a 4 digit int
            test_field.data = "12345"
            with self.assertRaises(ValidationError):
                calc.validate_PostCode(test_field)

            #test 5: when data is a 4 digit int
            test_field.data = "8888"
            self.assertEqual(None, calc.validate_PostCode(test_field))

def main():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestForm)
    unittest.TextTestRunner().run(test_suite)


main()



