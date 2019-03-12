#Namespace AppConstants
class AppConstants(object):

    def cableSize(self, current_from_each_machine):
        #return the cable size from a set of defined constants
        cable_values = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95,
        120, 150, 185, 240, 300, 400]
        cable_ranges = [[0, 14], [15, 20], [21, 26], [27, 32], [33, 45],
        [46, 58], [59, 76], [77, 93], [94, 150], [151, 180], [181, 225],
        [226, 260], [261, 290], [291, 340], [341, 400], [401, 460], [461, 520]]
        for i in cable_ranges:
            if i[0] < current_from_each_machine <= i[1]:
                return cable_values[cable_ranges.index(i)]

    def breakerSize(self, current_from_each_machine):
        #return the breaker size from a set of defined constants
        breaker_values = [i for i in range(5, 705, 5)]
        breaker_ranges = [[i-5.5, i-0.5] for i in breaker_values]
        for i in breaker_ranges:
            if i[0] < current_from_each_machine <= i[1]:
                return breaker_values[breaker_ranges.index(i)]

    def lampLumen(self, a):
        data = {
            'Thorn forceLED (120)': 120,
            'Thorn forceLED pro (137)': 137,
            'Tonic Gimbal (100)': 100,
            'HiPak proLED (135)': 135
        }
        return data[a]
