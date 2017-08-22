# -*- coding:utf-8 -*-  

import re
import sys

from workflow import Workflow, web


def lookup(ip):
    addr = u""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Referer": "http://www.ipip.net/"
    }
    
    resp = web.post("http://www.ipip.net/ip.html", data={"ip":ip}, headers=headers, timeout=3)
    resp.raise_for_status()
    match = re.search(r'<span style="color: rgb\(243, 102, 102\);">(\S+?)</span>[\s\S]*?<div><span id="myself">([\s\S]*?)</span>', resp.text)
    if match:
        ip, addr = match.group(1), match.group(2).strip().replace(u"  ", u" ")
    
    return ip, addr


def main(wf):
    ip = "" if not wf.args else wf.args[0]
    ip, addr = lookup(ip)
    txt = ip + u"\n" + addr
    wf.add_item(title=ip, subtitle=addr, valid=True, arg=txt)
    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
