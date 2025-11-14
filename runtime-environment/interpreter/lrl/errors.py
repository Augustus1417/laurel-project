def string_with_arrows(text, pos_start, pos_end):
    """Return a caret (^) highlighted snippet for an error span.

    The implementation uses the line (ln) and column (col) metadata from
    the provided positions to render one or more lines with carets under
    the offending span.
    """
    if pos_end is None:
        pos_end = pos_start

    # Clamp inputs
    pos_end_col = getattr(pos_end, 'col', getattr(pos_start, 'col', 0))
    start_line_idx = getattr(pos_start, 'ln', 0)
    end_line_idx = getattr(pos_end, 'ln', start_line_idx)

    lines = text.split('\n') if isinstance(text, str) else []
    if not lines:
        return ''

    # Ensure indices are in range
    start_line_idx = max(0, min(start_line_idx, len(lines) - 1))
    end_line_idx = max(0, min(end_line_idx, len(lines) - 1))

    result_lines = []
    for line_index in range(start_line_idx, end_line_idx + 1):
        line_text = lines[line_index]
        col_start = pos_start.col if line_index == start_line_idx else 0
        col_end = pos_end_col if line_index == end_line_idx else len(line_text)
        col_start = max(0, min(col_start, len(line_text)))
        col_end = max(col_start + 1, min(col_end, len(line_text)))
        result_lines.append(line_text)
        result_lines.append(' ' * col_start + '^' * (col_end - col_start))

    return '\n'.join(result_lines)

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result  = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context
        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return 'Traceback (most recent call last):\n' + result
