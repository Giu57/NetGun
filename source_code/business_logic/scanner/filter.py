import os

class Filter:
    __TRANSPORT_PROTOCOLS_SUPPORTED = {"tcp":"","udp":"-sU"}

    def __init__(self, transport_protocol: str = "tcp", advanced_options : list[str] = None, aggressivity : int = 2):
        assert transport_protocol in Filter.__TRANSPORT_PROTOCOLS_SUPPORTED, "Invalid Transport Protocol Selected. Use TCP or UDP"
        self.transport_protocol = transport_protocol
        assert Filter.check_aggressivity(aggressivity) == True, "Invalid Threads Number check_threads(threads) failed"
        self.aggressivity = aggressivity
        self.advanced_options = ""

        if advanced_options is not None:
            self.advanced_options += Filter.advanced_options_to_string(advanced_options)

        self.advanced_options += " " + Filter.__TRANSPORT_PROTOCOLS_SUPPORTED[transport_protocol] + " -" + str(aggressivity)



    @classmethod
    def advanced_options_to_string(self, advanced_options : list[str]):
        """Convert the list of advanced options specified in a string that can be used in nmap library"""
        output = ""
        for option in advanced_options:
            output += " -" + option

        return output

    @classmethod
    def check_aggressivity(cls, aggressivity : int):
        """Check if the aggressivity specified is realistic"""
        if aggressivity >= 0 and aggressivity <= 4:
            return True
        else:
            return False