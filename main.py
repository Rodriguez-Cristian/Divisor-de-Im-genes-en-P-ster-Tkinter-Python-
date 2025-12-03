import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ---------------------------------------------------------
#  Divisor de Imagen en Poster con Interfaz Tkinter
# ---------------------------------------------------------

def generar_pdf(imagen_path, salida_pdf, cols, rows):
    try:
        img = Image.open(imagen_path)
        w, h = img.size

        tile_w = w // cols
        tile_h = h // rows

        PAGE_W, PAGE_H = A4
        c = canvas.Canvas(salida_pdf, pagesize=A4)

        for row in range(rows):
            for col in range(cols):

                left = col * tile_w
                top = row * tile_h
                right = left + tile_w
                bottom = top + tile_h

                parte = img.crop((left, top, right, bottom))

                temp = f"temp_{row}_{col}.png"
                parte.save(temp)

                img_ratio = parte.width / parte.height
                page_ratio = PAGE_W / PAGE_H

                if img_ratio > page_ratio:
                    new_w = PAGE_W
                    new_h = PAGE_W / img_ratio
                else:
                    new_h = PAGE_H
                    new_w = PAGE_H * img_ratio

                x = (PAGE_W - new_w) / 2
                y = (PAGE_H - new_h) / 2

                c.drawImage(temp, x, y, width=new_w, height=new_h, preserveAspectRatio=True)
                c.showPage()

                os.remove(temp)

        c.save()
        return True

    except Exception as e:
        print(e)
        return False


# =========================================================
#  TKINTER UI
# =========================================================

def seleccionar_imagen():
    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.bmp")]
    )
    if archivo:
        entrada_imagen.delete(0, "end")
        entrada_imagen.insert(0, archivo)

def crear_poster():
    imagen = entrada_imagen.get()
    cols = entrada_cols.get()
    rows = entrada_rows.get()

    if not imagen:
        messagebox.showerror("Error", "Seleccioná una imagen.")
        return

    try:
        cols = int(cols)
        rows = int(rows)
    except:
        messagebox.showerror("Error", "Columnas y filas deben ser números.")
        return

    salida = filedialog.asksaveasfilename(
        title="Guardar PDF",
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")]
    )

    if not salida:
        return

    ok = generar_pdf(imagen, salida, cols, rows)

    if ok:
        messagebox.showinfo("Éxito", "PDF generado correctamente.")
    else:
        messagebox.showerror("Error", "Ocurrió un problema generando el PDF.")


# =========================================================
#  VENTANA PRINCIPAL
# =========================================================

root = Tk()
root.title("Divisor de Poster - by Cristian Rodriguez")
root.geometry("400x240")

Label(root, text="Imagen seleccionada:").pack(pady=5)
entrada_imagen = Entry(root, width=40)
entrada_imagen.pack()
Button(root, text="Buscar imagen", command=seleccionar_imagen).pack(pady=5)

Label(root, text="Columnas (ej: 2):").pack()
entrada_cols = Entry(root, width=10)
entrada_cols.insert(0, "2")
entrada_cols.pack()

Label(root, text="Filas (ej: 2):").pack()
entrada_rows = Entry(root, width=10)
entrada_rows.insert(0, "2")
entrada_rows.pack()

Button(root, text="Generar PDF", command=crear_poster).pack(pady=15)

root.mainloop()
