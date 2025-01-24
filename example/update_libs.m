function out = update_libs(model_name, libs_list)
    if ~isempty(model_name) && ~isempty(libs_list)
        pre = get_param(model_name, 'SimUserLibraries');
        libs = join(libs_list, newline());
        update = join([pre, libs], newline());
        set_param(model_name, 'SimUserLibraries', update);
    end
