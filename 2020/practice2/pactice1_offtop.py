
class CustomClass():
    def public_method(self):
        print('you can access me outside this class')

    def __private_method(self):
        print('you can not access me outside this class')

cc= CustomClass()
print('     Calling cc.public_method() :')
cc.public_method()
print('     Calling cc.__private_method() :')
try:
    cc.__private_method()
except Exception as e:
    print(e)
print('     Calling cc._CustomClass__private_method() :')
cc._CustomClass__private_method()
