from dataclasses import dataclass

@dataclass
class NumberNode:
    tok: any
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

@dataclass
class StringNode:
    tok: any
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

@dataclass
class ListNode:
    element_nodes: list
    pos_start: any
    pos_end: any

@dataclass
class VarAccessNode:
    var_name_tok: any
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

@dataclass
class VarAssignNode:
    var_name_tok: any
    value_node: any
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

@dataclass
class BinOpNode:
    left_node: any
    op_tok: any
    right_node: any
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

@dataclass
class UnaryOpNode:
    op_tok: any
    node: any
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

@dataclass
class IfNode:
    cases: list
    else_case: any
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

@dataclass
class ForNode:
    var_name_tok: any
    start_value_node: any
    end_value_node: any
    step_value_node: any
    body_node: any
    should_return_null: bool
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

@dataclass
class WhileNode:
    condition_node: any
    body_node: any
    should_return_null: bool
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

@dataclass
class FuncDefNode:
    var_name_tok: any
    arg_name_toks: list
    body_node: any
    should_auto_return: bool
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start
        self.pos_end = self.body_node.pos_end

@dataclass
class CallNode:
    node_to_call: any
    arg_nodes: list
    pos_start: any = None
    pos_end: any = None
    def __post_init__(self):
        self.pos_start = self.node_to_call.pos_start
        self.pos_end = (self.arg_nodes[-1].pos_end if len(self.arg_nodes) > 0 else self.node_to_call.pos_end)

@dataclass
class ReturnNode:
    node_to_return: any
    pos_start: any
    pos_end: any

@dataclass
class ContinueNode:
    pos_start: any
    pos_end: any

@dataclass
class BreakNode:
    pos_start: any
    pos_end: any

@dataclass
class StatementsNode:
    statements: list
    pos_start: any
    pos_end: any
