#!/usr/bin/python

# Set the location of the LightYears .py files here:
LIGHTYEARS_DIR = ""

# Save games and configuration files are stored in the user's
# home directory.


if ( __name__ == "__main__" ):
    import sys, os

    if (( LIGHTYEARS_DIR == None )
    or ( not os.path.exists(LIGHTYEARS_DIR) )):
        # Try current directory
        LIGHTYEARS_DIR = os.path.abspath(
                os.path.dirname(sys.argv[ 0 ]))

    sys.path.insert(0, os.path.join(LIGHTYEARS_DIR, 'code'))

    try:
        import startup
    except:
        print "Unable to find LightYears code in", LIGHTYEARS_DIR
        sys.exit(1)

    startup.Main(os.path.join(LIGHTYEARS_DIR, 'data'))

