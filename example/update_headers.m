function out = update_headers(model_name, headers_list)
    if ~isempty(model_name) && ~isempty(headers_list)
        out = get_param(model_name, 'SimCustomHeaderCode');
        for header = headers_list
            s = sprintf('#include "%s"\n', header);
            out = join([out, s], newline());
        end
        set_param(model_name, 'SimCustomHeaderCode', out);
    end
