# -*- coding: utf-8 -*-
#
# Copyright 2012 Institut für Experimentelle Kernphysik - Karlsruher Institut für Technologie
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from sqlalchemy import *
import hf

metadata = MetaData()
engine = None

def connect(implicit_execution=False):
    config = dict(hf.config.items("database"))
    hf.database.engine = engine_from_config(config, prefix="")
    if implicit_execution == True:
        metadata.bind = hf.database.engine

def disconnect():
    pass
