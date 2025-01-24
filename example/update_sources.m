function update_sources(model_name, sources_list)
    if ~isempty(model_name) && ~isempty(sources_list)
        pre = get_param(model_name, 'SimUserSources');
        sources = join(sources_list, newline());
        update = join([pre, sources], newline());
        set_param(model_name, 'SimUserSources', update);
    end
