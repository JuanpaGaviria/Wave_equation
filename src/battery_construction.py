def battery_structure(indexes, fold_number):

    layer_number = 2 * int(len(indexes)) * fold_number
    _layers_number = int(layer_number / 2)
    interface_number = layer_number - 1
    if fold_number == 0:
        layer_number = int(len(indexes))
        interface_number = 1
    battery_structure_map = []
    count = 0
    _count = 0
    for i in range(layer_number):
        battery_structure_map.append(indexes[count])
        count = count+1
        _count = _count+1
        if count == len(indexes):
            count = 0
        if _count == (layer_number / 2):
            count = len(indexes)-1
            for j in range(_layers_number):
                battery_structure_map.append(indexes[count])
                count = count-1
                if count < 0:
                    count = len(indexes)-1
            break
    return battery_structure_map
