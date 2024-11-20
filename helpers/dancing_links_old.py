class DancingLinksSudokuSolver:
    def __init__(self, board):
        self.board = board
        self.N = 9  # Kích thước bảng Sudoku (9x9)
        self.grid_size = self.N * self.N
        self.solution = []

    class Node:
        def __init__(self, column=None):
            self.left = self.right = self.up = self.down = self
            self.column = column  # Đại diện cột liên kết của node
            self.row = None  # Dòng trong ma trận

    def solve(self):
        header = self.create_sparse_matrix()
        
        self.debug_links(header);
        
        if self.dlx_solve(header):
            # Chuyển lời giải về dạng bảng
            self.update_solution_to_board()
            return True
        return False
    
    def debug_links(self, header):
    # Kiểm tra liên kết giữa các cột
        current = header.right
        visited = set()
        while current != header:
            assert current not in visited, "Cycle detected in column links"
            visited.add(current)
            print(f"Column: {id(current)} linked to Right: {id(current.right)} and Left: {id(current.left)}")
            current = current.right

    def create_sparse_matrix(self):
        """
        Tạo ma trận thưa cho Dancing Links dựa trên ràng buộc của Sudoku.
        """
        header = self.Node()  # Header của ma trận thưa
        column_nodes = []

        # Tạo cột cho các ràng buộc
        for _ in range(4 * self.grid_size):
            column = self.Node()
            column.column = column  # Node tự tham chiếu cột
            column_nodes.append(column)

        # Liên kết cột lại với nhau
        # Liên kết vòng giữa các cột
        for i in range(len(column_nodes)):
            column_nodes[i].left = column_nodes[i - 1]
            column_nodes[i - 1].right = column_nodes[i]
            
        
        
        
        # Liên kết vòng với header
        header.right = column_nodes[0]
        header.left = column_nodes[-1]
        column_nodes[0].left = header
        column_nodes[-1].right = header
        
        '''
        for i in range(len(column_nodes)):
            assert column_nodes[i].right.left == column_nodes[i], f"Column {i} link broken"
            assert column_nodes[i].left.right == column_nodes[i], f"Column {i} link broken"

        
        assert header.right.left == header, "Header links broken"
        assert header.left.right == header, "Header links broken"
        '''
    

    
        # Thêm hàng cho từng ô Sudoku
        for row in range(self.N):
            for col in range(self.N):
                value = self.board[row][col]
                if value == 0:
                    for num in range(1, 10):
                        self.add_row(column_nodes, row, col, num)
                else:
                    self.add_row(column_nodes, row, col, value)


        
        
        
        return header

    def add_row(self, column_nodes, row, col, num):
        """
        Thêm hàng vào ma trận thưa dựa trên các ràng buộc.
        """
        row_nodes = []
        constraints = [
            (row * 9 + col),                     # Ràng buộc 1: từng ô chỉ có 1 số
            (81 + row * 9 + num - 1),           # Ràng buộc 2: từng hàng chỉ có 1 số
            (162 + col * 9 + num - 1),          # Ràng buộc 3: từng cột chỉ có 1 số
            (243 + (row // 3 * 3 + col // 3) * 9 + num - 1)  # Ràng buộc 4: từng ô 3x3 chỉ có 1 số
        ]

        # Tạo node cho từng ràng buộc
        for constraint in constraints:
            column = column_nodes[constraint]
            node = self.Node(column=column)
            node.row = (row, col, num)  # Lưu thông tin về ô và giá trị
            row_nodes.append(node)

            # Liên kết dọc vào cột
            node.down = column
            node.up = column.up
            column.up.down = node
            column.up = node

        # Liên kết hàng ngang
        for i in range(len(row_nodes)):
            row_nodes[i].left = row_nodes[i - 1]
            row_nodes[i - 1].right = row_nodes[i]

    def dlx_solve(self, header):
        """
        Giải bài toán Exact Cover bằng Dancing Links.
        """
        if header.right == header:
            return True  # Đã giải xong


        # Chọn cột có ít hàng nhất
        column = self.select_column(header)

        # Xóa cột khỏi ma trận
        self.cover(column)
        

        
        # Duyệt qua các hàng trong cột
        for row in self.iterate_down(column):
            self.solution.append(row)
            for node in self.iterate_right(row):
                self.cover(node.column)

            

            # Đệ quy giải tiếp
            if self.dlx_solve(header):
                return True

            # Hoàn tác
            for node in self.iterate_left(row):
                self.uncover(node.column)
            self.solution.pop()

        # Phục hồi cột
        self.uncover(column)
        return False

    def cover(self, column):
        """
        Xóa cột và các hàng liên quan khỏi ma trận.
        """
        column.right.left = column.left
        column.left.right = column.right

        for row in self.iterate_down(column):
            for node in self.iterate_right(row):
                node.down.up = node.up
                node.up.down = node.down

    def uncover(self, column):
        """
        Phục hồi cột và các hàng liên quan vào ma trận.
        """
        for row in self.iterate_up(column):
            for node in self.iterate_left(row):
                node.down.up = node
                node.up.down = node

        column.right.left = column
        column.left.right = column

    '''
    def select_column(self, header):
        """
        Chọn cột có ít hàng nhất để giảm không gian tìm kiếm.
        """
        min_size = float('inf')
        selected_column = None

        for column in self.iterate_right(header):
            size = sum(1 for _ in self.iterate_down(column))
            if size < min_size:
                min_size = size
                selected_column = column
        return selected_column

                
    '''
    
    def select_column(self, header):
        column = header.right
        visited = set()
        while column != header:
            assert column not in visited, "Cycle detected in column traversal"
            visited.add(column)
            # Debug thông tin cột
            print(f"Visiting column: {column}")
            column = column.right
        return column


    def update_solution_to_board(self):
        """
        Chuyển lời giải từ danh sách `solution` thành bảng Sudoku.
        """
        for node in self.solution:
            row, col, num = node.row
            self.board[row][col] = num

    def iterate_down(self, column):
        node = column.down
        while node != column:
            yield node
            node = node.down

    def iterate_up(self, column):
        node = column.up
        while node != column:
            yield node
            node = node.up

    def iterate_right(self, row):
        node = row.right
        while node != row:
            yield node
            node = node.right

    def iterate_left(self, row):
        node = row.left
        while node != row:
            yield node
            node = node.left
            
        