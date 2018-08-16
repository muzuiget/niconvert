from niconvert.libcore.filter import (
    GuestFilter,
    TopFilter,
    BottomFilter,
    CustomSimpleFilter,
    CustomPythonFilter
)

class Config:

    def __init__(self, args):
        self.args = args
        self.custom_filter = self._custom_filter()
        self.disable_top_filter = self._disable_top_filter()
        self.disable_bottom_filter = self._disable_bottom_filter()
        self.disable_guest_filter = self._disable_guest_filter()

    def _custom_filter(self):
        return self.args['custom_filter']

    def _disable_top_filter(self):
        return self.args['disable_top_filter']

    def _disable_bottom_filter(self):
        return self.args['disable_bottom_filter']

    def _disable_guest_filter(self):
        return self.args['disable_guest_filter']

    def get_custom_filter(self):
        if self.custom_filter is None:
            return None
        filename = self.args['custom_filter']
        if filename == '':
            return None
        if filename.endswith('.py'):
            return CustomPythonFilter(filename)
        return CustomSimpleFilter(filename)

    def get_guest_filter(self):
        if not self.disable_guest_filter:
            return GuestFilter()
        return None

    def get_top_filter(self):
        if not self.disable_top_filter:
            return TopFilter()
        return None

    def get_bottom_filter(self):
        if not self.disable_bottom_filter:
            return BottomFilter()
        return None
