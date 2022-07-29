import struct
import math

import TBT_Utils as tbtu

# defines
BYTE_ARRAY_SIZE = 296


class SimulatorPacketGT7:
    # Position on the Track
    testibf : int
    Posit : float
    Position : float
    #= [0.0, 0.0, 0.0]

    # Rotation (Pitch/Yaw/Roll) from -1 to 1.
    Acceleration = [0.0, 0.0, 0.0]

    # Rotation (Pitch/Yaw/Roll) from -1 to 1.
    Rotation = [0.0, 0.0, 0.0]
    RelativeOrientationToNorth = 0.0
    Unknown_0x2C = [0.0, 0.0, 0.0]
    Unknown_0x38 = 0.0
    
    RPM = 0.0

    # Stays at 100, not fuel, nor tyre wear
    Unknown_0x48 = 0.0
    MetersPerSecond = 0.0

    # Value below 1.0 is below 0 ingame, so 2.0 = 1 x 100kPa

    TurboBoost = 0.0
    Unknown_0x54 = 0.0

    # Game will always send this.
    Unknown_Always85_0x58 = 0.0
    Unknown_Always110_0x5C = 0.0

    TireSurfaceTemperatureFL = 0.0
    TireSurfaceTemperatureFR = 0.0
    TireSurfaceTemperatureRL = 0.0
    TireSurfaceTemperatureRR = 0.0

    # Can't be more than 1000 laps worth - which is 1209599999, or else it's set to -1
    TotalTimeTicks = 0
    LapCount = 0
    LapsInRace = 0

    BestLapTime = 0
    LastLapTime = 0
    DayProgressionMS = 0

    # Needs more investigation
    PreRaceStartPositionOrQualiPos = 0
    NumCarsAtPreRace = 0

    MinAlertRPM = 0
    MaxAlertRPM = 0

    CalculatedMaxSpeed = 0

    Flags = 0
    CurrentGear = 0
    SuggestedGear = 0

    Throttle = 0
    Brake = 0

    TireFL_Unknown0x94_0 = 0.0
    TireFR_Unknown0x94_1 = 0.0
    TireRL_Unknown0x94_2 = 0.0
    TireRR_Unknown0x94_3 = 0.0

    TireFL_RevPerSecond = 0.0
    TireFR_RevPerSecond = 0.0
    TireRL_RevPerSecond = 0.0
    TireRR_RevPerSecond = 0.0

    TireFL_TireRadius = 0.0
    TireFR_TireRadius = 0.0
    TireRL_TireRadius = 0.0
    TireRR_TireRadius = 0.0

    TireFL_SusHeight = 0.0
    TireFR_SusHeight = 0.0
    TireRL_SusHeight = 0.0
    TireRR_SusHeight = 0.0

    # Seems to be related to assist, set to 1 when shifting, or handbraking
    Unknown_0xF4 = 0.0

    # The opposite? 0 instead of 1 - when this is set, RPM is set for the next value
    Unknown_0xF8 = 0.0

    # Depends on 0xF8
    RPMUnknown_0xFC = 0.0
    Unknown_0x100_GearRelated = 0.0
    GearRatios = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    CarCode = 0


# Function to print out the data structure
#
#
def printStatus(packet : SimulatorPacketGT7, showUnknown):
#    Console.SetCursorPosition(0, 0);
    print("Simulator Interface Packet")
    print("[Car Data]")
    print('- Car Code: ' + str(packet.CarCode) )
    print('- Throttle: ' + str(packet.Throttle) )
    print('- Brake: ' + str(packet.Brake) )
    print('- RPM: ' + str(packet.RPM) )
    print('- KPH: ' + str(( packet.MetersPerSecond) * 3.6) )
    print('- Turbo Boost: ' + str((( packet.TurboBoost) -1.0 ) * 100.0) + ':F2}kPa')

    if packet.SuggestedGear == 15:
        print('- Gear: ' + str(packet.CurrentGear) )
    else:
        print('- Gear: ' + str(packet.CurrentGear) + ' - Suggested: ' + str(packet.SuggestedGear) )

    print('- Flags: {packet.Flags,-100}')
    print('- Tires')
    print('    FL:' + str(packet.TireSurfaceTemperatureFL)[0:5] + ' FR:' + str(packet.TireSurfaceTemperatureFR)[0:5] )
    print('    RL:' + str(packet.TireSurfaceTemperatureRL)[0:5] + ' RR:' + str(packet.TireSurfaceTemperatureRR)[0:5] )

    print()
    print('[Race Data]')

    print('Timne ticks: ', packet.TotalTimeTicks[0] )
    ts_time = tbtu.TBT_TimeFormatter(packet.TotalTimeTicks[0] * 1000 / 60 )
    ts_time_str = str(ts_time.hours)[:2] +':'+ str(ts_time.minutes)[:2] +':'+ str(ts_time.seconds)[:2]
    print('- Total Session Time: ', ts_time_str )

    print('- Current Lap: ' + str(packet.LapCount) )

#    if (packet.BestLapTime.TotalMilliseconds == -1):
#        print("- Best: N/A      ")
#    else:
#       print("- Best: {packet.BestLapTime:mm\\:ss\\.fff}     ")

    if (packet.LastLapTime == -1):
        print("- Last: N/A      ")
    else:
        last_lap_time = tbtu.TBT_TimeFormatter(packet.LastLapTime)
        last_lap_str = str(last_lap_time.getMinutes())[:2] +':'+ str(last_lap_time.getSeconds())[:2] +'.'+ str(last_lap_time.getMillis())[:3]
        print('- Last: ',  last_lap_str) # {packet.LastLapTime:mm\\:ss\\.fff}     ")

    time_of_day = tbtu.TBT_TimeFormatter(packet.DayProgressionMS)
    tod_str = str(time_of_day.hours)[:2] +':'+ str(time_of_day.minutes)[:2] +':'+ str(time_of_day.seconds)[:2]
    print('- Time of Day: ', tod_str) #{TimeSpan.FromMilliseconds(packet.DayProgressionMS):hh\\:mm\\:ss}     ");

    print()
    print('[Positional Information]')
    print('- Position: ' + str(packet.Position) )
    print('- Accel: ' + str(packet.Acceleration) )
    print('- Rotation: ' + str(packet.Rotation) )

    if showUnknown  == True:
        print()
        print("[Unknowns]")
        print("0x2C (Vec3): {packet.Unknown_0x2C:F2}   ")
        print("0x38 (Float): {packet.Unknown_0x38:F2}   ")
        print("0x48 (Float): {packet.Unknown_0x48:F2}   ")
        print("0x54 (Float): {packet.Unknown_0x54:F2}   ")
        print("0x94 (Float): {packet.TireFL_Unknown0x94_0:F2} {packet.TireFR_Unknown0x94_1} {packet.TireRL_Unknown0x94_2} {packet.TireRR_Unknown0x94_3}   ");
        print("0xB4 (Float): {packet.TireFL_TireRadius:F2} {packet.TireFR_TireRadius} {packet.TireRL_TireRadius} {packet.TireRL_TireRadius}   ");
        print("0xC4 (Float): {packet.TireFL_SusHeight:F2} {packet.TireFR_SusHeight} {packet.TireRL_SusHeight} {packet.TireRL_SusHeight}   ");

        print("0xF4 (Float): {packet.Unknown_0xF4:F2}   ")
        print("0xF8 (Float): {packet.Unknown_0xF8:F2}   ")
        print("0xFC (Float): {packet.RPMUnknown_0xFC:F2}   ")


# Function to Read the raw decryped data mess   age packet and construct the data structure for output
#
#
def readData(data : bytes):
    sr = data

    # temporary
    # print('Data is:')
    # loopCounter = 0
    # while loopCounter < BYTE_ARRAY_SIZE:
    #     print(loopCounter, sr[loopCounter])
    #     loopCounter += 1


    dataPacket = SimulatorPacketGT7()
    bytePos = 0

    magic_num = int.from_bytes(sr[0:4], byteorder='little')
 #   print("Magic number: ", magic_num, type(magic_num))
    bytePos += 4

    dataPacket.Position = [ struct.unpack('f', sr[bytePos:bytePos + 4])[0], struct.unpack('f', sr[bytePos+4:bytePos+8]  ), struct.unpack('f', sr[bytePos+8:bytePos+12]) ]
    # Coords to track
    bytePos += 12
    dataPacket.Acceleration = [ struct.unpack('f', sr[bytePos:bytePos + 4]), struct.unpack('f', sr[bytePos+4:bytePos+8]), struct.unpack('f', sr[bytePos+8:bytePos+12]) ]
    # Accel in track pixel
    bytePos += 12
    dataPacket.Rotation = [ struct.unpack('f', sr[bytePos:bytePos + 4]), struct.unpack('f', sr[bytePos+4:bytePos+8]), struct.unpack('f', sr[bytePos+8:bytePos+12]) ]
    # Pitch/Yaw/Roll all -1 to 1
    bytePos += 12
    dataPacket.RelativeOrientationToNorth = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.Unknown_0x2C = [ struct.unpack('f', sr[bytePos:bytePos + 4]), struct.unpack('f', sr[bytePos+4:bytePos+8]), struct.unpack('f', sr[bytePos+8:bytePos+12]) ]
    bytePos += 12
    dataPacket.Unknown_0x38 = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.RPM = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
 
    # Skip IV
    bytePos += 8

    # get other values
    dataPacket.Unknown_0x48 = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.MetersPerSecond = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.TurboBoost = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.Unknown_0x54 = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.Unknown_Always85_0x58 = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.Unknown_Always110_0x5C = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.TireSurfaceTemperatureFL = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.TireSurfaceTemperatureFR = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.TireSurfaceTemperatureRL = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4
    dataPacket.TireSurfaceTemperatureRR = struct.unpack('f', sr[bytePos:bytePos + 4])[0]
    bytePos += 4    

    dataPacket.TotalTimeTicks = struct.unpack('i', sr[bytePos:bytePos + 4]) # can't be more than MAX_LAPTIME1000 - which is 1209599999, or else it's set to -1
    bytePos += 4
    dataPacket.LapCount = struct.unpack('H', sr[bytePos:bytePos + 2])[0]
    bytePos += 2
    dataPacket.LapsInRace = struct.unpack('H', sr[bytePos:bytePos + 2])[0]
    bytePos += 2
    dataPacket.BestLapTime = struct.unpack('i', sr[bytePos:bytePos + 4])[0]         # int32
    bytePos += 4
    dataPacket.LastLapTime = struct.unpack('i', sr[bytePos:bytePos + 4])[0]         # int32
    bytePos += 4
    dataPacket.DayProgressionMS = struct.unpack('I', sr[bytePos:bytePos + 4])[0]    # uint32
    bytePos += 4
    dataPacket.PreRaceStartPositionOrQualiPos = struct.unpack('H', sr[bytePos:bytePos + 2])[0]
    bytePos += 2
    dataPacket.NumCarsAtPreRace = struct.unpack('H', sr[bytePos:bytePos + 2])[0]
    bytePos += 2
    dataPacket.MinAlertRPM = struct.unpack('H', sr[bytePos:bytePos + 2])[0]
    bytePos += 2
    dataPacket.MaxAlertRPM = struct.unpack('H', sr[bytePos:bytePos + 2])[0]
    bytePos += 2
    dataPacket.CalculatedMaxSpeed = struct.unpack('H', sr[bytePos:bytePos + 2])[0]
    bytePos += 2

#    dataPacket.Flags = (SimulatorFlags)sr.ReadInt16();
    bytePos += 2

 #   bits = struct.unpack('B', sr[bytePos:bytePos + 1])
    bits  = int.from_bytes(sr[bytePos:bytePos + 1], byteorder='little')
    bytePos += 1
    dataPacket.CurrentGear = bits & 0b1111
    dataPacket.SuggestedGear = bits >> 4

    dataPacket.Throttle = struct.unpack('B', sr[bytePos:bytePos + 1])[0]
    bytePos += 1
    dataPacket.Brake = struct.unpack('B', sr[bytePos:bytePos + 1])[0]
    bytePos += 1

    # Jump to car code
    bytePos = 296 - 4   # 
    dataPacket.CarCode = struct.unpack('I', sr[bytePos:bytePos + 4])[0]

    return dataPacket

