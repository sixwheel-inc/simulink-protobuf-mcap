NOT_ALLOWED_U = set({"uint8", "uint16"})
NOT_ALLOWED_I = set({"int8", "int16"})
NOT_ALLOWED_OTHER = set({"string"})


def order_busses_by_dependency(mat_structure, root_bus="DenseLog"):
    """assumes there are no cycles in the bus structure, will ignore cycles if they exist"""

    assert root_bus in mat_structure.keys()

    all_busses = set(mat_structure.keys())

    ordered_busses = [root_bus]
    index = 0
    while index < len(ordered_busses):
        current = ordered_busses[index]
        children = mat_structure[current].values()
        unvisited_children = sorted(
            set([x for x in children if x in all_busses and x not in ordered_busses])
        )
        ordered_busses.extend(unvisited_children)
        assert len(ordered_busses) == len(set(ordered_busses))  # ensure no duplicates
        index += 1

    ordered_busses.reverse()

    # assert len(ordered_busses) == len(mat_structure.keys())  # ensure all busses
    ordered_busses_dict = {}
    for bus in ordered_busses:
        ordered_busses_dict[bus] = mat_structure[bus]

    return ordered_busses, ordered_busses_dict
