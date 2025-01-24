function clean_sources(model_name)	
  set_param(model_name, 'SimCustomHeaderCode', "");
  set_param(model_name, 'SimUserSources', "");
  set_param(model_name, 'SimUserLibraries', "");
  set_param(model_name, 'SimCustomInitializer', "");
  set_param(model_name, 'SimCustomTerminator', "");
