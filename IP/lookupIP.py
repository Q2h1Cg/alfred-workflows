# -*- coding: utf-8 -*-

import re
import sys
from collections import OrderedDict

from workflow import Workflow, web

patterns = OrderedDict([
    [u'IP', u'<input type="text" name="ip" value="(\S+?)"'],
    [u'运营商', u'<td>运营商</td>[\s\S]+?line-height: 46px;">(\S+?)</span>'],
    [u'地理位置', u'<td>地理位置</td>[\s\S]+?height: 46px;">(\S+?)</span>'],
    [u'高精度地理位置', u'国内高精度</span></th>[\s\S]+?line-height: 46px;">(\S+?)<span style'],
])


def lookup(ip):
    resp = web.post(
        'https://www.ipip.net/ip.html',
        data={'ip': ip},
        headers={'Referer': 'https://www.ipip.net/'},
        timeout=3
    )
    resp.raise_for_status()

    info = OrderedDict()
    for key, pattern in patterns.items():
        results = re.findall(pattern, resp.text)
        info[key] = results[0] if results else u''

    return info


def main(wf):
    ip = wf.args[0] if wf.args else ''
    info = lookup(ip)
    subtitle = u' - '.join([value for value in info.values() if value])
    text = u'\n'.join([key + u'：' + value for key, value in info.items() if value])
    wf.add_item(valid=True, title=info['IP'], subtitle=subtitle, arg=text)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
