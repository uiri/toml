import datetime

def loads(s):
    implicitgroups = []
    """Returns a dictionary containing s, a string, parsed as toml."""
    retval = {}
    currentlevel = retval
    if isinstance(s, str):
        sl = list(s)
        openarr = 0
        openstring = False
        beginline = True
        keygroup = False
        delnum = 1
        for i in xrange(len(sl)):
            if sl[i] == '"' and sl[i-1] != '\\':
                openstring = not openstring
            if keygroup and (sl[i] == ' ' or sl[i] == '\t'):
                keygroup = False
            if sl[i] == '#' and not openstring and not keygroup:
                j = i
                while sl[j] != '\n':
                    sl.insert(j, ' ')
                    sl.pop(j+1)
                    j += 1
            if sl[i] == '[' and not openstring and not keygroup:
                if beginline:
                    keygroup = True
                else:
                    openarr += 1
            if sl[i] == ']' and not openstring and not keygroup:
                if keygroup:
                    keygroup = False
                else:
                    openarr -= 1
            if sl[i] == '\n':
                if openstring:
                    raise Exception("Unbalanced quotes")
                if openarr:
                    sl.insert(i, ' ')
                    sl.pop(i+1)
                else:
                    beginline = True
            elif beginline and sl[i] != ' ' and sl[i] != '\t':
                beginline = False
                keygroup = True
        s = ''.join(sl)
        s = s.split('\n')
    else:
        raise Exception("What exactly are you trying to pull?")
    for line in s:
        line = line.strip()
        if line == "":
            continue
        if line[0] == '[':
            line = line[1:].split(']', 1)
            if line[1].strip() != "":
                raise Exception("Key group not on a line by itself.")
            line = line[0]
            groups = line.split('.')
            currentlevel = retval
            for i in xrange(len(groups)):
                group = groups[i]
                if group == "":
                    raise Exception("Can't have a keygroup with an empty name")
                try:
                    currentlevel[group]
                    if i == len(groups) - 1:
                        if group in implicitgroups:
                            implicitgroups.remove(group)
                        else:
                            raise Exception("What? "+group+" already exists?"+str(currentlevel))
                except KeyError:
                    if i != len(groups) - 1:
                        implicitgroups.append(group)
                    currentlevel[group] = {}
                currentlevel = currentlevel[group]
        elif "=" in line:
            i = 1
            pair = line.split('=', i)
            while pair[-1][0] != ' ' and pair[-1][0] != '\t':
                i += 1
                pair = line.split('=', i)
            newpair = []
            newpair.append('='.join(pair[:-1]))
            newpair.append(pair[-1])
            pair = newpair
            pair[0] = pair[0].strip()
            pair[1] = pair[1].strip()
            value, vtype = load_value(pair[1])
            try:
                currentlevel[pair[0]]
                raise Exception("Duplicate keys!")
            except KeyError:
                currentlevel[pair[0]] = value
    return retval

def load_value(v):
    if v == 'true':
        return (True, "bool")
    elif v == 'false':
        return (False, "bool")
    elif v[0] == '"':
        testv = v[1:].split('"')
        closed = False
        for tv in testv:
            if tv == '':
                closed = True
            elif tv[-1] != '\\':
                if closed:
                    raise Exception("Stuff after closed string. WTF?")
                else:
                    closed = True
        escapes = ['0', 'n', 'r', 't', '"', '\\']
        escapedchars = ['\0', '\n', '\r', '\t', '\"', '\\']
        escapeseqs = v.split('\\')[1:]
        backslash = False
        for i in escapeseqs:
            if i == '':
                backslash = not backslash
            else:
                if i[0] not in escapes and i[0] != 'x' and not backslash:
                    raise Exception("Reserved escape sequence used")
                if backslash:
                    backslash = False
        if "\\x" in v:
            hexchars = ['0', '1', '2', '3', '4', '5', '6', '7',
                        '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
            hexbytes = v.split('\\x')
            newv = unicode(hexbytes[0])
            hexbytes = hexbytes[1:]
            for hx in hexbytes:
                hxb = ""
                if hx[0].lower() in hexchars:
                    hxb += hx[0].lower()
                    if hx[1].lower() in hexchars:
                        hxb += hx[1].lower()
                if len(hxb) != 2:
                    raise Exception("Invalid escape sequence")
                newv += unichr(int(hxb, 16))
                newv += unicode(hx[2:])
            v = newv
        for i in xrange(len(escapes)):
            v = v.replace("\\"+escapes[i], escapedchars[i])
        return (unicode(v[1:-1]), "str")
    elif v[0] == '[':
        return (load_array(v), "array")
    elif len(v) == 20 and v[-1] == 'Z':
        if v[10] == 'T':
            return (datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ"), "date")
        else:
            raise Exception("Wait, what?")
    else:
        itype = "int"
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        neg = False
        if v[0] == '-':
            neg = True
            v = v[1:]
        if '.' in v:
            if v.split('.', 1)[1] == '':
                raise Exception("This float is missing digits after the point")
            if v[0] not in digits:
                raise Exception("This float doesn't have a leading digit")
            v = float(v)
            itype = "float"
        else:
            v = int(v)
        if neg:
            return (0 - v, itype)
        return (v, itype)


def load_array(a):
    atype = None
    retval = []
    a = a.strip()
    if '[' not in a[1:-1]:
        a = a[1:-1].split(',')
    else:
        al = list(a[1:-1])
        a = []
        openarr = 0
        j = 0
        for i in xrange(len(al)):
            if al[i] == '[':
                openarr += 1
            elif al[i] == ']':
                openarr -= 1
            elif al[i] == ',' and not openarr:
                a.append(''.join(al[j:i]))
                j = i+1
        a.append(''.join(al[j:]))
    for i in xrange(len(a)):
        a[i] = a[i].strip()
        if a[i] != '':
            nval, ntype = load_value(a[i])
            if atype:
                if ntype != atype:
                    raise Exception("Not a homogeneous array")
            else:
                atype = ntype
            retval.append(nval)
    return retval

def dumps(o):
    """Returns a string containing the toml corresponding to o, a dictionary"""
    retval = ""
    addtoretval, sections = dump_sections(o)
    retval += addtoretval
    while sections != {}:
        newsections = {}
        for section in sections:
            addtoretval, addtosections = dump_sections(sections[section])
            if addtoretval:
                retval += "["+section+"]\n"
                retval += addtoretval
            for s in addtosections:
                newsections[section+"."+s] = addtosections[s]
        sections = newsections
    return retval

def dump_sections(o):
    retstr = ""
    retdict = {}
    for section in o:
        if not isinstance(o[section], dict):
            retstr += section + " = " + str(dump_value(o[section])) + '\n'
        else:
            retdict[section] = o[section]
    return (retstr, retdict)

def dump_value(v):
    if isinstance(v, list):
        t = []
        retval = "["
        for u in v:
            t.append(dump_value(u))
        while t != []:
            s = []
            for u in t:
                if isinstance(u, list):
                    for r in u:
                        s.append(r)
                else:
                    retval += " " + str(u) + ","
            t = s
        retval += "]"
        return retval
    if isinstance(v, (str, unicode)):
        escapes = ['\\', '0', 'n', 'r', 't', '"']
        escapedchars = ['\\', '\0', '\n', '\r', '\t', '\"']
        for i in xrange(len(escapes)):
            v = v.replace(escapedchars[i], "\\"+escapes[i])
        return str('"'+v+'"')
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, datetime.datetime):
        return v.isoformat()[:19]+'Z'
    return v
