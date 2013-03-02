import datetime

def dumps(s):
    retval = {}
    currentlevel = retval
    if isinstance(s, str):
        sl = list(s)
        openarr = 0
        openstring = False
        delnum = 1
        for i in xrange(len(sl)):
            if sl[i] == '"':
                openstring = not openstring
            if sl[i] == '#' and not openstring:
                j = i
                while sl[j] != '\n':
                    sl.insert(j, ' ')
                    sl.pop(j+1)
                    j += 1
            if sl[i] == '[' and not openstring:
                openarr += 1
            if sl[i] == ']' and not openstring:
                openarr -= 1
            if sl[i] == '\n' and openarr:
                sl.insert(i, ' ')
                sl.pop(i+1)
        s = ''.join(sl)
        s = s.split('\n')
    else:
        raise Exception("What exactly are you trying to pull?")
    for line in s:
        line = line.strip()
        if line == "":
            continue
        if line[0] == '[':
            groups = line[1:-1].split('.')
            currentlevel = retval
            for i in xrange(len(groups)):
                group = groups[i]
                try:
                    currentlevel[group]
                    if i == len(groups) - 1:
                        raise Exception("What? "+group+" already exists?"+str(currentlevel))
                except KeyError:
                    currentlevel[group] = {}
                currentlevel = currentlevel[group]
        elif "=" in line:
            pair = line.split('=', 1)
            for i in xrange(len(pair)):
                pair[i] = pair[i].strip()
            value = dump_value(pair[1])
            currentlevel[pair[0]] = value
    return retval

def dump_value(v):
    if v == 'true':
        return True
    elif v == 'false':
        return False
    elif v[0] == '"':
        escapes = ['0', 'n', 'r', 't', '"', '\\']
        escapedchars = ['\0', '\n', '\r', '\t', '\"', '\\']
        for i in xrange(len(escapes)):
            v = v.replace("\\"+escapes[i], escapedchars[i])
        return unicode(v[1:-1])
    elif v[0] == '[':
        return dump_array(v)
    elif len(v) == 20 and v[-1] == 'Z':
        if v[10] == 'T':
            return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
        else:
            raise Exception("Wait, what?")
    else:
        try:
            int(v)
            return int(v)
        except ValueError:
            return float(v)


def dump_array(a):
    retval = []
    if '[' not in a[1:-1]:
        a = a[1:-1].split(',')
    else:
        al = list(a[1:-1])
        a = []
        openarr = 0
        j = 1
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
            retval.append(dump_value(a[i]))
    return retval

def loads(o):
    retval = ""
    addtoretval, sections = load_sections(o)
    retval += addtoretval
    while sections != {}:
        newsections = {}
        for section in sections:
            addtoretval, addtosections = load_sections(sections[section])
            if addtoretval:
                retval += "["+section+"]\n"
                retval += addtoretval
            for s in addtosections:
                newsections[section+"."+s] = addtosections[s]
        sections = newsections
    return retval

def load_sections(o):
    retstr = ""
    retdict = {}
    for section in o:
        if not isinstance(o[section], dict):
            retstr += section + " = " + str(load_value(o[section])) + '\n'
        else:
            retdict[section] = o[section]
    return (retstr, retdict)

def load_value(v):
    if isinstance(v, list):
        t = []
        retval = "["
        for u in v:
            t.append(load_value(u))
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
