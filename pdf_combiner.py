import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys
from pypdf import PdfWriter, PdfReader

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class PDFCombinerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Combineur de PDF / Par Alexandre M. (alexandre196)")
        self.geometry("650x540")
        self.resizable(True, True)

        # Icône de la fenêtre
        try:
            icon_path = os.path.join(sys._MEIPASS, "pdf_combiner.ico") if hasattr(sys, "_MEIPASS") else "pdf_combiner.ico"
            self.iconbitmap(icon_path)
        except Exception:
            pass

        self.pdf_files = []
        self.selected_index = None
        self._build_ui()

    def _build_ui(self):
        # Titre
        ctk.CTkLabel(
            self, text="📄 Combineur de PDF",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(25, 4))

        ctk.CTkLabel(
            self, text="Ajoutez vos fichiers PDF et combinez-les en un seul",
            font=ctk.CTkFont(size=12), text_color="gray"
        ).pack(pady=(0, 16))

        # Boutons principaux
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=24, pady=(0, 8))

        ctk.CTkButton(
            btn_frame, text="➕ Ajouter des PDF",
            command=self.add_files, width=160
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_frame, text="🗑 Supprimer",
            command=self.remove_selected,
            fg_color="#e74c3c", hover_color="#c0392b", width=120
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_frame, text="🧹 Tout effacer",
            command=self.clear_all,
            fg_color="gray", hover_color="#555", width=130
        ).pack(side="left")

        # Boutons réordonnancement
        order_frame = ctk.CTkFrame(self, fg_color="transparent")
        order_frame.pack(fill="x", padx=24, pady=(0, 10))

        ctk.CTkButton(
            order_frame, text="⬆ Monter",
            command=self.move_up,
            fg_color="#f39c12", hover_color="#d68910", width=110
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            order_frame, text="⬇ Descendre",
            command=self.move_down,
            fg_color="#f39c12", hover_color="#d68910", width=120
        ).pack(side="left")

        ctk.CTkLabel(
            order_frame, text="← Cliquez sur un fichier pour le sélectionner",
            font=ctk.CTkFont(size=11, slant="italic"), text_color="gray"
        ).pack(side="left", padx=12)

        # Zone liste
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        ctk.CTkLabel(
            list_frame, text="Fichiers à combiner (dans l'ordre) :",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=12, pady=(10, 4))

        self.listbox_frame = ctk.CTkScrollableFrame(list_frame, height=200)
        self.listbox_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.placeholder = ctk.CTkLabel(
            self.listbox_frame,
            text="Aucun fichier ajouté\nCliquez sur « Ajouter des PDF » pour commencer",
            font=ctk.CTkFont(size=11, slant="italic"), text_color="gray"
        )
        self.placeholder.pack(pady=40)

        self.row_widgets = []

        # Bas : statut + bouton combiner
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=24, pady=(0, 20))

        self.status_label = ctk.CTkLabel(
            bottom_frame, text="0 fichier ajouté",
            font=ctk.CTkFont(size=11), text_color="gray"
        )
        self.status_label.pack(side="left")

        ctk.CTkButton(
            bottom_frame, text="✅  Combiner les PDF",
            command=self.combine_pdfs,
            fg_color="#27ae60", hover_color="#1e8449",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=190, height=38
        ).pack(side="right")

    # ── Gestion des fichiers ──────────────────────────────────────────────────

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Sélectionner des fichiers PDF",
            filetypes=[("Fichiers PDF", "*.pdf")]
        )
        for f in files:
            if f not in self.pdf_files:
                self.pdf_files.append(f)
        self._refresh_list()

    def remove_selected(self):
        if self.selected_index is None:
            messagebox.showinfo("Info", "Sélectionnez un fichier à supprimer.")
            return
        self.pdf_files.pop(self.selected_index)
        self.selected_index = None
        self._refresh_list()

    def clear_all(self):
        if self.pdf_files and messagebox.askyesno("Confirmer", "Effacer tous les fichiers ?"):
            self.pdf_files.clear()
            self.selected_index = None
            self._refresh_list()

    def move_up(self):
        i = self.selected_index
        if i is None or i == 0:
            return
        self.pdf_files[i - 1], self.pdf_files[i] = self.pdf_files[i], self.pdf_files[i - 1]
        self.selected_index = i - 1
        self._refresh_list(select=i - 1)

    def move_down(self):
        i = self.selected_index
        if i is None or i >= len(self.pdf_files) - 1:
            return
        self.pdf_files[i + 1], self.pdf_files[i] = self.pdf_files[i], self.pdf_files[i + 1]
        self.selected_index = i + 1
        self._refresh_list(select=i + 1)

    # ── Affichage ─────────────────────────────────────────────────────────────

    def _refresh_list(self, select=None):
        for w in self.row_widgets:
            w.destroy()
        self.row_widgets.clear()

        if select is not None:
            self.selected_index = select

        if not self.pdf_files:
            self.placeholder.pack(pady=40)
            self.status_label.configure(text="0 fichier ajouté")
            return

        self.placeholder.pack_forget()

        for i, path in enumerate(self.pdf_files):
            is_selected = (i == self.selected_index)
            row = ctk.CTkFrame(
                self.listbox_frame, corner_radius=6,
                fg_color=("#3b8ed0", "#1f6aa5") if is_selected else ("gray90", "gray20")
            )
            row.pack(fill="x", pady=3, padx=2)

            num = ctk.CTkLabel(row, text=f"{i + 1}.", width=28,
                               font=ctk.CTkFont(size=11, weight="bold"))
            num.pack(side="left", padx=(8, 4), pady=8)

            name = ctk.CTkLabel(row, text=os.path.basename(path),
                                font=ctk.CTkFont(size=11), anchor="w")
            name.pack(side="left", fill="x", expand=True, pady=8)

            for widget in (row, num, name):
                widget.bind("<Button-1>", lambda e, idx=i: self._select_row(idx))

            self.row_widgets.append(row)

        count = len(self.pdf_files)
        self.status_label.configure(
            text=f"{count} fichier{'s' if count > 1 else ''} ajouté{'s' if count > 1 else ''}"
        )

    def _select_row(self, idx):
        self.selected_index = idx
        self._refresh_list()

    # ── Combinaison ───────────────────────────────────────────────────────────

    def combine_pdfs(self):
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Attention", "Ajoutez au moins 2 fichiers PDF à combiner.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Enregistrer le PDF combiné",
            defaultextension=".pdf",
            filetypes=[("Fichier PDF", "*.pdf")],
            initialfile="combine.pdf"
        )
        if not output_path:
            return

        try:
            writer = PdfWriter()
            total_pages = 0
            for pdf_path in self.pdf_files:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)
                    total_pages += 1

            with open(output_path, "wb") as out_file:
                writer.write(out_file)

            messagebox.showinfo(
                "Succès ✅",
                f"PDF combiné avec succès !\n\n"
                f"📄 {len(self.pdf_files)} fichiers fusionnés\n"
                f"📃 {total_pages} pages au total\n\n"
                f"Enregistré : {os.path.basename(output_path)}"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")


if __name__ == "__main__":
    app = PDFCombinerApp()
    app.mainloop()