import argparse

from dcicutils.command_utils import script_catch_errors
from ..submission import upload_item_data


EPILOG = __doc__


def main(simulated_args_for_testing=None):
    parser = argparse.ArgumentParser(  # noqa - PyCharm wrongly thinks the formatter_class is invalid
        description="Submits a data bundle part",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('part_filename', help='a local Excel filename that is the part file')
    parser.add_argument('--uuid', '-u', help='uuid identifier', default=None)
    parser.add_argument('--server', '-s', help="an http or https address of the server to use", default=None)
    parser.add_argument('--env', '-e', help="a portal environment name for the server to use", default=None)
    parser.add_argument('--no_query', '-nq', action="store_true",
                        help="suppress requests for user input", default=False)
    args = parser.parse_args(args=simulated_args_for_testing)

    with script_catch_errors():

        upload_item_data(item_filename=args.part_filename, uuid=args.uuid, server=args.server,
                         env=args.env, no_query=args.no_query)


if __name__ == '__main__':
    main()
