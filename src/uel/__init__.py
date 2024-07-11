# yapf: disable
__all__ = ['is_identifier_center_char_or_end_char', 'ASTToByteCodeCollectionCompiler', 'BT_STACK_TOP_AS_GQUEUE_TOP', 'BT_GQUEUE_TOP_AS_STACK_TOP', 'BaseHTTPRequestHandler', 'UELBuildtimeException', 'BT_POP_JUMP_IF_FALSE', 'UELBytecodeCompiler', 'UELMakeObjectError', 'runtime_type_check', 'UnknownSyntaxError', 'PushStackValueNode', 'SimpleFunctionCall', 'BT_SEQUENCE_APPEND', 'IS_CAN_MAKE_OBJECT', 'bytecode_optimizer', 'CallFunctionNode', 'BT_MAKE_SEQUENCE', 'UEFunctionObject', 'UELBaseException', 'UELRuntimeError', 'UEErr_SetString', 'BUILTIN_MODULES', 'initialization', 'ThrowException', 'ExpressionNode', 'UELSyntaxError', 'uel_new_object', '_UERunTaskDesc', 'UENumberObject', 'ContainerNode', 'ascii_letters', 'BT_LOAD_CONST', 'BT_STORE_NAME', 'ast_optimizer', 'import_module', 'default_patch', 'BytecodeInfo', 'TT_IDENTIFER', 'TooDotsError', 'AbstractNode', 'FunctionNode', 'SequenceNode', 'VariableNode', 'UELException', 'FunctionType', 'make_exports', 'AbstractTask', 'UEArgParser', '__version__', 'TT_KEYWORDS', 'TT_FUNCTION', 'single_call', 'CustomError', '_decompress', 'ImportNode', 'TT_KEYWORD', 'RaiseError', 'ModuleNode', 'RepeatNode', 'ReturnNode', 'SingleNode', 'decompress', 'HTTPServer', 'contextlib', 'excepthook', 'ModuleType', 'TT_STRING', 'BinOpNode', 'MinusNode', 'TT_IMPORT', 'TT_REPEAT', 'TT_RETURN', 'TokenNode', 'threading', 'BT_RETURN', 'TypeAlias', 'linecache', '_compress', 'BuildCode', 'LifoQueue', 'ParamSpec', 'Sequence', 'builtins', 'UEObject', 'overload', 'Optional', 'Position', 'TT_COMMA', 'TT_EQUAL', 'TT_FLOAT', 'TT_MINUS', 'is_start', 'objprint', 'Constant', 'MultNode', 'with_out', 'BT_MINUS', 'bytecode', 'deepcopy', 'compress', 'Callable', 'Iterator', 'ENCODING', 'TT_SEMI', 'TT_RPAR', 'TT_LPAR', 'TT_LSQB', 'TT_RSQB', 'AddNode', 'DivNode', 'IsEqual', 'PutNode', 'TT_CALL', 'TT_ELSE', 'TT_PUSH', 'BT_CALL', 'BT_JUMP', 'BT_QPUT', 'BT_QTOP', 'TypeVar', 'wcwidth', 'os.path', 'DIRNAME', 'RunCode', 'Generic', 'c_ulong', 'pointer', 'UETask', 'objstr', 'DIGITS', 'TT_ADD', 'TT_DIV', 'TT_EOF', 'TT_INT', 'TT_MUL', 'Nerver', 'IfNode', 'TT_END', 'TT_PUT', 'lookup', 'BT_ADD', 'BT_DIV', 'BT_MUL', 'BT_POP', 'BT_PUT', 'typing', 'stderr', 'pickle', 'atexit', 'pprint', 'Parser', 'throw', 'Empty', 'Tuple', 'Frame', 'Stack', 'final', 'Union', 'TT_IF', 'TT_IS', 'TT_OP', 'BT_IS', '_exit', 'RESET', 'start', 'parse', 'DEBUG', 'Queue', 'runpy', 'Lexer', 'Ueval', 'wraps', 'exit', 'main', 'List', 'argv', 'Main', 'Self', 'time', 'math', 'sys', 'Any', 'RED', 'os', 'BT', 'io', 'IO', 're', 't']
from uel.builder.bytecode.asttobytecodecollectioncompiler import ASTToByteCodeCollectionCompiler
from uel.builder.token.tools.identifier import is_identifier_center_char_or_end_char
from uel.builder.bytecode.bytecodeinfo import BT_GQUEUE_TOP_AS_STACK_TOP
from uel.builder.bytecode.bytecodeinfo import BT_STACK_TOP_AS_GQUEUE_TOP
from uel.builder.bytecode.uelbytecodecompiler import UELBytecodeCompiler
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.errors.runtime.uelmakeobjecterror import UELMakeObjectError
from uel.builder.bytecode.bytecodeinfo import BT_POP_JUMP_IF_FALSE
from uel.errors.uelbuildtimeexception import UELBuildtimeException
from uel.builder.ast.pushstackvaluenode import PushStackValueNode
from uel.builder.ast.simplefunctioncall import SimpleFunctionCall
from uel.builder.bytecode.bytecodeinfo import BT_SEQUENCE_APPEND
from uel.builder.bytecode.bytecodeinfo import BT_MAKE_SEQUENCE
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.builder.ast.callfunctionnode import CallFunctionNode
from uel.errors.unknownsyntaxerror import UnknownSyntaxError
from uel.builder.bytecode.bytecodeinfo import BT_LOAD_CONST
from uel.builder.bytecode.bytecodeinfo import BT_STORE_NAME
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.tools.func.wrapper.single_call import single_call
from uel.builder.ast.expressionnode import ExpressionNode
from uel.builder.bytecode import bytecodeinfo as bytecode
from uel.builder.token.tokenconstants import TT_IDENTIFER
from uel.builder.token.tokenconstants import TT_FUNCTION
from uel.builder.token.tokenconstants import TT_KEYWORDS
from uel.errors.ueerror_setstring import UEErr_SetString
from uel.errors.uelbaseexception import UELBaseException
from uel.builder.ast.containernode import ContainerNode
from uel.builder.bytecode.bytecodeinfo import BT_RETURN
from uel.builder.token.tokenconstants import TT_KEYWORD
from uel.builder.token.tools.identifier import is_start
from uel.builder.bytecode.bytecodeinfo import BT_MINUS
from uel.builder.token.tokenconstants import TT_IMPORT
from uel.builder.token.tokenconstants import TT_REPEAT
from uel.builder.token.tokenconstants import TT_RETURN
from uel.builder.token.tokenconstants import TT_STRING
from uel.builder.ast.abstractnode import AbstractNode
from uel.builder.ast.functionnode import FunctionNode
from uel.builder.ast.sequencenode import SequenceNode
from uel.builder.ast.variablenode import VariableNode
from uel.builder.bytecode.bytecodeinfo import BT_CALL
from uel.builder.bytecode.bytecodeinfo import BT_JUMP
from uel.builder.bytecode.bytecodeinfo import BT_QPUT
from uel.builder.bytecode.bytecodeinfo import BT_QTOP
from uel.builder.token.tokenconstants import TT_COMMA
from uel.builder.token.tokenconstants import TT_EQUAL
from uel.builder.token.tokenconstants import TT_FLOAT
from uel.builder.token.tokenconstants import TT_MINUS
from uel.runner.task.abstracttask import AbstractTask
from uel.builder.bytecode.bytecodeinfo import BT_ADD
from uel.builder.bytecode.bytecodeinfo import BT_DIV
from uel.builder.bytecode.bytecodeinfo import BT_MUL
from uel.builder.bytecode.bytecodeinfo import BT_POP
from uel.builder.bytecode.bytecodeinfo import BT_PUT
from uel.builder.token.tokenconstants import TT_CALL
from uel.builder.token.tokenconstants import TT_ELSE
from uel.builder.token.tokenconstants import TT_LPAR
from uel.builder.token.tokenconstants import TT_LSQB
from uel.builder.token.tokenconstants import TT_PUSH
from uel.builder.token.tokenconstants import TT_RPAR
from uel.builder.token.tokenconstants import TT_RSQB
from uel.builder.token.tokenconstants import TT_SEMI
from uel.errors.throwexception import ThrowException
from uel.errors.uelsyntaxerror import UELSyntaxError
from uel.pyexceptions.customerror import CustomError
from uel.tools.func.wrapper.with_out import with_out
from uel.builder.bytecode.bytecodeinfo import BT_IS
from uel.builder.token.tokenconstants import TT_ADD
from uel.builder.token.tokenconstants import TT_DIV
from uel.builder.token.tokenconstants import TT_END
from uel.builder.token.tokenconstants import TT_EOF
from uel.builder.token.tokenconstants import TT_INT
from uel.builder.token.tokenconstants import TT_MUL
from uel.builder.token.tokenconstants import TT_PUT
from uel.builder.token.tokenconstants import TT_IF
from uel.builder.token.tokenconstants import TT_IS
from uel.builder.token.tokenconstants import TT_OP
from uel.bytecodefile._compress import _decompress
from uel.libary.default.patch import default_patch
from uel.builder.ast.importnode import ImportNode
from uel.builder.ast.modulenode import ModuleNode
from uel.builder.ast.repeatnode import RepeatNode
from uel.builder.ast.returnnode import ReturnNode
from uel.builder.ast.singlenode import SingleNode
from uel.builder.token.tokennode import TokenNode
from uel.builder.bytecode.bytecodeinfo import BT
from uel.bytecodefile._compress import _compress
from uel.bytecodefile.compress import decompress
from uel.errors.toodotserror import TooDotsError
from uel.errors.uelexception import UELException
from uel.builder.ast.binopnode import BinOpNode
from uel.builder.ast.minusnode import MinusNode
from uel.libary.builtins import BUILTIN_MODULES
from uel.runner.task.buildcode import BuildCode
from http.server import BaseHTTPRequestHandler
from uel.bytecodefile.compress import compress
from uel.hook.initiation import initialization
from uel.builder.ast.constant import Constant
from uel.builder.ast.multnode import MultNode
from uel.errors.raiseerror import RaiseError
from uel.optimizer import bytecode_optimizer
from uel.builder.ast.addnode import AddNode
from uel.builder.ast.divnode import DivNode
from uel.builder.ast.isequal import IsEqual
from uel.builder.ast.putnode import PutNode
from uel.libary.helpers import make_exports
from uel.runner.task.runcode import RunCode
from uel.errors.runtime.throw import throw
from uel.hook.excepthook import excepthook
from uel.objects import IS_CAN_MAKE_OBJECT
from uel.pyexceptions.nerver import Nerver
from uel.builder.ast.ifnode import IfNode
from uel.builder.position import Position
from uel.ueargparse import _UERunTaskDesc
from uel.objects import UEFunctionObject
from uel.optimizer import ast_optimizer
from uel.impl.sequence import Sequence
from uel.objects import UENumberObject
from uel.objects import uel_new_object
from uel.ueargparse import UEArgParser
from uel.builder.parser import Parser
from importlib import import_module
from string import digits as DIGITS
from uel.builder.lexer import Lexer
from uel.version import __version__
from http.server import HTTPServer
from uel.constants import ENCODING
from uel.runner.frame import Frame
from uel.runner.stack import Stack
from uel.runner.ueval import Ueval
from uel.ue_web.ueweb import start
from uel.constants import DIRNAME
from uel.ueargparse import UETask
from string import ascii_letters
from uel.objects import UEObject
from uel.constants import DEBUG
from types import FunctionType
from unicodedata import lookup
from objprint import objprint
from uel.objects import parse
from types import ModuleType
from typing import ParamSpec
from typing import TypeAlias
from uel.colors import RESET
from functools import wraps
from objprint import objstr
from queue import LifoQueue
from typing import Callable
from typing import Iterator
from typing import Optional
from typing import overload
from ctypes import c_ulong
from ctypes import pointer
from typing import Generic
from typing import TypeVar
from uel.colors import RED
from copy import deepcopy
from pprint import pprint
from uel.main import Main
from typing import Tuple
from typing import Union
from typing import final
from uel.cli import main
from queue import Empty
from queue import Queue
from typing import List
from typing import Self
from sys import stderr
from typing import Any
from typing import IO
from os import _exit
from sys import argv
from sys import exit
from typing import *
import typing as t
import contextlib
import linecache
import threading
import builtins
import os.path
import wcwidth
import atexit
import pickle
import typing
import runpy
import math
import time
import sys
import io
import os
import re