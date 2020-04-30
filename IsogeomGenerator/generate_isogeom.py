import argparse
import vol as v

def parse_arguments():
    """parse user args
    """

    parser = argparse.ArgumentParser(description="Generate isosurface geometry from a Cartesian mesh with VisIt and MOAB")

    # select mode: start-to-finsih, VisIt only, MOAB only
    parser.add_argument('-M', '--mode',
                        action = 'store',
                        nargs = 1,
                        choices = ['full', 'visit', 'moab'],
                        default = 'full',
                        required = False,
                        metavar = 'MODE',
                        dest = 'mode',
                        type = str,
                        help = "Mode for generating geometry:\n" +\
                                "    full (default): start-to-finish generation " +\
                                "from a Cartesian mesh file to a " +\
                                "DAGMC-compliant geometry.\n" +\
                                "    visit: only generate the isosurface meshes using VisIt.\n" +\
                                "    moab: only generate the geometry with MOAB starting from the VisIt mesh files."
                        )

    parser.add_argument('-f', '--filename',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'MESH_FILENAME',
                        dest = 'mesh_file',
                        type = str,
                        help = 'Relative path to the cartesian mesh file used to generate isosurfaces. ' +\
                            'Required for full mode or visit-only mode.'
                        )

    parser.add_argument('-d', '--data',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'NAME',
                        dest = 'data',
                        type = str,
                        help = 'String representing the name of the data on the Cartesian ' +\
                            'mesh file used to generate the isosurfaces. ' +\
                            'Required for full mode or visit-only mode.',
                        )

    parser.add_argument('-lv', '--levelvalues',
                        action = 'store',
                        nargs = '+',
                        required = False,
                        default = None,
                        metavar = 'VAL1 VAL2 ...',
                        dest = 'levels',
                        type = float,
                        help = 'List of values used to generate isosurfaces in VisIt. ' +\
                            'Not required for full or visit-only modes if levels are not generated or provided from a file. ' +\
                            'Only required for moab-only mode if levels are not provided in a file.'
                        )
    parser.add_argument('-lf', '--levelfile',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'LEVELS_FILE',
                        dest = 'level_file',
                        type = str,
                        help = 'Relative path to file containing values to use for the isosurface levels. ' +\
                            'File should be structured to have one value (float) per line.'
                        )
    parser.add_argument('-gl', '--generatelevels',
                        action = 'store',
                        nargs = 1,
                        choices = [None, 'ratio', 'log', 'lin'],
                        required = False,
                        default = None,
                        metavar = 'LEVEL_GEN_MODE',
                        dest = 'levelgenmode',
                        type = str,
                        help = 'If set, specifies the mode for generating ' +\
                            'level values to be used for the isosurfaces in ' +\
                            'full mode or visit-only mode.\n' +\
                            'If used, values for the min level (-lmin), ' +\
                            'max level (-lmax), and the ratio or number of levels (-N) ' +\
                            'are also required.\n' +\
                            'Only required if level values are not assigned (-lv) or provided in a file (-lf). \n' +\
                            'Options:\n' +\
                            '    ratio: N is the ratio between levels ranging from the min value upto, but not exceeding, the max value.\n' +\
                            '    log: N is the number of levels to be evenly spaced logarithmically between the min and max values.\n' +\
                            '    log: N is the number of levels to be evenly spaced linearly between the min and max values.'
                        )

    parser.add_argument('-lmin', '--levelmin',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'MIN_VAL',
                        dest = 'minN',
                        type = float,
                        help = 'float, minimum value to use for generating set ' +\
                            'of level values to be used for the isosurfaces. ' +\
                            'Only required if generating levels for full mode or visit-only mode. ' +\
                            'If used, must also provide a maximum value (-lmax).'
                        )

    parser.add_argument('-lmax', '--levelmax',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'MAX_VAL',
                        dest = 'maxN',
                        type = float,
                        help = 'float, maximum value to use for generating set ' +\
                            'of level values to be used for the isosurfaces. ' +\
                            'Only required if generating levels for full mode or visit-only mode. ' +\
                            'If used, must also provide a minimum value (-lmin).'
                        )

    parser.add_argument('-N', '--numlevels',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'N',
                        dest = 'N',
                        type = float,
                        help = 'If generating levels (-gl), it is either ' +\
                            'the ratio between adjacent level values (ratio mode), ' +\
                            'or the number of levels to generate (log or lin mode).'
                        )

    parser.add_argument('-db', '--database',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = "/tmp",
                        metavar = 'PATH',
                        dest = 'db',
                        type = str,
                        help = 'Relative path to folder for isosurface meshfiles. ' +\
                            'In full mode, it is where isosurface files will written ' +\
                            'to from Visit and read from for creating the geometry. ' +\
                            'In visit only mode, this is where files will be written. ' +\
                            'In moab only mode, this is where files will be read from. ' +\
                            'Default is a folder named tmp/ in the current directory.'
                        )

    parser.add_argument('-m', '--mergetol',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = 1e-5,
                        metavar = 'MERGE_TOL',
                        dest = 'mergetol',
                        type = float,
                        help = 'Merge tolerance for mesh based merging of ' +\
                            'coincident surfaces. Default=1e-5.'
                        )

    parser.add_argument('-n', '--norm',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = 1,
                        metavar = 'NORM_FACTOR',
                        dest = 'norm',
                        type = float,
                        help = 'All level values will be multiplied by this normalization factor ' +\
                            'when the geometry is generated. Default=1'
                        )

    parser.add_argument('-v', '--viz',
                        action = 'store_true',
                        required = False,
                        dest = 'tagviz',
                        help = 'If set, surfaces generated in full or moab-only mode ' +\
                            'will be tagged with data for visualization purposes.'
                        )

    parser.add_argument('-wl', '--writelevels',
                        action = 'store_true',
                        required = False,
                        dest = 'writelevels',
                        help = 'If set, values used for generating isosurfaces ' +\
                            'in full or visit-only mode will be written to a file named levels.txt ' +\
                            'in the database folder. ' +\
                            'File can then be read in with the --levelfile argument.'
                        )

    parser.add_argument('-tv', '--tagval',
                        action = 'append',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'TAG_VAL',
                        dest = 'tagvals',
                        type = float,
                        help = 'Use with --tagname. Value will be assigned to ' +\
                            'a MOAB tag on the geometry whose name corresponds to --tagname specified. ' +\
                            'Option can be used multiple times for multiple tags. ' +\
                            'The number of times this option is used must match the number of times --tagname is used.'
                        )

    parser.add_argument('-tn', '--tagname',
                        action = 'append',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'TAG_NAME',
                        dest = 'tagnames',
                        type = str,
                        help = 'Use with --tagval. Name will be used to create ' +\
                            'a MOAB tag on the geometry with this name whose value ' +\
                            'is the corresponding --tagval. ' +\
                            'Option can be used multiple times for multiple tags. ' +\
                            'The number of times this option is used must match the number of times --tagval is used.'
                        )

    parser.add_argument('-g', '--geomfile',
                        action = 'store',
                        nargs = 1,
                        required = False,
                        default = None,
                        metavar = 'GEOM_FILENAME',
                        dest = 'geomfile',
                        type = str,
                        help = 'Filename and relative path to write generated isosurface geometry file. ' +\
                            'Must be either a .h5m or .vtk file name. Default name is geom-DATA.h5m ' +\
                            'where DATA is the name of data specified by -d if provided. ' +\
                            'If not provided, then default is geom.h5m' +\
                            'Default location is the database location (-db).'
                        )

    args = parser.parse_args()
    return args


