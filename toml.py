import datetime, decimal, re

try:
    _range = xrange
except NameError:
    unicode = str
    _range = range
    basestring = str
    unichr = chr

def load(f):
    """Returns a dictionary containing the named file parsed as toml."""
    if isinstance(f, basestring):
        with open(f) as ffile:
            return loads(ffile.read())
    elif isinstance(f, list):
        for l in f:
            if not isinstance(l, basestring):
                raise Exception("Load expects a list to contain filenames only")
        d = []
        for l in f:
            d.append(load(l))
        r = {}
        for l in d:
            toml_merge_dict(r, l)
        return r
    elif f.read:
        return loads(f.read())
    else:
        raise Exception("You can only load a file descriptor, filename or list")

def loads(s, _dict=dict):
    """Returns a dictionary containing s, a string, parsed as toml."""
    implicitgroups = []
    retval = _dict()
    currentlevel = retval
    if isinstance(s, basestring):
        try:
            s.decode('utf8')
        except AttributeError:
            pass
        sl = list(s)
        openarr = 0
        openstring = False
        openstrchar = ""
        multilinestr = False
        arrayoftables = False
        beginline = True
        keygroup = False
        keyname = False
        delnum = 1
        for i in range(len(sl)):
            if keyname and not openstring:
                if sl[i] == '\n':
                    raise Exception("Key name found without value. Reached end of line.")
                if sl[i] == '#':
                    raise Exception("Found invalid character in key name: '#'")
                if sl[i] == '=':
                    keyname = False
                else:
                    continue
            if sl[i] == "'" and openstrchar != '"':
                k = 1
                try:
                    while sl[i-k] == "'":
                        k += 1
                        if k == 3:
                            break
                except IndexError:
                    pass
                if k == 3:
                    multilinestr = not multilinestr
                    openstring = multilinestr
                else:
                    openstring = not openstring
                if openstring:
                    openstrchar = "'"
                else:
                    openstrchar = ""
            if sl[i] == '"' and openstrchar != "'":
                oddbackslash = False
                k = 1
                tripquote = False
                try:
                    while sl[i-k] == '"':
                        k += 1
                        if k == 3:
                            tripquote = True
                            break
                    while sl[i-k] == '\\':
                        oddbackslash = not oddbackslash
                        k += 1
                except IndexError:
                    pass
                if not oddbackslash:
                    if tripquote:
                        multilinestr = not multilinestr
                        openstring = multilinestr
                    else:
                        openstring = not openstring
                if openstring:
                    openstrchar = '"'
                else:
                    openstrchar = ""
            if sl[i] == '#' and not openstring and not keygroup and \
                    not arrayoftables:
                j = i
                try:
                    while sl[j] != '\n':
                        sl.insert(j, ' ')
                        sl.pop(j+1)
                        j += 1
                except IndexError:
                    break
            if sl[i] == '[' and not openstring and not keygroup and \
                    not arrayoftables:
                if beginline:
                    if sl[i+1] == '[':
                        arrayoftables = True
                    else:
                        keygroup = True
                else:
                    openarr += 1
            if sl[i] == ']' and not openstring:
                if keygroup:
                    keygroup = False
                elif arrayoftables:
                    if sl[i-1] == ']':
                        arrayoftables = False
                else:
                    openarr -= 1
            if sl[i] == '\n':
                if openstring or multilinestr:
                    if not multilinestr:
                        raise Exception("Unbalanced quotes")
                    if sl[i-1] == "'" or sl[i-1] == '"':
                        sl.insert(i, sl[i-1])
                        sl.pop(i+1)
                        sl[i-3] = ' '
                elif openarr:
                    sl.insert(i, ' ')
                    sl.pop(i+1)
                else:
                    beginline = True
            elif beginline and sl[i] != ' ' and sl[i] != '\t':
                beginline = False
                if not keygroup and not arrayoftables:
                    if sl[i] == '=':
                        raise Exception("Found empty keyname. ")
                    keyname = True
        s = ''.join(sl)
        s = s.split('\n')
    else:
        raise Exception("What exactly are you trying to pull?")
    multikey = None
    multilinestr = ""
    multibackslash = False
    for line in s:
        line = line.strip()
        if multikey:
            if multibackslash:
                strippedline = line.lstrip(' \t\n')
                if strippedline == '':
                    continue
                multilinestr += strippedline
            else:
                multilinestr += line
            multibackslash = False
            if len(line) > 2 and line[-1] == multilinestr[0] and \
                    line[-2] == multilinestr[0] and line[-3] == multilinestr[0]:
                value, vtype = load_value(multilinestr)
                currentlevel[multikey] = value
                multikey = None
                multilinestr = ""
            else:
                k = len(multilinestr) -1
                while k > -1 and multilinestr[k] == '\\':
                    multibackslash = not multibackslash
                    k -= 1
                if multibackslash:
                    multilinestr = multilinestr[:-1]
                else:
                    multilinestr += "\n"
            continue
        if line == "":
            continue
        if line[0] == '[':
            arrayoftables = False
            if line[1] == '[':
                arrayoftables = True
                line = line[2:].split(']]', 1)
            else:
                line = line[1:].split(']', 1)
            if line[1].strip() != "":
                raise Exception("Key group not on a line by itself.")
            line = line[0]
            if '[' in line:
                raise Exception("Key group name cannot contain '['")
            if ']' in line:
                raise Exception("Key group name cannot contain']'")
            groups = line.split('.')
            currentlevel = retval
            for i in range(len(groups)):
                group = groups[i]
                if group == "":
                    raise Exception("Can't have a keygroup with an empty name")
                try:
                    currentlevel[group]
                    if i == len(groups) - 1:
                        if group in implicitgroups:
                            implicitgroups.remove(group)
                            if arrayoftables:
                                raise Exception("An implicitly defined table can't be an array")
                        elif arrayoftables:
                            currentlevel[group].append({})
                        else:
                            raise Exception("What? "+group+" already exists?"+str(currentlevel))
                except TypeError:
                    if i != len(groups) - 1:
                        implicitgroups.append(group)
                    currentlevel = currentlevel[-1]
                    try:
                        currentlevel[group]
                    except KeyError:
                        currentlevel[group] = {}
                        if i == len(groups) - 1 and arrayoftables:
                            currentlevel[group] = [{}]
                except KeyError:
                    if i != len(groups) - 1:
                        implicitgroups.append(group)
                    currentlevel[group] = {}
                    if i == len(groups) - 1 and arrayoftables:
                        currentlevel[group] = [{}]
                currentlevel = currentlevel[group]
                if arrayoftables:
                    try:
                        currentlevel = currentlevel[-1]
                    except KeyError:
                        pass
        elif "=" in line:
            i = 1
            pair = line.split('=', i)
            l = len(line)
            while pair[-1][0] != ' ' and pair[-1][0] != '\t' and \
                    pair[-1][0] != "'" and pair[-1][0] != '"' and \
                    pair[-1][0] != '[' and pair[-1] != 'true' and \
                    pair[-1] != 'false':
                try:
                    float(pair[-1])
                    break
                except ValueError:
                    try:
                        datetime.datetime.strptime(pair[-1], "%Y-%m-%dT%H:%M:%SZ")
                        break
                    except ValueError:
                        raise Exception("What's the datatype of '"+pair[-1]+"'?")
            newpair = []
            newpair.append('='.join(pair[:-1]))
            newpair.append(pair[-1])
            pair = newpair
            pair[0] = pair[0].strip()
            pair[1] = pair[1].strip()
            if len(pair[1]) > 2 and (pair[1][0] == '"' or pair[1][0] == "'") \
                    and pair[1][1] == pair[1][0] and pair[1][2] == pair[1][0] \
                    and not (len(pair[1]) > 5 and pair[1][-1] == pair[1][0] \
                                 and pair[1][-2] == pair[1][0] and \
                                 pair[1][-3] == pair[1][0]):
                k = len(pair[1]) -1
                while k > -1 and pair[1][k] == '\\':
                    multibackslash = not multibackslash
                    k -= 1
                if multibackslash:
                    multilinestr = pair[1][:-1]
                else:
                    multilinestr = pair[1] + "\n"
                multikey = pair[0]
            else:
                value, vtype = load_value(pair[1])
            try:
                currentlevel[pair[0]]
                raise Exception("Duplicate keys!")
            except KeyError:
                if multikey:
                    continue
                else:
                    currentlevel[pair[0]] = value
    return retval

