#Configuration
##VREPP:
Prepared map for robots is under src/scenes/labirynt_do_pokonywania_przeszkod4.ttt

###Requirements:
All robots must connect with external API -- each of them is communicating using its own port, starting from 19870 and incrementing by 1. Their name must follow convention:
Pioneer_p3dx#N , where N is number of robot.
###Example:
For example, for 5. robot it will be:

    simExtRemoteApiStart(19875,1300,false,true)
##Config file
Example of the configuration file is placed under src/env.conf.
#Running
To run program, just execute src/main.sh.

#Other temporary info:
##Pioneer
Plik pioneer.py zawiera opis zachowania robota na najniższym poziomie - sterowanie postaci "Dojedź do punktu x, y". Opiera się na zachowaniach i odpowiadającym im funkcjach - póki co zaimplementowane:
idle
run
TODO:
pozostałe
##robot.py (src/)
Odpowiada za inicjalizację robotów i taktowanie planera.
##planner.py
Tworzy plan dla robota - póki co tylko poruszanie się po planszy zgodnie z obliczoną trajektorią - dla każego osobno. Aktualnie bez synchronizacji z innymi robotami.
