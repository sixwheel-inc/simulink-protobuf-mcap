from dense_log_codegen.order_busses import (
    order_busses_by_dependency,
    NOT_ALLOWED_U,
    NOT_ALLOWED_I,
    NOT_ALLOWED_OTHER,
)

BUS_FIELD = "  {type} {name};\n"
BUS_MESSAGE_FIELD = "  Bus_{type} {name};\n"
BUS_STRUCT = """
typedef struct _Bus_{bus_name} {{
{fields}
}} Bus_{bus_name};
"""
BUS_HEADER = """
// AUTOGENERATED FILE, DO NOT EDIT //
#ifndef _BUS_H_
#define _BUS_H_

#include <stdint.h>
#include <stdbool.h>

{messages}

#endif
"""


def generate_bus_h(mat_structure):
    ordered_busses, _ = order_busses_by_dependency(mat_structure)

    messages = []
    for bus_name in ordered_busses:
        bus = mat_structure[bus_name]
        fields = []
        for i, (name, type_) in enumerate(bus.items()):
            if type_ == "boolean":
                type_ = "bool"
            elif type_ == "single":
                type_ = "float"
            elif type_ in set(
                [
                    "uint8",
                    "uint16",
                    "uint32",
                    "uint64",
                    "int8",
                    "int16",
                    "int32",
                    "int64",
                ]
            ):
                type_ = type_ + "_t"
            elif type_ in NOT_ALLOWED_OTHER:
                raise NotImplementedError("ERROR: {} is not supported!".format(type_))

            if type_ in mat_structure:
                fields.append(BUS_MESSAGE_FIELD.format(name=name, type=type_))
            else:
                fields.append(BUS_FIELD.format(name=name, type=type_))
        messages.append(BUS_STRUCT.format(bus_name=bus_name, fields="".join(fields)))
    return BUS_HEADER.format(messages="".join(messages))


def get_cap_indices(s):
    return [i for i, c in enumerate(s) if c.isupper()]


def get_proto_field_name(name):
    start_index = 0
    proto_field_name = ""
    for cap_index in get_cap_indices(name):
        if cap_index == 0:
            continue
        if name[cap_index - 1] != "_" and (
            (cap_index != len(name) - 1 and name[cap_index + 1].islower())
            or name[cap_index - 1].islower()
            or name[cap_index - 1].isdigit()
        ):
            proto_field_name += name[start_index:cap_index] + "_"
            start_index = cap_index

    proto_field_name += name[start_index:]
    proto_field_name = proto_field_name.lower()
    return proto_field_name


BUS_TO_PROTO_DEF = """
void bus_to_proto_{bus_name}(const Bus_{bus_name} *bus, struct {bus_name_proto} *proto);
"""
BUS_TO_PROTO_H = """
// AUTOGENERATED FILE, DO NOT EDIT //
#ifndef _BUS_TO_PROTO_H_
#define _BUS_TO_PROTO_H_
#include <stdint.h>
#include <stdbool.h>
#include "{pb_h}"
#include "{bus_h}"

{defs}
#endif
"""


def generate_bus_to_proto_h(mat_structure, pb_h, bus_h):
    defs = []
    for bus_name, bus in mat_structure.items():
        bus_name_proto = get_proto_field_name(bus_name) + "_t"
        defs.append(
            BUS_TO_PROTO_DEF.format(bus_name=bus_name, bus_name_proto=bus_name_proto)
        )

    return BUS_TO_PROTO_H.format(pb_h=pb_h, bus_h=bus_h, defs="".join(defs))


PROTO_TO_BUS_FUNCTION_DEF = """
void proto_to_bus_{proto_name}(const struct {proto_type} *proto, Bus_{bus_name} *bus);
"""
PROTO_TO_BUS_H = """
// AUTOGENERATED FILE, DO NOT EDIT //
#ifndef _proto_to_bus_H_
#define _proto_to_bus_H_
#include <stdint.h>
#include <stdbool.h>
#include "{pb_h}"
#include "{bus_h}"

{functions}
#endif
"""


def generate_proto_to_bus_h(mat_structure, pb_h, bus_h):
    _, ordered_busses = order_busses_by_dependency(mat_structure)
    functions = []
    for bus_name, bus in ordered_busses.items():
        spaced_name = get_proto_field_name(bus_name)
        for i, (name, type_) in enumerate(bus.items()):
            if type_ == "boolean":
                type_ = "bool"
            elif type_ == "single":
                type_ = "float"
            elif type_ in NOT_ALLOWED_OTHER:
                raise NotImplementedError("ERROR: {} is not supported!".format(type_))
            elif type_ in set(
                [
                    "uint8",
                    "uint16",
                    "uint32",
                    "uint64",
                    "int8",
                    "int16",
                    "int32",
                    "int64",
                ]
            ):
                type_ = type_ + "_t"

        functions.append(
            PROTO_TO_BUS_FUNCTION_DEF.format(
                proto_name=spaced_name, proto_type=spaced_name + "_t", bus_name=bus_name
            )
        )

    return PROTO_TO_BUS_H.format(pb_h=pb_h, bus_h=bus_h, functions="".join(functions))


