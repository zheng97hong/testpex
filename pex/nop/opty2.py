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

import random

from pex.arch import X86
from .opty2_tables import Opty2Tables


class Opty2:
    x86 = X86()
    table = Opty2Tables().StateTable

    def generate_sled(self, length, save_registers=[], badchars=b''):
        if length <= 0:
            return b''

        sled = b''
        prev = 256
        slen = 0

        counts = [0 for i in range(prev)]

        mask = 0
        for i in save_registers:
            mask |= 1 << self.x86.get_reg_num(i)

        mask = mask << 16

        bad_bytes = [1 for i in range(len(badchars))]
        while length > 0:
            low = -1
            lows = []

            for i in self.table[prev]:
                for j in i:
                    if (j & mask) != 0:
                        continue
                    if ((j >> 8) & 0xff) > slen:
                        continue

                    byte = j & 0xff
                    if bad_bytes[byte] == 1:
                        continue

                    if low == -1 or low > counts[byte]:
                        low = counts[byte]
                        lows = [byte]
                    elif low == counts[byte]:
                        lows.append(byte)

            if low == -1:
                raise RuntimeError("Failed to find a valid byte!")

            prev = lows[random.randint(len(lows))]
            counts[prev] += 1
            sled = bytes([prev]) + sled

            slen += 1
            length -= 1

        return sled