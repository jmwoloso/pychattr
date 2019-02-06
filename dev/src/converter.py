#
# Author: Judd Cohen (Zen)
# No License, Public Domain, do what you'd like.
#

import os
import os.path


class CPP2PY(object):
    debug = False

    def convert(self, filename, targetFile):
        buffer = ""
        lastLine = ""

        # these are always included at the top of the output file
        imports = ['import sys',
                   'import time',
                   'import os',
                   'import os.path', ]

        # these are included only if we find references to them
        ogreImport = 'import ogre.renderer.OGRE as ogre'
        oisImport = 'import ogre.io.OIS as OIS'
        newtImport = 'import ogre.physics.OgreNewt as OgreNewt'
        ceguiImport = 'import ogre.gui.CEGUI as CEGUI'

        if os.path.exists(filename):
            file = open(filename, "r")
            for line in file:
                # a flag we can set to false to speed things up if we discover theres
                # no code on a particular line
                codeExists = True
                skipCurrentLine = False
                if self.debug: print
                "1: " + line.strip("\n")

                # if the line is ONLY a comment, we can skip a lot of the string replacements
                commentPos = line.find("//")
                if commentPos == 0:
                    codeExists = False
                elif commentPos > 0:
                    tmp = line[0:commentPos - 1]
                    tmp = tmp.strip(" ")
                    tmp = tmp.strip("\t")
                    if tmp == "":
                        codeExists = False

                # we dont actually want to strip down the line like this yet, but we do so
                # to check if its basically empty (hence the stupid var name)
                tmp = line.strip(" ")
                tmp = tmp.strip("\t")
                tmp = tmp.strip("\n")
                tmp = tmp.replace("{", "")
                if tmp == "": codeExists = False

                # skip all the parsing fun if the whole line is a comment
                line = line.replace("//", "#")
                line = line.rstrip("\n")
                if codeExists:
                    # clean up the end of the line so we can easily test the last real char
                    line = line.rstrip(";")
                    line = line.rstrip(" ")
                    line = line.rstrip("\t")

                    # all the easy replacements
                    line = line.replace("->", ".")
                    line = line.replace("::", ".")
                    line = line.replace("Ogre.", "ogre.")
                    line = line.replace("/*", "###")
                    line = line.replace("*/", "###")
                    line = line.replace("true", "True")
                    line = line.replace("false", "False")
                    line = line.replace("\t", "    ")
                    line = line.replace("&&", "and")
                    line = line.replace("||", "or")
                    line = line.replace("NULL", "None")
                    line = line.replace("struct", "class")
                    line = line.replace("case", "if")
                    line = line.replace("ogre.StringConverter.toString",
                                        "str")
                    line = line.replace("ogre.StringConverter.parseInt",
                                        "str")
                    line = line.replace(
                        "ogre.StringConverter.parseBool", "str")

                    # replace ifdef with a regular if else
                    if (line.find("#ifdef") != -1):
                        line = line.strip(" ")
                        var = line.split(" ")[1]
                        line = "if " + var + " == False:"
                    if (line.find("#else") != -1):
                        line = "else:"
                    if (line.find("#endif") != -1):
                        line = ""

                    # if any of these modules are used, add an import statement at the top
                    if (line.lower().find("ogre") != -1) and (
                            ogreImport not in imports):
                        imports.append(ogreImport)
                    if (line.lower().find("ois") != -1) and (
                            oisImport not in imports):
                        imports.append(oisImport)
                    if (line.lower().find("ogrenewt") != -1) and (
                            newtImport not in imports):
                  #
# Author: Judd Cohen (Zen)
# No License, Public Domain, do what you'd like.
#

import os
import os.path


