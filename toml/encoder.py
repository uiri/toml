import datetime
import re
import sys

from toml.decoder import InlineTableDict

if sys.version_info >= (3,):
    unicode = str


def dump(o, f):
    """Writes out dict as toml to a file

    Args:
        o: Object to dump into toml
        f: File descriptor where the toml should be stored

    Returns:
        String containing the toml corresponding to dictionary

    Raises:
        TypeError: When anything other than file descriptor is passed
    """

    if not f.write:
        raise TypeError("You can only dump an object to a file descriptor")
    d = dumps(o)
    f.write(d)
    return d


def dumps(o, encoder=None):
    """Stringifies input dict as toml

    Args:
        o: Object to dump into toml

        preserve: Boolean parameter. If true, preserve inline tables.

    Returns:
        String containing the toml corresponding to dict
    """

    retval = ""
    if encoder is None:
        encoder = TomlEncoder()
    addtoretval, sections = encoder._dump_sections(o, "")
    retval += addtoretval
    while sections != {}:
        newsections = {}
        for section in sections:
            addtoretval, addtosections = encoder._dump_sections(
                sections[section], section)

            if addtoretval or (not addtoretval and not addtosections):
                if retval and retval[-2:] != "\n\n":
                    retval += "\n"
                retval += "[" + section + "]\n"
                if addtoretval:
                    retval += addtoretval
            for s in addtosections:
                newsections[section + "." + s] = addtosections[s]
        sections = newsections
    return retval


class TomlEncoder(object):

    def __init__(self, preserve=False):
        self.preserve = preserve

    def _dump_sections(self, o, sup):
        retstr = ""
        if sup != "" and sup[-1] != ".":
            sup += '.'
        retdict = o.__class__()
        arraystr = ""
        for section in o:
            section = unicode(section)
            qsection = section
            if not re.match(r'^[A-Za-z0-9_-]+$', section):
                if '"' in section:
                    qsection = "'" + section + "'"
                else:
                    qsection = '"' + section + '"'
            if not isinstance(o[section], dict):
                arrayoftables = False
                if isinstance(o[section], list):
                    for a in o[section]:
                        if isinstance(a, dict):
                            arrayoftables = True
                if arrayoftables:
                    for a in o[section]:
                        arraytabstr = "\n"
                        arraystr += "[[" + sup + qsection + "]]\n"
                        s, d = self._dump_sections(a, sup + qsection)
                        if s:
                            if s[0] == "[":
                                arraytabstr += s
                            else:
                                arraystr += s
                        while d != {}:
                            newd = {}
                            for dsec in d:
                                s1, d1 = self._dump_sections(d[dsec], sup +
                                                             qsection + "." +
                                                             dsec)
                                if s1:
                                    arraytabstr += ("[" + sup + qsection +
                                                    "." + dsec + "]\n")
                                    arraytabstr += s1
                                for s1 in d1:
                                    newd[dsec + "." + s1] = d1[s1]
                            d = newd
                        arraystr += arraytabstr
                else:
                    if o[section] is not None:
                        retstr += (qsection + " = " +
                                   unicode(_dump_value(o[section])) + '\n')
            elif self.preserve and isinstance(o[section], InlineTableDict):
                retstr += (qsection + " = " + _dump_inline_table(o[section]))
            else:
                retdict[qsection] = o[section]
        retstr += arraystr
        return (retstr, retdict)


def _dump_inline_table(section):
    """Preserve inline table in its compact syntax instead of expanding
    into subsection.

    https://github.com/toml-lang/toml#user-content-inline-table
    """
    retval = ""
    if isinstance(section, dict):
        val_list = []
        for k, v in section.items():
            val = _dump_inline_table(v)
            val_list.append(k + " = " + val)
        retval += "{ " + ", ".join(val_list) + " }\n"
        return retval
    else:
        return unicode(_dump_value(section))


def _dump_value(v):
    dump_funcs = {
        str: lambda: _dump_str(v),
        unicode: lambda: _dump_str(v),
        list: lambda: _dump_list(v),
        bool: lambda: unicode(v).lower(),
        float: lambda: _dump_float(v),
        datetime.datetime: lambda: v.isoformat().replace('+00:00', 'Z'),
    }
    # Lookup function corresponding to v's type
    dump_fn = dump_funcs.get(type(v))
    # Evaluate function (if it exists) else return v
    return dump_fn() if dump_fn is not None else v


def _dump_str(v):
    v = "%r" % v
    if v[0] == 'u':
        v = v[1:]
    singlequote = v.startswith("'")
    v = v[1:-1]
    if singlequote:
        v = v.replace("\\'", "'")
        v = v.replace('"', '\\"')
    v = v.replace("\\x", "\\u00")
    return unicode('"' + v + '"')


def _dump_list(v):
    t = []
    retval = "["
    for u in v:
        t.append(_dump_value(u))
    while t != []:
        s = []
        for u in t:
            if isinstance(u, list):
                for r in u:
                    s.append(r)
            else:
                retval += " " + unicode(u) + ","
        t = s
    retval += "]"
    return retval


def _dump_float(v):
    return "{0:.16}".format(v).replace("e+0", "e+").replace("e-0", "e-")
