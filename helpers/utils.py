from uuid import UUID


def checkField(required:[str],data:dict):
    not_present=[]
    for key in required:
        if key not in data.keys():
            not_present.append(key)
    return not_present

def checkValidUUID(uuid_string):
    try:
        if not isinstance(uuid_string, str):
            return False
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True