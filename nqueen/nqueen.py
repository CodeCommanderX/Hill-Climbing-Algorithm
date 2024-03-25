import time
import cv2
import os
from board import Board
from utils import RESULTS_DIR, make_dirs


class QueenPlaces:
    def __init__(self, size):
        self.size = size

        self.solutions = []

    def solve(self):
        #Giải quyết vấn đề 8 quân hậu
        rows = [""] * self.size
        self.find_queens(rows, 0)

    def find_queens(self, rows, column_index):
        #Tìm tất cả các vị trí có thể có và kiểm tra với check_position
        if column_index == self.size:
            self.solutions.append(rows.copy())
            self.show(rows)
            return True

        for column in range(self.size):
            if self.check_position(rows, column_index, column):
                rows[column_index] = column
                self.find_queens(rows, column_index + 1)

    def check_position(self, rows, column_index, column) -> bool:
        #Kiểm tra bất kỳ giao điểm nào trong trục ngang, dọc và chéo.
        #return: bool
        #    Đúng nếu không có giao nhau
        #    Sai nếu có giao nhau
        for i in range(column_index):
            if rows[i] == column or rows[i] - i == column - column_index or rows[i] + i == column + column_index:
                return False
        return True

    def show(self, rows: list):
        #Hiển thị kết quả tìm được
        rows2d = [['X' if column == rows[row] else '-' for column in range(self.size)] for row in range(self.size)]
        print(f"Đường đi {len(self.solutions)}:")
        for row in rows2d:
            print(row)
        print("\n", "" * 10, "\n")


if __name__ == '__main__':
    size = 8

    qp = QueenPlaces(size)

    start_time = time.time()

    qp.solve()

    end_time = time.time()

    print(f"Tìm thấy {len(qp.solutions)} đường đi trong {str(end_time - start_time)[:7]} giây.")

    # ===========================================
    # Show with CV2
    # ===========================================

    result_path = make_dirs(os.path.join(RESULTS_DIR, f"{size}x{size}"))

    for solution_index, rows in enumerate(qp.solutions):
        # Tạo bàn cờ 
        board = Board(size=size)

        # Đặt quân hậu vào bàn cờ
        for row_index, column_index in enumerate(rows):
            board.put('queen', (row_index, column_index))

        # Vẽ quân hậu
        board.draw()

        #Lưu kết quả vào hình ảnh
        board.write(os.path.join(result_path, f'{solution_index}.png'))

        #Đánh số thứ tự cách sắp xếp
        board.panel = cv2.putText(board.panel, f'{solution_index}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Hiển thị cách đi
        board.show()

