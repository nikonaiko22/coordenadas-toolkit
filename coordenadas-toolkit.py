import tkinter as tk
from math import atan, pi, cos, sin, sqrt
from tkinter import messagebox

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x180")
        self.configure(bg="#ecf0f1")

        tk.Label(self, text="Usuario:", bg="#ecf0f1").pack(pady=(20,5))
        self.user_entry = tk.Entry(self)
        self.user_entry.pack()

        tk.Label(self, text="Contraseña:", bg="#ecf0f1").pack(pady=(10,5))
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack()

        tk.Button(self, text="Iniciar Sesión", command=self.check_login).pack(pady=15)

    def check_login(self):
        user = self.user_entry.get()
        password = self.pass_entry.get()
        # Validación Admin
        if user == "Admin" and password == "911":
            self.destroy()  # Cierra la ventana de login
            app = App()     # Crea y muestra la ventana principal
            app.mainloop()
        # Validación Tester
        elif user == "Tester" and password == "Tester2123":
            self.destroy()
            app = App()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


#empieza codigo 
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculo Geomensor")
        self.geometry("900x600")
        self.configure(bg="#bdc3c7")

        self.sidebar = tk.Frame(self, bg="#2c3e50", width=250)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(self, bg="#ecf0f1")
        self.main_area.pack(side="right", expand=True, fill="both")

        self.frames = {
            "Inicio": self.frame_inicio(),
            "Cálculo del Azimut": self.frame_azimut(),
            "Cálculo de coordenadas": self.frame_coordenadas(),
            "Calcular ángulo de trabajo y DH": self.frame_angulo_dh(),
            "Distancia mínima": self.frame_distancia_minima(),
            "Punto de intersección entre dos líneas rectas": self.frame_interseccion_rectas(),
            "Cálculo del área de un polígono": self.frame_area_poligono(),
        }

        self.create_sidebar_buttons()
        self.show_frame("Inicio")

    def make_frame(self, title):
        frame = tk.Frame(self.main_area, bg="#ecf0f1")
        label = tk.Label(frame, text=title, font=("Segoe UI", 22, "bold"), bg="#ecf0f1", fg="#2c3e50")
        label.pack(pady=30)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        return frame

    def frame_inicio(self):
        frame = tk.Frame(self.main_area, bg="#ecf0f1")
        tk.Label(frame, text="Calculadora Topográfica", font=("Segoe UI", 28, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=40)
        tk.Label(frame, text="Versión 2.0.1", font=("Segoe UI", 18), bg="#ecf0f1", fg="#34495e").pack(pady=12)
        tk.Label(frame, text="Creado por Nicolás Castro", font=("Segoe UI", 16), bg="#ecf0f1", fg="#7f8c8d").pack(pady=8)
        tk.Label(frame, text="Estado: BETA", font=("Segoe UI", 16, "italic"), bg="#ecf0f1", fg="#e67e22").pack(pady=8)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        return frame
    
    ### calculo de azimut

    def frame_azimut(self):
        
        frame = tk.Frame(self.main_area, bg="#ecf0f1")

        tk.Label(frame, text="Cálculo del Azimut", font=("Segoe UI", 22, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=25)

        form_container = tk.Frame(frame, bg="#f7f9fa", bd=2, relief="groove")
        form_container.pack(padx=40, pady=10, anchor="w")

        labels = ["Norte Estación", "Este Estación", "Norte Calaje", "Este Calaje"]
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = tk.Label(form_container, text=label + ":", bg="#f7f9fa", font=("Segoe UI", 13, "bold"), fg="#34495e")
            lbl.grid(row=i, column=0, sticky="e", padx=(10, 20), pady=12)

            entry = tk.Entry(form_container, font=("Segoe UI", 13), width=18, relief="flat", bg="#ecf0f1", fg="#2c3e50")
            entry.grid(row=i, column=1, sticky="w", pady=12, padx=(0, 10))
            entry.config(highlightthickness=1, highlightcolor="#2980b9", highlightbackground="#bdc3c7")

            def make_clear_function(e=entry):
                return lambda: e.delete(0, tk.END)

            clear_btn = tk.Button(form_container, text="🧹", font=("Segoe UI", 12), relief="flat", bg="#d0d7de", fg="#2c3e50",
                                  width=2, command=make_clear_function())
            clear_btn.grid(row=i, column=2, padx=(0,15), pady=12)

            self.entries[label] = entry

        buttons_frame = tk.Frame(frame, bg="#ecf0f1")
        buttons_frame.pack(pady=25, padx=40, anchor="w")

        self.calc_btn = tk.Button(buttons_frame, text="Calcular Azimut", font=("Segoe UI", 14, "bold"),
                             bg="#3498db", fg="white", relief="flat", padx=15, pady=8, command=self.calcular_deltas)
        self.calc_btn.pack(side="left")

        self.result_frame = tk.Frame(frame, bg="#ecf0f1")
        self.result_frame.pack(padx=40, pady=(0,10), anchor="w")
        self.result_frame.pack_forget()

        self.delta_n_label = tk.Label(self.result_frame, text="", font=("Segoe UI", 14),
                                      bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=25)
        self.delta_n_label.pack(anchor="w", pady=4)

        self.delta_e_label = tk.Label(self.result_frame, text="", font=("Segoe UI", 14),
                                      bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=25)
        self.delta_e_label.pack(anchor="w", pady=4)

        self.cuadrante_label = tk.Label(self.result_frame, text="", font=("Segoe UI", 14, "bold"),
                                        bg="#fefefe", fg="#8e44ad", relief="solid", bd=1, padx=10, pady=5, width=25)
        self.cuadrante_label.pack(anchor="w", pady=4)

        self.rumbo_label = tk.Label(self.result_frame, text="", font=("Segoe UI", 14),
                                    bg="#fefefe", fg="#27ae60", relief="solid", bd=1, padx=10, pady=5, width=25)
        self.rumbo_label.pack(anchor="w", pady=4)

        self.azimut_label = tk.Label(self.result_frame, text="", font=("Segoe UI", 14),
                                     bg="#fefefe", fg="#c0392b", relief="solid", bd=1, padx=10, pady=5, width=25)
        self.azimut_label.pack(anchor="w", pady=4)

        # Botón Copiar Azimut ubicado debajo de azimut_label, oculto 
        self.copy_btn = tk.Button(self.result_frame, text="Copiar Azimut", font=("Segoe UI", 12, "bold"),
                             bg="#27ae60", fg="white", relief="flat", padx=15, pady=8, command=self.copy_azimut)
        self.copy_btn.pack_forget()

        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        return frame

    def calcular_deltas(self):
        # Código existente para calcular azimut. NO modificar.
        if any(self.entries[label].get().strip() == "" for label in ["Norte Estación", "Este Estación", "Norte Calaje", "Este Calaje"]):
            return

        try:
            N1 = float(self.entries["Norte Estación"].get())
            E1 = float(self.entries["Este Estación"].get())
            N2 = float(self.entries["Norte Calaje"].get())
            E2 = float(self.entries["Este Calaje"].get())

            delta_n = N2 - N1
            delta_e = E2 - E1

            self.delta_n_label.config(text=f"Delta Norte: {delta_n:.4f}")
            self.delta_e_label.config(text=f"Delta Este: {delta_e:.4f}")

            if delta_n > 0 and delta_e > 0:
                cuadrante = "Cuadrante I"
            elif delta_n < 0 and delta_e > 0:
                cuadrante = "Cuadrante II"
            elif delta_n < 0 and delta_e < 0:
                cuadrante = "Cuadrante III"
            elif delta_n > 0 and delta_e < 0:
                cuadrante = "Cuadrante IV"
            elif delta_n == 0 and delta_e == 0:
                cuadrante = "Punto sin desplazamiento"
            else:
                cuadrante = "Sobre eje o indefinido"

            self.cuadrante_label.config(text=cuadrante)

            if delta_n != 0:
                rumbo_rad = atan(abs(delta_e / delta_n))
                rumbo_gon = rumbo_rad * (200 / pi)
                self.rumbo_label.config(text=f"Rumbo: {rumbo_gon:.4f} gon")

                if cuadrante == "Cuadrante I":
                    azimut = rumbo_gon
                elif cuadrante == "Cuadrante II":
                    azimut = 200 - rumbo_gon
                elif cuadrante == "Cuadrante III":
                    azimut = 200 + rumbo_gon
                elif cuadrante == "Cuadrante IV":
                    azimut = 400 - rumbo_gon
                else:
                    azimut = None

                if azimut is not None:
                    self.azimut_label.config(text=f"Azimut: {azimut:.4f} gon")
                    self.ultimo_azimut = f"{azimut:.4f} gon"
                    if not self.copy_btn.winfo_ismapped():
                        self.copy_btn.pack(anchor="w", pady=8)
                else:
                    self.azimut_label.config(text="Azimut: indefinido")
                    self.ultimo_azimut = None
                    if self.copy_btn.winfo_ismapped():
                        self.copy_btn.pack_forget()

            else:
                self.rumbo_label.config(text="Rumbo: indefinido")
                self.azimut_label.config(text="Azimut: indefinido")
                self.ultimo_azimut = None
                if self.copy_btn.winfo_ismapped():
                    self.copy_btn.pack_forget()

            self.result_frame.pack(padx=40, pady=(0,10), anchor="w")

        except ValueError:
            self.delta_n_label.config(text="Delta Norte: Entrada inválida")
            self.delta_e_label.config(text="Delta Este: Entrada inválida")
            self.cuadrante_label.config(text="")
            self.rumbo_label.config(text="")
            self.azimut_label.config(text="")
            if self.copy_btn.winfo_ismapped():
                self.copy_btn.pack_forget()

    def copy_azimut(self):
        if hasattr(self, "ultimo_azimut") and self.ultimo_azimut:
            self.clipboard_clear()
            self.clipboard_append(self.ultimo_azimut)

    # Cálculo de Coordenadas
    def frame_coordenadas(self):
        frame = tk.Frame(self.main_area, bg="#ecf0f1")
        tk.Label(frame, text="Cálculo de Coordenadas", font=("Segoe UI", 22, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=25)

        form = tk.Frame(frame, bg="#f7f9fa", bd=2, relief="groove")
        form.pack(padx=40, pady=10, anchor="w")

        labels = [
            "Norte Estación",
            "Este Estación",
            "Norte Calaje",
            "Este Calaje",
            "Ángulo Cente (gon)",
            "Distancia DH (m)"
        ]

        self.coord_entries_coordenadas = {}  # diccionario independiente
        for i, label in enumerate(labels):
            lbl = tk.Label(form, text=label + ":", bg="#f7f9fa", font=("Segoe UI", 13, "bold"), fg="#34495e")
            lbl.grid(row=i, column=0, sticky="e", padx=(10, 20), pady=12)

            entry = tk.Entry(form, font=("Segoe UI", 13), width=18, relief="flat", bg="#ecf0f1", fg="#2c3e50")
            entry.grid(row=i, column=1, sticky="w", pady=12, padx=(0, 10))
            entry.config(highlightthickness=1, highlightcolor="#2980b9", highlightbackground="#bdc3c7")

            def make_clear_function(e=entry):
                return lambda: e.delete(0, tk.END)

            clear_btn = tk.Button(form, text="🧹", font=("Segoe UI", 12), relief="flat", bg="#d0d7de", fg="#2c3e50",
                                  width=2, command=make_clear_function())
            clear_btn.grid(row=i, column=2, padx=(0, 15), pady=12)

            self.coord_entries_coordenadas[label] = entry

        btn_frame = tk.Frame(frame, bg="#ecf0f1")
        btn_frame.pack(pady=25, padx=40, anchor="w")

        calc_btn = tk.Button(btn_frame, text="Calcular Coordenadas", font=("Segoe UI", 14, "bold"),
                             bg="#3498db", fg="white", relief="flat", padx=15, pady=8,
                             command=self.calcular_coordenadas)
        calc_btn.pack(side="left")

        self.coord_result_frame = tk.Frame(frame, bg="#ecf0f1")
        self.coord_result_frame.pack(padx=40, pady=(0, 10), anchor="w")
        self.coord_result_frame.pack_forget()

        self.result_azimut_label = tk.Label(self.coord_result_frame, text="", font=("Segoe UI", 14),
                                           bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=38)
        self.result_azimut_label.pack(anchor="w", pady=4)

        self.result_at_label = tk.Label(self.coord_result_frame, text="", font=("Segoe UI", 14),
                                       bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=38)
        self.result_at_label.pack(anchor="w", pady=4)

        self.result_cpn_label = tk.Label(self.coord_result_frame, text="", font=("Segoe UI", 14),
                                         bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=38)
        self.result_cpn_label.pack(anchor="w", pady=4)

        self.result_cpe_label = tk.Label(self.coord_result_frame, text="", font=("Segoe UI", 14),
                                         bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=38)
        self.result_cpe_label.pack(anchor="w", pady=4)

        self.result_nuevo_n_label = tk.Label(self.coord_result_frame, text="", font=("Segoe UI", 14),
                                            bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=38)
        self.result_nuevo_n_label.pack(anchor="w", pady=4)

        self.result_nuevo_e_label = tk.Label(self.coord_result_frame, text="", font=("Segoe UI", 14),
                                            bg="white", fg="#2c3e50", relief="solid", bd=1, padx=10, pady=5, width=38)
        self.result_nuevo_e_label.pack(anchor="w", pady=4)

        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        return frame

    def calcular_coordenadas(self):
        for key in self.coord_entries_coordenadas:
            if self.coord_entries_coordenadas[key].get().strip() == "":
                return

        try:
            N_est = float(self.coord_entries_coordenadas["Norte Estación"].get())
            E_est = float(self.coord_entries_coordenadas["Este Estación"].get())
            N_cal = float(self.coord_entries_coordenadas["Norte Calaje"].get())
            E_cal = float(self.coord_entries_coordenadas["Este Calaje"].get())
            ang_cente = float(self.coord_entries_coordenadas["Ángulo Cente (gon)"].get())
            dh = float(self.coord_entries_coordenadas["Distancia DH (m)"].get())

            delta_n = N_cal - N_est
            delta_e = E_cal - E_est

            if delta_n == 0 and delta_e == 0:
                self.coord_result_frame.pack_forget()
                return

            if delta_n > 0 and delta_e > 0:
                cuadrante = 1
            elif delta_n < 0 and delta_e > 0:
                cuadrante = 2
            elif delta_n < 0 and delta_e < 0:
                cuadrante = 3
            elif delta_n > 0 and delta_e < 0:
                cuadrante = 4
            else:
                self.coord_result_frame.pack_forget()
                return

            if delta_n != 0:
                rumbo_rad = atan(abs(delta_e / delta_n))
                rumbo_gon = rumbo_rad * (200 / pi)
            else:
                self.coord_result_frame.pack_forget()
                return

            if cuadrante == 1:
                azimut = rumbo_gon
            elif cuadrante == 2:
                azimut = 200 - rumbo_gon
            elif cuadrante == 3:
                azimut = 200 + rumbo_gon
            else:
                azimut = 400 - rumbo_gon

            ang_trabajo = azimut + ang_cente

            cpn = dh * cos(ang_trabajo * pi / 200)
            cpe = dh * sin(ang_trabajo * pi / 200)

            n_punto = N_est + cpn
            e_punto = E_est + cpe

            self.result_azimut_label.config(text=f"Azimut (gon): {azimut:.4f}")
            self.result_at_label.config(text=f"Ángulo de trabajo (gon): {ang_trabajo:.4f}")
            self.result_cpn_label.config(text=f"Coordenada Parcial Norte (CPN): {cpn:.4f}")
            self.result_cpe_label.config(text=f"Coordenada Parcial Este (CPE): {cpe:.4f}")
            self.result_nuevo_n_label.config(text=f"Nueva Coordenada Norte: {n_punto:.4f}")
            self.result_nuevo_e_label.config(text=f"Nueva Coordenada Este: {e_punto:.4f}")

            self.coord_result_frame.pack(padx=40, pady=(0, 10), anchor="w")

        except ValueError:
            self.coord_result_frame.pack_forget()

    # Calculo Angulo de trabajo / dh   
    def frame_angulo_dh(self):
        frame = tk.Frame(self.main_area, bg="#ecf0f1")

        etiquetas = [
                "Norte Estación", "Este Estación",
                "Norte Calaje", "Este Calaje",
                "Norte Punto", "Este Punto"
        ]

        self.coord_entries = {}

        for i, texto in enumerate(etiquetas):
                tk.Label(frame, text=texto, bg="#ecf0f1").grid(row=i, column=0, sticky="e", padx=5, pady=2)
                entry = tk.Entry(frame)
                entry.grid(row=i, column=1, padx=5, pady=2)
                self.coord_entries[texto] = entry

                # Botón para limpiar entrada individual
                btn_clear = tk.Button(frame, text="🧹", width=2,
                                command=lambda e=entry: e.delete(0, tk.END))
                btn_clear.grid(row=i, column=2, padx=5, pady=2)

        # Botón para calcular
        tk.Button(frame, text="Calcular", command=self.calcular_dh).grid(row=6, column=0, columnspan=3, pady=10)

        # Resultado
        self.dh_result = tk.Label(frame, text="", justify="left", anchor="w", bg="#ecf0f1")
        self.dh_result.grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        return frame

    def calcular_azimut_cuadrante_rumbo(self, delta_n, delta_e):
        if delta_n == 0 and delta_e == 0:
            return None, "Punto sin desplazamiento", None

        if delta_n > 0 and delta_e > 0:
            cuadrante = "Cuadrante I"
        elif delta_n < 0 and delta_e > 0:
            cuadrante = "Cuadrante II"
        elif delta_n < 0 and delta_e < 0:
            cuadrante = "Cuadrante III"
        elif delta_n > 0 and delta_e < 0:
            cuadrante = "Cuadrante IV"
        elif delta_n == 0 and delta_e == 0:
            cuadrante = "Punto sin desplazamiento"
        else:
            cuadrante = "Sobre eje o indefinido"

        # Calcular rumbo
        if delta_n != 0:
            rumbo_rad = atan(abs(delta_e / delta_n))
            rumbo_gon = rumbo_rad * (200 / pi)
        else:
            rumbo_gon = 100 if delta_e > 0 else 300

        # Calcular azimut
        if cuadrante == "Cuadrante I":
            azimut = rumbo_gon
        elif cuadrante == "Cuadrante II":
            azimut = 200 - rumbo_gon
        elif cuadrante == "Cuadrante III":
            azimut = 200 + rumbo_gon
        elif cuadrante == "Cuadrante IV":
            azimut = 400 - rumbo_gon
        else:
            azimut = None

        return azimut, cuadrante, rumbo_gon

    def calcular_dh(self):
        try:
            N_est = float(self.coord_entries["Norte Estación"].get())
            E_est = float(self.coord_entries["Este Estación"].get())
            N_cal = float(self.coord_entries["Norte Calaje"].get())
            E_cal = float(self.coord_entries["Este Calaje"].get())
            N_pun = float(self.coord_entries["Norte Punto"].get())
            E_pun = float(self.coord_entries["Este Punto"].get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
            return

        # Calaje → Estación
        deltaN_cal_est = N_cal - N_est
        deltaE_cal_est = E_cal - E_est
        az_cal, cuadrante_cal, rumbo_cal = self.calcular_azimut_cuadrante_rumbo(deltaN_cal_est, deltaE_cal_est)

        # Punto → Estación
        deltaN_pun_est = N_pun - N_est
        deltaE_pun_est = E_pun - E_est
        az_pun, cuadrante_pun, rumbo_pun = self.calcular_azimut_cuadrante_rumbo(deltaN_pun_est, deltaE_pun_est)

        if az_cal is None or az_pun is None:
            messagebox.showerror("Error", "No se pudo calcular azimut por coordenadas iguales.")
            return

        # Ángulo de trabajo
        angulo_trabajo = az_pun - az_cal
        if angulo_trabajo < 0:
            angulo_trabajo += 400

        # Distancia horizontal
        dh = sqrt((N_pun - N_est)**2 + (E_pun - E_est)**2)

        resultado = (
            f"📍 Calaje → Estación:\n"
            f"  - Azimut: {az_cal:.4f} gon\n"
            f"  - Cuadrante: {cuadrante_cal}\n"
            f"  - Rumbo: {rumbo_cal:.4f} gon\n\n"
            f"📍 Punto → Estación:\n"
            f"  - Azimut: {az_pun:.4f} gon\n"
            f"  - Cuadrante: {cuadrante_pun}\n"
            f"  - Rumbo: {rumbo_pun:.4f} gon\n\n"
            f"🧭 Ángulo de trabajo: {angulo_trabajo:.4f} gon\n"
            f"📏 Distancia Horizontal (DH): {dh:.4f} m"
        )

        self.dh_result.config(text=resultado)
    # Calculo Dist Minima
    def calcular_distancia_minima(self, xa, ya, xb, yb, xc, yc):
        numerador = abs((xb - xa)*(ya - yc) - (xa - xc)*(yb - ya))
        denominador = sqrt((xb - xa)**2 + (yb - ya)**2)
        if denominador == 0:
            return None  # Línea no válida (puntos A y B iguales)
        return numerador / denominador
    
    def frame_distancia_minima(self):
        frame = tk.Frame(self.main_area, bg="#ecf0f1")

        tk.Label(frame, text="Distancia Mínima Punto a Línea", font=("Segoe UI", 22, "bold"),
                 bg="#ecf0f1", fg="#2c3e50").pack(pady=25)

        # Contenedor para inputs
        container = tk.Frame(frame, bg="#f7f9fa", bd=2, relief="groove")
        container.pack(padx=40, pady=10, anchor="w")

        # Labels y Entradas para punto A
        tk.Label(container, text="Coordenadas Punto A (x, y):", bg="#f7f9fa", font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=0, column=0, sticky="w", pady=5)
        self.dist_xa = tk.Entry(container, width=10)
        self.dist_xa.grid(row=0, column=1, padx=10, pady=5)
        self.dist_ya = tk.Entry(container, width=10)
        self.dist_ya.grid(row=0, column=2, padx=10, pady=5)

        # Punto B
        tk.Label(container, text="Coordenadas Punto B (x, y):", bg="#f7f9fa", font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=1, column=0, sticky="w", pady=5)
        self.dist_xb = tk.Entry(container, width=10)
        self.dist_xb.grid(row=1, column=1, padx=10, pady=5)
        self.dist_yb = tk.Entry(container, width=10)
        self.dist_yb.grid(row=1, column=2, padx=10, pady=5)

        # Punto C
        tk.Label(container, text="Coordenadas Punto C (x, y):", bg="#f7f9fa", font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=2, column=0, sticky="w", pady=5)
        self.dist_xc = tk.Entry(container, width=10)
        self.dist_xc.grid(row=2, column=1, padx=10, pady=5)
        self.dist_yc = tk.Entry(container, width=10)
        self.dist_yc.grid(row=2, column=2, padx=10, pady=5)

        # Botón calcular
        tk.Button(frame, text="Calcular Distancia", bg="#3498db", fg="white", font=("Segoe UI", 14, "bold"),
                  relief="flat", padx=15, pady=8, command=self.procesar_distancia).pack(pady=20)

        # Resultado
        self.resultado_distancia = tk.Label(frame, text="", font=("Segoe UI", 14), bg="#ecf0f1", fg="#2c3e50")
        self.resultado_distancia.pack()

        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        return frame

    def procesar_distancia(self):
        try:
            xa = float(self.dist_xa.get())
            ya = float(self.dist_ya.get())
            xb = float(self.dist_xb.get())
            yb = float(self.dist_yb.get())
            xc = float(self.dist_xc.get())
            yc = float(self.dist_yc.get())
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingrese valores numéricos válidos.")
            return

        distancia = self.calcular_distancia_minima(xa, ya, xb, yb, xc, yc)
        if distancia is None:
            messagebox.showerror("Error", "Los puntos A y B no pueden ser iguales.")
            return

        self.resultado_distancia.config(text=f"Distancia mínima: {distancia:.4f}")

    # Calculo Interseccion recta

    def calcular_punto_interseccion(self):
        try:
          norte_1a = float(self.entry_norte_1a.get())
          este_1a = float(self.entry_este_1a.get())
          norte_2a = float(self.entry_norte_2a.get())
          este_2a = float(self.entry_este_2a.get())
          norte_1b = float(self.entry_norte_1b.get())
          este_1b = float(self.entry_este_1b.get())
          norte_2b = float(self.entry_norte_2b.get())
          este_2b = float(self.entry_este_2b.get())
        except ValueError:
          messagebox.showerror("Error de entrada", "Por favor, ingrese valores numéricos válidos.")
          return

        A1 = este_2a - este_1a
        B1 = norte_1a - norte_2a
        C1 = A1 * norte_1a + B1 * este_1a

        A2 = este_2b - este_1b
        B2 = norte_1b - norte_2b
        C2 = A2 * norte_1b + B2 * este_1b

        Pad = A1 * B2 - A2 * B1

        if Pad == 0:
          self.result_distance.config(text="Las rectas son paralelas")
        else:
          x = (B2 * C1 - B1 * C2) / Pad
          y = (A1 * C2 - A2 * C1) / Pad
          self.result_distance.config(text=f"Punto de intersección: ({x:.6f}, {y:.6f})")

    def frame_interseccion_rectas(self):
        frame = tk.Frame(self.main_area, bg="#ecf0f1")

        tk.Label(frame, text="Intersección de Dos Rectas", font=("Segoe UI", 22, "bold"),
                 bg="#ecf0f1", fg="#2c3e50").pack(pady=25)

        container = tk.Frame(frame, bg="#f7f9fa", bd=2, relief="groove")
        container.pack(padx=40, pady=10, anchor="w")

        tk.Label(container, text="Recta A - Punto 1 (N, E):", bg="#f7f9fa",
                 font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_norte_1a = tk.Entry(container, width=10)
        self.entry_norte_1a.grid(row=0, column=1, padx=10, pady=5)
        self.entry_este_1a = tk.Entry(container, width=10)
        self.entry_este_1a.grid(row=0, column=2, padx=10, pady=5)

        tk.Label(container, text="Recta A - Punto 2 (N, E):", bg="#f7f9fa",
                 font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_norte_2a = tk.Entry(container, width=10)
        self.entry_norte_2a.grid(row=1, column=1, padx=10, pady=5)
        self.entry_este_2a = tk.Entry(container, width=10)
        self.entry_este_2a.grid(row=1, column=2, padx=10, pady=5)

        tk.Label(container, text="Recta B - Punto 1 (N, E):", bg="#f7f9fa",
                 font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_norte_1b = tk.Entry(container, width=10)
        self.entry_norte_1b.grid(row=2, column=1, padx=10, pady=5)
        self.entry_este_1b = tk.Entry(container, width=10)
        self.entry_este_1b.grid(row=2, column=2, padx=10, pady=5)

        tk.Label(container, text="Recta B - Punto 2 (N, E):", bg="#f7f9fa",
                 font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_norte_2b = tk.Entry(container, width=10)
        self.entry_norte_2b.grid(row=3, column=1, padx=10, pady=5)
        self.entry_este_2b = tk.Entry(container, width=10)
        self.entry_este_2b.grid(row=3, column=2, padx=10, pady=5)

        tk.Button(frame, text="Calcular Intersección", bg="#3498db", fg="white",
                  font=("Segoe UI", 14, "bold"), relief="flat", padx=15, pady=8,
                  command=self.calcular_punto_interseccion).pack(pady=20)

        self.result_distance = tk.Label(frame, text="", font=("Segoe UI", 14),
                                        bg="#ecf0f1", fg="#2c3e50")
        self.result_distance.pack()

        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        return frame

    # Área Del Poligono 5 vertices

    def frame_area_poligono(self):
        frame = tk.Frame(self.main_area, bg="#ecf0f1")

        tk.Label(frame, text="Cálculo Área Polígono 5 Puntos", font=("Segoe UI", 22, "bold"),
                 bg="#ecf0f1", fg="#2c3e50").pack(pady=25)

        container = tk.Frame(frame, bg="#f7f9fa", bd=2, relief="groove")
        container.pack(padx=40, pady=10, anchor="w")

        self.entries_poligono = []

        for i in range(5):
            tk.Label(container, text=f"Punto {i+1} - X:", bg="#f7f9fa",
                     font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=i, column=0, sticky="w", pady=5)
            entry_x = tk.Entry(container, width=10)
            entry_x.grid(row=i, column=1, padx=10, pady=5)

            tk.Label(container, text=f"Punto {i+1} - Y:", bg="#f7f9fa",
                     font=("Segoe UI", 13, "bold"), fg="#34495e").grid(row=i, column=2, sticky="w", pady=5)
            entry_y = tk.Entry(container, width=10)
            entry_y.grid(row=i, column=3, padx=10, pady=5)

            self.entries_poligono.append((entry_x, entry_y))

        tk.Button(frame, text="Calcular Área", bg="#3498db", fg="white",
                  font=("Segoe UI", 14, "bold"), relief="flat", padx=15, pady=8,
                  command=self.procesar_area_poligono).pack(pady=20)

        self.lbl_resultado_area = tk.Label(frame, text="", font=("Segoe UI", 14),
                                           bg="#ecf0f1", fg="#2c3e50")
        self.lbl_resultado_area.pack()

        return frame

    def procesar_area_poligono(self):
        try:
            puntos = []
            for entry_x, entry_y in self.entries_poligono:
                x = float(entry_x.get())
                y = float(entry_y.get())
                puntos.append((x, y))

            area = self.calcular_area_poligono(puntos)
            self.lbl_resultado_area.config(text=f"Área del polígono: {area:.4f} unidades²")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa todos los valores numéricos correctamente.")

    def calcular_area_poligono(self, puntos):
        # Asegurar que el polígono esté cerrado
        if puntos[0] != puntos[-1]:
            puntos.append(puntos[0])

        area = 0
        for i in range(len(puntos) - 1):
            x1, y1 = puntos[i]
            x2, y2 = puntos[i + 1]
            area += x1 * y2 - y1 * x2

        return abs(area) / 2

    def create_sidebar_buttons(self):
        for i, key in enumerate(self.frames):
            btn = tk.Button(self.sidebar, text=key, font=("Segoe UI", 14, "bold"), bg="#34495e", fg="white",
                            relief="flat", bd=0, padx=20, pady=15,
                            command=lambda k=key: self.show_frame(k))
            btn.pack(fill="x", pady=2)

    def show_frame(self, key):
        for f in self.frames.values():
            f.place_forget()
        self.frames[key].place(relx=0, rely=0, relwidth=1, relheight=1)
            
# Al ejecutar el script, abrir primero login
if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()