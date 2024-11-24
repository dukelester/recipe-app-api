from unittest.mock import patch, call
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('django.core.management.base.BaseCommand.check')
class CommandTests(SimpleTestCase):
    """Test the wait_for_db management command."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database when the database is available."""
        # Mock check to return True (database ready)
        patched_check.return_value = True

        # Call the command
        call_command('wait_for_db')

        # Ensure check is called exactly once with the 'default' database
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep', return_value=None)
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when it raises OperationalError at first.
        """
        # Mock check to raise OperationalError the first two times,then succeed
        patched_check.side_effect = [OperationalError, OperationalError, True]

        # Call the command
        call_command('wait_for_db')

        # Ensure check is called three times
        self.assertEqual(patched_check.call_count, 3)

        # Ensure check is called with the 'default' database
        patched_check.assert_has_calls([call(databases=['default'])] * 3)

        # Ensure time.sleep is called twice (between failures)
        self.assertEqual(patched_sleep.call_count, 2)
