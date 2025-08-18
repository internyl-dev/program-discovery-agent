
def denest_dict(d:dict):
    denested_dict = {}

    def _addindex(d:dict, index:int):
        i=0

        while i < len(d):
            i+=1
            key = list(d.keys())[0]
            d[f"{key}{index}"] = d[key]
            del d[key]

    def _decouple(l:list):
        index=-1

        for i in l:
            index+=1
            if isinstance(i, dict):
                _addindex(i, index)
                _denest(i)
            
            elif isinstance(i, (list, tuple)):
                _decouple(i)
            
            else:
                continue

    def _denest(d:dict):
        for key in d:
            if isinstance(d[key], dict):
                _denest(d[key])

            elif isinstance(d[key], (list, tuple)):
                _decouple(d[key])

            else:
                denested_dict[key] = d[key]
    
    _denest(d)
    return denested_dict