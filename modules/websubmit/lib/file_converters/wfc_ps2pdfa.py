import os
import shutil

from invenio.websubmit_file_converter_utils import InvenioWebSubmitFileConverterError, debug, execute_command
from invenio.config import CFG_ETCDIR, CFG_PATH_GS


CFG_CONVERTER_NEEDS_WORKING_DIR = True

def converter(input_file, output_file, working_dir, title=None, **dummy):
    """
    Transform any PS into a PDF/A (see: <http://www.pdfa.org/>)
    @param input_file [string] the input file name
    @param output_file [string] the output_file file name, None for temporary generated
    @param title [string] the title of the document. None for autodiscovery.
    @param pdfopt [bool] whether to linearize the pdf, too.
    @return [string] output_file input_file
    raise InvenioWebSubmitFileConverterError in case of errors.
    """

    if not title:
        raise InvenioWebSubmitFileConverterError("It's impossible to automatically discover the title. Please specify it as a parameter")

    debug("Extracted title is %s" % title)

    shutil.copy(os.path.join(CFG_ETCDIR, 'websubmit', 'file_converter_templates', 'ISOCoatedsb.icc'), working_dir)
    pdfa_header = open(os.path.join(CFG_ETCDIR, 'websubmit', 'file_converter_templates', 'PDFA_def.ps')).read()
    pdfa_header = pdfa_header.replace('<<<<TITLEMARKER>>>>', title)
    outputpdf = os.path.join(working_dir, 'output_file.pdf')
    open(os.path.join(working_dir, 'PDFA_def.ps'), 'w').write(pdfa_header)
    execute_command(CFG_PATH_GS, '-sProcessColorModel=DeviceCMYK', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dNOOUTERSAVE', '-dUseCIEColor', '-sDEVICE=pdfwrite', '-sOutputFile=output_file.pdf', 'PDFA_def.ps', input_file, cwd=working_dir)
    shutil.move(outputpdf, output_file)
    return output_file

def check_prerequisities():
    return bool(CFG_PATH_GS)

def get_conversion_map():
    return {'.ps' : {'.pdf;pdfa' : {}}}