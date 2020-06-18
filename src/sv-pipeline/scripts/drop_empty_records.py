#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Ryan Collins <rlcollins@g.harvard.edu>
# Distributed under terms of the MIT license.

"""
Drop records with no non-reference genotypes from an input VCF
Alternative to VCFTools, which rounds GQ to a max of 99
"""

import argparse
import sys
import pysam


def drop_nonref_gts(vcf, fout):
    NULL_GT = [(0, 0), (None, None), (0, ), (None, ), (None, 2)]
    samples = [s for s in vcf.header.samples]

    # for record in vcf.fetch():
    #     nonref = svu.get_called_samples(record)
    #     if len(nonref) > 0:
    #         fout.write(record)

    for record in vcf.fetch():
        for s in samples:
            if record.samples[s]['GT'] not in NULL_GT:
                fout.write(record)
                break


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('vcf', help='Input vcf (supports "stdin").')
    parser.add_argument('fout', help='Output file (supports "stdout").')

    args = parser.parse_args()

    if args.vcf in '- stdin'.split():
        vcf = pysam.VariantFile(sys.stdin) 
    else:
        vcf = pysam.VariantFile(args.vcf)

    if args.fout in '- stdout'.split():
        fout = pysam.VariantFile(sys.stdout, 'w', header=vcf.header)
    else:
        fout = pysam.VariantFile(args.fout, 'w', header=vcf.header)

    drop_nonref_gts(vcf, fout)

    fout.close()


if __name__ == '__main__':
    main()
