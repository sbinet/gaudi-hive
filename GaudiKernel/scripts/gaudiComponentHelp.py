#!/usr/bin/env python
"""
Print help messages for gaudi components
"""
from Gaudi import Configuration
import os, sys

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(prog = os.path.basename(sys.argv[0]), usage = "%prog [options] ")
    parser.add_option("-l", "--list", action="store_true", dest="list", default = False, help="list all available components.")
    parser.add_option("-n", "--name", action="store", dest="name", help="dump all info about component of given name.")
    parser.set_defaults(root = os.path.join("..","python"))
    opts, args = parser.parse_args()

    cfgDb = Configuration.cfgDb 
    if opts.list:
        print "Available components:\n%s" %(21*"=") 
        for item in sorted(cfgDb):
            print "  %s (from %s)" %(item, cfgDb[item]["lib"]) 
        sys.exit()
    elif opts.name:
        name = opts.name
        if name not in cfgDb:
            print "Component %s not found." %(name)
            sys.exit()
        print "\nDumping component information for %s:\n%s" %(name, (35 + len(name))*"=")
        print "  Library: %s" %(cfgDb[name]["lib"])
        print "  Package: %s" %(cfgDb[name]["package"])
        print "\nProperties:\n%s" %(11*"-")
        try:
          properties = getattr(Configuration,name)().getPropertiesWithDescription()
        except AttributeError:
          print "  Not a configurable component. No properties to show." 
          sys.exit()  
        for label, (value, desc) in properties.iteritems():
            print ("  %s\t : %s\t (%s) " %(label, value, str(desc).replace("None", " no description ") )).expandtabs(30)
        sys.exit()
