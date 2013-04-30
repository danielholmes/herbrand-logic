from herbrand.syntax import *

abby = ObjectConstant('abby')
bess = ObjectConstant('bess')
cody = ObjectConstant('cody')
dana = ObjectConstant('dana')
object_constants = [abby, bess, cody, dana]

likes_relation = RelationConstant('likes', Arity(2))
relation_constants = [
    likes_relation
]
s = Signature(object_constants, [], relation_constants)
print("Base:")
print("\n".join([str(b) for b in s.base]))

w_variable = ObjectVariable('w')
x_variable = ObjectVariable('x')
y_variable = ObjectVariable('y')
z_variable = ObjectVariable('z')

# Abby likes everyone bess likes
# Vy.(likes(bess, y) => likes(abby, y))
sentence = UniversalSentence(
    [y_variable],
    Implication(
        RelationalSentence(likes_relation, [bess, y_variable]),
        RelationalSentence(likes_relation, [abby, y_variable])
    )
)

# Cody likes everyone who likes her
# Vx.(likes(x, cody) => likes(cody, x))
sentence = UniversalSentence(
    [x_variable],
    Implication(
        RelationalSentence(likes_relation, [x_variable, cody]),
        RelationalSentence(likes_relation, [cody, x_variable])
    )
)

# Cody likes somebody who likes her
# Ez.(likes(z, cody) ^ likes(cody, z))
sentence = ExistentialSentence(
    [z_variable],
    Conjunction(
        RelationalSentence(likes_relation, [z_variable, cody]),
        RelationalSentence(likes_relation, [cody, z_variable])
    )
)

# Nobody likes herself
# -Ew.likes(w, w)
sentence = Negation(
    ExistentialSentence(
        [w_variable],
        RelationalSentence(
            likes_relation,
            [w_variable, w_variable]
        )
    )
)

# Everybody likes somebody
# Vx.Ey.likes(x, y)
UniversalSentence(
    [x_variable],
    ExistentialSentence(
        [y_variable],
        RelationalSentence(
            likes_relation,
            [x_variable, y_variable]
        )
    )
)

# There is someone everybody likes
# Ey.Vx.likes(x, y)
ExistentialSentence(
    [y_variable],
    UniversalSentence(
        [x_variable],
        RelationalSentence(
            likes_relation,
            [x_variable, y_variable]
        )
    )
)