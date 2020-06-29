#  _  __         _          ___       _               ___ _           _
# | |/ /_ _ __ _| |_ ___ __/ __| __ _| |___ _ __  ___| _ \ |_  _ __ _(_)_ _
# | ' <| '_/ _` |  _/ _ (_-<__ \/ _` | / _ \ '  \/ -_)  _/ | || / _` | | ' \
# |_|\_\_| \__,_|\__\___/__/___/\__,_|_\___/_|_|_\___|_| |_|\_,_\__, |_|_||_|
#                                                               |___/
# License: BSD License ; see LICENSE
#
# Main authors: Philipp Bucher (https://github.com/philbucher)
#

# set up testing environment (before anything else)
import initialize_testing_environment

# python imports
import sys
import unittest
from unittest.mock import patch, MagicMock

@unittest.skipIf(initialize_testing_environment.IS_EXECUTED_IN_SALOME, 'This test cannot be executed in Salome to not mess with "salome_pluginsmanager"')
@patch('PyQt5.QtWidgets.QMessageBox')
@patch('kratos_salome_plugin.salome_utilities.GetVersions', return_value= [10,0,0])
@patch('kratos_salome_plugin.gui.plugin_controller.PluginController')
class TestSalomePlugins(unittest.TestCase):
    def test_CreatePluginController(self,
        mock_plugin_controller,
        mock_fct_get_versions,
        mock_message_box):
        """Test for checking if the initialization of the PluginController works correctly
        This must only be done once per salome session and not every time the plugin is reopened,
        otherwise data is lost
        """

        sys.modules['salome_pluginsmanager'] = MagicMock()
        sys.modules['qtsalome'] = MagicMock()

        self.addCleanup(lambda: DeleteModuleIfExisting('salome_pluginsmanager'))
        self.addCleanup(lambda: DeleteModuleIfExisting('qtsalome'))

        self.assertEqual(mock_plugin_controller.call_count, 0)
        self.assertEqual(mock_fct_get_versions.call_count, 0)
        self.assertEqual(mock_message_box.call_count, 0)

        # this does sth when importing, hence doing it inside the test
        from salome_plugins import InitializePlugin

        self.assertEqual(mock_plugin_controller.call_count, 0)
        self.assertEqual(mock_fct_get_versions.call_count, 1) # called during importing
        self.assertEqual(mock_message_box.call_count, 0)

        salome_context = None # this should not be used hence passing None
        InitializePlugin(salome_context)

        self.assertEqual(mock_plugin_controller.call_count, 1)
        self.assertEqual(mock_fct_get_versions.call_count, 2)
        self.assertEqual(mock_message_box.call_count, 0) # not used if version is ok (which it is in this test)

        # calling it a seconf time is like pressing the plugin button a second time in salome
        # this should NOT re-create the PluginController, otherwise data is lost
        # also the version check should only be done once
        InitializePlugin(None)

        self.assertEqual(mock_plugin_controller.call_count, 1, msg="PluginController was not initialized correctly!")
        self.assertEqual(mock_fct_get_versions.call_count, 2)
        self.assertEqual(mock_message_box.call_count, 0) # not used if version is ok (which it is in this test)


def DeleteModuleIfExisting(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]


if __name__ == '__main__':
    unittest.main()