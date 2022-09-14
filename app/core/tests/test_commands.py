"""
Test custom Django manamgnet commands
"""
from unittest.mock import patch # for mocking
from psycopg2 import OperationalError as Psycopg2Error # one of the errors we might get when connecting b4 the db is erasy
from django.core.management import call_command # helper functions by django that allows us to call a comamdn by name
from django.db.utils import OperationalError # another error that can be thrown by the db depending on what state it is in
from django.test import SimpleTestCase

#patch to mock the behaviour of our db. at top as we do for all functions in hrere
#core.management.commands.wait_for_db.Command.check <- is the command to be mocked to be tested for exception or value
@patch ('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""

    #magic object is passed by patch
    def test_wait_for_db_ready(self , patched_check):
        """ Test waiting for db if db ready"""
        #patched_check.return_value = True # just return true value

        #call_command('wait_for_db') # will execite the code inside wait for db and also check if the command is working and can be called

        #check if check method is called
        #patched_check.assert_called_once_with(databases=['default'])

    #test when db is not ready
    @patch('time.sleep') #patch the sleep so we do not wait in the tests
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """test wating for db when getting operational error"""
        #Psycopg2Error - pstgres has not started then this error is raised
        #OperationalError - postgres is read to take connections but the db is not ready to use - raised from Django
        #The sixth time we call it , it should return true
        #patched_check.side_effect= [Psycopg2Error]* 2 +  [OperationalError] * 3 + [True]

        #self.assertEqual(patched_check.call_count, 6) # checking if we call it 6 times only above

       # patched_check.assert_called_with(databases=['default']) # making sure patch check is being called with databasedefault







