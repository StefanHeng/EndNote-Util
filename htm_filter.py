"""
Removes irrelevant fields Given a htm export from EndNote
"""
import re
from itertools import chain
from datetime import datetime

from icecream import ic
from markdownify import markdownify


def flatten(l):
    return [i for lst in l for i in lst]


def my_date():
    def nth(n):
        # Taken from https://stackoverflow.com/a/20007730/10732321
        return '%d%s' % (n, 'tsnrhtdd'[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
    t = datetime.today()
    return f'{t.strftime("%a. %b.")} {nth(t.day)}, {t.strftime("%Y")}'


class EdnFilter:
    def __init__(self, fnm):
        self.fnm = fnm
        with open(fnm, 'r') as fl:
            self.lns = list(map(str.strip, fl.readlines()))
            self.i_s = self.lns.index('<body>') + 1
            self.i_e = self.lns.index('</body>')

    def __call__(self, relevant, exp=True, title='References', md=True):
        """
        :param relevant: Exported reference entries will have `relevant` fields in that order, if present
        :param exp: If true, export to file; otherwise, return string representation
        :param title: Title of file
        :param md: If true, export in markdown format; `htm` otherwise
        :return: HTML or markdown representation of the `relevant` fields, sorted by time
        """
        def is_start(ln):
            """ Start of each reference entry """
            return re.match(f'^<b>Reference Type: </b>', ln)

        body = self.lns[self.i_s:self.i_e]
        idxs_strt = list(filter(lambda i: is_start(body[i]), range(len(body))))

        def _get_range_idx(idxs):
            return [(idx_, idxs[i+1] if i < len(idxs)-1 else -1) for i, idx_ in enumerate(idxs)]
        idxs_ref = _get_range_idx(idxs_strt)

        def relev(ln):
            return any(re.match(f'^<b>({k}):</b>', ln) for k in relevant)

        def _get_key(s):
            return re.match(f'^<b>(.+):</b>', s).group(1)

        def _get_single(b):
            idxs_entry = list(filter(lambda i: b[i].startswith('<b>'), range(len(b))))
            idxs_relevant = list(filter(lambda i: relev(b[i]), idxs_entry))

            def idx_range(idx_s):
                i = idxs_entry.index(idx_s) + 1
                return (idx_s, idxs_entry[i]) if i < len(idxs_entry) else (idx_s, -1)

            idxs_keep = list(map(idx_range, idxs_relevant))
            body_ = list(chain(b[s:e] for s, e in idxs_keep))
            body_ = sorted(body_, key=lambda x: relevant.index(_get_key(x[0])))
            body_ = flatten(body_)
            body_.append('<hr>' if md else '<br><hr>')

            return body_

        lns = list.copy(self.lns)
        entries = [_get_single(body[i_s:i_e]) for i_s, i_e in idxs_ref]

        def _get_year(l):
            s = ''.join(filter(lambda s_: '<b>Year:</b>' in s_ or '<b>Year of Conference:</b>' in s_, l))
            m = re.match(r'^<b>Year:</b> (.+)<p>', s) or re.match(r'^<b>Year of Conference:</b> (.+)<p>', s)
            return m.group(1)
        entries = flatten(sorted(entries, key=_get_year))
        lns[self.i_s:self.i_e] = [x + '\n<p>' for x in entries] if md else entries

        if md:
            lns[2] = ''
            idx = lns.index('<body>')
            lns[idx:idx] = [
                f'<h1>{title}</h1>',
                '<p>Stefan/Yuzhao Heng</p>',
                f'<p>Since {my_date()}</p>',
                '<br>'
            ]

        st = '\n'.join(lns)
        if md:
            st = markdownify(st)
            st = st[:20].strip() + st[20:]
            while st[-3:] == '\n' * 3:  # Looks like too much newline char per `markdownify`
                st = st[:-3]

        if exp:
            fnm_ = f'{self.fnm.removesuffix(".htm")}, filtered' + ('.md' if md else '.htm')
            ic(fnm_)
            open(fnm_, 'a').close()  # Create file in OS
            with open(fnm_, 'w') as fl:
                fl.write(st)
        else:
            return st


if __name__ == '__main__':
    f = 'EndNote Library.htm'
    ef = EdnFilter(f)
    ef(['Title', 'Author', 'Year', 'Year of Conference', 'Research Notes'], exp=True)
