class Tracker:
    @staticmethod
    def source_flags_for_search():
        raise NotImplementedError

    @staticmethod
    def source_flags_for_creation():
        raise NotImplementedError

    @staticmethod
    def announce_url():
        raise NotImplementedError

    @staticmethod
    def site_shortname():
        raise NotImplementedError

    @staticmethod
    def reciprocal_tracker():
        raise NotImplementedError

class OpsTracker(Tracker):
    @staticmethod
    def source_flags_for_search():
        return [b"OPS", b"APL"]

    @staticmethod
    def source_flags_for_creation():
        return [b"OPS", b"APL", b""]

    @staticmethod
    def announce_url():
        return "https://home.opsfet.ch/announce"

    @staticmethod
    def site_shortname():
        return "OPS"

    @staticmethod
    def reciprocal_tracker():
        return RedTracker

class RedTracker(Tracker):
    @staticmethod
    def source_flags_for_search():
        return [b"RED", b"PTH"]

    @staticmethod
    def source_flags_for_creation():
        return [b"RED", b"PTH", b""]

    @staticmethod
    def announce_url():
        return "https://flacsfor.me/announce"

    @staticmethod
    def site_shortname():
        return "RED"

    @staticmethod
    def reciprocal_tracker():
        return OpsTracker

# Consistently handle API responses by using the GazelleAPI class
# Simplify output filepath generation logic by removing the need for it in this context