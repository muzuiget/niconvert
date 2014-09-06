from ..libcore.utils import intceil


class Collision(object):
    ''' 碰撞处理 '''

    def __init__(self, line_count):
        self.line_count = line_count
        self.leaves = self._leaves()

    def _leaves(self):
        return [0] * self.line_count

    def detect(self, display):
        ''' 碰撞检测

        返回行号和时间偏移
        '''
        beyonds = []
        for i, leave in enumerate(self.leaves):
            beyond = display.danmaku.start - leave
            # 某一行有足够空间，直接返回行号和 0 偏移
            if beyond >= 0:
                return i, 0
            beyonds.append(beyond)

        # 所有行都没有空间了，那么找出哪一行能在最短时间内让出空间
        soon = max(beyonds)
        line_index = beyonds.index(soon)
        offset = -soon
        return line_index, offset

    def update(self, leave, line_index, offset):
        ''' 更新碰撞信息 '''
        self.leaves[line_index] = intceil(leave + offset)
