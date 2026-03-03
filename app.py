"""Immersive desktop matrix calculator UI."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from matrix_ops import (
    MatrixValidationError,
    add_matrices,
    multiply_matrices,
    subtract_matrices,
)


class MatrixCalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Immersive Matrix Calculator")
        self.root.geometry("980x640")
        self.root.configure(bg="#0a0f1f")

        self.rows_a = tk.IntVar(value=2)
        self.cols_a = tk.IntVar(value=2)
        self.rows_b = tk.IntVar(value=2)
        self.cols_b = tk.IntVar(value=2)

        self.entries_a: list[list[tk.Entry]] = []
        self.entries_b: list[list[tk.Entry]] = []

        self._build_ui()
        self._render_matrices()

    def _build_ui(self) -> None:
        title = tk.Label(
            self.root,
            text="Matrix Calculator",
            fg="#e5ecff",
            bg="#0a0f1f",
            font=("Segoe UI", 28, "bold"),
            pady=16,
        )
        title.pack()

        control_frame = tk.Frame(self.root, bg="#0a0f1f")
        control_frame.pack(fill="x", padx=14, pady=6)

        self._build_dim_controls(control_frame)

        matrix_frame = tk.Frame(self.root, bg="#0a0f1f")
        matrix_frame.pack(fill="both", expand=True, padx=14, pady=10)

        self.panel_a = self._panel(matrix_frame, "Matrix A")
        self.panel_b = self._panel(matrix_frame, "Matrix B")
        self.panel_result = self._panel(matrix_frame, "Result", readonly=True)

        self.panel_a.grid(row=0, column=0, sticky="nsew", padx=8)
        self.panel_b.grid(row=0, column=1, sticky="nsew", padx=8)
        self.panel_result.grid(row=0, column=2, sticky="nsew", padx=8)

        matrix_frame.columnconfigure((0, 1, 2), weight=1)
        matrix_frame.rowconfigure(0, weight=1)

        action_frame = tk.Frame(self.root, bg="#0a0f1f")
        action_frame.pack(fill="x", padx=14, pady=(0, 16))

        self._action_button(action_frame, "A + B", self._on_add).pack(
            side="left", padx=8
        )
        self._action_button(action_frame, "A - B", self._on_subtract).pack(
            side="left", padx=8
        )
        self._action_button(action_frame, "A × B", self._on_multiply).pack(
            side="left", padx=8
        )
        self._action_button(action_frame, "Clear", self._on_clear).pack(side="right", padx=8)

    def _build_dim_controls(self, parent: tk.Frame) -> None:
        def labeled_spinbox(frame: tk.Frame, text: str, var: tk.IntVar) -> None:
            tk.Label(
                frame,
                text=text,
                fg="#cad8ff",
                bg="#0a0f1f",
                font=("Segoe UI", 10, "bold"),
            ).pack(side="left", padx=(10, 4))
            tk.Spinbox(
                frame,
                from_=1,
                to=8,
                textvariable=var,
                width=4,
                font=("Consolas", 11),
                bg="#141f3d",
                fg="#f4f7ff",
                buttonbackground="#243462",
                relief="flat",
            ).pack(side="left")

        sub_a = tk.Frame(parent, bg="#0a0f1f")
        sub_b = tk.Frame(parent, bg="#0a0f1f")
        sub_a.pack(side="left", padx=8)
        sub_b.pack(side="left", padx=8)

        tk.Label(
            sub_a,
            text="Matrix A",
            fg="#7ea8ff",
            bg="#0a0f1f",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        labeled_spinbox(sub_a, "Rows", self.rows_a)
        labeled_spinbox(sub_a, "Cols", self.cols_a)

        tk.Label(
            sub_b,
            text="Matrix B",
            fg="#7ea8ff",
            bg="#0a0f1f",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        labeled_spinbox(sub_b, "Rows", self.rows_b)
        labeled_spinbox(sub_b, "Cols", self.cols_b)

        self._action_button(parent, "Apply Dimensions", self._render_matrices).pack(
            side="right", padx=8
        )

    def _panel(self, parent: tk.Widget, title: str, readonly: bool = False) -> tk.Frame:
        wrapper = tk.Frame(parent, bg="#131b33", bd=0, padx=12, pady=12)
        tk.Label(
            wrapper,
            text=title,
            fg="#ecf2ff",
            bg="#131b33",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")

        grid = tk.Frame(wrapper, bg="#131b33")
        grid.pack(fill="both", expand=True, pady=(10, 4))
        wrapper.grid_container = grid  # type: ignore[attr-defined]

        if readonly:
            text = tk.Text(
                grid,
                height=18,
                width=26,
                font=("Consolas", 12),
                bg="#0d152d",
                fg="#c8facc",
                insertbackground="#c8facc",
                relief="flat",
                state="disabled",
            )
            text.pack(fill="both", expand=True)
            wrapper.result_text = text  # type: ignore[attr-defined]

        return wrapper

    def _entry(self, parent: tk.Widget) -> tk.Entry:
        return tk.Entry(
            parent,
            width=6,
            justify="center",
            font=("Consolas", 11),
            bg="#0d152d",
            fg="#e9efff",
            insertbackground="#e9efff",
            relief="flat",
        )

    def _render_matrices(self) -> None:
        self.entries_a = self._render_grid(self.panel_a.grid_container, self.rows_a.get(), self.cols_a.get())
        self.entries_b = self._render_grid(self.panel_b.grid_container, self.rows_b.get(), self.cols_b.get())
        self._set_result("Result will appear here.")

    def _render_grid(self, parent: tk.Widget, rows: int, cols: int) -> list[list[tk.Entry]]:
        for child in parent.winfo_children():
            child.destroy()

        entries: list[list[tk.Entry]] = []
        for r in range(rows):
            row_entries: list[tk.Entry] = []
            for c in range(cols):
                cell = self._entry(parent)
                cell.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                cell.insert(0, "0")
                row_entries.append(cell)
            entries.append(row_entries)

        for i in range(cols):
            parent.grid_columnconfigure(i, weight=1)

        return entries

    def _parse_matrix(self, entries: list[list[tk.Entry]], name: str) -> list[list[float]]:
        matrix: list[list[float]] = []
        try:
            for row in entries:
                matrix.append([float(cell.get()) for cell in row])
        except ValueError as exc:
            raise MatrixValidationError(f"{name} contains a non-numeric value.") from exc

        return matrix

    def _format_matrix(self, matrix: list[list[float]]) -> str:
        return "\n".join(
            "[ " + "  ".join(f"{value:.2f}".rstrip("0").rstrip(".") for value in row) + " ]"
            for row in matrix
        )

    def _set_result(self, text: str) -> None:
        result_text = self.panel_result.result_text
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", text)
        result_text.config(state="disabled")

    def _compute(self, op_name: str) -> None:
        a = self._parse_matrix(self.entries_a, "Matrix A")
        b = self._parse_matrix(self.entries_b, "Matrix B")

        operations = {
            "add": add_matrices,
            "subtract": subtract_matrices,
            "multiply": multiply_matrices,
        }

        try:
            result = operations[op_name](a, b)
        except MatrixValidationError as exc:
            messagebox.showerror("Math Rule Violation", str(exc))
            self._set_result("Operation failed. Check dimensions and values.")
            return

        self._set_result(self._format_matrix(result))

    def _on_add(self) -> None:
        self._compute("add")

    def _on_subtract(self) -> None:
        self._compute("subtract")

    def _on_multiply(self) -> None:
        self._compute("multiply")

    def _on_clear(self) -> None:
        self._render_matrices()

    def _action_button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#2a4da5",
            fg="#eef4ff",
            activebackground="#3561cc",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
        )


def main() -> None:
    root = tk.Tk()
    MatrixCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
