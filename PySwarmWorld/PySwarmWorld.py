#!/usr/bin/env python3
from World import *
from Swarm import *
from Obstacle import *
from Destination import *
from BoidSwarm import *
from WsnSwarm import *
from Globals import *
import sys

status = Globals()
myWorld = World(status.X,status.Y,"crash.jpg")
myWorld.start()

destination = Destination(myWorld.screen.get_size()[0]/2,myWorld.screen.get_size()[1]/2, True)

myWorld.pushDestination(destination)

status.running = False
status.total_iterations = 0

myWorld.intro()
    
while True:
        
    status.time_passed = myWorld.clock.tick(status.frameRate)
    status.time_passed_seconds = status.time_passed / status.systemSpeed
    status.frame = status.getFrame()
        
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
        if event.type == MOUSEBUTTONDOWN:                
            if event.button == 1:
                x, y = event.pos
                if status.inputMode == 0:
                    if myWorld.getSwarmSize() < status.maxParticipants:
                        if myWorld.collision(x, y):
                            print("Participant Collision at %s,%s" % (x, y))
                        else:    
                            participant = Participant(x, y, status.neighbourDistance, status.minDistance, status.maxDistance, status.maxSpeed, status.sensorRange)
                            myWorld.swarms[0].pushBot(participant)
                            print("ADDED - Participant [%s]-([%s][%s]) Total - [%s]" % (participant.id, participant.x, participant.y, myWorld.getSwarmSize()))
                    else:
                        print("MAX Participants for PySwarm Reached (%s) (NOTE: Includes Deleted and Killed!)" % (status.maxParticipants))                        
                elif status.inputMode == 1:
                    destination = Destination(x, y)
                    myWorld.pushDestination(destination)
                    print("ADDED - Destination [%s,%s][%s]" % (destination.x, destination.y, destination.id))
                else:
                    obstacle = Obstacle(x, y, status.obstacleRepulsion)
                    myWorld.pushObstacle(obstacle)
                    print("ADDED - Obstacle [%s,%s][%s]" % (obstacle.x, obstacle.y, obstacle.id))
                    

            if event.button == 3:
                if status.inputMode == 0:
                    if myWorld.removeParticipant():
                        print("Participant Removed!")
                elif status.inputMode == 1:
                    if myWorld.removeDestination():
                        print("Destination Removed!")
                else:
                    if myWorld.removeObstacle():
                        print("Obstacle Removed!")



        if event.type == KEYDOWN:
            
            shifted = (pygame.key.get_mods() & KMOD_LSHIFT)
            
