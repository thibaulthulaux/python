import argparse
import os

# parser = argparse.ArgumentParser(
#   usage=f'''{os.path.basename(__file__)} [options] <command> [<args>]

# Python helper script for devs

# Commands:
#   machine   Create and remove machines
#   service   Start and stop services


# Run 'docker COMMAND --help' for more information on a command.
# '''
# )

parser=argparse.ArgumentParser(
  add_help=True,
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description="""here description""",
  epilog=f"""Run {os.path.basename(__file__)} [command] --help for more information on a command."""
  )

# parser.add_argument("--arg1", action="store")
# parser.add_argument("--arg2", action="store")
# parser.add_argument("--arg3", action="store")

subparser = parser.add_subparsers(dest="subparser")

machine = subparser.add_parser("machine")
machine.add_argument("create", action="store")
machine.add_argument("list", action="store")
machine.add_argument("rm", action="store")


service = subparser.add_parser("service")
service.add_argument("start", action="store")
service.add_argument("stop", action="store")

# parser.add_argument("name")

# parser.add_argument(
#   "-n",
#   dest="now",
#   action="store_true",
#   help="shows now"
#   )

args = parser.parse_args()

print("\n - Args:")
print(args)

print("\n - Subparser:")
print(args.subparser)


# args = parser.parse_args(["thibault"])

# print(f"{args.name}")

# if args.now:
#     now = datetime.datetime.now()
#     print(now)

print("\n----")
parser.print_usage()

print("\n----")
parser.print_help()