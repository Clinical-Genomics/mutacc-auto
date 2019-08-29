import pytest
from pathlib import Path
import os
from mock import patch

from mutacc_auto.recipes.import_recipe import *
from mutacc_auto.commands.command import Command

@patch.object(Command, 'call')
def test_import_extracted_case(command):

    import_extracted_case('case','config', 'binary')
