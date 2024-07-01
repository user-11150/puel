# pylint:disable=C0103
# pylint:disable=C0411
# pylint:disable=C0116
import typing as t
from queue import Empty, Queue
from types import FunctionType
from typing import (List, Optional, Any, Union)

from uel.utils.get_stack_top import get_stack_top

from uel.builder.bytecode.bytecodeinfo import (
    BT_ADD, BT_CALL, BT_DIV, BT_IS, BT_JUMP, BT_LOAD_CONST,
    BT_MAKE_SEQUENCE, BT_MINUS, BT_MUL, BT_POP, BT_POP_JUMP_IF_FALSE,
    BT_PUT, BT_QPUT, BT_QTOP, BT_RETURN, BT_SEQUENCE_APPEND, BT_STORE_NAME
)
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.objects import parse
from uel.objects import UEBooleanObject
from uel.objects import UECallableObject
from uel.objects import UEFunctionObject
from uel.objects import UESequenceObject
from uel.objects import UEObject
from uel.runner.frame import Frame
from uel.runner.stack import Stack
from uel.tools.func.share.runtime_type_check import runtime_type_check
from inspect import getfullargspec

__all__ = ["Ueval"]


class Ueval:
    """
    Runner
    """
    def __init__(
        self,
        bytecodes: List[BytecodeInfo],
        frame: Optional[Frame] = None,
        filename: str | None = None
    ) -> None:
        self.stopd = False
        self.frame = frame or Frame(
            # Stack
            Stack[Any](),
            # index
            0,
            # bytecodes
            bytecodes,
            # Prev_frame
            None,
            filename if filename is not None else "<unknown>",
            # Variables
            {},
            # Gqueue
            Queue()
        )

    @property
    def stack_top(self) -> Any:
        return get_stack_top(self.frame)

    def stack_push(self, value: Any) -> None:
        self.frame.stack.push(value)

    def uelEval_EvalBytecodeDefault(self) -> None:
        while True:
            while self.frame.idx < len(self.frame.bytecodes):
                if self.stopd:
                    break
                try:
                    try:
                        b = self.frame.bytecodes[self.frame.idx]
                    except IndexError:
                        pass
                    else:
                        self._eval(b)
                except Exception as e:
                    print(
                        f"Error on {self.frame.filename}, bytecode: {self.frame.idx} {self.frame.bytecodes}"
                    )
                    raise e
            if self.frame.prev_frame is None:
                break
            self.frame = self.frame.prev_frame

            # self.frame.idx += 1

    def equal(self, x: UEObject, y: UEObject) -> bool:
        if hasattr(x, "val") and hasattr(y, "val"):
            return bool(x.val == y.val)

        return bool(x == y)

    def next(self):
        self.frame.idx += 1

    def _eval(self, bytecode_info: BytecodeInfo) -> None:
        if bytecode_info.bytecode_type == BT_LOAD_CONST:
            self.stack_push(bytecode_info.value)
            self.next()

        elif bytecode_info.bytecode_type == BT_ADD:
            self.binary_op(self.frame, bytecode_info)
            self.next()

        elif bytecode_info.bytecode_type == BT_MINUS:
            self.binary_op(self.frame, bytecode_info)
            self.next()

        elif bytecode_info.bytecode_type == BT_MUL:
            self.binary_op(self.frame, bytecode_info)
            self.next()

        elif bytecode_info.bytecode_type == BT_DIV:
            self.binary_op(self.frame, bytecode_info)
            self.next()

        elif bytecode_info.bytecode_type == BT_IS:
            left_value = parse(self.stack_top, self.frame)
            right_val = parse(self.stack_top, self.frame)

            if hasattr(left_value, "tp_equal"):
                self.stack_push(
                    left_value.tp_equal(right_val).tp_bytecode()
                )
            elif hasattr(right_val, "tp_equal"):
                self.stack_push(
                    right_val.tp_equal(left_value).tp_bytecode()
                )
            else:
                result = UEBooleanObject(
                    str(self.equal(left_value, right_val))
                )
                self.stack_push(result.tp_bytecode())
            self.next()

        elif bytecode_info.bytecode_type == BT_STORE_NAME:
            name = bytecode_info.value
            val = parse(self.stack_top, self.frame)
            self.frame.variables[name] = val  # type: ignore
            self.next()

        elif bytecode_info.bytecode_type == BT_QPUT:
            self.frame.gqueue.put(self.stack_top)
            self.next()

        elif bytecode_info.bytecode_type == BT_POP:
            try:
                self.stack_top  # pylint: disable=W
            except Empty:
                pass
            self.next()

        elif bytecode_info.bytecode_type == BT_PUT:
            self.print(self.stack_top)
            self.next()

        elif bytecode_info.bytecode_type == BT_JUMP:
            self.jump(bytecode_info.value)