def check_levels(args):
    if args.levels != None:
        return True
    if args.level_file != None:
        return True
    if args.levelgenmode in ['ratio', 'log', 'lin']:
        if args.minN == None or args.maxN == None or args.N == None:
            return False
        else:
            return True
    return False


def no_info_error(item, f1, f2):
    message = "No {} provided. Please provide with {} or {}.".format(item, f1, f2)
    raise RuntimeError(message)


def level_error():
    raise RuntimeError("Incompatible or incomplete level information provided.")


def check_full_visit_args(args):
    """If mode is full mode (start to finish) or visit only mode, check
    the required input arguments. Does not check the validity of other
    optional arguments.
    """
    if args.mesh_file == None:
        no_info_error("Cartesian mesh file", "-f", "--filename")
    if args.data == None:
        no_info_error("data name", "-d", "--data")
    res = check_levels(args)
    if res == False:
        level_error()


def check_moab_args(args):
    """Check that required arguments for the moab-only mode have been
    provided. Does not check for optional arguments.
    """
    res = check_levels(args)
    if res == False:
        level_error()


def check_arguments(args):
    """Check that the user has provided valid combinations of arguments
    to perform tasks.
    """
    # check full mode
    if args.mode in ['full', 'visit']:
        check_full_visit_args(args)

    # check moab only mode
    if args.mode == 'moab':
        check_moab_args(args)

def main():

    args = parse_arguments()
    check_arguments(args)


if __name__ == "__main__":
    main()
