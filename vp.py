#!/usr/bin/env python

class Volume:
    CONVERSION_SCALE = {"us_cup":48.0, "us_tbsp":3.0, "us_tsp":1.0}
    def __init__(self, **kwargs):
        assert(len(kwargs.keys()) == 1)
        self.unit = kwargs.keys()[0]
        self.value = kwargs[self.unit]

    @staticmethod
    def from_tsp(tsp, unit):
        val = Volume.convert("us_tsp", unit, tsp)
        return Volume(**{unit:val})

    def __add__(self, other):
        return Volume.from_tsp(self.us_tsp + other.us_tsp, self.unit)

    def __sub__(self, other):
        return Volume.from_tsp(self.us_tsp - other.us_tsp, self.unit)

    def __div__(self, other):
        return Volume.from_tsp(self.us_tsp / float(other), self.unit)

    def __mul__(self, other):
        return Volume.from_tsp(self.us_tsp * other, self.unit)

    def __cmp__(self, v2):
        assert(type(v2) == type(self) or v2 == 0 )
        qt1 = self.us_tsp
        if type(v2) == type(self):
            qt2 = v2.us_tsp
        else:
            qt2 = 0
        if abs(qt1-qt2) < 1./16:
            return 0
        if qt1 > qt2:
            return 1
        else:
            return -1

    @property
    def us_cup(self):
        return Volume.convert(self.unit, "us_cup",  self.value)

    @property
    def us_tbsp(self):
        return Volume.convert(self.unit, "us_tbsp",  self.value)

    @property
    def us_tsp(self):
        return Volume.convert(self.unit, "us_tsp",  self.value)

    @staticmethod
    def convert(unit1,unit2,val):
        if unit1 == unit2:
            return val
        return val * (Volume.CONVERSION_SCALE[unit1] / Volume.CONVERSION_SCALE[unit2])


    def __str__(vol):
        v = VolumeStringBuilder()

        if vol == 0:
            return str(v)

        # Check how many cups fit
        while vol.us_cup > 0.24999999999:
            cups = vol.us_cup
            third = 0.33333333333333
            if cups > third and (cups/third)%1 < 0.001:
                vol = vol - Volume(us_cup=third)
                v.cup+=third
            else:
                vol = vol - Volume(us_cup=0.25)
                v.cup+=0.25

        if vol == 0:
            return str(v)

        while vol.us_tbsp > 0.999:
            vol = vol - Volume(us_tbsp=1)
            v.tbsp+=1


        if vol != Volume(us_tsp=2./3):
            if vol > Volume(us_tbsp=0.5):
                v.tbsp+=0.5
                vol = vol - Volume(us_tbsp=0.5)

        if vol == 0:
            return str(v)

        v.tsp+=vol.us_tsp
        return str(v).strip().rstrip()


class VolumeStringBuilder:
    def __init__(self):
        self.cup = 0
        self.tbsp = 0
        self.tsp = 0

    @staticmethod
    def format_measure(val, precision=0.001):
        if precision != 0.001:
            buff = "(imprecise)"
        else:
            buff = ""
        if int(val) > 0 : # More than one
            buff+=str(int(val))
            val-=int(val)
        if abs(val-1.0000) < precision: buff+="1"
        elif abs(val-0.8333333) < precision: buff+="1/3 + 1/2"
        elif abs(val-0.75) < precision: buff+="3/4"
        elif abs(val-0.6666666) < precision: buff+="2/3"
        elif abs(val-0.5) < precision: buff+="1/2"
        elif abs(val-0.3333333) < precision: buff+="1/3"
        elif abs(val-0.25) < precision: buff+="1/4"
        elif abs(val-0.125) < precision: buff+="1/8"
        elif abs(val-0.00) < precision: pass
        else:
            return VolumeStringBuilder.format_measure(val, precision*10+precision)
        return buff

    def __str__(self):
        s = ""
        if self.cup >= 0.01:
            s+=" %s cup"%VolumeStringBuilder.format_measure(self.cup)
        if self.tbsp >= 0.01:
            s+=" %s tablespoon"%VolumeStringBuilder.format_measure(self.tbsp)
        if self.tsp >= 0.01:
            s+=" %s teaspoon"%VolumeStringBuilder.format_measure(self.tsp)

        if self.cup <= 0.01 and self.tbsp <= 0.01 and self.tsp <= 0.01:
            return "CRUMBS"
        return s.strip()


if __name__ == '__main__':
    assert(str(Volume(us_cup=1./4)) == "1/4 cup")
    assert(str(Volume(us_cup=1./4)/3) == "1 tablespoon 1 teaspoon")
    assert(str( Volume(us_cup=1./3) + Volume(us_cup=1./3) ) == "2/3 cup")
    assert(str(Volume(us_cup=1./4)/2) == "2 tablespoon")
    assert(str(Volume(us_cup=1./4)/4) == "1 tablespoon")
    assert(str(Volume(us_cup=1./4)/12) == "1 teaspoon")
    assert(str(Volume(us_tsp=1)*3) == "1 tablespoon")
    assert(str(Volume(us_cup=1./4) + Volume(us_tbsp=4)) == "1/2 cup")
    assert(str(Volume(us_cup=1./4)/48) == "1/4 teaspoon")
