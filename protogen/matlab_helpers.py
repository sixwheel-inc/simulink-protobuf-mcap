import matlab.engine


import os
import shutil


def make_mat_structure(eng, dense_log_mat="dense_log.mat"):

    eng.workspace["top_bus_def"] = eng.load(dense_log_mat, nargout=1)
    busses = {}

    # NOTE: createMATLABStruct was turining uint32 into int64, so we cannot use it
    # instead, we use the BusElements to get the actual types
    for bus_def in eng.workspace["top_bus_def"]:

        if bus_def.startswith("Bus_"):
            print(f"bus_def: {bus_def} starts with Bus_, skip")
            # ignore bus that we generate via c-struct
            continue

        if bus_def in ["EncodedBytes"]:
            print(f"bus_def: {bus_def} is EncodedBytes, skip")
            # ignore this, not part of the root
            continue

        num_elements = int(
            eng.eval(
                "length(top_bus_def.{bus_def}.Elements)".format(bus_def=bus_def),
                nargout=1,
            )
        )

        print(f"bus_def: {bus_def} {num_elements}")

        bus = {}
        for i in range(1, num_elements + 1):

            name = eng.eval(
                "top_bus_def.{bus_def}.Elements({i}).Name;".format(
                    bus_def=bus_def, i=i
                ),
                nargout=1,
            )

            type_ = eng.eval(
                "top_bus_def.{bus_def}.Elements({i}).DataType;".format(
                    bus_def=bus_def, i=i
                ),
                nargout=1,
            )

            type_ = type_.replace("Bus: ", "")
            bus[name] = type_
            print(f"  {bus_def}[{i}] -> {name} : {type_}")
        busses[bus_def] = bus

    return busses


def find_and_rename_root_bus(mat_structure, root_name="DenseLog"):
    """We don't want extra bus definitions that aren't used by any other bus"""
    all_depended_on = set()
    for bus_name, bus in mat_structure.items():
        for name, type_ in bus.items():
            if type_ in mat_structure:
                all_depended_on.add(type_)

    roots = set(mat_structure.keys()) - all_depended_on

    assert len(roots) == 1
    root = roots.pop()
    mat_structure[root_name] = mat_structure.pop(root)

    assert root_name not in all_depended_on
    assert root_name in mat_structure.keys()
    return root_name


def get_engine():
    engines = matlab.engine.find_matlab()
    if len(engines) == 0 or engines[0] == "":
        print("start new matlab engine instance")
        eng = matlab.engine.start_matlab()
    else:
        print(f"join existing matlab engine {engines[0]}")
        eng = matlab.engine.connect_matlab(engines[0])
    return eng
