#!/usr/bin/env python3

from World import *
from Swarm import *
from Obstacle import *
from Destination import *
from BoidSwarm import *
from Globals import *
import sys, getopt


def main():
    myWorld = World()
    status = Globals()
    
    verbose = False
    runTime = 0
    worldName = "X"
    totalTime = 0.0
    compressConcave = 0
    perimeter = 0
    physicsMoveTowardsDestination = 0
    physicsFlyTowardsCentre = 0 
    physicsMoveAway = 0
    physicsAvoidObstacle = 0
    physicsMoveTowardsDestination = 0
    physicsCompressConcave = 0
    frameRate = 0
    neighbourDistance = 0
    minDistance = 0
    maxSpeed = 0
    
    status.total_iterations = 0
    status.compressConcave = False
    status.startTime = 0;
    status.energyRecording = True
    status.processing = True    
    status.finiteMachine = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhw:c:p:t:s:m:n:C:R:o:O:D:V:S:", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h","--help"):
            usage()
            sys.exit(0)
        elif o in ("-w"):
            worldName = a

    print("VERSION: %s" % status.version)
            
    if not myWorld.loadWorld(worldName):
        print("+-----------------------+")
        print("| Error World Not Found!|")
        print("+-----------------------+\n")
        usage()
        exit(0)
    print("+-----------------------+")
    print("|     Loaded World      |")
    print("+-----------------------+")
    print("%s Loaded!" % (worldName))
    print("%s Bots" % myWorld.getSwarmSize())
    print("%s Destinations" % myWorld.getDestinationSize())
    print("%s Obstacles" % myWorld.getObstacleSize())
        
    compressConcave = status.compressConcave
    perimeter = status.perimeter
    physicsMoveTowardsDestination = status.physicsMoveTowardsDestination
    physicsFlyTowardsCentre = status.physicsFlyTowardsCentre
    physicsMoveAway = status.physicsMoveAway
    physicsAvoidObstacle = status.physicsAvoidObstacle
    physicsMoveTowardsDestination = status.physicsMoveTowardsDestination
    physicsCompressConcave = status.physicsCompressConcave
    frameRate = status.frameRate
    maxSpeed = status.maxSpeed
    neighbourDistance = status.neighbourDistance
    minDistance = status.minDistance

    for o, a in opts:
        if o in ("-c"):
            compressConcave = int(a)
        elif o in ("-p"):
            perimeter = int(a)
        elif o in ("-s"):
            frameRate = int(a) # sample rate
        elif o in ("-t"):
            runTime = int(a)
        elif o in ("-n"):
            neighbourDistance = int(a)
        elif o in ("-o"):
            obstacleRepulsion = int(a)
        elif o in ("-m"):
            minDistance = int(a)
        elif o in ("-D"):
            physicsMoveTowardsDestination = int(a)
        elif o in ("-C"):
            physicsFlyTowardsCentre = int(a)
        elif o in ("-R"):
            physicsMoveAway = int(a)
        elif o in ("-O"):
            physicsAvoidObstacle = int(a)
        elif o in ("-V"):
            physicsCompressConcave = int(a)
        elif o in ("-S"):
            maxSpeed = int(a)

    status.compressConcave = compressConcave

    status.perimeter = perimeter
    status.physicsMoveTowardsDestination = physicsMoveTowardsDestination
    status.physicsFlyTowardsCentre = physicsFlyTowardsCentre
    status.physicsMoveAway = physicsMoveAway
    status.physicsCompressConcave = physicsCompressConcave
    status.physicsAvoidObstacle = physicsAvoidObstacle
    status.obstacleRepulsion = obstacleRepulsion
    status.frameRate = frameRate
    status.maxSpeed = maxSpeed
    status.neighbourDistance = neighbourDistance
    status.minDistance = minDistance
    status.minDistance = minDistance
    
    status.time_passed_seconds = status.frameRate / 100

    myWorld.swarmObstacleRepel(status.obstacleRepulsion)
    myWorld.swarmSpeed(status.maxSpeed)
    myWorld.swarmNeighbourDistance(status.neighbourDistance)
    myWorld.swarmMinDistance(status.minDistance)

    print("+-----------------------+")
    print("| Simulation Parameters |")
    print("+-----------------------+")
    print("Compress - %s" % (status.compressConcave))
    print("GPS - %s" % (status.perimeterName[status.perimeter]))
    print("Sample Rate - %ss" % (status.time_passed_seconds))
    print("Min Distance - %s Units" % (status.minDistance))
    print("Neighbour Range - %s Units" % (status.neighbourDistance))
    print("Obstacle Range - %s Units" % (status.obstacleRepulsion))
    print("================================")
    print("Destination Physics - %s" % (status.physicsMoveTowardsDestination))
    print("Cohesion Physics - %s" % (status.physicsFlyTowardsCentre))
    print("Repulsion Physics - %s" % (status.physicsMoveAway))
    print("Obstacle Physics - %s" % (status.physicsAvoidObstacle))
    print("Compression Physics - %s" % (status.physicsCompressConcave))
    print("================================")

    if runTime:
        print("Duration - %ss" % (runTime))
        print("================================")
    
    logDate = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    status.logCount = 0;
    status.log.start(logDate,"Swarm.sql")

    while status.processing == True:
        totalTime += status.time_passed_seconds
#        status.frame = status.getFrame()
        print(".",end="")
        sys.stdout.flush()
        myWorld.process()
        if runTime > 0:
            if (totalTime > runTime):
                status.processing = False
    
    logDate = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    status.log.finish(logDate)
    print()
    print("======= COMPLETE =======")


def usage():
    print("Usage:%s [OPTIONS]" % (os.path.basename(__file__)))
    print("-c <compress>")
    print("-p <perimeter>")
    print("-w <world>")
    print("-t <time>")
    print("-d <destination physics>")
    print("-s <sample rate>")
    print("-n <neighbour distance>")
    print("-m <minimum distance>")
    print("-v Verbose")
    print("-h Help")
    print("-D <physicsMoveTowardsDestination>")
    print("-C <physicsFlyTowardsCentre>")
    print("-R <physicsMoveAway>")
    print("-O <physicsAvoidObstacle>")
    print("-V <physicsCompressConcave>")
    print("-S <maxSpeed>")
    print("\ne.g. python3 ./PySwarmWorldCLI.py -w TESTBEDSWARMBIG -c 0 -D 0 -C 5 -R 15 -s 10 -p 2 -n 60 -m 40 -S 20 -t 65\n")
    
if __name__ == "__main__":
    main()  