PROGRAM_NAME=fds
# The default number of MPI processes is 1
N_PROCESSES=1
TEMP=$(getopt --name $PROGRAM_NAME --options hvn: --longoptions help,version -- "$@")

if [ $? -ne 0 ]; then
        echo "Error parsing arguments. Try $PROGRAM_NAME --help"
        exit
fi

usage() {
    printf "usage: fds [--version] [--help] <FDS-FILE>\n\n"
    printf "options:\n"
    printf "    -h/--help     Show this information.\n"
    printf "    -v/--version  Show version.\n"
    printf "    -n/--version  Set the number of MPI processes.\n"
}

eval set -- "$TEMP"
while true; do
        case $1 in
                -h|--help)
                        usage
                        exit 0
                ;;
                -v|--version)
                        printf "%s %s\n" "$PROGRAM_NAME" "$PROGRAM_VERSION"
                        exit 0
                ;;
                -n)
                        N_PROCESSES="$2"; shift 2; continue
                ;;
                --)
                        # End of options
                        break
                ;;
                *)
                        printf "Unknown option %s\n" "$1"
                        exit 1
                ;;
        esac
done
set "$@"
. /opt/intel/oneapi/setvars.sh
exec mpiexec -np "$N_PROCESSES" "$FDS_EXEC" "$@"