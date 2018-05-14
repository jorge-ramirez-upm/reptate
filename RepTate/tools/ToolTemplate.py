# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Tool and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2018): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module ToolTemplate

Template file for creating a new Tool
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Tool import Tool
from QTool import QTool
from DataTable import DataTable


class ToolTemplate(CmdBase):
    """[summary]
    
    [description]
    """
    toolname = 'TemplateTool'
    description = 'Template Tool'
    citations = ''

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIToolTemplate(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLToolTemplate(
                name, parent_dataset, axarr)


class BaseToolTemplate:
    """[summary]
    
    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/en/latest/manual/Tools/template.html'
    toolname = ToolTemplate.toolname
    citations = ToolTemplate.citations

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main Tool function
        # self.parameters['param1'] = Parameter(
            # name='param1',
            # value=1,
            # description='parameter 1',
            # type=ParameterType.real,
            # opt_type=OptType.const)


    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def calculate(self, f=None, v=None):
        """Template function that returns the square of the y, according to the view
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        n = v.n

        tt = self.tables[f.file_name_short]
        tt.num_columns = n+1
        # Here, we assume that all series have the same x axis
        s = f.data_table.series[0][0]
        x = np.array(s.get_xdata())
        tt.num_rows = len(x)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = x

        for i in range(n):
            s = f.data_table.series[0][i]
            y = np.array(s.get_ydata())

            tt.data[:, i+1] = y*y


class CLToolTemplate(BaseToolTemplate, Tool):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUIToolTemplate(BaseToolTemplate, QTool):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the Tool here: