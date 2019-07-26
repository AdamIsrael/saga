import argparse
import importlib
import os
import os.path
# import saga
import saga.compile
import saga.stats
import saga.templates
import saga.utils
import saga.workspace

from shutil import copytree
import yaml

def get_argparser():
    parser = argparse.ArgumentParser(description='Saga document system')

    subparsers = parser.add_subparsers()

    # Initialize the workspace
    init_p = subparsers.add_parser('init')
    init_p.add_argument('--verbose', action='store_true')
    init_p.set_defaults(func=args_init)

    # New Projects
    new_p = subparsers.add_parser('new')

    # TODO: Integrate with templates
    new_p.add_argument(
        'type', 
        choices=saga.utils.templates, 
        help='The type of project to create'
    )
    new_p.add_argument('name', help='The name of the project to create')
    new_p.set_defaults(func=args_new)

    # Compile
    compile_p = subparsers.add_parser('compile')

    compile_p.add_argument(
        'target', 
        choices=['draft', 'outline', 'bible'], 
        help='The target to compile to'
    )

    compile_p.set_defaults(func=args_compile)

    # Stats
    stats_p = subparsers.add_parser('stats')

    stats_p.add_argument(
        'target', 
        default='words',
        const='all',
        nargs='?',
        choices=['words', 'other'], 
        help='The target to compile to'
    )
    stats_p.set_defaults(func=args_stats)

    return parser

def args_compile(args):
    print("Compiling...")
    # print(args)

    print(__file__)
    print(os.path.dirname(__file__))
    here = saga.find_saga_config()
    # print("Saga: {}".format(here))
    # return

    if here:
        print("We're in a project folder")
        # TODO: Make sure we're in a project folder, not just
        # under the initialized saga directory

        metadata = {}

        # Load the saga defaults
        with open("{}/saga.yaml".format(here)) as f:
            metadata = yaml.safe_load(f)

        phere = os.getcwd()
        project = os.path.basename(phere)
        if os.path.exists("{}/saga.yaml".format(phere)):
            # Map the project-specific config
            with open("{}/saga.yaml".format(phere)) as f:
                pmeta = yaml.safe_load(f)
                metadata = {**metadata, **pmeta}
            # print(metadata)
            # return
            compiler = saga.compile.Compiler(
                # Tell the compiler where saga is
                saga=saga.find_saga_lib(),
            )

        else:
            print("Not a valid saga project!")

        if args.target == 'draft':
            print("Compiling a draft...")
            compiler.CompileDraft(metadata=metadata)

def args_init(args):
    workspace = saga.workspace.Workspace()

    if args.verbose:
        print("Initializing workspace")

    workspace.Initialize()

def args_new(args):
    # TODO: There should be a function that returns a bool if we're in the saga root, and one that returns the path to the root
    # so that we always create new projects in the right place.
    here = os.getcwd()
    print(here)

    # Instantiate the template
    if args.type:
        module = importlib.import_module("saga.templates." + args.type)

        # Get the path to the module's templates
        templateFiles = "{}/{}".format(
            os.path.dirname(module.__file__),
            args.type
        )

        # Get the path to where the new project will be created
        here = "{}/{}".format(here, module.basedir)

        # Make the base directory, if it doesn't exist
        if not os.path.exists(here):
            os.makedirs(here)

        # TODO: We need to make sure the name is valid for a directory name
        here = "{}/{}".format(here, args.name)

        # Does this project already exist?
        if os.path.exists(here):
            print("Error: Project {} already exists in {}".format(args.name, module.basedir))
            return

        # Copy the template to the new project
        copytree(
            templateFiles,
            here,
        )
        print("{} created!".format(here))

def args_stats(args):
    if args.target == 'words':
        print('words words words words punchline')

        # TODO: print out word count and stats, broken down by draft, outline, and research

        stats = saga.stats.Stats(
            saga=saga.find_saga_lib(),
        )

        # Word Count by type
        # words = stats.WordCount()

        draft = stats.WordCount.Draft
        outline = stats.WordCount.Outline
        research = stats.WordCount.Research

        # draft = words['Draft']
        # outline = words['Outline']
        # research = words['Research']

        print("Draft: {:,} words".format(draft))
        print("Outline: {:,} words".format(outline))
        print("Research: {:,} words".format(research))

        print("Total: {:,} words".format(draft + outline + research))
    pass


def main():
    parser = get_argparser()

    args = parser.parse_args()

    # Execute the sub-command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()