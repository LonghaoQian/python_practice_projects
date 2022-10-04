"""
Copyright (C) 2022 Longhao Qian

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

-------------------------------------------------------------------------------

This file contains the experiment data loading classes

"""

import csv

# basic loading function:
class CsvData:
    def __init__(self, fileName):
        # load thress .csv files
        rows = list()
        with open(fileName) as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
        # separate the tiles and other rows
        self.numOfColumns = len(rows[0])
        self.nunOfRows = len(rows) - 1
        self.labels = rows[0]
        self.content = rows[1:-1]

# forest experiment scene
class ForestScene:

    def __init__(self, measurementFile, paraFile, landMarkFile):
        # load thress .csv files
        self.measurements = CsvData(measurementFile)
        self.para = CsvData(paraFile)
        self.landmarks = CsvData(landMarkFile)