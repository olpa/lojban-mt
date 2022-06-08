import json
import re
import sys


def update_from_rafsi(li, _dict):
    if not li:
        return
    (rafsi, gismu, en) = re.split('\\s+', li, 2)
    assert (len(rafsi) == 3) or ((len(rafsi) == 4) and ("'" in rafsi)), (
            f'Bad rafsi: {rafsi}')
    assert rafsi not in _dict
    _dict[rafsi] = gismu
    if len(gismu) == 5:
        _dict[gismu[:4]] = gismu


def update_from_gismu(li, _dict):
    if not li:
        return
    if 'gismu list' in li:  # header
        return
    # 1) do not confuse with english text
    # 2) add a tail ' NULL ' so that `split` works always
    li = li[:20] + ' NULL '
    (_, gismu, rafsi, _) = re.split('\\s+', li, 3)
    if not rafsi or rafsi == 'NULL':
        rafsi = gismu[:4]
    if rafsi == 'brod':  # corner case for brode/brodi/etc
        return
    if rafsi not in _dict:
        _dict[rafsi] = gismu
    else:
        assert gismu == _dict[rafsi], (
                f"Update from gismu. Want to set: '{rafsi}' to '{gismu}', "
                f"but is already '{_dict[rafsi]}'")


def write_py(h, _dict):
    print('# Auto-generated, do not edit\n', file=h)
    print('_map = ', file=h, end='')
    json.dump(_dict, h, indent=2)
    print('\n\n\ndef rafsi_to_gismu(rafsi, default=None):', file=h)
    print('    return _map.get(rafsi, default)', file=h)


def main():
    assert len(sys.argv) == 4, (
            'Provide three command-line arguments: '
            'rafsi file, gismu file, output file')
    (rafsi_file, gismu_file, out_file) = sys.argv[1:]
    _dict = {}
    with open(rafsi_file) as h:
        for li in h:
            update_from_rafsi(li, _dict)
    with open(gismu_file) as h:
        for li in h:
            update_from_gismu(li, _dict)
    with open(out_file, 'w') as h:
        write_py(h, _dict)


main()
