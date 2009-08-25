from invenio.bibdocfile import normalize_format

CFG_CONVERTER_DOESNT_NEED_WORKING_DIR="CFG_CONVERTER_DOESNT_NEED_WORKING_DIR"
CFG_CONVERTER_NEEDS_WORKING_DIR="CFG_CONVERTER_NEEDS_WORKING_DIR"

class InvenioWebSubmitFileConverterError(Exception):
    """
    This Exception is raised within the WebSubmit File Converter framework
    to signal any error.
    """
    pass

def create_temporary_file(output_ext):
    """
    Return the path to a temporary file ready to be used.
    """
    try:
        (fd, output_file) = tempfile.mkstemp(suffix=output_ext, dir=CFG_TMPDIR)
        os.close(fd)
        return output_file
    except IOError, err:
        raise InvenioWebSubmitFileConverterError("It's impossible to create a temporary file: %s" % err)

def prepare_io(input_file, output_file=None, output_ext=None, need_working_dir=True):
    """Clean input_file and the output_file."""
    from invenio.bibdocfile import decompose_file, normalize_format
    output_ext = normalize_format(output_ext)
    debug('Preparing IO for input=%s, output=%s, output_ext=%s' % (input_file, output_file, output_ext))
    if output_ext is None:
        if output_file is None:
            output_ext = '.tmp'
        else:
            output_ext = decompose_file(output_file, skip_version=True)[2]
    if output_file is None:
        try:
            (fd, output_file) = tempfile.mkstemp(suffix=output_ext, dir=CFG_TMPDIR)
            os.close(fd)
        except IOError, err:
            raise InvenioWebSubmitFileConverterError("It's impossible to create a temporary file: %s" % err)
    else:
        output_file = os.path.abspath(output_file)
        if os.path.exists(output_file):
            os.remove(output_file)

    if need_working_dir:
        try:
            working_dir = tempfile.mkdtemp(dir=CFG_TMPDIR, prefix='conversion')
        except IOError, err:
            raise InvenioWebSubmitFileConverterError("It's impossible to create a temporary directory: %s" % err)

        input_ext = decompose_file(input_file, skip_version=True)[2]
        new_input_file = os.path.join(working_dir, 'input' + input_ext)
        shutil.copy(input_file, new_input_file)
        input_file = new_input_file
    else:
        working_dir = None
        input_file = os.path.abspath(input_file)

    debug('IO prepared: input_file=%s, output_file=%s, working_dir=%s' % (input_file, output_file, working_dir))
    return (input_file, output_file, working_dir)


def clean_working_dir(working_dir):
    """
    Remove the working_dir.
    """
    debug('Cleaning working_dir: %s' % working_dir)
    shutil.rmtree(working_dir)


def execute_command(cwd=None, filename_out=None, filename_err=None, *args):
    """Wrapper to run_process_with_timeout."""
    debug("Executing: %s" % args)
    res, stdout, stderr = run_process_with_timeout(args, cwd=cwd, filename_out=filename_out, filename_err=filename_err)
    if res != 0:
        error("Error when executin %s" % args)
        raise InvenioWebSubmitFileConverterError("Error in running %s\n stdout:\n%s\nstderr:\n%s\n" % (args, stdout, stderr))
    return stdout


def execute_command_with_stderr(cwd=None, filename_out=None, *args):
    """Wrapper to run_process_with_timeout."""
    debug("Executing: %s" % args)
    res, stdout, stderr = run_process_with_timeout(args, cwd=cwd, filename_out=filename_out)
    if res != 0:
        error("Error when executin %s" % args)
        raise InvenioWebSubmitFileConverterError("Error in running %s\n stdout:\n%s\nstderr:\n%s\n" % (args, stdout, stderr))
    return stdout, stderr
