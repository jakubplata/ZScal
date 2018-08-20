#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

Kontur = namedtuple('Kontur', ['ozn', 'pow', 'pow_a'])


class Dzialka(object):

    def __init__(self, nr, pow, zero_flag=0, pow_flag=0, **kwargs):
        self.nr = nr
        self.pow = round(int(pow), -2)
        self.zero_flag = zero_flag
        self.pow_flag = pow_flag
        self.dane_kontury_lista = kwargs.get('kontury', [])
        self.kontury = self.create_kontury(self.dane_kontury_lista)
        if self.zero_flag:
            self.mod_zero_flag()
        if self.pow_flag:
            self.mod_pow_flag()

    def check_zero(self, pow):
        if pow == 0:
            return True
        else:
            return False

    def kontur_update_pow_a(self, ind, value):
        kontur_old = self.kontury.pop(ind)
        kontur_new = kontur_old._replace(pow_a=value)
        self.kontury.insert(ind, kontur_new)

    def mod_zero_flag(self):
        for nr, k in enumerate(self.kontury):
            if k.pow_a == 0:
                self.kontur_update_pow_a(nr, 100)

    def mod_pow_flag(self):
        sum_k = sum([k.pow_a for k in self.kontury])
        dif = sum_k - self.pow
        if dif == 100:
            new_pow = self.kontury[0].pow_a - 100
            self.kontur_update_pow_a(0, new_pow)
        elif dif == -100:
            new_pow = self.kontury[0].pow_a + 100
            self.kontur_update_pow_a(0, new_pow)

    def check_pow(self):
        sum_k = sum([k.pow_a for k in self.kontury])
        if sum_k != self.pow:
            return (True, ' UWAGA: różnice powierzchni działka: {} - użytki {}'
                    .format(self.pow, str(sum_k)))
        else:
            return False, ''

    def create_kontury(self, data):
        kontury = []
        for row in data:
            ozn, pow = row[0:2]
            pow_zaok = round(int(pow), -2)
            k = Kontur(ozn, pow, pow_zaok)
            kontury.append(k)
        return kontury

    def norm_line(self, txt1, txt2):
        line_length = 30
        n = line_length - len(txt1) - len(txt2)
        return txt1 + ' ' * n + txt2

    def text_to_write(self):
        check_pow, warn_pow = self.check_pow()
        warn_z = ' UWAGA: Zerowa powierzchnia!!!'
        count_warn_z = 0
        if check_pow:
            txt = self.norm_line(self.nr, str(self.pow)) + warn_pow + '\n'
        else:
            txt = self.norm_line(self.nr, str(self.pow)) + '\n'
        for k in self.kontury:
            if self.check_zero(k.pow_a):
                count_warn_z += 1
                txt += self.norm_line(k.ozn, str(k.pow_a)) + warn_z + '\n'
            else:
                txt += self.norm_line(k.ozn, str(k.pow_a)) + '\n'
        txt += '**\n'
        return txt, count_warn_z, check_pow
