# -*- coding: utf-8 -*-
"""The skip goes under the button, not between it and the field.

Sitting above Continue it read as part of the form, and it interrupted the
path from the field to the action. Below the buttons it is what it is: the
way out for the few people who do not have a website.
"""
import io
import sys

OLD = """        (step.skip ? '<button type="button" class="rec-flow-skip">' +
          esc(step.skip) + '</button>' : '') +
        '<div class="rec-flow-act">' +
          (at > 0 ? '<button type="button" class="rec-flow-back">Back</button>' : '') +
          // a single choice answers and carries on by itself; picking several
          // does not, so a multi step keeps its Continue
          (step.chipsOnly && !step.multi ? '' :
            '<button type="button" class="rec-flow-next">Continue</button>') +
        '</div>';"""

NEW = """        '<div class="rec-flow-act">' +
          (at > 0 ? '<button type="button" class="rec-flow-back">Back</button>' : '') +
          // a single choice answers and carries on by itself; picking several
          // does not, so a multi step keeps its Continue
          (step.chipsOnly && !step.multi ? '' :
            '<button type="button" class="rec-flow-next">Continue</button>') +
        '</div>' +
        (step.skip ? '<button type="button" class="rec-flow-skip">' +
          esc(step.skip) + '</button>' : '');"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
