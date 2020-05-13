import argparse
from looker_deployer.commands import deploy_boards, deploy_code, deploy_connections, deploy_content


loc = "looker.ini"


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    setup_board_subparser(subparsers)
    setup_code_subparser(subparsers)
    setup_connections_subparser(subparsers)
    setup_content_subparser(subparsers)
    args = parser.parse_args()
    args.func(args)


def setup_board_subparser(subparsers):
    boards_subparser = subparsers.add_parser("boards")
    boards_subparser.add_argument("--source", required=True, help="which environment to source the board from")
    boards_subparser.add_argument("--target", required=True, nargs="+", help="which target environment(s) to deploy to")
    boards_subparser.add_argument("--board", required=True, help="which board to deploy")
    boards_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")

    boards_subparser.add_argument(
        "--title-change",
        help="if updating title, the old title to replace in target environments"
    )

    boards_subparser.add_argument("--debug", action="store_true", help="set logger to debug for more verbosity")
    boards_subparser.set_defaults(func=deploy_boards.main)


def setup_code_subparser(subparsers):
    code_subparser = subparsers.add_parser("code")
    code_subparser.add_argument("--hub", action="store_true", help="flag to deploy hub project")
    code_subparser.add_argument("--spoke", nargs='+', help="which spoke(s) to deploy")
    code_subparser.add_argument("--hub-exclude", nargs="+", help="which projects should be ignored from hub deployment")
    code_subparser.add_argument("--debug", action="store_true", help="set logger to debug for more verbosity")
    code_subparser.set_defaults(func=deploy_code.main)


def setup_connections_subparser(subparsers):
    connections_subparser = subparsers.add_parser("connections")
    connections_subparser.add_argument("--source", required=True, help="which environment to source the board from")
    connections_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    connections_subparser.add_argument(
        "--target",
        required=True,
        nargs="+",
        help="which target environment(s) to deploy to"
    )
    connections_subparser.add_argument("--pattern", help="regex pattern to filter which connections are deployed")
    connections_subparser.add_argument(
        "--include-password",
        action="store_true",
        help="should passwords be set from the ini file?"
    )
    connections_subparser.add_argument("--debug", action="store_true", help="set logger to debug for more verbosity")
    connections_subparser.set_defaults(func=deploy_connections.main)


def setup_content_subparser(subparsers):
    content_subparser = subparsers.add_parser("content")
    content_subparser.add_argument("--env", required=True, help="What environment to deploy to")
    content_subparser.add_argument("--ini", default=loc, help="ini file to parse for credentials")
    content_subparser.add_argument("--debug", action="store_true", help="set logger to debug for more verbosity")
    content_subparser.add_argument("--recursive", action="store_true", help="Should folders deploy recursively")
    content_subparser.add_argument("--target-folder", help="override the default target folder with a custom path")
    content_group = content_subparser.add_mutually_exclusive_group(required=True)
    content_group.add_argument("--folders", nargs="+", help="Folders to fully deploy")
    content_group.add_argument("--dashboards", nargs="+", help="Dashboards to deploy")
    content_group.add_argument("--looks", nargs="+", help="Looks to deploy")
    content_group.add_argument("--export", help="pull content from dev")
    content_subparser.set_defaults(func=deploy_content.main)
