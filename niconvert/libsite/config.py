from niconvert.libcore.filter import (
    BottomFilter,
    CustomPythonFilter,
    CustomSimpleFilter,
    GuestFilter,
    TopFilter,
)

class Config:

    def __init__(self, args):
        self.args = args

    def get_guest_filter(self):
        if not self.args['guest_filter']:
            return None
        return GuestFilter()

    def get_top_filter(self):
        if not self.args['top_filter']:
            return None
        return TopFilter()

    def get_bottom_filter(self):
        if not self.args['bottom_filter']:
            return None
        return BottomFilter()

    def get_custom_filter(self):
        filename = self.args['custom_filter']
        if filename is None:
            return None
        if filename.endswith('.py'):
            return CustomPythonFilter(filename)
        return CustomSimpleFilter(filename)
