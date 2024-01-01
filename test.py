import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-w', '--website', help='Choose website you want to crawl (dantri or vnexpress)')

# Read arguments from command line
args = parser.parse_args()
 
if args.website:
    print("Displaying Output as: % s" % args.website)