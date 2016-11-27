import tempfile
import os
import re
import subprocess

class EbookGenerator(object):
    def __init__(self, data):
        self.data = data

    def setup(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_dir_path = self.tmp_dir.name
        
    def cleanup(self):
        self.tmp_dir.cleanup()

    def generate_mobi(self):
        print("SELF DATA")
        print(self.data)
        current_path = os.path.dirname(os.path.realpath(__file__))

        filename = "".join([c for c in self.data["title"] if re.match(r'\w', c)])

        with open('{0}/{1}.html'.format(self.tmp_dir.name, filename), 'w+') as f:
            f.write(self.data["html"])

        with open('{0}/{1}-metadata.xml'.format(self.tmp_dir.name, filename), 'w+') as f:
            f.write("""<dc:title>{0}</dc:title>\n
                    <dc:creator opf:file-as="Daily Ebook" opf:role="aut">
                    Daily Ebook</dc:creator>""".format(self.data["title"]))

        subprocess.call(["pandoc",
                        "-S",
                        "-s",
                        "-o" + "{0}/{1}.epub".format(self.tmp_dir.name, filename) ,
                        "--epub-stylesheet={0}/epub-meta/style.css".format(current_path),
                        "--epub-metadata={0}/{1}-metadata.xml".format(self.tmp_dir.name, filename),
                        "--toc",
                        "{0}/{1}.html".format(self.tmp_dir.name, filename)])

        subprocess.call(["ebook-convert",
                        "{0}/{1}.epub".format(self.tmp_dir.name, filename),
                        "{0}/{1}.mobi".format(self.tmp_dir.name, filename),
                        "--input-profile=kindle"])

        return "{0}/{1}.mobi".format(self.tmp_dir.name, filename)