def load_unicode_escapes(v, hexbytes, prefix):
    hexchars = ['0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    skip = False
    i = len(v) - 1
    while i > -1 and v[i] == '\\':
        skip = not skip
        i -= 1
    for hx in hexbytes:
        if skip:
            skip = False
            i = len(hx) - 1
            while i > -1 and hx[i] == '\\':
                skip = not skip
                i -= 1
            v += prefix
            v += hx
            continue
        hxb = ""
        try:
            if hx[0].lower() in hexchars:
                hxb += hx[0].lower()
                if hx[1].lower() in hexchars:
                    hxb += hx[1].lower()
                if hx[2].lower() in hexchars:
                    hxb += hx[2].lower()
                    if hx[3].lower() in hexchars:
                        hxb += hx[3].lower()
        except IndexError:
            if len(hxb) != 2:
                raise Exception("Invalid escape sequence")
        if len(hxb) != 4 and len(hxb) != 2:
            raise Exception("Invalid escape sequence")
        v += unichr(int(hxb, 16))
        v += unicode(hx[len(hxb):])
    return v

def load_value(v):
    if v == 'true':
        return (True, "bool")
    elif v == 'false':
        return (False, "bool")
    elif v[0] == '"':
        testv = v[1:].split('"')
        if testv[0] == '' and testv[1] == '':
            testv = testv[2:-2]
        closed = False
        for tv in testv:
            if tv == '':
                closed = True
            else:
                oddbackslash = False
                try:
                    i = -1
                    j = tv[i]
                    while j == '\\':
                        oddbackslash = not oddbackslash
                        i -= 1
                        j = tv[i]
                except IndexError:
                    pass
                if not oddbackslash:
                    if closed:
                        raise Exception("Stuff after closed string. WTF?")
                    else:
                        closed = True
        escapes = ['0', 'b', 'f', '/', 'n', 'r', 't', '"', '\\']
        escapedchars = ['\0', '\b', '\f', '/', '\n', '\r', '\t', '\"', '\\']
        escapeseqs = v.split('\\')[1:]
        backslash = False
        for i in escapeseqs:
            if i == '':
                backslash = not backslash
            else:
                if i[0] not in escapes and i[0] != 'u' and i != 'U' and \
                        not backslash:
                    raise Exception("Reserved escape sequence used")
                if backslash:
                    backslash = False
        for prefix in ["\\u", "\\U"]:
            if prefix in v:
                hexbytes = v.split(prefix)
                v = load_unicode_escapes(hexbytes[0], hexbytes[1:], prefix)
        for i in range(len(escapes)):
            if escapes[i] == '\\':
                v = v.replace("\\"+escapes[i], escapedchars[i])
            else:
                v = re.sub("([^\\\\](\\\\\\\\)*)\\\\"+escapes[i], "\\1"+escapedchars[i], v)
        if v[1] == '"':
            v = v[2:-2]
        return (v[1:-1], "str")
    elif v[0] == "'":
        if v[1] == "'":
            v = v[2:-2]
        return (v[1:-1], "str")
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
        strarray = False
        tmpa = a[1:-1].strip()
        if tmpa != '' and tmpa[0] == '"':
            strarray = True
        a = a[1:-1].split(',')
        b = 0
        if strarray:
            while b < len(a) - 1:
                while a[b].strip()[-1] != '"' and a[b+1].strip()[0] != '"':
                    a[b] = a[b] + ',' + a[b+1]
                    if b < len(a) - 2:
                        a = a[:b+1] + a[b+2:]
                    else:
                        a = a[:b+1]
                b += 1
    else:
        al = list(a[1:-1])
        a = []
        openarr = 0
        j = 0
        for i in range(len(al)):
            if al[i] == '[':
                openarr += 1
            elif al[i] == ']':
                openarr -= 1
            elif al[i] == ',' and not openarr:
                a.append(''.join(al[j:i]))
                j = i+1
        a.append(''.join(al[j:]))
    for i in range(len(a)):
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

def dump(o, f):
    """Writes out to f the toml corresponding to o. Returns said toml."""
    if f.write:
        d = dumps(o)
        f.write(d)
        return d
    else:
        raise Exception("You can only dump an object to a file descriptor")

def dumps(o):
    """Returns a string containing the toml corresponding to o, a dictionary"""
    retval = ""
    addtoretval, sections = dump_sections(o, "")
    retval += addtoretval
    while sections != {}:
        newsections = {}
        for section in sections:
            addtoretval, addtosections = dump_sections(sections[section], section)
            if addtoretval:
                retval += "["+section+"]\n"
                retval += addtoretval
            for s in addtosections:
                newsections[section+"."+s] = addtosections[s]
        sections = newsections
    return retval

def dump_sections(o, sup):
    retstr = ""
    if sup != "" and sup[-1] != ".":
        sup += '.'
    retdict = {}
    arraystr = ""
    for section in o:
        if not isinstance(o[section], dict):
            arrayoftables = False
            if isinstance(o[section], list):
                for a in o[section]:
                    if isinstance(a, dict):
                        arrayoftables = True
            if arrayoftables:
                for a in o[section]:
                    arraytabstr = ""
                    arraystr += "[["+sup+section+"]]\n"
                    s, d = dump_sections(a, sup+section)
                    if s:
                        if s[0] == "[":
                            arraytabstr += s
                        else:
                            arraystr += s
                    while d != {}:
                        newd = {}
                        for dsec in d:
                            s1, d1 = dump_sections(d[dsec], sup+section+"."+dsec)
                            if s1:
                                arraytabstr += "["+sup+section+"."+dsec+"]\n"
                                arraytabstr += s1
                            for s1 in d1:
                                newd[dsec+"."+s1] = d1[s1]
                        d = newd
                    arraystr += arraytabstr
            else:
                if o[section] is not None:
                    retstr += (section + " = " +
                               str(dump_value(o[section])) + '\n')
        else:
            retdict[section] = o[section]
    retstr += arraystr
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
        v = "%r" % v
        if v[0] == 'u':
            v = v[1:]
        singlequote = v[0] == "'"
        v = v[1:-1]
        if singlequote:
            v = v.replace("\\'", "'")
            v = v.replace('"', '\\"')
        v = v.replace("\\x", "\\u00")
        return str('"'+v+'"')
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, datetime.datetime):
        return v.isoformat()[:19]+'Z'
    if isinstance(v, float):
        return '{0:f}'.format(decimal.Decimal(str(v)))
    return v

def toml_merge_dict(a, b):
    for k in a:
        if isinstance(a[k], dict):
            try:
                b[k]
            except KeyError:
                continue
            if isinstance(b[k], dict):
                b[k] = toml_merge_dict(a[k], b[k])
            else:
                raise Exception("Can't merge dict and nondict in toml object")
    a.update(b)
    return a
