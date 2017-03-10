#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class RXVException(Exception):
    pass


class ResponseException(RXVException):
    """Exception raised when yamaha receiver responded with an error code"""
    pass

ReponseException = ResponseException


class MenuUnavailable(RXVException):
    """Menu control unavailable for current input"""
    pass


class PlaybackUnavailable(RXVException):
    """Raised when playback function called on unsupported source."""
    def __init__(self, source, action):
        super(PlaybackUnavailable, self).__init__('{} does not support {}'.format(source, action))
