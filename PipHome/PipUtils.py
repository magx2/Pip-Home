def copy_all_config_to_kw(config, kw, prefix):
    items = config[prefix]
    for item in items:
        if item not in kw.keys():
            kw[item] = items[item]
