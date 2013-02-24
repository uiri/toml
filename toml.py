import datetime

def parse(s):
    retval = {}
    currentlevel = retval
    if isinstance(s, str):
        s = s.split('\n')
    for line in s:
        line = line.strip()
        if '#' in line:
            if '"' not in line:
                line = line.split("#")[0]
            else:
                quoted = line.split('"')
                for i in xrange(len(quoted)):
                    if i%2 == 0:
                        if '#' in quoted[i]:
                            quoted[i] = quoted[i].split("#")[0]
                            quoted = quoted[:i]
                            quoted.append('')
                line = '"'.join(quoted)
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
