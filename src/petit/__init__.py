"""
Library of utility code useful for systems administrators, analyzing and
manipulating log data.
"""
###############################################################################
#
# Writen By: Scott McCarty
# Date: 8/2009
# Email: scott.mccarty@gmail.com
# Version: 0.8.8
#
# Copyright (C) 2009 Scott McCarty
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################

# NOTE: this module deliberately does no sys.path manipulation and installs no
# warning filters. It used to do both; a library that mutates global state on
# import makes its host's behaviour depend on import order.

from .api import (
    Analysis,
    Group,
    analyze_lines,
    analyze_text,
    detect_format,
    hash_lines,
    hash_text,
)
from .errors import (
    DataFileError,
    EmptyLogError,
    ParseError,
    PetitError,
)
from .LogHash import IDENTIFIER, FingerprintScore, pull_identifiers

__all__ = [
    "IDENTIFIER",
    "Analysis",
    "DataFileError",
    "EmptyLogError",
    "FingerprintScore",
    "Group",
    "ParseError",
    "PetitError",
    "analyze_lines",
    "analyze_text",
    "detect_format",
    "hash_lines",
    "hash_text",
    "pull_identifiers",
]

