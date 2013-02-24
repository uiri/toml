def parse(s):
    retval = {}
    currentlevel = retval
    if isinstance(s, str):
        s = s.split('\n')
    for line in s:
        line = line.strip()
        line = line.split("#")[0]
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
            currentlevel[pair[0]] = pair[1]
    return retval
