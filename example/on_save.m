addpath("../protogen/");
clearvars;
make_bus("run_example/To Mcap Bus");
save("example.mat");

% proto_gen_command = 'regenerate_proto_bindings.bat'
% gen_result = system(proto_gen_command)
% 
% if gen_result ~= 0
%   error('Failed to generate proto bindings. Command exited with code %d.', gen_result);
% end
