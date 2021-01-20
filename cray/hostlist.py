"""A slurm-style hostlist processor.

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
# MIT License
#
# Copyright (c) 2018, Lawrence Livermore National Security, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Copyright (c) 2019, Cray Inc.
#
# Local modification of original source

# pylint: disable=too-many-locals, too-many-branches

import re


def split_nodelist(nodelist):
    """
    split_nodelist takes a compressed hostlist string and returns an array of
    individual components but leaves expansion []s in place.
    :param: nodelist: The hostlist string.
    :return: An array of components with expansions in place.
    """
    line = nodelist.replace(',', ' ')
    add_comma = False
    index = 0
    for char in line:
        if char in '[':
            add_comma = True
        if char in ']':
            add_comma = False
        if char in ' ' and add_comma:
            line = line[:index] + ',' + line[index+1:]
        index = index + 1
    return line.split(' ')


def expand(nodelist):
    """
    expand takes in a compressed hostlist string and returns all hosts listed.
    :param: nodelist: The hostlist string.
    :return: The expanded hostlist string.
    """
    if nodelist.find('[') == -1:
        return nodelist

    node_list = split_nodelist(nodelist)

    result_hostlist = []
    for node in node_list:
        nodelist_match = r"(\w*-?)\[((,?[0-9]+-?,?-?){0,})\](.*)?"
        if re.search(nodelist_match, node):
            match = re.search(nodelist_match, node)

            extra_expand = expand(match.group(4))
            # holds the ranges of nodes as a string
            # now we can manipulate the string and cast it to a list of numbers
            oldstr = str(match.group(2))
            left_br = oldstr.replace("[", "")
            right_br = left_br.replace("]", "")
            num_list = right_br.split(',')

            final_list = []
            for elem in num_list:
                # if it is a range of numbers, break it by the hyphen and
                # create a list
                if '-' in elem:
                    tmp_list = elem.replace("-", ",").split(",")

                    rng_list = range(int(tmp_list[0]), int(tmp_list[1]) + 1)
                    final_list.extend(rng_list)
                else:
                    final_list.append(int(elem))

            # put final list in ascending order and append cluster name to
            # each node number
            final_list.sort()

            # convert to string array
            hostlist_tmp = []
            for elem in final_list:
                hostlist_tmp.append(str(elem))

            # append hostname to the node numbers
            hostlist_no_suffix = []
            for elem in hostlist_tmp:
                hostlist_no_suffix.append(match.group(1) + elem)

            # append suffix to hostlist if there is one
            final_hostlist = []
            for elem in hostlist_no_suffix:
                if extra_expand:
                    for extra_elem in "".join(extra_expand.split()).split(','):
                        final_hostlist.append(elem + extra_elem)
                else:
                    final_hostlist.append(elem)

            result_hostlist.append('%s' % ','.join(map(str, final_hostlist)))
        else:
            result_hostlist.append(node)

    return ','.join(result_hostlist)
