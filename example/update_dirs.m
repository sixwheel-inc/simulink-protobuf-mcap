function update_Dirs(model_name, dirs_list)
    if ~isempty(model_name) && ~isempty(dirs_list)
        pre = get_param(model_name, 'SimUserIncludeDirs');
        dirs = join(dirs_list, newline());
        update = join([pre, dirs], newline());
        set_param(model_name, 'SimUserIncludeDirs', update);
    end