PROTO_TO_BUS_ANY = "  bus->{name} = proto->{proto_name};\n"
PROTO_TO_BUS_CONVERT = (
    "  proto_to_bus_{proto_fn_name}(proto->{proto_name}, &bus->{name});\n"
)
PROTO_TO_BUS_IMPL = """
void proto_to_bus_{proto_name}(const struct {proto_type} *proto, Bus_{bus_name} *bus) {{
{fields}
}}
"""
PROTO_TO_BUS_C = """
// AUTOGENERATED FILE, DO NOT EDIT //
#include "{proto_to_bus_h}"

{impls}
"""


def generate_proto_to_bus_c(mat_structure, proto_to_bus_h):
    impls = []
    for bus_name, bus in mat_structure.items():
        fields = []
        spaced_name = get_proto_field_name(bus_name)
        for i, (name, type_) in enumerate(bus.items()):
            spaced_proto_name = get_proto_field_name(name)
            spaced_type_name = get_proto_field_name(type_)
            if type_ in mat_structure:
                fields.append(
                    PROTO_TO_BUS_CONVERT.format(
                        proto_fn_name=spaced_type_name,
                        name=name,
                        proto_name=spaced_proto_name + "_p",
                    )
                )
            else:
                fields.append(
                    PROTO_TO_BUS_ANY.format(name=name, proto_name=spaced_proto_name)
                )
        impls.append(
            PROTO_TO_BUS_IMPL.format(
                proto_name=spaced_name,
                proto_type=spaced_name + "_t",
                bus_name=bus_name,
                fields="".join(fields),
            )
        )
    return PROTO_TO_BUS_C.format(proto_to_bus_h=proto_to_bus_h, impls="".join(impls))


BUS_TO_PROTO_MESSAGE = (
    "  {bus_name}_{proto_field_type}_alloc(proto);\n"
    + "  bus_to_proto_{type}(&bus->{name}, proto->{proto_field_name});\n"
)
BUS_TO_PROTO_UINT = "  proto->{proto_field_name} = (uint32_t)bus->{name};\n"
BUS_TO_PROTO_INT = "  proto->{proto_field_name} = (int32_t)bus->{name};\n"
BUS_TO_PROTO_ANY = "  proto->{proto_field_name} = bus->{name};\n"
BUS_TO_PROTO_IMPL = """
void bus_to_proto_{bus_name}(const Bus_{bus_name} *bus, struct {bus_name_proto} *proto) {{
{fields}
}}
"""
BUS_TO_PROTO_C = """
// AUTOGENERATED FILE, DO NOT EDIT //
#include "{busses_to_proto_h}"

{impls}
"""


def generate_bus_to_proto_c(mat_structure, busses_to_proto_h):
    impls = []
    for bus_name, bus in mat_structure.items():
        fields = []
        spaced_name = get_proto_field_name(bus_name)
        for i, (name, type_) in enumerate(bus.items()):
            proto_field_name = get_proto_field_name(name)
            if type_ in NOT_ALLOWED_U:
                fields.append(
                    BUS_TO_PROTO_UINT.format(
                        proto_field_name=proto_field_name, name=name
                    )
                )
            elif type_ in NOT_ALLOWED_I:
                fields.append(
                    BUS_TO_PROTO_INT.format(
                        proto_field_name=proto_field_name, name=name
                    )
                )
            elif type_ in NOT_ALLOWED_OTHER:
                raise NotImplementedError("ERROR: {} is not supported!".format(type_))
            elif type_ in mat_structure:
                fields.append(
                    BUS_TO_PROTO_MESSAGE.format(
                        bus_name=spaced_name,
                        proto_field_type=proto_field_name,
                        proto_field_name=proto_field_name + "_p",
                        type=type_,
                        name=name,
                    )
                )
            else:
                fields.append(
                    BUS_TO_PROTO_ANY.format(
                        proto_field_name=proto_field_name, name=name
                    )
                )
        bus_name_proto = spaced_name + "_t"
        impls.append(
            BUS_TO_PROTO_IMPL.format(
                bus_name=bus_name, bus_name_proto=bus_name_proto, fields="".join(fields)
            )
        )
    return BUS_TO_PROTO_C.format(
        busses_to_proto_h=busses_to_proto_h, impls="".join(impls)
    )
