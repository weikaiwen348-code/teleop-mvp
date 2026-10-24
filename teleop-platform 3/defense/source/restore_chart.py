"""Preserve the original chart and embedded workbook lost on deck re-export.

Text/table editing is performed by Artifact Tool. This narrowly scoped package
repair copies the unchanged chart lineage from the original, never new values.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import posixpath
import sys

source, candidate, output = map(Path, sys.argv[1:])
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
with ZipFile(source) as original, ZipFile(candidate) as draft:
    data = {name: draft.read(name) for name in draft.namelist()}
    source_rels = E.fromstring(original.read('ppt/slides/_rels/slide6.xml.rels'))
    draft_rels = E.fromstring(draft.read('ppt/slides/_rels/slide6.xml.rels'))
    old_chart = next(x for x in source_rels if x.attrib['Type'].endswith('/chart'))
    new_chart = next(x for x in draft_rels if x.attrib['Type'].endswith('/chart'))
    chart_part = posixpath.normpath(posixpath.join('ppt/slides', old_chart.attrib['Target'])).lstrip('/')
    new_chart.set('Target', old_chart.attrib['Target'])
    E.register_namespace('', REL)
    data['ppt/slides/_rels/slide6.xml.rels'] = E.tostring(draft_rels, encoding='utf-8', xml_declaration=True)
    chart_rel = posixpath.join(posixpath.dirname(chart_part), '_rels', posixpath.basename(chart_part)+'.rels')
    copied = [chart_part, chart_rel]
    for rel in E.fromstring(original.read(chart_rel)):
        if rel.attrib.get('TargetMode') == 'External':
            raise ValueError('unexpected external chart dependency')
        copied.append(posixpath.normpath(posixpath.join(posixpath.dirname(chart_part), rel.attrib['Target'])).lstrip('/'))
    for name in copied:
        data[name] = original.read(name)
    # Preserve the original content type of every restored dependency.
    old_types = E.fromstring(original.read('[Content_Types].xml'))
    new_types = E.fromstring(data['[Content_Types].xml'])
    for item in old_types:
        if item.tag.endswith('Override') and item.attrib['PartName'].lstrip('/') in copied:
            key, value = 'PartName', item.attrib['PartName']
        elif item.tag.endswith('Default') and any(n.endswith('.'+item.attrib['Extension']) for n in copied):
            key, value = 'Extension', item.attrib['Extension']
        else:
            continue
        if not any(x.attrib.get(key)==value for x in new_types):
            new_types.append(item)
    E.register_namespace('', CT)
    data['[Content_Types].xml'] = E.tostring(new_types, encoding='utf-8', xml_declaration=True)
    with ZipFile(output,'w',compression=ZIP_DEFLATED) as final:
        for name, raw in data.items():
            final.writestr(name,raw)
    print('Preserved original chart/workbook bytes:',copied)
