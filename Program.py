class Program:
    def __init__(self, op=None, left=None, right=None):
        self.op = op # Operation Type
        self.left = left # For Sequence: left program
        self.right = right #For Sequence: right program or args
        if op and left and right:
            self.complexity = left.complexity + right.complexity
        elif op:
            self.complexity = 1
        else:
            self.complexity = 0
    def __str__(self):
        if self.op == "Sequence":
            left_op = self.left.op if self.left else "None"
            right_op = self.right.op if self.right else "None"
            return f"Sequence({left_op}, {right_op})"
        elif self.op == "ColorChange":
            return f"ColorChange({self.right[0]}, {self.right[1]})"
        elif self.op == "Mirror":
            return f"Mirror({self.right})"
        elif self.op == "Rotate":
            return f"Rotate({self.right})"
        elif self.op == "Scale2x2":
            return "Scale2x2()"
        elif self.op == "Scale3x3":
            return "Scale3x3()"
        elif self.op == "Scale2x1":
            return "Scale2x1()"
        elif self.op == "Scale1x2":
            return "Scale1x2()"
        elif self.op == "ResizeIrregular":
            return f"ResizeIrregular({self.right[0]}x{self.right[1]})"
        elif self.op == "PositionalShift":
            return f"PositionalShift({self.right[0]}, {self.right[1]}, {self.right[2]}, {self.right[3]})"
        elif self.op == "ColorMapMultiple":
            return f"ColorMapMultiple({dict(self.right)})"
        elif self.op == "ScaleWithColorMap":
            return f"ScaleWithColorMap({self.right[0]}, {dict(self.right[1])})"
        elif self.op == "SwapColors":
            return f"SwapColors({self.right[0]}, {self.right[1]})"
        elif self.op == "DiagonalReflection":
            return f"DiagonalReflection({self.right[0]}, {self.right[1]})"
