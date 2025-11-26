import math
import sys
from .errors import RTError

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def execute(self, args):
        from .runtime import RTResult
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                from .runtime import RTResult
                return None, RTError(other.pos_start, other.pos_end, 'Division by zero', self.context)
            return Number(self.value / other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        c = Number(self.value)
        c.set_pos(self.pos_start, self.pos_end)
        c.set_context(self.context)
        return c

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        c = String(self.value)
        c.set_pos(self.pos_start, self.pos_end)
        c.set_context(self.context)
        return c

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except Exception:
                return None, RTError(other.pos_start, other.pos_end, 'Element index out of bounds', self.context)
        return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except Exception:
                return None, RTError(other.pos_start, other.pos_end, 'Element index out of bounds', self.context)
        return None, Value.illegal_operation(self, other)

    def copy(self):
        c = List(self.elements)
        c.set_pos(self.pos_start, self.pos_end)
        c.set_context(self.context)
        return c

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        from .runtime import Context, SymbolTable
        new_ctx = Context(self.name, self.context, self.pos_start)
        new_ctx.symbol_table = SymbolTable(new_ctx.parent.symbol_table)
        return new_ctx

    def check_args(self, arg_names, args):
        from .runtime import RTResult
        res = RTResult()
        if len(args) > len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end, f"{len(args) - len(arg_names)} too many args passed into {self}", self.context))
        if len(args) < len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end, f"{len(arg_names) - len(args)} too few args passed into {self}", self.context))
        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        from .runtime import RTResult
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        from .runtime import RTResult
        from .interpreter import Interpreter
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()
        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return():
            return res
        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            return res
        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)

    def copy(self):
        c = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        c.set_context(self.context)
        c.set_pos(self.pos_start, self.pos_end)
        return c

    def __repr__(self):
        return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        from .runtime import RTResult
        res = RTResult()
        exec_ctx = self.generate_new_context()
        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)
        # Support varargs when method.arg_names is None
        if getattr(method, 'arg_names', []) is None:
            # populate arg0, arg1, ... without count checking
            for index, argument in enumerate(args):
                argument.set_context(exec_ctx)
                exec_ctx.symbol_table.set(f'arg{index}', argument)
        else:
            res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
            if res.should_return():
                return res
        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        c = BuiltInFunction(self.name)
        c.set_context(self.context)
        c.set_pos(self.pos_start, self.pos_end)
        return c

    def __repr__(self):
        return f"<built-in function {self.name}>"

    # Builtins
    def execute_say(self, exec_ctx):
        # Print any number of arguments
        # Args are populated as arg0, arg1, ... in exec_ctx
        printed_values = []
        index = 0
        while True:
            val = exec_ctx.symbol_table.get(f'arg{index}')
            if val is None:
                break
            printed_values.append(str(val))
            index += 1
        output = " ".join(printed_values)
        # Emit SAY_OUTPUT marker so the UI can pause execution
        print(f"SAY_OUTPUT:{output}", flush=True)
        
        # Wait for a continue signal from the UI (read one line from stdin)
        # This blocks the Python process until the user clicks Continue
        try:
            sys.stdin.readline()
        except:
            pass  # If stdin is closed, just continue
        
        from .runtime import RTResult
        return RTResult().success(Number.null)
    execute_say.arg_names = None  # None means varargs

    def execute_get_int(self, exec_ctx):
        return self._read_from_stdin(exec_ctx, prompt_type="int")
    execute_get_int.arg_names = ['arg0']

    def execute_get_float(self, exec_ctx):
        return self._read_from_stdin(exec_ctx, prompt_type="float")
    execute_get_float.arg_names = ['arg0']

    def execute_get_string(self, exec_ctx):
        return self._read_from_stdin(exec_ctx, prompt_type="string")
    execute_get_string.arg_names = ['arg0']

    def _success_number(self, number):
        from .runtime import RTResult
        return RTResult().success(Number(number))

    def _read_from_stdin(self, exec_ctx, prompt_type="string"):
        from .runtime import RTResult

        prompt_value = exec_ctx.symbol_table.get('arg0')
        prompt_text = str(prompt_value) if prompt_value is not None else ""
        request_payload = f"{prompt_type}:{prompt_text}"
        print(f"INPUT_REQUEST:{request_payload}", flush=True)

        while True:
            user_input = sys.stdin.readline()
            if user_input == "":
                return RTResult().failure(
                    RTError(self.pos_start, self.pos_end, "No input received; stream closed.", self.context)
                )

            value = user_input.rstrip("\r\n")

            if prompt_type == "int":
                try:
                    return self._success_number(int(value))
                except ValueError:
                    print(f"Invalid integer: {value}", flush=True)
                    print(f"INPUT_REQUEST:{request_payload}", flush=True)
            elif prompt_type == "float":
                try:
                    return RTResult().success(Number(float(value)))
                except ValueError:
                    print(f"Invalid float: {value}", flush=True)
                    print(f"INPUT_REQUEST:{request_payload}", flush=True)
            else:
                return RTResult().success(String(value))

# Predeclare builtins we need
BuiltInFunction.say = BuiltInFunction('say')
BuiltInFunction.get_int = BuiltInFunction('get_int')
BuiltInFunction.get_float = BuiltInFunction('get_float')
BuiltInFunction.get_string = BuiltInFunction('get_string')
