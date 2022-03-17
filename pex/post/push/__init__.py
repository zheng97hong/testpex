#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from collections import OrderedDict

from pex.tools.type import TypeTools

from pex.post.push.echo import Echo
from pex.post.push.bash_echo import BashEcho
from pex.post.push.printf import Printf
from pex.post.push.certutil import Certutil


class Push:
    type_tools = TypeTools()

    push_methods = OrderedDict({
        'printf': [
            type_tools.platforms['unix'],
            Printf()
        ],
        'echo': [
            type_tools.platforms['unix'],
            Echo()
        ],
        'bash_echo': [
            type_tools.platforms['unix'],
            BashEcho()
        ],
        'certutil': [
            type_tools.platforms['windows'],
            Certutil()
        ]
    })

    def push(self, platform, sender, data, location, args=[], method=None, linemax=100):
        if method in self.push_methods or not method:
            if not method:
                for push_method in self.push_methods:
                    if platform in self.push_methods[push_method][0]:
                        method = push_method

                if not method:
                    return None
            else:
                if platform not in self.push_methods[method][0]:
                    return None

            self.push_methods[method][1].push(
                sender=sender,
                data=data,
                location=location,
                args=args,
                linemax=linemax
            )
            return location
        return None