class CPP2PY(object):
    debug = False

    def convert(self, filename, targetFile):
        buffer = ""
        lastLine = ""

        # these are always included at the top of the output file
        imports = ['import sys',
                   'import time',
                   'import os',
                   'import os.path', ]

        # these are included only if we find references to them
        ogreImport = 'import ogre.renderer.OGRE as ogre'
        oisImport = 'import ogre.io.OIS as OIS'
        newtImport = 'import ogre.physics.OgreNewt as OgreNewt'
        ceguiImport = 'import ogre.gui.CEGUI as CEGUI'

        if os.path.exists(filename):
            file = open(filename, "r")
            for line in file:
                # a flag we can set to false to speed things up if we discover theres
                # no code on a particular line
                codeExists = True
                skipCurrentLine = False
                if self.debug: print
                "1: " + line.strip("\n")

                # if the line is ONLY a comment, we can skip a lot of the string replacements
                commentPos = line.find("//")
                if commentPos == 0:
                    codeExists = False
                elif commentPos > 0:
                    tmp = line[0:commentPos - 1]
                    tmp = tmp.strip(" ")
                    tmp = tmp.strip("\t")
                    if tmp == "":
                        codeExists = False

                # we dont actually want to strip down the line like this yet, but we do so
                # to check if its basically empty (hence the stupid var name)
                tmp = line.strip(" ")
                tmp = tmp.strip("\t")
                tmp = tmp.strip("\n")
                tmp = tmp.replace("{", "")
                if tmp == "": codeExists = False

                # skip all the parsing fun if the whole line is a comment
                line = line.replace("//", "#")
                line = line.rstrip("\n")
                if codeExists:
                    # clean up the end of the line so we can easily test the last real char
                    line = line.rstrip(";")
                    line = line.rstrip(" ")
                    line = line.rstrip("\t")

                    # all the easy replacements
                    line = line.replace("->", ".")
                    line = line.replace("::", ".")
                    line = line.replace("Ogre.", "ogre.")
                    line = line.replace("/*", "###")
                    line = line.replace("*/", "###")
                    line = line.replace("true", "True")
                    line = line.replace("false", "False")
                    line = line.replace("\t", "    ")
                    line = line.replace("&&", "and")
                    line = line.replace("||", "or")
                    line = line.replace("NULL", "None")
                    line = line.replace("struct", "class")
                    line = line.replace("case", "if")
                    line = line.replace("ogre.StringConverter.toString",
                                        "str")
                    line = line.replace("ogre.StringConverter.parseInt",
                                        "str")
                    line = line.replace(
                        "ogre.StringConverter.parseBool", "str")

                    # replace ifdef with a regular if else
                    if (line.find("#ifdef") != -1):
                        line = line.strip(" ")
                        var = line.split(" ")[1]
                        line = "if " + var + " == False:"
                    if (line.find("#else") != -1):
                        line = "else:"
                    if (line.find("#endif") != -1):
                        line = ""

                    # if any of these modules are used, add an import statement at the top
                    if (line.lower().find("ogre") != -1) and (
                            ogreImport not in imports):
                        imports.append(ogreImport)
                    if (line.lower().find("ois") != -1) and (
                            oisImport not in imports):
                        imports.append(oisImport)
                    if (line.lower().find("ogrenewt") != -1) and (
                            newtImport not in imports):
                        imports.append(newtImport)
                    if (line.lower().find("cegui") != -1) and (
                            ceguiImport not in imports):
                        imports.append(ceguiImport)

                    if self.debug: print
                    "2: " + line.strip("\n") + "\n-----------"

                # comment out end braces instead of removing them (handy to see where they are)
                line = line.replace("}", "#}")

                # if the line consists of only a sole open brace, add a : to the previous
                # line and skip this line entirely
                if line.strip(" ") == "{":
                    lastLine = lastLine + ":"
                    skipCurrentLine = True

                # write the last line to the buffer
                buffer += lastLine + "\n"

                # set lastLine to the current line for the next iteration
                # unless we just used it to add a :, in which case we just skip it
                if not skipCurrentLine:
                    lastLine = line
                else:
                    lastLine = ""

            file.close()

            # write out the imports we need to the top of the buffer
            importsBuffer = ""
            for imp in imports:
                importsBuffer += imp + "\n"

            buffer = importsBuffer + buffer

            # and write the resulting "python" script to a file
            outputfile = open(targetFile, "w")
            outputfile.write(buffer)
            outputfile.close()

        else:  # if file not found
            raise IOError(0, filename,
                          "The script '" + filename + "' could not be found.")


if __name__ == "__main__":
    parser = CPP2PY()
    parser.convert("ChannelAttribution.cpp", "ChannelAttribution.py")      imports.append(newtImport)
                    if (line.lower().find("cegui") != -1) and (
                            ceguiImport not in imports):
                        imports.append(ceguiImport)

                    if self.debug: print
                    "2: " + line.strip("\n") + "\n-----------"

                # comment out end braces instead of removing them (handy to see where they are)
                line = line.replace("}", "#}")

                # if the line consists of only a sole open brace, add a : to the previous
                # line and skip this line entirely
                if line.strip(" ") == "{":
                    lastLine = lastLine + ":"
                    skipCurrentLine = True

                # write the last line to the buffer
                buffer += lastLine + "\n"

                # set lastLine to the current line for the next iteration
                # unless we just used it to add a :, in which case we just skip it
                if not skipCurrentLine:
                    lastLine = line
                else:
                    lastLine = ""

            file.close()

            # write out the imports we need to the top of the buffer
            importsBuffer = ""
            for imp in imports:
                importsBuffer += imp + "\n"

            buffer = importsBuffer + buffer

            # and write the resulting "python" script to a file
            outputfile = open(targetFile, "w")
            outputfile.write(buffer)
            outputfile.close()

        else:  # if file not found
            raise IOError(0, filename,
                          "The script '" + filename + "' could not be found.")


if __name__ == "__main__":
    parser = CPP2PY()
    parser.convert("ChannelAttribution.cpp", "ChannelAttribution.py")