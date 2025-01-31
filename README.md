# Simulink Protobuf Mcap

## TODO Make this a Simulink Toolbox

In order for this to work as a toolbox, we need to get rid of some dependencies.

- [ ] replace python w/ matlab
  - python has nice string / template formatting, we will need to make our own in matlab
- [ ] drop bazel / bazelisk
  - using it to run python, won't be needed

## Dependencies needed to run the Example

### bazel (TODO: remove this dependency)

Currently using this as a reliable way to get the Mcap library source code.

TODO: should probably replace this w/ curl or something simpler.

### cmake/vcpkg

Typically we use bazel, but we found this to be the easier way to make DLLs that Simulink can link to and run without crashing.

## Running the Example
