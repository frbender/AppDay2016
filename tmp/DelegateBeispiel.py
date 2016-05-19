class Klasse1:
    delegate = object()

    def doSomethingCool(self):
        self.delegate.blub()

    def bla(self):
        print("Bla")


class Delegierter:
    def blub(self):
        print("TOLL")


d = Delegierter()
k = Klasse1()

k.delegate = d

k.doSomethingCool()


###############################

class Klasse2:
    delegate = object()

    def doSomethingCool(self):
        self.delegate.bla()

    def blub(self):
        print("Blub")


k1 = Klasse1()
k2 = Klasse2()
k1.delegate = k2
k2.delegate = k1

k1.doSomethingCool()
k2.doSomethingCool()
