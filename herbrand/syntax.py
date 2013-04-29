from abc import ABCMeta, abstractproperty
import itertools

class Word(object):
    def __init__(self, label):
        self._label = label

    @property
    def label(self):
        return self._label

    def __str__(self):
        return self.label

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.label)

class ObjectVariable(Word):
    def __init__(self, label):
        # TODO: Assert begins with u v w x y z
        super(ObjectVariable, self).__init__(label)

class Constant(Word):
    def __init__(self, label):
        # TODO: Assert begins with a-t or numbers
        super(Constant, self).__init__(label)

# Objects e.g. joe, stanford, usa, 2345
class ObjectConstant(Constant):
    pass

# Functions such as mother, father, age, plus, times
class FunctionConstant(Constant):
    def __init__(self, label, arity):
        super(self.__class__, self).__init__(label)
        self._arity = arity

    @property
    def arity_amount(self):
        return self._arity.amount

# Relations such as knows, loves
class RelationConstant(Constant):
    def __init__(self, label, arity):
        super(self.__class__, self).__init__(label)
        self._arity = arity

    @property
    def arity_amount(self):
        return self._arity.amount

    def get_sentence_permutations(self, arguments):
        assert(len(arguments) >= self.arity_amount)
        perms = itertools.product(arguments, repeat=self.arity_amount)
        return frozenset([
            RelationalSentence(self, argument_perm)
            for argument_perm in perms
        ])

class Arity(object):
    def __init__(self, amount):
        assert(amount >= 1)
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def __str__(self):
        if self.amount == 1:
            return 'unary'
        elif self.amount == 2:
            return 'binary'
        elif self.amount == 3:
            return 'ternary'
        else:
            return 'n-ary'

class Signature(object):
    def __init__(self, object_constants, function_constants, relation_constants):
        assert(len(object_constants) > 0)
        assert(len(relation_constants) > 0)

        self._object_constants = frozenset(object_constants)
        self._function_constants = frozenset(function_constants)
        self._relation_constants = frozenset(relation_constants)

    @property
    def base(self):
        return frozenset([
            p
            for r in self._relation_constants
            for p in r.get_sentence_permutations(self._object_constants) 
        ])

class Term(object):
    def __init__(self, object):
        # TODO: Assert object is a variable, object constant or functional term
        self._object = object

    @property
    def object(self):
        return self._object

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.object)

    def __str__(self):
        return str(self.object)

class FunctionalTerm(object):
    def __init__(self, function_constant, terms):
        assert(function_constant.arity_amount == len(terms))

        self._function_constant = function_constant
        self._terms = tuple(terms)

    @property
    def terms(self):
        return self._terms

    def __str__(self):
        term_strings = [str(term) for term in self.terms]
        return '%s(%s)' % (self._function_constant, ", ".join(term_strings))

class Sentence(object):
    __meta__ = ABCMeta

    @property
    @abstractproperty
    def is_ground(self):
        # True if contains no variables, false if does
        pass

# Cannot be nested in terms or relational sentences
class RelationalSentence(Sentence):
    def __init__(self, relation_constant, terms):
        assert(relation_constant.arity_amount == len(terms))
        self._relation_constant = relation_constant
        self._terms = tuple(terms)

    def __str__(self):
        term_strings = [str(t) for t in self._terms]
        return "%s(%s)" % (self._relation_constant, ",".join(term_strings))

    def __repr__(self):
        term_reprs = [repr(t) for t in self._terms]
        return "%s(%s)" % (self._relation_constant, ",".join(term_reprs))


class LogicalSentence(Sentence):
    pass

class Negation(LogicalSentence):
    pass

class Conjunction(LogicalSentence):
    pass

class Disjunction(LogicalSentence):
    pass

class Implication(LogicalSentence):
    pass

class Reduction(LogicalSentence):
    pass

class Equivalence(LogicalSentence):
    pass


# Can be nested within other sentences
class QuantifiedSentence(Sentence):
    def __init__(self, quantified_variables, sentence):
        self._quantified_variables = tuple(quantified_variables)
        self._sentence = sentence

    def is_variable_bound(self, variable):
        if variable not in self._sentence.all_variables:
            raise ValueError("Variable %s not in sentence" % variable)

        return variable in self._quantified_variables

    @property
    def is_closed(self):
        return self._quantified_variables == self._sentence.all_variables

    @property
    def is_open(self):
        return not self.is_closed

class UniversalSentence(QuantifiedSentence):
    pass

class ExistentialSentence(QuantifiedSentence):
    pass