import os
import os.path
import pypandoc
from pandocfilters import walk, toJSONFilter
import saga.language
import saga.utils
import tempfile


class Compiler():
    def __init__(self, *args, **kwargs):
        self.saga = kwargs['saga']


    def CompileDraft(self, metadata):
        print (self.saga)

        # Get the current project directory
        here = os.getcwd()
        
        # The current draft
        draft = os.path.normpath(os.path.join(here, "Draft"))

        # Where we store all compiled drafts
        drafts = os.path.normpath(os.path.join(
            saga.find_saga_config(), 
            "Drafts"
        ))
        # print("Drafts: {}".format(drafts))
        # return
        # print(draft)

        # Get the configuration


        #############################################
        # Join all parts into a single Markdown doc #
        #############################################

        # Get a list of all the individual parts
        files = self.getFiles(draft)
        # print(files)

        # Open temporary file to store unified Markdown
        buffer = []

        last = len(files) - 1
        for i, file in enumerate(files):
            # Slurp the file
            with open(file, 'r') as f:
                buffer += f.readlines()

            # Preprocessor

            # Put a line after each scene
            if i != last:
                buffer.append('')
                buffer.append("***")
                buffer.append('')

        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as fp:
            # Write to temporary file
            fp.write("\n".join(buffer).encode('utf-8'))
            fp.close()

        w = saga.language.Words(buffer)
        wordcount = w.getWordCount()

        # First convert to RTF
        rtf = pypandoc.convert_file(
            fp.name,
            'rtf',
            format='md',
            extra_args=[
                '--data-dir={}/.pandoc/'.format(saga.find_saga_lib()),
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
                '-V', 'wordcount:{:,}'.format(wordcount),
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
        if not os.path.exists(drafts):
            os.mkdir(drafts)

        print("Writing output...")
        with open('{}/{}.rtf'.format(drafts, metadata['running-title']), 'w') as f:
            f.write(rtf)

        # Delete the temporary file
        os.unlink(fp.name)

        # TODO: Convert the finished RTF to other formats
        # for format in ['odt', 'docx', 'pdf']:
        # pypandoc.convert_file(
        #     '{}/{}.rtf'.format(drafts, metadata['running-title']),
        #     'odt',
        # )

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
