# Simulink Protobuf Mcap

Automatically generate .proto, and .cpp/.h code to read / write a Simulink Bus to disk as an Mcap.

### why?

Suppose you use Simulink ERT (or similar) to deploy your simulink models to some platform or testbed: this replaces all your tedious boilerplate w/ automatically generated and updating code that you don't need to maintain, there's no way for errors to manifest in the middleware.

### Example

#### Lets say your model looks like this:

![exampl-model](https://github.com/user-attachments/assets/a84d3bcd-9757-4c9f-9555-c6ef85fcf1db)

#### You could then deploy your model using something like the following model, and a build toolchain like Simulink ERT, or other.

![run-example](https://github.com/user-attachments/assets/1d8c0d2c-7bae-4bf8-abe5-308e283a13b2)

#### Then once you collect the .mcap files from your deployment, you can view them in Foxglove or Replay them into your model like below

![replay-example](https://github.com/user-attachments/assets/c8728e1f-3f2d-4d05-b369-2aa73d767141)

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
