import os
import os.path
import pypandoc
import tempfile


class Compiler():
    def __init__(self, *args, **kwargs):
        self.saga = kwargs['saga']


    def CompileDraft(self):
        print (self.saga)

        # Get the current project directory
        here = os.getcwd()
        draft = os.path.normpath(os.path.join(here, "Draft"))
        # print(draft)

        # Get the configuration


        #############################################
        # Join all parts into a single Markdown doc #
        #############################################

        # Get a list of all the individual parts
        files = self.getFiles(draft)
        print(files)

        # Open temporary file to store unified Markdown
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as fp:

            # Add header content

            for file in files:
                buffer = []

                # Open file
                with open(file, 'r') as f:
                    # Read file
                    buffer = f.readlines()

                # Preprocessor
                buffer.append("* * *")
                buffer.append('')
                print(buffer)

                # Write to temporary file
                fp.write("\n".join(buffer).encode('utf-8'))

                # Write separator
                # fp.write(b"\n***\n")
                # 

            fp.seek(0)
            print(fp.readlines())

            fp.close()
            print(fp.name)

            # Is there a metadata.yaml?

            # For each format defined in the yaml config
            output = pypandoc.convert_file(
                fp.name,
                'rtf',
                format='md',
                outputfile="/tmp/somefile.rtf",
                extra_args=[
                    # 'metadata.yaml', 
                    '--data-dir={}/.pandoc/'.format(self.saga),
                    '--template=template.rtf',
                    # Pass metadata variables here
                    '-V', 'title:The Foo of Bar',
                    '-V', 'author:Adam Israel',
                    '-V', 'wordcount:1,234',

                ]
            )

            # Delete the temporary file
            os.unlink(fp.name)

        # Check the Word Count
        # Check the grammar/rules

        pass

    def getFiles(self, path):
        """Get a list of files in this folder.

        :param path str: The path to the files to list

        :return: The list of files, sorted in ascending order
        """
        entries = []

        for file in os.listdir(path):
            fpath = os.path.join(path, file)
            if os.path.isdir(fpath):

                entries += self.getFiles(fpath)
            else:
                entries.append(fpath)
        
        return sorted(entries)
