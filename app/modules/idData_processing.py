from .database_functions import read_voters

def verify_voter_registration(eid_data):
    voters = read_voters()
    for voter in voters:
        if all(voter[k] == eid_data.get(k, None) for k in eid_data.keys()):
            return True
    return False