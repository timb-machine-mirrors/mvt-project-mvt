# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021 The MVT Project Authors.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from mvt.common.indicators import Indicators
from mvt.common.module import run_module
from mvt.ios.modules.mixed.safari_browserstate import SafariBrowserState

from ..utils import get_backup_folder


class TestSafariBrowserStateModule:
    def test_parsing(self):
        m = SafariBrowserState(base_folder=get_backup_folder(), log=logging, results=[])
        m.is_backup = True
        run_module(m)
        assert m.file_path != None
        assert len(m.results) == 1
        assert len(m.timeline) == 1
        assert len(m.detected) == 0

    def test_detection(self, indicator_file):
        m = SafariBrowserState(base_folder=get_backup_folder(), log=logging, results=[])
        m.is_backup = True
        ind = Indicators(log=logging)
        ind.parse_stix2(indicator_file)
        # Adds a file that exists in the manifest.
        ind.ioc_files[0]["domains"].append("en.wikipedia.org")
        m.indicators = ind
        run_module(m)
        assert len(m.detected) == 1
        assert len(m.results) == 1
        assert m.results[0]["tab_url"] == "https://en.wikipedia.org/wiki/NSO_Group"