#        elif bytecode_info.bytecode_type ==BT_IF_TRUE_JUMP:
#            val = parse(self.stack_top, self.frame)
#            if self.tp_bool(val):
#                self.jump(bytecode_info.value)
#            self.next()
#
#        elif bytecode_info.bytecode_type ==BT_IF_FALSE_JUMP:
#            value = parse(self.stack_top, self.frame)
#            if not self.tp_bool(value):
#                self.jump(bytecode_info.value)
#            self.next()

        elif bytecode_info.bytecode_type == BT_POP_JUMP_IF_FALSE:
            obj = parse(self.stack_top, self.frame)
            if not self.tp_bool(obj):
                self.jump(bytecode_info.value)
                return
            self.next()

        elif bytecode_info.bytecode_type == BT_CALL:
            self.call_function()

        elif bytecode_info.bytecode_type == BT_RETURN:
            if self.frame.prev_frame is None:
                throw(UELRuntimeError, "'return' outside function")
                return
            self.frame.prev_frame.gqueue.put_nowait(self.stack_top)
            self.frame = self.frame.prev_frame

        elif bytecode_info.bytecode_type == BT_MAKE_SEQUENCE:
            self.stack_push(UESequenceObject())
            self.next()

        elif bytecode_info.bytecode_type == BT_SEQUENCE_APPEND:
            item = parse(self.stack_top, self.frame)
            sequ = parse(self.stack_top, self.frame)

            if type(sequ) is not UESequenceObject:
                return
            sequ.val.append(item)
            self.stack_push(sequ)
            self.next()

        else:
            prettyd = bytecode_info.pretty_with_bytecode_type(
                bytecode_info.bytecode_type
            )[0]
            raise ValueError("Not support type:" + f"{prettyd}")

    def call_function(self) -> None:
        def getFunctionArgumentLength(
            fn: Union[UEFunctionObject, UECallableObject, FunctionType]
        ) -> int:
            if type(fn) is UEFunctionObject:
                return len(fn.args)
            try:
                return len(getfullargspec(fn).args) - 1
            except Exception as e:
                if issubclass(type(fn), UEObject):
                    throw(
                        UELRuntimeError,
                        f"TypeError: {fn.tp_str()} is not a callable"
                    )
                else:
                    raise e

        function: Union[UEFunctionObject, UECallableObject,
                        FunctionType] = parse(
                            self.stack_top, self.frame
                        )  # type: ignore

        arguments: list[UEObject] = []
        for _ in range(0, getFunctionArgumentLength(function)):
            arguments.insert(0, self.frame.gqueue.get_nowait())
        if type(function) is UEFunctionObject:
            self.next()
            function.tp_call(self, args=arguments, frame=self.frame)
            # print(self.frame)
        else:
            if not hasattr(function, "__call__"):
                throw(
                    UELRuntimeError,
                    f"TypeError: {function.tp_str()} is not a callable"
                )
            result: UEObject = function(self.frame, *arguments)
            if result is not None:
                self.frame.gqueue.put_nowait(result)
            self.next()

    def jump(self, idx: t.Any) -> None:
        if type(idx) is not int:
            raise TypeError("Arg 1 must be a int")
        self.frame.idx = idx - 1

    def tp_bool(self, val: UEObject) -> bool:
        if hasattr(val, "val"):
            return bool(val.val)
        return True

    def binary_op(self, frame: Frame, bytecode_info: BytecodeInfo) -> None:
        right_value = parse(self.stack_top, frame)
        left_value = parse(self.stack_top, frame)

        fn_name: str

        if bytecode_info.bytecode_type == BT_ADD:
            fn_name = "tp_add"
        elif bytecode_info.bytecode_type == BT_MINUS:
            fn_name = "tp_minus"
        elif bytecode_info.bytecode_type == BT_MUL:
            fn_name = "tp_mult"
        elif bytecode_info.bytecode_type == BT_DIV:
            fn_name = "tp_div"
        else:
            raise ValueError
        if (
            (
                hasattr(left_value, fn_name) and
                hasattr(right_value, fn_name)
            )
        ):
            result = getattr(left_value, fn_name)(right_value)
        else:
            throw(UELRuntimeError("[TypeError] Unable add"))
        frame.stack.push(result.tp_bytecode())

    def print(self, uelobject: UEObject) -> None:
        print(parse(uelobject, self.frame).tp_str(), end="")
