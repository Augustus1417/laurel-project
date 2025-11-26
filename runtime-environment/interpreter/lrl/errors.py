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

    # Compute width for line numbers so things align nicely
    max_line_no = end_line_idx + 1
    digits = len(str(max_line_no))

    result_lines = []
    for line_index in range(start_line_idx, end_line_idx + 1):
        line_text = lines[line_index]
        col_start = pos_start.col if line_index == start_line_idx else 0
        col_end = pos_end_col if line_index == end_line_idx else len(line_text)
        # Clamp to valid range for the current line
        col_start = max(0, min(col_start, len(line_text)))
        col_end = max(0, min(col_end, len(line_text)))

        # Prefix line with a right-aligned line number and a separator, e.g. "  3 |"
        prefix = str(line_index + 1).rjust(digits) + ' | '
        result_lines.append(prefix + line_text)

        # Determine caret length. We avoid forcing a caret on empty, non-start lines
        caret_len = col_end - col_start
        if caret_len <= 0:
            # If this is the start line, show a single caret at the insertion point
            if line_index == start_line_idx:
                caret_len = 1
            else:
                # Skip adding a caret line for empty/non-highlighted lines
                continue

        # Caret line should match prefix length + column offset
        caret_offset = digits + 3 + col_start  # digits + ' | ' length
        caret_line = ' ' * caret_offset + '^' * caret_len
        result_lines.append(caret_line)

    return '\n'.join(result_lines)

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def hint(self):
        """Optional short, beginner-friendly hint for how to fix the error."""
        return ''

    def as_string(self):
        # Friendly header
        location = f"File '{self.pos_start.fn}', line {self.pos_start.ln + 1}, column {getattr(self.pos_start, 'col', 0) + 1}"
        result  = f"{self.error_name}: {self.details}\n\n"
        result += f"Where: {location}\n\n"
        # Code snippet with arrows
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)

        # Add a very short hint if available
        hint_text = self.hint()
        if hint_text:
            result += '\n\nHint: ' + hint_text

        # Make message concise and beginner-friendly
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

    def hint(self):
        return 'There is an unsupported character at the highlighted spot. Remove or replace it with a valid character (letters, numbers, parentheses, operators, etc.).'

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

    def hint(self):
        return 'A character (like ), ], or a colon) is missing. Check for unmatched parentheses or missing separators near the highlighted area.'

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

    def hint(self):
        # Provide a contextual, actionable hint when possible.
        d = (self.details or "").lower()
        # Common pattern: parser reports Expected ...
        if 'expected' in d:
            # Detect incomplete assignment like `a =` (identifier or value expected)
            if 'identifier' in d or 'int' in d or 'float' in d or '+' in d or '-' in d or '(' in d or '[' in d:
                return (
                    "It looks like an expression or value was expected here (for example after `=`). "
                    "If you started an assignment like `a =`, provide a value or expression on the right-hand side."
                )
            if 'if' in d or 'for' in d or 'while' in d:
                return (
                    "A statement (like an `if`, `for`, or `while`) was expected here. "
                    "Make sure you haven't accidentally left a line blank or omitted required keywords."
                )
            if 'fun' in d:
                return (
                    "A function declaration was expected here. If you intended to declare a function, use the `fun` keyword and provide a name and parameter list, e.g. `fun myFunc(x)`."
                )
            # Generic fallback for Expected lists
            # Try to shorten the details to a human-friendly fragment
            cleaned = self.details.replace('Expected', '').strip(': ').strip()
            return f"Expected one of: {cleaned}. Check for missing operators or incomplete expressions."

        # Generic hint if we can't infer specifics
        return "The code here doesn't match the expected syntax. Check for missing operators, incomplete assignments (like `a =`), unmatched parentheses, or extra tokens."

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        # Generate a shorter, friendly call stack then the code snippet
        result  = self.generate_traceback()
        result += f"{self.error_name}: {self.details}\n\n"
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)

        hint_text = self.hint()
        if hint_text:
            result += '\n\nHint: ' + hint_text

        return result

    def generate_traceback(self):
        # Build a list of frames (line number, context name).
        frames = []
        pos = self.pos_start
        ctx = self.context
        while ctx:
            frames.append((pos.ln + 1, ctx.display_name))
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        if not frames:
            return ''

        # If the only frame is the top-level program frame, omit the trace to
        # avoid showing an unfamiliar call stack header to beginners.
        if len(frames) == 1 and frames[0][1] == '<program>':
            return ''

        # Otherwise produce a short, beginner-friendly header and list frames.
        result_lines = []
        # Show frames in the same order as before (most recent last).
        for ln, name in reversed(frames):
            result_lines.append(f"  Line {ln}, in {name}\n")

        return 'Execution trace:\n' + ''.join(result_lines)

    def hint(self):
        return 'A runtime error occurred during execution. Check the highlighted code so you can assess where you went wrong.'
