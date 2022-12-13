from collections import defaultdict;

class AlgorithmX:

    def solveSudoku(self, board):
        # mark as (0, row, value) to record values in row
        rows = set() 
        # (1, col, value) to record values in column
        cols = set() 
        # (2, cell, value) to record values in each 3x3 spot
        cells = set() 
        # (3, row, col) to record cell index
        spots = set()
        # count how many spots to be filled
        count_spots = 0

        for row_index in range(9):
            row = board[row_index]
            for col_index in range(9):
                # find the spot that needs to be filled
                if row[col_index] == "0":
                    count_spots += 1
                    continue

                val = int(row[col_index])
                rows.add((0, row_index, val))
                cols.add((1, col_index, val))

                cell_spot = self.get_cell_spot(row_index, col_index)
                cells.add((2, cell_spot, val))

                spots.add((3, row_index, col_index))

        # build index mapping
        resource_to_values_mapping = defaultdict(set)
        values_to_resource_mapping = defaultdict(set)

        for row in range(9):
            for col in range(9):
                for val in range(1, 10):
                    row_res = (0, row, val)
                    col_res = (1, col, val)
                    cell_res = (2, self.get_cell_spot(row, col), val)
                    small_cell_res = (3, row, col)

                    if (row_res not in rows) and (col_res not in cols) and (cell_res not in cells) and (small_cell_res not in spots):
                        curr_val = (row, col, val)
                        resource_to_values_mapping[row_res].add(curr_val)
                        resource_to_values_mapping[col_res].add(curr_val)
                        resource_to_values_mapping[cell_res].add(curr_val)
                        resource_to_values_mapping[small_cell_res].add(curr_val)
                        values_to_resource_mapping[curr_val].add(row_res)
                        values_to_resource_mapping[curr_val].add(col_res)
                        values_to_resource_mapping[curr_val].add(cell_res)
                        values_to_resource_mapping[curr_val].add(small_cell_res)

        solution = []
        self.solve(resource_to_values_mapping, values_to_resource_mapping, solution, count_spots)

        for r, c, val in solution:
            board[r][c] = str(val)

    # backtrack solving 
    def solve(self, resource_to_values_mapping, values_to_resource_mapping, solution, count_spots):
        if len(solution) == count_spots:
            return True

        if len(resource_to_values_mapping) == 0:
            return False
        
        min_res, values = min(resource_to_values_mapping.items(), key=lambda rv: len(rv[1]))

        for val in list(values):
            rv_pairs_to_remove = set()

            for r in values_to_resource_mapping[val]:
                for v2 in resource_to_values_mapping[r]:
                    for r2 in values_to_resource_mapping[v2]:
                        rv_pairs_to_remove.add((r2, v2))

            for r, v in rv_pairs_to_remove:
                resource_to_values_mapping[r].remove(v)
                values_to_resource_mapping[v].remove(r)

                if len(resource_to_values_mapping[r]) == 0:
                    del resource_to_values_mapping[r]

            solution.append(val)
            if self.solve(resource_to_values_mapping, values_to_resource_mapping, solution, count_spots):
                return True

            solution.pop()

            for r, v in rv_pairs_to_remove:
                resource_to_values_mapping[r].add(v)
                values_to_resource_mapping[v].add(r)

        return False

    # divide the 9x9 board to 9 3x3 spots, get the cell belongs to which spot
    def get_cell_spot(self, row, col):
        return row // 3 + (col // 3) * 3