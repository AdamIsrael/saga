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
        print("Saga: {}".format(self.saga))
        # return
        # Get the current project directory
        here = os.getcwd()
        
        # The current draft
        draft = os.path.normpath(os.path.join(here, "Draft"))

        # Where we store all compiled drafts
        drafts = os.path.normpath(os.path.join(
            saga.find_saga_config(), 
            "Drafts"
        ))

        (tmpMarkdown, buffer) = self.join_markdown(draft)

        w = saga.language.Words(buffer)
        wordcount = w.getWordCount()

        # First convert to RTF
        rtf = pypandoc.convert_file(
            tmpMarkdown,
            'rtf',
            format='md',
            extra_args=[
                '--data-dir={}/.pandoc/'.format(saga.find_saga_lib()),
                '--template=template.rtf',
                # '--lua-filter={}/.pandoc/rtf.lua'.format(saga.find_saga_lib()),
                # Pass metadata variables here
                '-V', 'doublespacing:yes',
                '-V', 'title:{}'.format(metadata['title']),
                '-V', 'running-title:{}'.format(metadata['running-title']),
                '-V', 'author:{}'.format(metadata['author']),
                '-V', 'email:{}'.format(metadata['email']),
                '-V', 'surname:{}'.format(metadata['surname']),
                '-V', 'fullname:{}'.format(metadata['name']),
                '-V', 'address1:{}'.format(metadata['address1']),
                '-V', 'address2:{}'.format(metadata['address2']),
                '-V', 'city:{}'.format(metadata['city']),
                '-V', 'state:{}'.format(metadata['state']),
                '-V', 'zipcode:{}'.format(metadata['zipcode']),
                '-V', 'country:{}'.format(metadata['country']),
                '-V', 'phone:{}'.format(metadata['phone']),
                '-V', 'wordcount:{:,}'.format(wordcount),
            ],
            filters=[
                # Format chapter headings
                "{}/saga/filters/headers.py".format(saga.find_saga_lib()),

                # Convert scene breaks
                "{}/saga/filters/hr_to_scene_break.py".format(saga.find_saga_lib()),
        
                # Standard Manuscript Format, as defined by Bill Shunn:
                # https://shunn.net/format/story.html
                "{}/saga/filters/smf.py".format(saga.find_saga_lib()),
            ]
        )

        # Post-processing
        print("Post-processing...")


        # The paragraph spacing of the RTF writer can't be overridden with a filter, so do it in post
        # rtf = rtf.replace("\\pard \\ql \\f0 \\sa180 \\li0 \\fi0", "\\pard \\ql \\f0 \\sa180 \\li0 \\fi720 \\sl480\\slmult1")

        # Replace the HorizontalRule with our scene break.
        # rtf = rtf.replace("\\emdash\\emdash\\emdash\\emdash\\emdash", "#")

        # Fix chapter headings
        # '\\fi0\\li0\\pagebb\\sb4320\\sa1440\\qc
        
        # Write the output
        if not os.path.exists(drafts):
            os.mkdir(drafts)

        print("Writing output...")
        with open('{}/{}.rtf'.format(drafts, metadata['running-title']), 'w') as f:
            f.write(rtf)

        # Delete the temporary file
        os.unlink(tmpMarkdown)

        # TODO: Convert the finished RTF to other formats
        # for format in ['odt', 'docx', 'pdf']:
        # pypandoc.convert_file(
        #     '{}/{}.rtf'.format(drafts, metadata['running-title']),
        #     'odt',
        # )

        # Check the Word Count
        # Check the grammar/rules

        pass

    def CompileOutline():
        pass

    """
    Internal methods
    """

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

    #############################################
    # Join all parts into a single Markdown doc #
    #############################################
    def join_markdown(self, path):
        """Join markdown

        Join all Markdown into a single Markdown document

        :param path str: The base path to the documents to join

        :return tuple: A tuple containing the temporary file name and the buffer of contents.
        """

        # Get a list of all the individual parts
        files = self.getFiles(path)
        # print(sorted(files))
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
        return (fp.name, buffer)

