
function setup_example_bindings(model_name)

  fprintf("setting up example bindings in: %s\n", model_name);
    
	% copy external header and .dll into extenal-libs folder
	system("import-example.bat");

	% update .dll searchpath with example folder
	setenv("PATH", fullfile(pwd, "example") + ";" + getenv("PATH"));
	display(getenv("PATH"));
	addpath('example');

	% load SimOut struct definiton into simulink workspace
	Simulink.importExternalCTypes('example/example.h','Names',{'Bus_Example', 'ExampleReplayStatus'});
	
	% update model configs with header and .dll 
  update_headers(model_name, "example.h");
  set_param(model_name, 'SimUserLibraries', 'example.dll');

  % update model configs with init / exit code
  set_param(model_name, 'SimCustomInitializer', 'StartExampleReplay("example.mcap");');
  set_param(model_name, 'SimCustomTerminator', 'EndExampleReplay();');
