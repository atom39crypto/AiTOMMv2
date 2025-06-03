import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = r'Core\Memo\memory.db'  # Update this path as needed

class SQLiteViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("SQLite DB Browser")
        self.master.geometry("1200x700")

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.full_data = []
        self.columns = []
        self.table_name = ""

        self.setup_ui()
        self.populate_table_list()

    def setup_ui(self):
        # === TOP PANEL: Table selector + filter + delete ===
        top_frame = tk.Frame(self.master)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(top_frame, text="Select Table:").pack(side=tk.LEFT)
        self.table_dropdown = ttk.Combobox(top_frame, state='readonly', width=30)
        self.table_dropdown.pack(side=tk.LEFT, padx=10)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.load_table_data)

        tk.Label(top_frame, text="Filter:").pack(side=tk.LEFT, padx=(20, 0))
        self.filter_entry = tk.Entry(top_frame, width=40)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_entry.bind("<KeyRelease>", self.apply_filter)

        self.delete_btn = ttk.Button(top_frame, text="🗑 Delete Selected", command=self.delete_selected)
        self.delete_btn.pack(side=tk.RIGHT)

        self.delete_table_btn = ttk.Button(top_frame, text="❌ Delete Table", command=self.delete_current_table)
        self.delete_table_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # === TABLE FRAME with independent scrollbars ===
        table_frame = tk.Frame(self.master)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        y_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            show='headings',
            selectmode="extended",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    def populate_table_list(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in self.cursor.fetchall()]
            self.table_dropdown['values'] = tables
            if tables:
                self.table_dropdown.current(0)
                self.load_table_data()
            else:
                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = []
        except Exception as e:
            messagebox.showerror("Error Loading Tables", str(e))

    def load_table_data(self, event=None):
        self.table_name = self.table_dropdown.get()
        try:
            self.cursor.execute(f"SELECT rowid, * FROM {self.table_name}")
            self.full_data = self.cursor.fetchall()
            raw_columns = [desc[0] for desc in self.cursor.description]

            self.columns = raw_columns[1:]  # hide rowid from display

            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = self.columns
            self.tree["show"] = "headings"
            self.tree.column("#0", width=0, stretch=False)

            for col in self.columns:
                col_width = 300 if "content" in col.lower() or "message" in col.lower() else 150
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.W, width=col_width, stretch=True)

            for row in self.full_data:
                rowid = row[0]
                display_row = row[1:]
                self.tree.insert("", tk.END, values=display_row, iid=str(rowid))

        except Exception as e:
            messagebox.showerror("Error Loading Data", f"Failed to load data from '{self.table_name}':\n{e}")

    def apply_filter(self, event=None):
        keyword = self.filter_entry.get().lower()
        filtered = [row for row in self.full_data if any(keyword in str(cell).lower() for cell in row)]

        self.tree.delete(*self.tree.get_children())
        for row in filtered:
            rowid = row[0]
            display_row = row[1:]
            self.tree.insert("", tk.END, values=display_row, iid=str(rowid))

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select row(s) to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete {len(selected_items)} selected row(s)?")
        if not confirm:
            return

        for item in selected_items:
            rowid = int(item)
            try:
                self.cursor.execute(f"DELETE FROM {self.table_name} WHERE rowid = ?", (rowid,))
                self.conn.commit()
                self.tree.delete(item)
            except Exception as e:
                messagebox.showerror("Error Deleting Row", f"Could not delete rowid {rowid}:\n{e}")

        self.load_table_data()

    def delete_current_table(self):
        table = self.table_dropdown.get()
        if not table:
            messagebox.showinfo("No Table Selected", "Please select a table to delete.")
            return

        confirm = messagebox.askyesno("Confirm Table Deletion", f"Are you sure you want to permanently delete the table '{table}'?")
        if not confirm:
            return

        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
            self.conn.commit()
            messagebox.showinfo("Table Deleted", f"Table '{table}' has been deleted.")

            self.populate_table_list()
            self.tree.delete(*self.tree.get_children())
            self.columns = []
            self.full_data = []
            self.table_name = ""

        except Exception as e:
            messagebox.showerror("Error Deleting Table", f"Failed to delete table '{table}':\n{e}")

def main():
    root = tk.Tk()
    app = SQLiteViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
