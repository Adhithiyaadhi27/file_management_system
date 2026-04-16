persons = []  # (id, name)

def add_person(pid, name):
    persons.append((pid, name))


def update_person(pid, new_name):
    for i, (id_, _) in enumerate(persons):
        if id_ == pid:
            persons[i] = (pid, new_name)
            break

def delete_person_list(pid):
    for i, (id_, _) in enumerate(persons):
        if id_ == pid:
            persons.pop(i)
            break