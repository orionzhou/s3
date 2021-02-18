#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as op
import sys
import logging
#import boto3

from jcvi.apps.base import sh, mkdir

def s3_sync(args, down=False):
    os.chdir(args.dirh)
    bucket = f"{args.bucket}"
    if not down and not op.exists(bucket):
        print("%s does not exist" % bucket)
        sys.exit(1)
    elif down and not op.exists(bucket):
        mkdir(bucket)
    dry = "--dry-run" if args.dry else ''
    cmd = "s3cmd -c %s/appconfig/s3cfg2" % os.environ['git'] if args.personal else "s3cmd"
    cmd += " sync --delete-removed --acl-public --follow-symlinks --exclude '.git/* .github/*'"
    # sh("%s %s --exclude '*.css' %s/ s3://%s/" % (cmd, dry, bucket, bucket))
    # sh("%s %s --content-type 'text/css' --exclude '*' --include '*.css' %s/ s3://%s/" % (cmd, dry, bucket, bucket))
    bucket_str = f"s3://{bucket} {bucket}/" if down else f"{bucket}/ s3://{bucket}"
    sh(f"{cmd} {dry} --no-mime-magic --guess-mime-type {bucket_str}")

def s3_up(args):
	s3_sync(args, down=False)

def s3_down(args):
	s3_sync(args, down=True)

if __name__ == "__main__":
    import argparse
    ps = argparse.ArgumentParser(
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            description = 'Amazon S3 utilities'
    )
    sp = ps.add_subparsers(title = 'available commands', dest = 'command')

    sp1 = sp.add_parser("up",
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            help = "upload to s3 bucket")
    # allowed_buckets = ['igv','igv-data','multiqc','share']
    sp1.add_argument('bucket', help = 'bucket path')
    sp1.add_argument('--dirh', default="%s/s3" % os.environ["proj"], help = 'local directory for S3')
    #sp1.add_argument('--pre', default="zhoup-", help="bucket prefix")
    sp1.add_argument('--personal', action="store_true", help="use personal aws account instead of msi account?")
    sp1.add_argument('--dry', action="store_true", help="dry run?")
    sp1.set_defaults(func = s3_up)

    sp1 = sp.add_parser("down",
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            help = "download s3 bucket to local directory")
    sp1.add_argument('bucket', help = 'bucket path')
    sp1.add_argument('--dirh', default="%s/s3" % os.environ["proj"], help = 'local directory for S3')
    sp1.add_argument('--personal', action="store_true", help="use personal aws account instead of msi account?")
    sp1.add_argument('--dry', action="store_true", help="dry run?")
    sp1.set_defaults(func = s3_down)

    args = ps.parse_args()
    if args.command:
        args.func(args)
    else:
        print('Error: need to specify a sub command\n')
        ps.print_help()

