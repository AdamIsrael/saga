import os
import os.path
import pypandoc
from pandocfilters import walk, toJSONFilter
import tempfile


class Compiler():
    def __init__(self, *args, **kwargs):
        self.saga = kwargs['saga']


    def CompileDraft(self, metadata):
        print (self.saga)

        # Get the current project directory
        here = os.getcwd()
        draft = os.path.normpath(os.path.join(here, "Draft"))
        output = os.path.normpath(os.path.join(here, "Output"))

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
            
            last = len(files) - 1
            for i, file in enumerate(files):
                buffer = []

                # Open file
                with open(file, 'r') as f:
                    # Read file
                    buffer = f.readlines()

                # Preprocessor

                # Put a line after each scene
                if i != last:
                    buffer.append('')
                    buffer.append("***")
                    buffer.append('')

                # Write to temporary file
                fp.write("\n".join(buffer).encode('utf-8'))

 

            fp.seek(0)
            print(fp.readlines())

            fp.close()
            print(fp.name)

            # Is there a metadata.yaml?
            print(metadata)
            # For each format defined in the yaml config
            rtf = pypandoc.convert_file(
                fp.name,
                'rtf',
                format='md',
                # outputfile="/tmp/somefile.rtf",
                extra_args=[
                    # 'metadata.yaml', 
                    '--data-dir={}/.pandoc/'.format(self.saga),
                    '--template=template.rtf',
                    # Pass metadata variables here
                    '-V', 'title:{}'.format(metadata['title']),
                    '-V', 'running-title:{}'.format(metadata['running-title']),
                    '-V', 'author:Adam Israel',
                    '-V', 'email:adam@adamisrael.com',
                    '-V', 'surname:Israel',
                    '-V', 'fullname:Adam Israel',
                    '-V', 'address1:17 Vanier Dr.',
                    '-V', 'address2:P.O. Box 1946',
                    '-V', 'city:Tilbury',
                    '-V', 'state:ON',
                    '-V', 'zipcode:N0P 2L0',
                    '-V', 'country:Canada',
                    '-V', 'phone:(226) 229-1337',
                    '-V', 'wordcount:1,234',
                ],
                filters=[
                    # os.path.join(self.saga, 'saga/filters', 'hr_to_scene_break.py'),
                ]
            )

            # Post-processing
            print("Post-processing...")

            # Replace the HorizontalRule with our scene break.
            # TODO: See if a filter will work with this.
            rtf = rtf.replace("\\emdash\\emdash\\emdash\\emdash\\emdash", "#")

            # Write the output
            if not os.path.exists(output):
                os.mkdir(output)

            print("Writing output...")
            with open('{}/{}.rtf'.format(output, metadata['running-title']), 'w') as f:
                f.write(rtf)

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
