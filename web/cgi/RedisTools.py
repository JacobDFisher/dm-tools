def nameBuilder(start, *args):
    if type(start)==bytes:
        retStr = str(start, 'utf-8')
    else:
        retStr = str(start)
    for part in args:
        if type(part)==bytes:
            retStr+=':'+str(part, 'utf-8')
        else:
            retStr+=':'+str(part)
    return retStr
