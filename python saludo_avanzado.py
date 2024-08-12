import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import csv
import os
import smtplib
from email.mime.text import MIMEText

class InfoFormulario:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario de Información Personal")
        self.root.geometry("600x700")
        self.root.configure(bg="#f5f5f5")
        self.crear_widgets()
        self.iniciar_temporizador()

    def crear_widgets(self):
        # Frame para entrada de datos
        entrada_frame = tk.Frame(self.root, bg="#f5f5f5")
        entrada_frame.pack(pady=20, padx=20, fill="x")

        tk.Label(entrada_frame, text="Nombre:", bg="#f5f5f5", font=("Arial", 12)).pack(pady=5)
        self.nombre_entry = tk.Entry(entrada_frame, font=("Arial", 12))
        self.nombre_entry.pack(pady=5, fill=tk.X)

        tk.Label(entrada_frame, text="Edad:", bg="#f5f5f5", font=("Arial", 12)).pack(pady=5)
        self.edad_entry = tk.Entry(entrada_frame, font=("Arial", 12))
        self.edad_entry.pack(pady=5, fill=tk.X)

        tk.Label(entrada_frame, text="Película favorita:", bg="#f5f5f5", font=("Arial", 12)).pack(pady=5)
        self.pelicula_entry = tk.Entry(entrada_frame, font=("Arial", 12))
        self.pelicula_entry.pack(pady=5, fill=tk.X)

        tk.Label(entrada_frame, text="Club favorito:", bg="#f5f5f5", font=("Arial", 12)).pack(pady=5)
        self.club_entry = tk.Entry(entrada_frame, font=("Arial", 12))
        self.club_entry.pack(pady=5, fill=tk.X)

        # Botones
        button_frame = tk.Frame(self.root, bg="#f5f5f5")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Mostrar Resultado", command=self.mostrar_resultado, font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Guardar en CSV", command=self.guardar_csv, font=("Arial", 12), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Ver Historial", command=self.ver_historial, font=("Arial", 12), bg="#FFC107", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Enviar por Correo", command=self.enviar_correo, font=("Arial", 12), bg="#FF5722", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Guardar en TXT", command=self.guardar_txt, font=("Arial", 12), bg="#673AB7", fg="white").pack(side=tk.LEFT, padx=10)

        # Temporizador
        self.temporizador_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f5f5f5")
        self.temporizador_label.pack(pady=10)

    def iniciar_temporizador(self):
        self.inicio_tiempo = datetime.datetime.now()
        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        tiempo_transcurrido = datetime.datetime.now() - self.inicio_tiempo
        self.temporizador_label.config(text=f"Tiempo desde que abriste la aplicación: {str(tiempo_transcurrido).split('.')[0]}")
        self.root.after(1000, self.actualizar_temporizador)

    def obtener_edad(self):
        try:
            edad = int(self.edad_entry.get())
            if edad < 0:
                messagebox.showerror("Error", "La edad no puede ser negativa.")
                return None
            return edad
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número válido.")
            return None

    def validar_entrada(self):
        nombre = self.nombre_entry.get().strip()
        pelicula_favorita = self.pelicula_entry.get().strip()
        club = self.club_entry.get().strip()
        if not nombre or not pelicula_favorita or not club:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        return True

    def guardar_datos(self, nombre, edad, pelicula_favorita, club, año_nacimiento):
        with open("datos_usuario.txt", "w") as archivo:
            archivo.write(f"Nombre: {nombre}\n")
            archivo.write(f"Edad: {edad}\n")
            archivo.write(f"Película Favorita: {pelicula_favorita}\n")
            archivo.write(f"Club: {club}\n")
            archivo.write(f"Año de Nacimiento: {año_nacimiento}\n")

    def guardar_csv(self):
        nombre = self.nombre_entry.get().strip()
        edad = self.obtener_edad()
        pelicula_favorita = self.pelicula_entry.get().strip()
        club = self.club_entry.get().strip()
        año_actual = datetime.datetime.now().year
        año_nacimiento = año_actual - edad

        if not self.validar_entrada() or edad is None:
            return

        with open("datos_usuario.csv", mode="a", newline="") as archivo_csv:
            escritor = csv.writer(archivo_csv)
            if os.stat("datos_usuario.csv").st_size == 0:
                escritor.writerow(["Nombre", "Edad", "Película Favorita", "Club", "Año de Nacimiento"])
            escritor.writerow([nombre, edad, pelicula_favorita, club, año_nacimiento])

        messagebox.showinfo("Guardado", "Los datos se han guardado en datos_usuario.csv")

    def ver_historial(self):
        historial_ventana = tk.Toplevel(self.root)
        historial_ventana.title("Historial de Resultados")
        historial_ventana.geometry("600x400")

        historial_text = tk.Text(historial_ventana, wrap=tk.WORD, font=("Arial", 12))
        historial_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        if os.path.exists("datos_usuario.csv"):
            with open("datos_usuario.csv", mode="r") as archivo_csv:
                lector = csv.reader(archivo_csv)
                for fila in lector:
                    historial_text.insert(tk.END, ', '.join(fila) + "\n")
        else:
            historial_text.insert(tk.END, "No hay historial disponible.")

        # Botón para cerrar la ventana de historial
        cerrar_button = tk.Button(historial_ventana, text="Cerrar", command=historial_ventana.destroy, font=("Arial", 12), bg="#f44336", fg="white")
        cerrar_button.pack(pady=10)

    def enviar_correo(self):
        import smtplib
        from email.mime.text import MIMEText

        nombre = self.nombre_entry.get().strip()
        edad = self.obtener_edad()
        pelicula_favorita = self.pelicula_entry.get().strip()
        club = self.club_entry.get().strip()
        año_actual = datetime.datetime.now().year
        año_nacimiento = año_actual - edad

        if not self.validar_entrada() or edad is None:
            return

        mensaje = f"Hola {nombre},\n\nAquí tienes un resumen de los datos que ingresaste:\n"
        mensaje += f"Edad: {edad} años\n"
        mensaje += f"Año de Nacimiento: {año_nacimiento}\n"
        mensaje += f"Película Favorita: {pelicula_favorita}\n"
        mensaje += f"Club: {club}\n"

        if edad < 18:
            mensaje += "¡Estás en la mejor etapa de tu vida para explorar y aprender! No dudes en aprovechar cada momento.\n"
        elif 18 <= edad <= 65:
            mensaje += "¡Estás en la etapa ideal para avanzar en tu carrera y disfrutar de la vida! Mantén el enfoque en tus metas.\n"
        else:
            mensaje += "¡Has acumulado mucha experiencia y sabiduría! Disfruta de cada día y sigue compartiendo tus conocimientos.\n"

        # Información sobre el club
        info_club = self.mostrar_informacion_club(club, edad)
        if info_club:
            mensaje += "\nDatos interesantes sobre tu club:\n" + info_club + "\n"

        mensaje += "Sugerencia de actividad: "
        if edad < 18:
            mensaje += "Quizás quieras unirte a actividades recreativas o explorar nuevas aficiones.\n"
        elif 18 <= edad <= 65:
            mensaje += "Podrías considerar actividades que te ayuden a relajarte y disfrutar tu tiempo libre.\n"
        else:
            mensaje += "¿Qué tal disfrutar de un buen libro o pasar tiempo con amigos y familia?\n"

        mensaje += f"\nFecha y hora actuales: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Guardar los datos en un archivo de texto temporal
        with open("datos_usuario_temp.txt", "w") as archivo_temp:
            archivo_temp.write(mensaje)

        # Enviar el correo
        from_email = "tu_email@example.com"
        to_email = "destinatario@example.com"
        password = "tu_contraseña"

        msg = MIMEText(mensaje)
        msg['Subject'] = "Resumen de Información Personal"
        msg['From'] = from_email
        msg['To'] = to_email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(from_email, password)
                server.send_message(msg)
            messagebox.showinfo("Éxito", "Correo enviado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo. {str(e)}")

    def mostrar_informacion_club(self, club, edad):
        info_club = {
            "River Plate": "River Plate es uno de los clubes más importantes de Argentina, conocido por su historia y éxitos en torneos nacionales e internacionales.",
            "Boca Juniors": "Boca Juniors es otro club emblemático argentino, famoso por su gran afición y rivalidad histórica con River Plate.",
            # Agrega más clubes si es necesario
        }
        return info_club.get(club, "No se encontró información sobre el club.")

    def guardar_txt(self):
        nombre = self.nombre_entry.get().strip()
        edad = self.obtener_edad()
        pelicula_favorita = self.pelicula_entry.get().strip()
        club = self.club_entry.get().strip()
        año_actual = datetime.datetime.now().year
        año_nacimiento = año_actual - edad

        if not self.validar_entrada() or edad is None:
            return

        with open("datos_usuario.txt", "w") as archivo_txt:
            archivo_txt.write(f"Nombre: {nombre}\n")
            archivo_txt.write(f"Edad: {edad}\n")
            archivo_txt.write(f"Película Favorita: {pelicula_favorita}\n")
            archivo_txt.write(f"Club: {club}\n")
            archivo_txt.write(f"Año de Nacimiento: {año_nacimiento}\n")

        messagebox.showinfo("Guardado", "Los datos se han guardado en datos_usuario.txt")

    def mostrar_resultado(self):
        nombre = self.nombre_entry.get().strip()
        edad = self.obtener_edad()
        pelicula_favorita = self.pelicula_entry.get().strip()
        club = self.club_entry.get().strip()
        año_actual = datetime.datetime.now().year
        año_nacimiento = año_actual - edad

        if not self.validar_entrada() or edad is None:
            return

        resultado_ventana = tk.Toplevel(self.root)
        resultado_ventana.title("Resultado")
        resultado_ventana.geometry("400x300")

        resultado_text = tk.Text(resultado_ventana, wrap=tk.WORD, font=("Arial", 12))
        resultado_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        resultado = f"Nombre: {nombre}\n"
        resultado += f"Edad: {edad} años\n"
        resultado += f"Año de Nacimiento: {año_nacimiento}\n"
        resultado += f"Película Favorita: {pelicula_favorita}\n"
        resultado += f"Club: {club}\n"

        if edad < 18:
            resultado += "Estás en una etapa genial para aprender y crecer. ¡Aprovecha cada momento al máximo!\n"
        elif 18 <= edad <= 65:
            resultado += "¡Estás en una etapa clave de tu vida! Sigue persiguiendo tus sueños y disfrutando cada experiencia.\n"
        else:
            resultado += "¡Has vivido muchas experiencias! Sigue disfrutando de la vida y compartiendo tu sabiduría.\n"

        info_club = self.mostrar_informacion_club(club, edad)
        if info_club:
            resultado += "\nDatos interesantes sobre tu club:\n" + info_club + "\n"

        resultado_text.insert(tk.END, resultado)
        resultado_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = InfoFormulario(root)
    root.mainloop()
