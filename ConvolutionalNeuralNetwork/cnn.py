class CNN:
    def convolution(self, grid, kernel, stride):
        self.pad(grid, len(kernel), len(kernel[0]), stride)
        return [[sum([grid[a + i*stride][b + j*stride] * kernel[a][b] for a in range(len(kernel)) for b in range(len(kernel[0]))]) for j in range((len(grid[0]) - len(kernel[0])) // stride + 1)] for i in range((len(grid) - len(kernel)) // stride + 1)]
    def pooling(self, grid, r, c, stride):
        self.pad(grid, r, c, stride)
        return [[max([grid[a + i*stride][b + j*stride] for a in range(r) for b in range(c)]) for j in range((len(grid[0]) - c) // stride + 1)] for i in range((len(grid) - r) // stride + 1)]
    def pad(self, grid, r, c, stride):
        for i in range(len(grid)):
            for j in range((len(grid[i]) - c) % stride):
                grid[i].append(0)
        for i in range((len(grid) - r) % stride):
            grid.append([0] * len(grid[0]))
        return grid
    
    