VolumePrinter
=============

Print volumes for US recipe in a friendly way


Usage
=====

    from vp import Volume
    
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
