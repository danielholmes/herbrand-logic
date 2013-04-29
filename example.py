from herbrand.syntax import *

object_constants = [ObjectConstant('a'), ObjectConstant('b')]
relation_constants = [
    RelationConstant('p', Arity(1)), 
    RelationConstant('q', Arity(2))
]
s = Signature(object_constants, [], relation_constants)
print("Base:")
print("\n".join([str(b) for b in s.base]))