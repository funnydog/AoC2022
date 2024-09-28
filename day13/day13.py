#!/usr/bin/env python3

import sys
import functools

# grammar
# list     : '[' elements ] ;
# elements : ε | element (',' element)* ;
# element  : NUMBER | list ;
# NUMBER   : '0'..'9'+ ;

class Parser(object):
    EOF      = -1
    INVALID  = 0
    LBRACKET = 1
    RBRACKET = 2
    COMMA    = 3
    NUMBER   = 4

    def __init__(self, txt):
        self.txt = txt
        self.idx = 0
        self.consume()

    def consume(self):
        if self.idx >= len(self.txt):
            self.lookahead, self.token = (self.EOF, None)
        elif self.txt[self.idx] == "[":
            self.lookahead, self.token = (self.LBRACKET, None)
            self.idx += 1
        elif self.txt[self.idx] == "]":
            self.lookahead, self.token = (self.RBRACKET, None)
            self.idx += 1
        elif self.txt[self.idx] == ",":
            self.lookahead, self.token = (self.COMMA, None)
            self.idx += 1
        elif self.txt[self.idx] in "0123456789":
            start = self.idx
            while self.idx < len(self.txt) and self.txt[self.idx] in "0123456789":
                self.idx += 1
            self.lookahead, self.token = (self.NUMBER, self.txt[start:self.idx])
        else:
            self.lookahead, self.token = (self.INVALID, None)

    def match(self, token):
        if token != self.lookahead:
            raise RuntimeError(f"Expected { token }, found { self.lookahead } instead")
        self.consume()

    def list(self):
        self.match(self.LBRACKET)
        result = self.elements()
        self.match(self.RBRACKET)
        return result

    def elements(self):
        elements = []
        if self.lookahead == self.NUMBER or self.lookahead == self.LBRACKET:
            elements.append(self.element())
            while self.lookahead == self.COMMA:
                self.match(self.COMMA)
                elements.append(self.element())
        return elements

    def element(self):
        if self.lookahead == self.NUMBER:
            value = int(self.token)
            self.match(self.NUMBER)
        elif self.lookahead == self.LBRACKET:
            value = self.list()
        else:
            raise RuntimeError(f"Expected { self.NUMBER } or { self.LBRACKET }, found { self.looakhead} instead")
        return value

def packet_cmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return (a - b) - (b - a)
    elif isinstance(a, list) and isinstance(b, int):
        return packet_cmp(a, [b])
    elif isinstance(a, int) and isinstance(b, list):
        return packet_cmp([a], b)
    else:
        i = 0
        while i < len(a) and i < len(b):
            v = packet_cmp(a[i], b[i])
            if v:
                return v
            i += 1
        if i < len(a):
            return 1
        if i < len(b):
            return -1
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            txt = f.read()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    packets = []
    for line in txt.splitlines():
        if line:
            # NOTE: easy but unsecure way
            # packets.append(eval(line))
            # NOTE: proper way
            packets.append(Parser(line).list())

    sumi = 0
    for i in range(0, len(packets), 2):
        if packet_cmp(packets[i], packets[i+1]) < 0:
            sumi += i // 2 + 1
    print("Part1:", sumi)

    div1 = [[2]]
    div2 = [[6]]
    packets.append(div1)
    packets.append(div2)
    packets.sort(key=functools.cmp_to_key(packet_cmp))
    print("Part2:", (packets.index(div1)+1) * (packets.index(div2)+1))

    for n in packets:
        print(n)
