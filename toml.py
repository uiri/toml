import datetime

def parse(s):
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
                while sl[j-1] != '\n':
                    sl.insert(j, ' ')
                    sl.pop(j-1)
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
            pair = line.split('=')
            for i in xrange(len(pair)):
                pair[i] = pair[i].strip()
            if pair[1] == 'true':
                value = True
            elif pair[1] == 'false':
                value = False
            elif pair[1][0] == '"' or pair[1][0] == '[':
                # arrays are kind of scaring me right now...
                value = pair[1]
            elif len(pair[1]) == 20 and pair[1][-1] == 'Z':
                if pair[1][10] == 'T':
                    value = datetime.datetime.strptime(pair[1], "%Y-%m-%dT%H:%M:%SZ")
            else:
                value = int(pair[1])
            currentlevel[pair[0]] = value
    return retval
