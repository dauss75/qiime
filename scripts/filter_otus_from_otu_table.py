#!/usr/bin/env python
# File created on 21 Dec 2011
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from itertools import izip
from numpy import inf, isinf
from qiime.pycogent_backports.parse_biom import parse_biom_table
from qiime.util import parse_command_line_parameters, make_option
from qiime.filter import filter_otus_from_otu_table

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
 make_option('-i','--input_fp',type="existing_filepath",
             help='the input otu table filepath in biom format'),
 make_option('-o','--output_fp',type="new_filepath",
             help='the output filepath in biom format'),
]
script_info['optional_options'] = [
 make_option('-n', 
             '--min_count',
             type='int',
             default=0,
             help="the minimum total observation count of an otu for that otu to be retained [default: %default]"),
 make_option('-x', 
             '--max_count',
             type='int',
             default=inf,
             help="the maximum total observation count of an otu for that otu to be retained [default: infinity]")

]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    input_fp = opts.input_fp
    output_fp = opts.output_fp
    
    min_count = opts.min_count
    max_count = opts.max_count
    
    if not (min_count != 0 or not isinf(max_count)):
        option_parser.error("No filtering requested. Must provide either "
                     "min counts or max counts (or some combination of those).")

    otu_table = parse_biom_table(open(opts.input_fp,'U'))
    output_f = open(opts.output_fp,'w')
    
    otu_ids_to_keep = otu_table.ObservationIds
    
    filtered_otu_table = filter_otus_from_otu_table(otu_table,
                                                       otu_ids_to_keep,
                                                       min_count,
                                                       max_count)
    output_f.write(filtered_otu_table.getBiomFormatJsonString())
    output_f.close()

if __name__ == "__main__":
    main()