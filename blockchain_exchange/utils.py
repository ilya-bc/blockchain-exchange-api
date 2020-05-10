from datetime import datetime


def timestamp_to_datetime(ts: str) -> datetime:
    """Convert UTC string to ``datetime``"""
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")


def pretty_print(params, offset=0, printer=repr):
    """Pretty print the dictionary 'params'

    Parameters
    ----------
    params : dict
        The dictionary to pretty print
    offset : int
        The offset in characters to add at the begin of each line.
    printer : callable
        The function to convert entries to strings, typically
        the builtin str or repr

    Notes
    -----
    Implementation is taken from ``sklearn.base._pprint`` with minor modifications
    to avoid additional dependencies.
    """
    # Do a multi-line justified repr:
    param_names = [p for p in params.keys() if p is not "cost"]
    param_names.sort()

    params_list = list()
    this_line_length = offset
    line_offset = " " * offset
    for i, name in enumerate(param_names):
        value = params[name]
        if isinstance(value, float):
            this_repr = '%s=%s' % (name, str(value))
        else:
            this_repr = '%s=%s' % (name, printer(value))
        if len(this_repr) > 500:
            this_repr = this_repr[:300] + '...' + this_repr[-100:]
        this_repr = f"\n{line_offset}{this_repr},"
        params_list.append(this_repr)
        this_line_length += len(this_repr)
    lines = ''.join(params_list)
    # Strip trailing space to avoid nightmare in doctests
    lines = '\n'.join(l.rstrip(' ') for l in lines.split('\n'))
    return lines
