
# cmd ------>type :  "python main.py --input_dir input/ --output_dir output/"
import argparse
import logging
import os
import subprocess
import sys
import json

from constants import DEFAULT_OUTPUT_DIRECTORY_NAME, VALID_IMAGE_EXTENSIONS, WINDOWS_CHECK_COMMAND, \
    DEFAULT_CHECK_COMMAND, TESSERACT_DATA_PATH_VAR

import xmltodict
import io
from collections import OrderedDict
import xmljson
from lxml.etree import fromstring, tostring

'''
def writeToJSONFile(path, fileName, data):
    filename_without_extension = os.path.splitext(fileName)[0]
    filePathNameWExt = path + filename_without_extension + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)
'''


def create_directory(path):
    """
    Create directory at given path if directory does not exist
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def check_path(path):
    """
    Check if file path exists or not
    :param path:
    :return: boolean
    """
    return bool(os.path.exists(path))


def get_command():
    """
    Check OS and return command to identify if tesseract is installed or not
    :return:
    """
    if sys.platform.startswith('win'):
        return WINDOWS_CHECK_COMMAND
    return DEFAULT_CHECK_COMMAND


def run_tesseract(filename, output_path, image_file_name, data, block):
    # Run tesseract

    filename_without_extension = os.path.splitext(filename)[0]
    text_file_path = os.path.join(output_path+"/", filename_without_extension)
    print("Inputted ALTO from : "+image_file_name)
    print("Outptted ALTO to : "+text_file_path)
    '''
    subprocess.run(['tesseract', image_file_name, text_file_path],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)'''
    subprocess.run(['tesseract', image_file_name, text_file_path, "alto"],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)

    #####################################Alto to json ########################################

    print("Now, Parsing XML : " + text_file_path + ".xml")
    with open(text_file_path + ".xml", 'rb') as fd:
        doc = xmltodict.parse(fd.read())
    #xml = fromstring(fd.read())
    #doc = xmljson.badgerfish.data(xml)
    fd.close()
    sarja = text_file_path[0:9]
    textline=""
    try:
        textblock = doc['alto']['Layout']['Page']['PrintSpace']['TextBlock']
        if type(textblock) is list:
        # b means index soho block+++++++++++++++++++++++data list+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            for b in textblock:
                headlineset = 'no'
                line = 1
                if type(b['TextLine']) is list:
                    #+++++++++++++++++++++++Textlines list++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    for l in b['TextLine']:                                                                            #
                        if type(l['String']) is list:                                                                  #
                            for s in l['String']:                                                                      #
                                if len(s['@CONTENT'].strip()) != 0:  # jodi word khali hoy tahle baads                 #
                                    textline += s['@CONTENT']+" "                                                      #
                        else:  # that means OrderedDict, one string inside TextLine                                    #
                            if len(l['String']['@CONTENT'].strip()) != 0:                                              #
                                textline += l['String']['@CONTENT'] + " "                                              #
                        # -----------insert a line to a textblock of many texblocks----------------------s
                        if len(textline.strip()) != 0: # finally line jodi khali hoy                                   #
                            if line == 1:
                                if len(textline.split()) == 1 or len(textline.split()) == 2 or len(textline.split()) == 3:
                                    if headlineset=='no':
                                        headlineset = textline                                                             #
                                        data[headlineset] = {}
                                    else:
                                        data[headlineset][line] = textline                                           #
                                        line += 1                                                       #
                                else:
                                    if headlineset !='no':
                                        data[headlineset][line] = textline                                           #
                                        line += 1
                                    else:
                                        data['textblock'+str(block)] = {}
                                        data['textblock'+str(block)][line] = textline                                                                      #
                                        line += 1
                            else:                                                                                      #
                                if headlineset != 'no':  # headline set
                                    data[headlineset][line] = textline                                           #
                                    line += 1
                                else:
                                    data['textblock'+str(block)][line] = textline                                #
                                    line += 1
                        textline = ""
                    if headlineset == 'no':
                        block +=1                                                                                  #
                    #for+++++++++++++++++++++++Textlines list end+++++++++++++++++++++++++++++++++++++++++++++++++++++++

                else:#+++++++++++++++++++++++Textline is  one (multiple textblock list)+++++++++++++++++++++++++++++++++
                    if type(b['TextLine']['String']) is list:                                                          #
                        for s in b['TextLine']['String']:                                                              #
                            if len(s['@CONTENT'].strip()) != 0:                                                        #
                                textline += s['@CONTENT'] + " "                                                        #
                    else:  # that means OrderedDict, one string inside TextLine
                        if len(b['TextLine']['String']['@CONTENT'].strip()) != 0:                                      #
                            textline += b['TextLine']['String']['@CONTENT'] + " "
                    # ---------ei textline for a textblock with one textline-------#                                   #
                    if len(textline.strip()) != 0:  # finally line jodi khali hoy
                        if len(textline.split()) == 1 or len(textline.split()) == 2 or len(textline.split()) == 3:     #
                            headlineset=textline
                            data[headlineset] = {} #because, only textline is in the textblock                   #
                        else:
                            data['textblock'+str(block)] = {}                                                    #
                            data['textblock'+str(block)][line] = textline
                            block += 1
                        line += 1                                                                                      #
                    textline = ""                                                                                      #
                #+++++++++++++++++++++++Textline is  one (multiple textblock list)++++++++++++++++++++++++++++++++++++++

        #+++++++++++++++++++++++++++++++++++++++++++++++++data list end++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #---------------------------------------------------------------------------------------------------------------else part of block
        #+++++++++++++++++++++++++++++++++++++++++++++++++Textblock is one+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        else:  # that means OrderedDict, textblock is one
            line = 1
            if type(textblock['TextLine']) is list:
                #+++++++++++++++++++++++Textlines list++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                for l in textblock['TextLine']:                                                                            #
                    if type(l['String']) is list:                                                                  #
                        for s in l['String']:                                                                      #
                            if len(s['@CONTENT'].strip()) != 0:  # jodi word khali hoy tahle baads                 #
                                textline += s['@CONTENT']+" "                                                      #
                    else:  # that means OrderedDict, one string inside TextLine                                    #
                        if len(l['String']['@CONTENT'].strip()) != 0:                                              #
                            textline += l['String']['@CONTENT'] + " "                                              #
                    # -----------insert a line to a textblock of many texblocks----------------------s
                    if len(textline.strip()) != 0: # finally line jodi khali hoy                                   #
                        if line == 1:
                            if len(textline.split()) == 1 or len(textline.split()) == 2 or len(textline.split()) == 3:
                                if headlineset=='no':
                                    headlineset = textline                                                             #
                                    data[headlineset] = {}
                                else:
                                    data[headlineset][line] = textline                                           #
                                    line += 1                                                       #
                            else:
                                if headlineset !='no':
                                    data[headlineset][line] = textline                                           #
                                    line += 1
                                else:
                                    data['textblock'+str(block)] = {}
                                    data['textblock'+str(block)][line] = textline                                                                      #
                                    line += 1
                        else:                                                                                      #
                            if headlineset != 'no':  # headline set
                                data[headlineset][line] = textline                                           #
                                line += 1
                            else:
                                data['textblock'+str(block)][line] = textline                                #
                                line += 1
                    textline = ""
                if headlineset == 'no':
                    block +=1                                                                                  #
                #for+++++++++++++++++++++++Textlines list end+++++++++++++++++++++++++++++++++++++++++++++++++++++++

            else:#+++++++++++++++++++++++Textline is  one (multiple textblock list)+++++++++++++++++++++++++++++++++
                if type(b['TextLine']['String']) is list:                                                          #
                    for s in b['TextLine']['String']:                                                              #
                        if len(s['@CONTENT'].strip()) != 0:                                                        #
                            textline += s['@CONTENT'] + " "                                                        #
                else:  # that means OrderedDict, one string inside TextLine
                    if len(b['TextLine']['String']['@CONTENT'].strip()) != 0:                                      #
                        textline += b['TextLine']['String']['@CONTENT'] + " "
                # ---------ei textline for a textblock with one textline-------#                                   #
                if len(textline.strip()) != 0:  # finally line jodi khali hoy
                    if len(textline.split()) == 1 or len(textline.split()) == 2 or len(textline.split()) == 3:     #
                        headlineset=textline
                        data[headlineset] = {} #because, only textline is in the textblock                   #
                    else:
                        data['textblock'+str(block)] = {}                                                    #
                        data['textblock'+str(block)][line] = textline
                        block += 1
                    line += 1                                                                                      #
                textline = ""                                                                                      #
            #+++++++++++++++++++++++Textline is  one (multiple textblock list)++++++++++++++++++++++++++++++++++++++

    #+++++++++++++++++++++++++++++++++++++++++++++++++data list end++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    except KeyError:
        data = {
            'text': 'KeyError'
        }
        with open(output_path + "/" + 'data.json', 'a+') as outfile:
            json.dump(data, outfile, sort_keys=False)
            outfile.write('\n')
        outfile.close()
        data = {}

    return block, data
def check_pre_requisites_tesseract():
    """
    Check if the pre-requisites required for running the tesseract application are satisfied or not
    :param : NA
    :return: boolean
    """
    check_command = get_command()
    logging.debug("Running `{}` to check if tesseract is installed or not.".format(check_command))

    result = subprocess.run([check_command, 'tesseract'], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error(
            "tesseract-ocr missing, install `tesseract` to resolve. Refer to README for more instructions.")
        return False

    logging.debug("Tesseract correctly installed!\n")

    if sys.platform.startswith('win'):
        environment_variables = os.environ
        logging.debug(
            "Checking if the Tesseract Data path is set correctly or not.\n")
        if TESSERACT_DATA_PATH_VAR in environment_variables:
            if environment_variables[TESSERACT_DATA_PATH_VAR]:
                path = environment_variables[TESSERACT_DATA_PATH_VAR]
                logging.debug("Checking if the path configured for Tesseract Data Environment variable `{}` \
                as `{}` is valid or not.".format(TESSERACT_DATA_PATH_VAR, path))
                if os.path.isdir(path) and os.access(path, os.R_OK):
                    logging.debug("All set to go!")
                    return True
                else:
                    logging.error(
                        "Configured path for Tesseract data is not accessible!")
                    return False
            else:
                logging.error("Tesseract Data path Environment variable '{}' configured to an empty string!\
                ".format(TESSERACT_DATA_PATH_VAR))
                return False
        else:
            logging.error("Tesseract Data path Environment variable '{}' needs to be configured to point to\
            the tessdata!".format(TESSERACT_DATA_PATH_VAR))
            return False
    else:
        return True


def main(input_path, output_path, file_type):
    # Check if tesseract is installed or not
    if not check_pre_requisites_tesseract():
        return

    # Check if a valid input directory is given or not
    if not check_path(input_path):
        logging.error("Nothing found at `{}`".format(input_path))
        return
    # Create output directory
    create_directory(output_path)

    # Check if input_path is directory or file
    if os.path.isdir(input_path):

        # Check if input directory is empty or not
        total_file_count = len(os.listdir(input_path))
        if total_file_count == 0:
            logging.error("No files found at your input location")
            return

        # Iterate over all images in the input directory
        # and get text from each image
        other_files = 0
        successful_files = 0

        data = {}
        block=1
        #f2 = open(output_path + "/" + "output.txt", "w")
        logging.info("Found total {} file(s)\n".format(total_file_count))

        for ctr, filename in enumerate(sorted(os.listdir(input_path))):

            logging.debug("Parsing {}".format(filename))
            extension = os.path.splitext(filename)[1]

            if extension.lower() not in VALID_IMAGE_EXTENSIONS:
                other_files += 1
                continue

            image_file_name = os.path.join(input_path, filename)

            block,data= run_tesseract(filename, output_path, image_file_name, data, block)
            successful_files += 1

            '''
            filename_without_extension = os.path.splitext(filename)[0]
            fn = output_path + "/" + filename_without_extension + ".txt"
            f = open(fn, encoding="utf8")
            psk = f.read()
            sk = psk.split("\n")
            for i in sk:
                if(i!=""and i!=" "):
                    f2.write(i)
                    f2.write("\n")


        f2 = open(output_path +"/"+ "output.txt", "r")
        filetolist = f2.read().split("\n")
        '''
        print(output_path+"/"+'data.json')
        with open(output_path + "/" + 'data.json', 'w+') as outfile:
            json.dump(data, outfile, sort_keys=False)
            outfile.write('\n')
        outfile.close()
        data = {}
        #writeToJSONFile(output_path, "New", data)

        logging.info("Parsing Completed!\n")

        if successful_files == 0:
            logging.error("No valid image file found.")
            logging.error("Supported formats: [{}]".format(
                ", ".join(VALID_IMAGE_EXTENSIONS)))
        else:
            logging.info(
                "Successfully parsed images: {}".format(successful_files))
            logging.info(
                "Files with unsupported file extensions: {}".format(other_files))

    else:
        filename = os.path.basename(input_path)
        run_tesseract(filename, output_path, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', help="Input directory where input images are stored")
    parser.add_argument('--input_file', help="Input image filepath")
    parser.add_argument('--output_dir', help="(Optional) Output directory for converted text")
    parser.add_argument('--f', help="(Optional) output file format")
    parser.add_argument('--debug', action='store_true', help="Enable verbose DEBUG logging")

    args = parser.parse_args()
    if not args.input_dir and not args.input_file:
        parser.error('Required either --input_file or --input_dir')

    if args.input_dir:
        input_path = os.path.abspath(args.input_dir)
    else:
        input_path = os.path.abspath(args.input_file)

    if args.f:
        file_type = args.f

    else:
        file_type = "hocr"

    if args.output_dir:
        output_path = os.path.abspath(args.output_dir)
    else:
        if os.path.isdir(input_path):
            output_path = os.path.join(input_path, DEFAULT_OUTPUT_DIRECTORY_NAME)
        else:
            dir_path = os.path.dirname(input_path)
            output_path = os.path.join(dir_path, DEFAULT_OUTPUT_DIRECTORY_NAME)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Check Python version
    if sys.version_info[0] < 3:
        logging.error("You are using Python {0}.{1}. Please use Python>=3".format(
            sys.version_info[0], sys.version_info[1]))
        exit()

    main(input_path, output_path, file_type)
