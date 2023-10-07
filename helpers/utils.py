def checkField(required:[str],data:dict):
    not_present=[]
    for key in required:
        if key not in data.keys():
            not_present.append(key)
    return not_present