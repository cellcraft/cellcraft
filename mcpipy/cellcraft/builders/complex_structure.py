import numpy as np


class ComplexStructure():
    def create_grid_from_items(self, blocksize, threshold):
        """
        :param item:        dict with
        :param blocksize:
        :param threshold:
        :return:
        """
        all_coordinates = [i.coordinates for i in self.items]
        grid = self.init_grid(all_coordinates, blocksize)
        shape = [len(d) - 1 for d in grid]
        return self.create_grid(grid, shape, threshold)

    def init_grid(self, coordinates, blocksize):
        """

        :param coordinates:
        :param blocksize:
        :return:
        """
        amax = np.amax([np.amax(coor, axis=0) for coor in coordinates], axis=0)
        amin = np.amin([np.amin(coor, axis=0) for coor in coordinates], axis=0)
        x = np.arange(amin[0], amax[0] + blocksize, blocksize)
        y = np.arange(amin[1], amax[1] + blocksize, blocksize)
        z = np.arange(amin[2], amax[2] + blocksize, blocksize)
        return x, y, z

    def create_grid(self, grid, shape, threshold):
        """

        :param grid:
        :param shape:
        :param threshold:
        :return:
        """
        values = np.zeros(shape)
        for item in self.items:
            H, _ = np.histogramdd(item.coordinates, bins=grid)
            values[H >= threshold] = item.id
        return values
