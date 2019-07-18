import argparse
import importlib
import os
import os.path
# import saga
import saga.compile
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
        if os.path.exists("{}/{}.yaml".format(phere, project)):
            # Map the project-specific config
            with open("{}/{}.yaml".format(phere, project)) as f:
                pmeta = yaml.safe_load(f)
                metadata = {**metadata, **pmeta}
            # print(metadata)
            # return
            compiler = saga.compile.Compiler(
                # Tell the compiler where saga is
                saga=here,
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