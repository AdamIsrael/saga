import os
import os.path
import pypandoc
from pandocfilters import walk, toJSONFilter
import saga.language
import saga.utils
import tempfile


class Stats():
    def __init__(self, *args, **kwargs):
        self.saga = kwargs['saga']

        self.wc = WordCount(saga=self.saga)

    @property
    def WordCount(self):
        return self.wc

class StatType():
    """Abstract class for stat types."""

    def __init__(self, *args, **kwargs):
        self.saga = kwargs['saga']

    """
    Internal methods
    """

    def __getFiles(self, path):
        """Get a list of files in this folder.

        :param path str: The path to the files to list

        :return: The list of files, sorted in ascending order
        """
        entries = []

        for file in os.listdir(path):
            fpath = os.path.join(path, file)
            if os.path.isdir(fpath):

                entries += self.__getFiles(fpath)
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
        files = self.__getFiles(path)
        # print(sorted(files))
        # Open temporary file to store unified Markdown
        buffer = []

        last = len(files) - 1
        for i, file in enumerate(files):
            if file[-2:] == "md":
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

class WordCount(StatType):
    def __init__(self, *args, **kwargs):
        self.saga = kwargs['saga']
        super().__init__(saga=self.saga)

    @property
    def Draft(self):
        return self.__getWordCount('Draft')

    @property
    def Outline(self):
        return self.__getWordCount('Outline')

    @property
    def Research(self):
        return self.__getWordCount('Research')


    # Where we store all compiled drafts
    def __getWordCount(self, type):
        here = os.getcwd()
        folder = os.path.normpath(os.path.join(here, type))
        wc = 0

        if os.path.exists(folder):
            (tmpMarkdown, buffer) = self.join_markdown(folder)

            w = saga.language.Words(buffer)
            wc = w.getWordCount()

        return wc

