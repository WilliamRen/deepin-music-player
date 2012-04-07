#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2012 Deepin, Inc.
#               2011~2012 Hou Shaohui
#
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from song import Song
from player import Player
from config import config
from lrc_download import ttplayer_engine
import utils

class LrcManager(object):
    
    def __init__(self):
        pass
        
    def get_lrc_search_str(self, song):    
        artist = song.get_str("artist")
        title = song.get_str("title")
        if artist:
            return "%s-%s.lrc" % (artist, title)
        else:
            return "%s.lrc" % title
        
    def get_lrc_filepath(self, song):    
        save_path = os.path.expanduser(config.get("lyrics", "save_lrc_path"))
        if not os.path.exists(save_path):
            utils.makedirs(save_path)
        fillpath = os.path.join(save_path, self.get_lrc_search_str(song))
        return fillpath
        
    def get_lrc(self, song, try_web=True):    
        
        lrc_path = self.get_lrc_filepath(song)
        
        # lrc already exist
        if os.path.exists(lrc_path):        
            return lrc_path
        
        # Search in local directory of the file
        if song.get("uri") != None and song.get_scheme() == "file":
            local_lrc = os.path.join(song.get_dir(), self.get_lrc_search_str(song))
            if os.path.exists(local_lrc):
                return local_lrc
            
        if not config.getboolean("setting", "offline") and try_web:    
            try:
                ret = False
                artist = song.get_str("artist")
                title = song.get_str("title")
                result = ttplayer_engine.request(artist, title)
                if result:
                    if config.getboolean("lyrics", "auto_download"):
                        ret = utils.download(result[0][2], lrc_path)
                        if ret:
                            return lrc_path
            except:            
                pass
        return None    
                
lrc_manager = LrcManager()        
        