# DYNAMICS AND PHYSICS KEYS
            if event.key == K_a:
                if shifted:
                    status.sensorRange += 1
                    myWorld.swarmSensorRange(status.sensorRange)
                    print("Sensor Range Increased")
                else:
                    if status.sensorRange > 0:
                        status.sensorRange -= 1
                        myWorld.swarmSensorRange(status.sensorRange)
                        print("Sensor Range Decreased")
                    else:
                        print("Sensor Range at 0")

            if event.key == K_1:
                if shifted:
                    status.neighbourDistance += 1
                    myWorld.swarmNeighbourDistance(status.neighbourDistance)
                    print("Bot Range Increased")
                else:
                    status.neighbourDistance -= 1 
                    myWorld.swarmNeighbourDistance(status.neighbourDistance)
                    print("Bot Range Decreased")
                    
            if event.key == K_2:
                if shifted:
                    status.minDistance += 1
                    myWorld.swarmMinDistance(status.minDistance)
                    print("Bot Closeness Increased")
                else:
                    status.minDistance -= 1
                    myWorld.swarmMinDistance(status.minDistance)
                    print("Bot Closeness Decreased")
                    
            if event.key == K_3:
                if shifted:
                    if ((status.maxSpeed + 1) < 1000.0):
                        status.maxSpeed += 1
                    else:
                        status.maxSpeed = 1000
                    myWorld.swarmSpeed(status.maxSpeed)
                    print("Bot Max Speed Increased")
                else:
                    if status.maxSpeed > 1:
                        status.maxSpeed -= 1
                    else:
                        status.maxSpeed = 0
                    myWorld.swarmSpeed(status.maxSpeed)
                    print("Bot Max Speed Decreased")

            if event.key == K_4:
                if shifted:
                    if ((status.obstacleRepulsion + 1) < 1000):
                        status.obstacleRepulsion += 1
                    else:
                        status.obstacleRepulsion = 1000
                    myWorld.swarmObstacleRepel(status.obstacleRepulsion)
                    print("Obstacle Repulsion Increased")
                else:
                    if status.obstacleRepulsion > 1:
                        status.obstacleRepulsion -= 1
                    else:
                        status.obstacleRepulsion = 0
                    myWorld.swarmObstacleRepel(status.obstacleRepulsion)
                    print("Obstacle Repulsion Decreased")

            if event.key == K_5:
                if shifted:
                    if status.processing:
                        print("Cannot change Sample Rate when Processing")
                    else:
                        if (status.sampleRate + 1) > status.frameRate:
                            status.sampleRate = status.frameRate
                            print("Sample Rate at Maximum")
                        else:
                            status.sampleRate += 1
                            print("Sample Rate Increased")
                else:
                    if status.processing:
                        print("Cannot change Sample Rate when Processing")
                    else:
                        if status.sampleRate > 1:
                            status.sampleRate -= 1
                            print("Sample Rate Decreased")
                        else:
                            print("Sample Rate Must be at least 1")

            if event.key == K_6:
                if shifted:
                    if status.processing:
                        print("Cannot change Frame Rate when Processing")
                    else:
                        status.frameRate += 1
                        status.frame = 0
                        print("Frame Rate Increased")
                else:
                    if status.processing:
                        print("Cannot change Frame Rate when Processing")
                    else:
                        if status.frameRate > 1:
                            status.frameRate -= 1
                            if status.sampleRate > status.frameRate:
                                status.sampleRate = status.frameRate
                            status.frame = 0
                            print("Frame Rate Decreased")
                        else:
                            print("Frame Rate Must be at least 1")

            if event.key == K_7:
                if shifted:
                    status.physicsFlyTowardsCentre += 1
                    print("Physics Fly Way Increased")
                else:
                    status.physicsFlyTowardsCentre -= 1
                    print("Physics Fly Way Decreased")

            if event.key == K_8:
                if shifted:
                    status.physicsMoveAway += 1
                    print("Physics Repulsion Increased")
                else:
                    status.physicsMoveAway -= 1
                    print("Physics Repulsion Decreased")
                    
            if event.key == K_9:
                if shifted:
                    status.physicsAvoidObstacle += 1
                    print("Physics Obstacle Repulsion Increased")
                else:
                    status.physicsAvoidObstacle -= 1
                    print("Physics Obstacle Repulsion Decreased")

            if event.key == K_0:
                if shifted:
                    status.physicsMoveTowardsDestination += 1
                    print("Physics Destination Cohesion Increased")
                else:
                    status.physicsMoveTowardsDestination -= 1
                    print("Physics Destination Cohesion Decreased")

            if event.key == K_MINUS:
                if shifted:
                    status.physicsCompressConcave += 1
                    print("Concave Compress Increased")
                else:
                    status.physicsCompressConcave -= 1
                    print("Concave Compress Decreased")

            if event.key == K_r:
                if shifted:                
                    status.neighbourRender = not status.neighbourRender
                    if status.neighbourRender:
                        print("NEIGHBOUR RENDER ENABLED")
                    else:
                        print("NEIGHBOUR RENDER DISABLED")
                else:
                    status.rangeRender = not status.rangeRender
                    if status.rangeRender:
                        print("RANGE RENDER ENABLED")
                    else:
                        print("RANGE RENDER DISABLED")
                            
            if event.key == K_v:
                status.sensorRender = not status.sensorRender
                if status.sensorRender:
                    print("SENSOR RENDER ENABLED")
                else:
                    print("SENSOR RENDER DISABLED")

            if event.key == K_z:
                status.compressConcave = not status.compressConcave
                if status.compressConcave:
                    print("COMPRESS ENABLED")
                else:
                    print("COMPRESS DISABLED")

            if event.key == K_x:
                if status.perimeter == status.perimeterMax:
                    status.perimeter = 0
                else:
                    status.perimeter += 1
                if status.perimeter > 0:
                    print("PERIMETER ENERGY ENABLED")
                else:
                    print("PERIMETER ENERGY DISABLED")
                             
    # OPERATION KEYS
            if event.key == K_i:
                if status.instructions == 2:
                    status.instructions = 0
                else:
                    status.instructions += 1
                if status.instructions > 0:
                    print("INSTRUCTIONS ENABLED")
                else:
                    print("INSTRUCTIONS DISABLED")

            elif event.key == K_n:
                if status.screenMode == 1:
                    status.screenMode = 0
                    print("SCREEN NORMAL")                    
                else:
                    status.screenMode += 1
                    print("SCREEN NEGATED")

            elif event.key == K_e:
                if status.processing:
                    print("CANNOT CHANGE ENERGY CONSUMPTION LOGGING DURING PROCESSING")
                else:
                    status.energyRecording = not status.energyRecording
                    if status.energyRecording:
                        logDate = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
                        status.startTime = 0;
                        status.logCount = 0;
                        status.log.start(logDate,"Swarm.sql")
                        print("RECORDING ENERGY CONSUMPTION")
                    else:
                        logDate = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
                        status.log.finish(logDate)
                        print("RECORDING ENERGY CONSUMPTION STOPPED")
                    
            elif event.key == K_p:
                if divmod(status.frameRate,status.sampleRate)[1] == 0:
                    status.processing = not status.processing
                    if status.processing:
                        print("PROCESSING ENABLED")
                    else:
                        print("PROCESSING DISABLED")
                else:
                    print("ERROR : Frame Rate must be divisable by Sample Rate")

            elif event.key == K_b:
                status.background = not status.background
                if status.background:
                    print("BACKGROUND ENABLED")
                else:
                    print("BACKGROUND DISABLED")

            elif event.key == K_f:
                status.finiteMachine = not status.finiteMachine
                if status.finiteMachine:
                    print("FINITE ENABLED")
                else:
                    print("FINITE DISABLED")

            elif event.key == K_m:
                if status.inputMode == 2:
                    status.inputMode = 0
                else:
                    status.inputMode += 1
                    
            elif event.key == K_c:
                myWorld.clearDestinations()
                myWorld.clearObstacles()
                myWorld.clearSwarms()
                print("SWARM RESET")
                            
            elif event.key == K_q:
                exit()

            elif event.key == K_l:
                status.processing = False
                print("Load World\n")
                print("Available Worlds\n")
                print("================\n")
                print(myWorld.worldList())
                print("================\n")
                worldName = input("World Name:")
                if len(worldName) > 1:
                    if myWorld.loadWorld(worldName):
                        print("World Loaded!")
                    else:
                        print("World Not Found!")
                else:
                    print("Loading World Cancelled!")
                    
                     
            elif event.key == K_s:
                status.processing = False
                print("Save World (NOTE: Will overwrite existing world!)\n")
                print("Available Worlds\n")
                print("================\n")
                print(myWorld.worldList())
                print("================\n")
                worldName = input("World Name:")
                if len(worldName) > 1:
                    if myWorld.saveWorld(worldName):
                        print("World Saved!")
                    else:
                        print("Error Saving World!")
                else:
                    print("Saving World Cancelled!")
                    
            elif event.key == K_g:
                if myWorld.snapshot():
                    print("Snapshot Taken!")
                else:
                    print("Snapshot Failed!")
                    
            pygame.event.clear()
                        
    myWorld.process()
    if (status.processing == False or (status.processing == True and status.render == True)):
        myWorld.render()


