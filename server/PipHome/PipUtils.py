def copy_all_config_to_kw(config, kw, prefix):
    items = config[prefix]
    for item in items:
        if item not in kw.keys():
            kw[item] = items[item]


# https://stackoverflow.com/a/49361727
def format_bytes(size):
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: "", 1: "Kb", 2: "Mb", 3: "Gb", 4: "Tb"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + power_labels[n]
