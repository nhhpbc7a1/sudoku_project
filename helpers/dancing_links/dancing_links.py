from collections.abc import Callable
from typing import Any, Generator, Tuple

from .sparse_matrix import Cell, Column, Matrix2D, SparseMatrix

from itertools import chain, product
from typing import List
import tkinter as tk
from tkinter import ttk

Solution = Tuple[int, ...]


def dlx(self, a: Matrix2D , grid: List[List[int]]) -> Generator[Solution, None, None]:
    """Knuth's Algorithm X implemented with Dancing Links"""




    assert (
        len(grid) == self.game_size**2
        and all((len(x) == self.game_size**2 for x in grid))
        and all(isinstance(x, int) and 0 <= x <= self.game_size**2 for x in chain(*grid))
    )
    
    possibilities = [
        (r, c, n)
        for r, c in product(range(self.game_size**2), range(self.game_size**2))
        for n in (range(self.game_size**2) if grid[r][c] == 0 else (grid[r][c] - 1,))
    ]






    def choose_col() -> Column:
        return min(loop_through(h, "r"), key=lambda col: col.size)

    def search() -> Generator[Solution, None, None]:
        # Success
        if h.r is h:
            yield tuple([int(x.name[1:].split("C")[0]) for x in stack])

        else:
            c = choose_col()
            cover_col(c)
            for r in loop_through(c, "d"):
                
                
                
                tmp = str(r)
                tmp = tmp.split("R")[1].split("C")[0]
                tmp_idx = int(tmp);
                tmp_r, tmp_c, tmp_n = possibilities[tmp_idx]  # Lấy thông tin (row, col, number)
                print(tmp_r, " ", tmp_c, " ", tmp_n+1);
                
                self.enter_robot_entries(tmp_r, tmp_c, tmp_n)
                
                stack.append(r)
                for j in loop_through(r, "r"):
                    cover_col(j.c)
                yield from search()
                # Backtrack
                stack.pop()
                for j in loop_through(r, "l"):
                    uncover_col(j.c)
                    
                self.robot1_entries[str(tmp_r + 1)+str(tmp_c + 1)].delete("all")

            uncover_col(c)

    h = SparseMatrix(a).h
    stack = []
    yield from search()


def apply_loop(
    func: Callable, head: Cell, direction: str
) -> Generator[Any, None, None]:
    assert direction in ("l", "r", "u", "d")
    x = head
    while True:
        x = getattr(x, direction)
        if x is head:
            break
        yield func(x)


def print_loop(cell: Cell, direction: str = "r") -> None:
    print(" -> ".join(apply_loop(str, cell, direction)))


def loop_through(cell: Cell, direction: str = "r") -> Generator[Cell, None, None]:
    return apply_loop(lambda x: x, cell, direction)


def unplug(cell: Cell, direction: str) -> None:
    if direction == "h":
        cell.l.r, cell.r.l = cell.r, cell.l
    elif direction == "v":
        cell.u.d, cell.d.u = cell.d, cell.u
    else:
        raise ValueError


def replug(cell: Cell, direction: str) -> None:
    if direction == "h":
        cell.l.r, cell.r.l = cell, cell
    elif direction == "v":
        cell.d.u, cell.u.d = cell, cell
    else:
        raise ValueError


def cover_col(c: Column) -> None:
    unplug(c, "h")
    for i in loop_through(c, "d"):
        for j in loop_through(i, "r"):
            unplug(j, "v")
            j.c.size -= 1


def uncover_col(c: Column) -> None:
    for i in loop_through(c, "u"):
        for j in loop_through(i, "l"):
            j.c.size += 1
            replug(j, "v")
    replug(c, "h")
