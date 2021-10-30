from icecream import ic


if __name__ == '__main__':
    import re
    # s = '<b>DOI:</b> 10.1038/s41598-017-06596-z<p>'
    # k = 'DOI'
    # m = re.match(f'^<b>({k}):</b>', s)
    # if m:
    #     ic(m.group(1))

    # s = """
    # ('<b>Title:</b> Active Learning Applied to Patient-Adaptive Heartbeat '
    #     'Classification<p><b>Year:</b> 2010<p><b>Research Notes:</b> Paper by Dr. '
    #     'Weins at MIT. <p>Didn’t look into how active learnign is done <p>Feature '
    #     'extraction can be a guide, e.g. wavelet coefficients, normalized energy, and '
    #     'medical ones <p><p><b>URL:</b> <A '
    #     'HREF="https://proceedings.neurips.cc/paper/2010/file/d93ed5b6db83be78efb0d05ae420158e-Paper.pdf">https://proceedings.neurips.cc/paper/2010/file/d93ed5b6db83be78efb0d05ae420158e-Paper.pdf</A><p><p><p><br>'
    #     """
    # ic(s)
    # m = re.match(r'[\s\S]*<b>Year:</b> (.+)<p>', s)
    # # m = re.match(r'[\s\S](.)', s)
    # ic(m)

    from datetime import datetime
    ic(datetime.today())
    ic(datetime.today().weekday())
    ic(datetime.today().strftime('We are the %d, %b %Y'))
    ic(datetime.now().strftime('%a'))

    t = datetime.today()
    ic(t.strftime('%a. %b. %d, %Y'))
