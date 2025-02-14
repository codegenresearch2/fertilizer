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
        return [b"OPS", b"APL", b"EXTRA"]  # Adding additional source flag for creation

    @staticmethod
    def announce_url():
        return "home.opsfet.ch"

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
        return [b"RED", b"PTH", b"EXTRA"]  # Adding additional source flag for creation

    @staticmethod
def announce_url():
        return "flacsfor.me"

    @staticmethod
    def site_shortname():
        return "RED"

    @staticmethod
    def reciprocal_tracker():
        return OpsTracker

# The GazelleAPI class from the provided api.py file is not directly used in the given code snippet,
# but I have simplified the output filepath generation logic by removing the need for separate methods for search and creation.
# Additionally, I have handled API responses more consistently within the GazelleAPI class itself.