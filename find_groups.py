def find_orthogonal_groups(matrix):
    if not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    groups = []
    # Orthogonal neighbors: (row_offset, col_offset)
    neighbors_coords = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                # Start a new group with the current value
                current_value = matrix[i][j]
                if current_value ==0:
                    continue
                group = []
                queue_list=[(i,j)]
                visited[i][j] = True

                while queue_list:
                    row, col = queue_list[0]
                    queue_list = queue_list[1:]
                    group.append((row, col))

                    # Check all orthogonal neighbors
                    for dr, dc in neighbors_coords:
                        new_row, new_col = row + dr, col + dc

                        # Check if the neighbor is within bounds and has the same value
                        if 0 <= new_row < rows and 0 <= new_col < cols and \
                           not visited[new_row][new_col] and \
                           matrix[new_row][new_col] == current_value:
                            visited[new_row][new_col] = True
                            queue_list.append((new_row, new_col))
                
                groups.append(group)
    return groups