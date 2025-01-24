from protogen.matlab_helpers import (
    make_mat_structure,
    get_engine,
)

from protogen.proto_generation import (
    generate_proto,
)

from protogen.cpp_generation import (
    generate_bus_h,
    generate_bus_to_proto_h,
    generate_bus_to_proto_c,
    generate_proto_to_bus_h,
    generate_proto_to_bus_c,
)

import shutil
import sys
import os

def get_stem_name(path):
    return os.path.splitext(os.path.basename(path))[0]

def main():
    argc = len(sys.argv)
    if argc != 2:
        print("[generate_example_proto]: wrong num args")
        print(
            "Usage: bazel run //example:generate_example_proto -- /abs/path/to/bus.mat /abs/path/to/output_dir"
        )
        exit(1)

    path_to_bus_mat = os.path.normpath(sys.argv[1])
    print("path_to_bus_mat: {}".format(path_to_bus_mat))

    path_to_output_dir = os.path.normpath(sys.argv[2])
    print("path_to_output_dir: {}".format(path_to_output_dir))

    eng = get_engine()
    mat_structure = make_mat_structure(eng, path_to_bus_mat)

    assert len(mat_structure.keys()) > 0

    bus_name = get_stem_name(path_to_bus_mat)
    print("bus_name: {}".format(bus_name))

    proto = generate_proto(mat_structure)
    write(os.path.join(path_to_output_dir, f"{bus_name}.proto"), proto)

    bus_h = generate_bus_h(mat_structure)
    write(os.path.join(path_to_output_dir, f"{bus_name}.h"), bus_h)

    includes = [
        f"{bus_name}.pb.h",
    ]
    bus_to_proto_h = generate_bus_to_proto_h(mat_structure, includes)
    write(os.path.join(path_to_output_dir, f"{bus_name}-to-proto.h"), bus_to_proto_h)

    bus_to_proto_cpp = generate_bus_to_proto_c(
        mat_structure, f"{bus_name}-to-proto.h"
    )
    write(os.path.join(path_to_output_dir, f"{bus_name}-to-proto.cpp"), bus_to_proto_cpp)

    proto_to_bus_h = generate_proto_to_bus_h(
        mat_structure, f"{bus_name}.h", f"{bus_name}.pb.h"
    )
    write(os.path.join(path_to_output_dir, f"proto-to-{bus_name}.h"), proto_to_bus_h)

    proto_to_bus_cpp = generate_proto_to_bus_c(mat_structure, f"proto-to-{bus_name}.h")
    write(os.path.join(path_to_output_dir, f"proto-to-{bus_name}.cpp"), proto_to_bus_cpp)

    format(path_to_project_root)


def write(path, data):
    # delete file if exists
    if os.path.exists(path):
        os.remove(path)

    # write to file
    with open(path, "w") as f:
        f.write(data)


if __name__ == "__main__":
    main()
