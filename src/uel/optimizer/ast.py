from uel.builder.ast.addnode import AddNode
from uel.builder.ast.binopnode import BinOpNode
from uel.builder.ast.callfunctionnode import CallFunctionNode
from uel.builder.ast.constant import Constant
from uel.builder.ast.containernode import ContainerNode
from uel.builder.ast.divnode import DivNode
from uel.builder.ast.expressionnode import ExpressionNode
from uel.builder.ast.functionnode import FunctionNode
from uel.builder.ast.ifnode import IfNode
from uel.builder.ast.importnode import ImportNode
from uel.builder.ast.isequal import IsEqual
from uel.builder.ast.minusnode import MinusNode
from uel.builder.ast.modulenode import ModuleNode
from uel.builder.ast.multnode import MultNode
from uel.builder.ast.pushstackvaluenode import PushStackValueNode
from uel.builder.ast.putnode import PutNode
from uel.builder.ast.repeatnode import RepeatNode
from uel.builder.ast.returnnode import ReturnNode
from uel.builder.ast.sequencenode import SequenceNode
from uel.builder.ast.singlenode import SingleNode
from uel.builder.ast.variablenode import VariableNode


def optexpr(ast):
    pass


def ast_optimizer(ast):
    if RepeatNode is type(ast):
        for child in ast.childrens:
            ast_optimizer(child)
    if ExpressionNode is type(ast):
        ast: ExpressionNode
        optexpr(ast.val)
