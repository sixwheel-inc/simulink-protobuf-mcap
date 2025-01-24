
% For the given Bus Creator / Inport (`bus_path`), load the bus heirarchy
% as an object into the workspace, and return the name of the object.

function make_bus(bus_path)
  Simulink.Bus.createObject(gcs, bus_path);
  end
